"""Dashboard web DGSSI — visualisation des audits de conformité."""
from flask import Flask, render_template_string
import psycopg2
import psycopg2.extras
import os

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host=os.environ.get("POSTGRES_HOST", "localhost"),
        port=os.environ.get("POSTGRES_PORT", "5432"),
        dbname=os.environ.get("POSTGRES_DB", "dgssi"),
        user=os.environ.get("POSTGRES_USER", "dgssi"),
        password=os.environ.get("POSTGRES_PASSWORD", "changeme"),
        cursor_factory=psycopg2.extras.RealDictCursor
    )

HTML = """
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>DGSSI — Plateforme de Conformité</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family: 'Segoe UI', sans-serif; background:#f0f2f5; color:#1a1a2e; }

header { background:linear-gradient(135deg,#0f3460,#16213e); color:white; padding:20px 40px; display:flex; align-items:center; gap:15px; }
header h1 { font-size:22px; font-weight:600; }
header span { font-size:13px; opacity:0.7; }

.container { max-width:1400px; margin:30px auto; padding:0 30px; }

.kpis { display:grid; grid-template-columns:repeat(4,1fr); gap:20px; margin-bottom:30px; }
.kpi { background:white; border-radius:12px; padding:24px; box-shadow:0 2px 8px rgba(0,0,0,0.08); border-left:4px solid #0f3460; }
.kpi .val { font-size:36px; font-weight:700; color:#0f3460; }
.kpi .lbl { font-size:13px; color:#666; margin-top:4px; }
.kpi.danger { border-left-color:#e74c3c; }
.kpi.danger .val { color:#e74c3c; }
.kpi.warn { border-left-color:#f39c12; }
.kpi.warn .val { color:#f39c12; }
.kpi.ok { border-left-color:#27ae60; }
.kpi.ok .val { color:#27ae60; }

.grid2 { display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-bottom:20px; }

.card { background:white; border-radius:12px; padding:24px; box-shadow:0 2px 8px rgba(0,0,0,0.08); }
.card h2 { font-size:15px; font-weight:600; color:#0f3460; margin-bottom:16px; padding-bottom:10px; border-bottom:2px solid #f0f2f5; }

table { width:100%; border-collapse:collapse; font-size:13px; }
th { background:#f8f9fa; padding:10px 12px; text-align:left; font-weight:600; color:#555; border-bottom:2px solid #e9ecef; }
td { padding:10px 12px; border-bottom:1px solid #f0f2f5; vertical-align:top; }
tr:hover td { background:#f8f9ff; }

.badge { display:inline-block; padding:3px 10px; border-radius:20px; font-size:11px; font-weight:600; }
.badge-red { background:#fde8e8; color:#c0392b; }
.badge-orange { background:#fef3e2; color:#d35400; }
.badge-green { background:#e8f8f0; color:#1e8449; }
.badge-blue { background:#e8f0fe; color:#1a73e8; }
.badge-gray { background:#f0f0f0; color:#555; }

.bar-wrap { background:#f0f2f5; border-radius:4px; height:8px; margin-top:4px; }
.bar-fill { height:8px; border-radius:4px; }
.bar-green { background:#27ae60; }
.bar-orange { background:#f39c12; }
.bar-red { background:#e74c3c; }

.stat-row { display:flex; justify-content:space-between; align-items:center; padding:8px 0; border-bottom:1px solid #f0f2f5; }
.stat-row:last-child { border-bottom:none; }

.timeline { display:flex; flex-direction:column; gap:8px; }
.timeline-item { display:flex; gap:12px; align-items:flex-start; }
.timeline-dot { width:10px; height:10px; border-radius:50%; background:#0f3460; margin-top:4px; flex-shrink:0; }
.timeline-content { font-size:13px; }
.timeline-date { font-size:11px; color:#999; }

.verify-badge { background:#fff3cd; color:#856404; padding:2px 8px; border-radius:4px; font-size:11px; }
</style>
</head>
<body>

<header>
  <div>
    <h1>Plateforme de Conformité DGSSI</h1>
    <span>Système d'Intelligence Documentaire — Audits DNSSI v2</span>
  </div>
</header>

<div class="container">

  <div class="kpis">
    <div class="kpi {% if audit.taux_conformite_global >= 80 %}ok{% else %}danger{% endif %}">
      <div class="val">{{ audit.taux_conformite_global }}%</div>
      <div class="lbl">Taux de conformité global</div>
    </div>
    <div class="kpi danger">
      <div class="val">{{ eval.nb_ecarts_critiques }}</div>
      <div class="lbl">Écarts critiques</div>
    </div>
    <div class="kpi {% if eval.statut == 'CONFORME' %}ok{% else %}danger{% endif %}">
      <div class="val" style="font-size:20px;">{{ eval.statut }}</div>
      <div class="lbl">Statut réglementaire (seuil {{ eval.seuil_applique }}%)</div>
    </div>
    <div class="kpi ok">
      <div class="val">{{ couverture }}%</div>
      <div class="lbl">Couverture référentiel DNSSI v2 (104 clauses)</div>
    </div>
  </div>

  <div class="grid2">

    <div class="card">
      <h2>Informations de l'audit</h2>
      <div class="stat-row"><span>IIV auditée</span><strong>{{ audit.iiv_nom }}</strong></div>
      <div class="stat-row"><span>Prestataire</span><strong>{{ audit.prestataire_audit }}</strong></div>
      <div class="stat-row"><span>Classification</span><span class="badge badge-orange">{{ audit.classification }}</span></div>
      <div class="stat-row"><span>Date d'extraction</span><strong>{{ audit.date_extraction.strftime('%d/%m/%Y %H:%M') }}</strong></div>
      <div class="stat-row"><span>Confiance extraction</span><strong>{{ "%.0f"|format(audit.confiance_extraction * 100) }}%</strong></div>
      <div class="stat-row"><span>Élément le plus exposé</span><span class="badge badge-red">{{ eval.element_le_plus_expose }}</span></div>
    </div>

    <div class="card">
      <h2>Historique des versions du rapport</h2>
      <div class="timeline">
        {% for v in versions %}
        <div class="timeline-item">
          <div class="timeline-dot"></div>
          <div class="timeline-content">
            <strong>{{ v.version }}</strong> — {{ v.commentaire }}
            <div class="timeline-date">{{ v.date.strftime('%d/%m/%Y') }}</div>
          </div>
        </div>
        {% endfor %}
      </div>
    </div>

  </div>

  <div class="card" style="margin-bottom:20px;">
    <h2>Audit de configuration technique — Résultats par équipement</h2>
    <table>
      <tr><th>Équipement</th><th>CRITIQUE</th><th>ÉLEVÉE</th><th>MOYENNE</th><th>FAIBLE</th><th>Score exposition</th></tr>
      {% for r in resultats %}
      {% set score = r.critique*4 + r.elevee*3 + r.moyenne*2 + r.faible %}
      <tr>
        <td><strong>{{ r.element_audite }}</strong></td>
        <td>{% if r.critique > 0 %}<span class="badge badge-red">{{ r.critique }}</span>{% else %}<span style="color:#ccc">0</span>{% endif %}</td>
        <td>{% if r.elevee > 0 %}<span class="badge badge-orange">{{ r.elevee }}</span>{% else %}<span style="color:#ccc">0</span>{% endif %}</td>
        <td>{% if r.moyenne > 0 %}<span class="badge badge-blue">{{ r.moyenne }}</span>{% else %}<span style="color:#ccc">0</span>{% endif %}</td>
        <td>{% if r.faible > 0 %}<span class="badge badge-gray">{{ r.faible }}</span>{% else %}<span style="color:#ccc">0</span>{% endif %}</td>
        <td>
          <div style="font-weight:600;">{{ score }}</div>
          <div class="bar-wrap"><div class="bar-fill {% if score > 50 %}bar-red{% elif score > 20 %}bar-orange{% else %}bar-green{% endif %}" style="width:{{ [score,100]|min }}%"></div></div>
        </td>
      </tr>
      {% endfor %}
    </table>
  </div>

  <div class="card" style="margin-bottom:20px;">
    <h2>Conformité DNSSI v2 — Couverture par chapitre</h2>
    <table>
      <tr><th>#</th><th>Chapitre</th><th>Clauses évaluées</th><th>Codes DNSSI</th></tr>
      {% for c in chapitres %}
      <tr>
        <td style="color:#999;">{{ loop.index }}</td>
        <td><strong>{{ c.nom_chapitre }}</strong></td>
        <td><span class="badge badge-green">{{ c.nb_clauses }} clauses</span></td>
        <td style="font-size:11px; color:#666; max-width:400px;">{{ c.clauses_str }}</td>
      </tr>
      {% endfor %}
    </table>
  </div>

  <div class="card" style="margin-bottom:20px;">
    <h2>Non-conformités extraites ({{ nc_total }} au total — {{ nc_a_verifier }} à vérifier)</h2>
    <table>
      <tr><th>Chapitre</th><th>Méthode</th><th>Constat</th><th>Confiance</th><th>Statut</th></tr>
      {% for nc in non_conformites[:30] %}
      <tr>
        <td style="font-size:12px;">{{ nc.chapitre_nom[:35] }}{% if nc.chapitre_nom|length > 35 %}...{% endif %}</td>
        <td><span class="badge badge-blue">{{ nc.methode_extraction }}</span></td>
        <td style="font-size:12px; max-width:500px;">{{ nc.resume_constat[:120] }}{% if nc.resume_constat|length > 120 %}...{% endif %}</td>
        <td>
          {% if nc.confiance >= 0.8 %}<span class="badge badge-green">{{ "%.0f"|format(nc.confiance*100) }}%</span>
          {% elif nc.confiance >= 0.5 %}<span class="badge badge-orange">{{ "%.0f"|format(nc.confiance*100) }}%</span>
          {% else %}<span class="badge badge-red">{{ "%.0f"|format(nc.confiance*100) }}%</span>{% endif %}
        </td>
        <td>{% if nc.a_verifier %}<span class="verify-badge">⚠ À vérifier</span>{% else %}<span class="badge badge-green">✓ Validé</span>{% endif %}</td>
      </tr>
      {% endfor %}
    </table>
    {% if nc_total > 30 %}<p style="text-align:center; padding:10px; color:#999; font-size:12px;">... et {{ nc_total - 30 }} autres non-conformités</p>{% endif %}
  </div>

</div>
</body>
</html>
"""

@app.route("/")
def dashboard():
    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT * FROM audits ORDER BY id DESC LIMIT 1")
    audit = cur.fetchone()

    cur.execute("SELECT * FROM evaluations_conformite WHERE audit_id = %s ORDER BY id DESC LIMIT 1", (audit["id"],))
    eval_ = cur.fetchone()

    cur.execute("SELECT * FROM historique_versions WHERE audit_id = %s ORDER BY date", (audit["id"],))
    versions = cur.fetchall()

    cur.execute("SELECT * FROM resultats_techniques WHERE audit_id = %s ORDER BY (critique*4+elevee*3+moyenne*2+faible) DESC", (audit["id"],))
    resultats = cur.fetchall()

    cur.execute("""
        SELECT c.*,
               json_array_length(c.clauses::json) as nb_clauses,
               array_to_string(ARRAY(SELECT json_array_elements_text(c.clauses::json) LIMIT 4), ', ') ||
               CASE WHEN json_array_length(c.clauses::json) > 4 THEN '...' ELSE '' END as clauses_str
        FROM chapitres c WHERE c.audit_id = %s ORDER BY c.id
    """, (audit["id"],))
    chapitres = cur.fetchall()

    cur.execute("""
        SELECT nc.*, c.nom_chapitre as chapitre_nom
        FROM non_conformites nc
        JOIN chapitres c ON nc.chapitre_id = c.id
        WHERE c.audit_id = %s
        ORDER BY nc.a_verifier, nc.id
    """, (audit["id"],))
    non_conformites = cur.fetchall()

    nc_total = len(non_conformites)
    nc_a_verifier = sum(1 for nc in non_conformites if nc["a_verifier"])

    total_clauses = sum(c["nb_clauses"] for c in chapitres)
    couverture = round(100 * total_clauses / 104, 1) if total_clauses else 0

    db.close()

    return render_template_string(HTML,
        audit=audit, eval=eval_, versions=versions,
        resultats=resultats, chapitres=chapitres,
        non_conformites=non_conformites,
        nc_total=nc_total, nc_a_verifier=nc_a_verifier,
        couverture=couverture
    )

if __name__ == "__main__":
    app.run(debug=True, port=5000)