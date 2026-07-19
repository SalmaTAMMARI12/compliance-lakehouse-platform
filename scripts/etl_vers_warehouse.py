"""ETL Gold + Postgres opérationnel -> Postgres warehouse (schéma étoile).
Idempotent : relançable sans dupliquer les lignes (ON CONFLICT).
"""
from __future__ import annotations

import os
import psycopg2
from psycopg2.extras import RealDictCursor

from dgssi_platform.infrastructure.storage.minio_client import telecharger_objet
from dgssi_platform.infrastructure.referentiel.loader import (
    charger_referentiel_dnssi,
    obtenir_exigences,
)
import json

DSN = (
    f"host={os.environ.get('POSTGRES_HOST', 'localhost')} "
    f"port={os.environ.get('POSTGRES_PORT', '5432')} "
    f"dbname={os.environ.get('POSTGRES_DB', 'dgssi')} "
    f"user={os.environ.get('POSTGRES_USER', 'dgssi')} "
    f"password={os.environ.get('POSTGRES_PASSWORD', '')}"
)


def _normaliser(code: str) -> str:
    return code.upper().replace("-", "").replace(" ", "").strip()


def seeder_referentiel(cur):
    """Remplit dim_chapitre et dim_exigence une seule fois, depuis le
    référentiel DNSSI (dimension statique, indépendante des audits)."""
    referentiel = charger_referentiel_dnssi()
    for chapitre in referentiel["chapitres"]:
        cur.execute(
            """INSERT INTO warehouse.dim_chapitre (numero, nom)
               VALUES (%s, %s)
               ON CONFLICT (numero) DO UPDATE SET nom = EXCLUDED.nom
               RETURNING chapitre_id""",
            (str(chapitre["numero"]), chapitre["nom"]),
        )
    for exigence in obtenir_exigences():
        cur.execute(
            "SELECT chapitre_id FROM warehouse.dim_chapitre WHERE nom = %s",
            (exigence.chapitre,),
        )
        row = cur.fetchone()
        chapitre_id = row["chapitre_id"] if row else None
        cur.execute(
            """INSERT INTO warehouse.dim_exigence (code, chapitre_id)
               VALUES (%s, %s)
               ON CONFLICT (code) DO NOTHING""",
            (exigence.code, chapitre_id),
        )


def upsert_dim(cur, table, id_col, unique_cols, values) -> int:
    cols = list(values.keys())
    placeholders = ", ".join(["%s"] * len(cols))
    updates = ", ".join(f"{c} = EXCLUDED.{c}" for c in cols if c not in unique_cols)
    conflict_target = ", ".join(unique_cols)
    query = f"""
        INSERT INTO warehouse.{table} ({", ".join(cols)})
        VALUES ({placeholders})
        ON CONFLICT ({conflict_target})
        DO UPDATE SET {updates if updates else cols[0] + ' = EXCLUDED.' + cols[0]}
        RETURNING {id_col}
    """
    cur.execute(query, list(values.values()))
    return cur.fetchone()[id_col]


def traiter_audit(cur, audit_row):
    audit_id = audit_row["id"]

    iiv_id = upsert_dim(cur, "dim_iiv", "iiv_id", ["nom", "secteur"], {
        "nom": audit_row["iiv_nom"], "secteur": audit_row["iiv_secteur"],
    })
    prestataire_id = upsert_dim(cur, "dim_prestataire", "prestataire_id", ["nom"], {
        "nom": audit_row["prestataire_audit"],
    })
    date_valeur = audit_row["date_extraction"].date()
    date_id = upsert_dim(cur, "dim_date", "date_id", ["date_valeur"], {
        "date_valeur": date_valeur,
        "annee": date_valeur.year,
        "mois": date_valeur.month,
        "trimestre": (date_valeur.month - 1) // 3 + 1,
    })

    cur.execute(
        "SELECT * FROM evaluations_conformite WHERE audit_id = %s", (audit_id,)
    )
    evaluation = cur.fetchone()
    if evaluation is None:
        print(f"  Audit {audit_id}: pas d'évaluation trouvée, ignoré pour fait_evaluation_audit")
    else:
        upsert_dim(cur, "fait_evaluation_audit", "fait_id", ["audit_source_id"], {
            "audit_source_id": audit_id,
            "iiv_id": iiv_id,
            "prestataire_id": prestataire_id,
            "date_id": date_id,
            "taux_conformite_global": audit_row["taux_conformite_global"],
            "statut": evaluation["statut"],
            "seuil_applique": evaluation["seuil_applique"],
            "nb_ecarts_critiques": evaluation["nb_ecarts_critiques"],
            "confiance_extraction": audit_row["confiance_extraction"],
        })

    cur.execute(
        "SELECT * FROM resultats_techniques WHERE audit_id = %s", (audit_id,)
    )
    for resultat in cur.fetchall():
        element_id = upsert_dim(cur, "dim_element_audite", "element_id", ["nom"], {
            "nom": resultat["element_audite"],
        })
        upsert_dim(cur, "fait_resultat_element", "fait_id", ["audit_source_id", "element_id"], {
            "audit_source_id": audit_id,
            "element_id": element_id,
            "critique": resultat["critique"],
            "elevee": resultat["elevee"],
            "moyenne": resultat["moyenne"],
            "faible": resultat["faible"],
        })

    if not audit_row["chemin_gold"]:
        print(f"  Audit {audit_id}: chemin_gold manquant, clauses ignorées")
        return

    gold_brut = telecharger_objet("gold", audit_row["chemin_gold"])
    gold = json.loads(gold_brut.decode("utf-8"))

    cur.execute("SELECT code, exigence_id FROM warehouse.dim_exigence")
    exigence_par_code_norm = {_normaliser(r["code"]): r["exigence_id"] for r in cur.fetchall()}

    nb_clauses = 0
    for chapitre in gold.get("chapitres", []):
        for code in chapitre.get("clauses", []):
            exigence_id = exigence_par_code_norm.get(_normaliser(code))
            if exigence_id is None:
                print(f"  Audit {audit_id}: code '{code}' introuvable dans dim_exigence, ignoré")
                continue
            cur.execute(
                """INSERT INTO warehouse.fait_clause_audit
                   (audit_source_id, exigence_id, est_couverte)
                   VALUES (%s, %s, TRUE)
                   ON CONFLICT (audit_source_id, exigence_id)
                   DO UPDATE SET est_couverte = TRUE""",
                (audit_id, exigence_id),
            )
            nb_clauses += 1
    print(f"  Audit {audit_id}: {nb_clauses} clauses chargées")


def main():
    conn = psycopg2.connect(DSN)
    conn.autocommit = False
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            print("Chargement du référentiel (chapitres + exigences)...")
            seeder_referentiel(cur)

            cur.execute("SELECT * FROM audits ORDER BY id")
            audits = cur.fetchall()
            print(f"{len(audits)} audit(s) à traiter")
            for audit_row in audits:
                print(f"Traitement audit id={audit_row['id']}...")
                traiter_audit(cur, audit_row)
        conn.commit()
        print("Terminé, transaction validée.")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()