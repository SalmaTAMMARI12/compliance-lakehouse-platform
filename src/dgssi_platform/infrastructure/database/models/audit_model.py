"""Modèles SQLAlchemy — tables Postgres pour les audits extraits."""

from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import JSON, Date, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class AuditModel(Base):
    __tablename__ = "audits"

    id: Mapped[int] = mapped_column(primary_key=True)
    hash_sha256: Mapped[str] = mapped_column(String(64), unique=True)
    iiv_nom: Mapped[str] = mapped_column(String(200))
    iiv_secteur: Mapped[str] = mapped_column(String(200))
    prestataire_audit: Mapped[str] = mapped_column(String(200))
    classification: Mapped[str] = mapped_column(String(100))
    taux_conformite_global: Mapped[float | None] = mapped_column(Float, nullable=True)
    date_extraction: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    confiance_extraction: Mapped[float] = mapped_column(Float)
    confiance_par_categorie: Mapped[dict] = mapped_column(JSON, default=dict)
    nb_ecarts_par_type: Mapped[dict] = mapped_column(JSON, default=dict)
    perimetres: Mapped[dict] = mapped_column(JSON, default=dict)
    referentiels_utilises: Mapped[list] = mapped_column(JSON, default=list)
    # perimetre_fonctionnel = section 1.1 (systemes concernes par l'audit
    # de conformite DNSSI). perimetre_technique = section 4.1 (equipements
    # concernes par l'audit technique). Deux perimetres distincts du meme
    # rapport, tous deux rattaches directement a AuditModel.


    historique_versions: Mapped[list["HistoriqueVersionModel"]] = relationship(
        back_populates="audit", cascade="all, delete-orphan"
    )
    resultats_techniques: Mapped[list["ResultatTechniqueModel"]] = relationship(
        back_populates="audit", cascade="all, delete-orphan"
    )
    chapitres: Mapped[list["ChapitreModel"]] = relationship(
        back_populates="audit", cascade="all, delete-orphan"
    )


class HistoriqueVersionModel(Base):
    __tablename__ = "historique_versions"

    id: Mapped[int] = mapped_column(primary_key=True)
    audit_id: Mapped[int] = mapped_column(ForeignKey("audits.id"))
    version: Mapped[str] = mapped_column(String(20))
    date: Mapped[date] = mapped_column(Date)
    commentaire: Mapped[str] = mapped_column(String(500))

    audit: Mapped[AuditModel] = relationship(back_populates="historique_versions")


class ResultatTechniqueModel(Base):
    __tablename__ = "resultats_techniques"

    id: Mapped[int] = mapped_column(primary_key=True)
    audit_id: Mapped[int] = mapped_column(ForeignKey("audits.id"))
    element_audite: Mapped[str] = mapped_column(String(200))
    critique: Mapped[int] = mapped_column(Integer)
    elevee: Mapped[int] = mapped_column(Integer)
    moyenne: Mapped[int] = mapped_column(Integer)
    faible: Mapped[int] = mapped_column(Integer)

    audit: Mapped[AuditModel] = relationship(back_populates="resultats_techniques")
class ChapitreModel(Base):
    __tablename__ = "chapitres"

    id: Mapped[int] = mapped_column(primary_key=True)
    audit_id: Mapped[int] = mapped_column(ForeignKey("audits.id"))
    nom_chapitre: Mapped[str] = mapped_column(String(200))
    clauses: Mapped[list] = mapped_column(JSON, default=list)
    notes_audit_synthese: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    # Codes DNSSI du chapitre (ex. ["POL-RISQUE", "POL-FORMEL"]) — le
    # libellé/objectif de chaque code vit dans le référentiel YAML, pas ici.

    audit: Mapped["AuditModel"] = relationship(back_populates="chapitres")
    non_conformites: Mapped[list["NonConformiteModel"]] = relationship(
        back_populates="chapitre", cascade="all, delete-orphan"
    )


class NonConformiteModel(Base):
    __tablename__ = "non_conformites"

    id: Mapped[int] = mapped_column(primary_key=True)
    chapitre_id: Mapped[int] = mapped_column(ForeignKey("chapitres.id"))
    texte_source: Mapped[str] = mapped_column(String(2000))
    resume_constat: Mapped[str] = mapped_column(String(500))
    recommandation: Mapped[str | None] = mapped_column(String(500), nullable=True)
    actifs_concernes: Mapped[list] = mapped_column(JSON, default=list)
    echeance: Mapped[str | None] = mapped_column(String(100), nullable=True)
    confiance: Mapped[float] = mapped_column(Float, default=0.0)
    methode_extraction: Mapped[str] = mapped_column(String(20), default="llm")
    a_verifier: Mapped[bool] = mapped_column(default=False)
    est_note: Mapped[bool] = mapped_column(default=False)
    # a_verifier=True : incohérence thématique détectée entre le chapitre
    # attendu et le contenu extrait (voir coherence_chapitre.py) — nécessite
    # une revue humaine avant d'être considéré fiable pour Power BI.

    chapitre: Mapped[ChapitreModel] = relationship(back_populates="non_conformites")


class EvaluationConformiteModel(Base):
    __tablename__ = "evaluations_conformite"

    id: Mapped[int] = mapped_column(primary_key=True)
    audit_id: Mapped[int] = mapped_column(ForeignKey("audits.id"))
    statut: Mapped[str] = mapped_column(String(20))
    seuil_applique: Mapped[float] = mapped_column(Float)
    nb_ecarts_critiques: Mapped[int] = mapped_column(Integer)
    element_le_plus_expose: Mapped[str] = mapped_column(String(200))
    date_evaluation: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)