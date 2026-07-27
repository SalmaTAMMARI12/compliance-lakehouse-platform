"""Dashboard web DGSSI — visualisation des audits de conformité.

Corrections apportées vs version précédente :
- Retrait du badge 'Type' (significatif/non_significatif/remarque) par
  constat : ce champ n'existe plus dans NonConformiteModel (décision
  architecturale : cette granularité n'est pas présente dans le rapport
  source, seul le total agrégé l'est). L'ancien code cherchait nc.type,
  qui n'existant pas retombait systématiquement sur "Remarque" — trompeur.
- Ajout du KPI nb_ecarts_par_type : le total OFFICIEL du rapport
  (ex. 11 significatifs / 7 non significatifs / 1 remarque), extrait par
  regex depuis la phrase de synthèse du rapport — fiable, à la différence
  d'une classification par constat individuel.
- Ajout de l'affichage des périmètres fonctionnel et technique.
- La couverture référentiel n'est plus codée en dur à 100 : elle est
  calculée à partir du nombre réel de clauses couvertes par les chapitres
  en base vs le nombre total de clauses du référentiel YAML.
- La colonne "Statut" (a_verifier) sur les non-conformités est conservée
  telle quelle : elle reflète un vrai signal de qualité déjà fiable.
- Ajout de /api/alerts : webhook recevant les notifications Grafana
  Alerting (règles métier DGSSI), voir dgssi_alerts.yml. Log uniquement
  pour l'instant, pas de persistance.
"""

import sys
import json
from pathlib import Path

# Add parent directory to sys.path to allow importing from src
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.dgssi_platform.shared.config import get_settings
from src.dgssi_platform.infrastructure.referentiel.loader import obtenir_exigences
from src.dgssi_platform.domain.services.calculer_taux_conformite import _normaliser

from flask import Flask, render_template_string, request, jsonify
import psycopg2
import psycopg2.extras

app = Flask(__name__)


def get_db():
    settings = get_settings()
    return psycopg2.connect(
        host=settings.postgres_host,
        port=settings.postgres_port,
        dbname=settings.postgres_db,
        user=settings.postgres_user,
        password=settings.postgres_password,
        cursor_factory=psycopg2.extras.RealDictCursor
    )


HTML = """
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>DGSSI — Plateforme de Conformité</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* { margin:0; padding:0; box-sizing:border-box; }
body { font-family: 'Inter', sans-serif; background:#f4f7f6; color:#1a1a2e; line-height:1.5; }

header { background:linear-gradient(135deg,#0a192f,#172a45); color:white; padding:20px 40px; display:flex; align-items:center; gap:15px; box-shadow:0 4px 12px rgba(0,0,0,0.1); }
header h1 { font-size:24px; font-weight:700; letter-spacing:-0.5px; }
header span { font-size:13px; opacity:0.8; font-weight:500; }

.container { max-width:1400px; margin:40px auto; padding:0 30px; }

.kpis { display:grid; grid-template-columns:repeat(4,1fr); gap:24px; margin-bottom:30px; }
.kpi { background:white; border-radius:16px; padding:24px; box-shadow:0 4px 20px rgba(0,0,0,0.03); border-left:5px solid #0a192f; transition:transform 0.2s ease, box-shadow 0.2s ease; }
.kpi:hover { transform:translateY(-2px); box-shadow:0 6px 24px rgba(0,0,0,0.06); }
.kpi .val { font-size:36px; font-weight:700; color:#0a192f; letter-spacing:-1px; }
.kpi .lbl { font-size:13px; color:#64748b; margin-top:8px; font-weight:500; }
.kpi.danger { border-left-color:#ef4444; }
.kpi.danger .val { color:#ef4444; }
.kpi.warn { border-left-color:#f59e0b; }
.kpi.warn .val { color:#f59e0b; }
.kpi.ok { border-left-color:#10b981; }
.kpi.ok .val { color:#10b981; }

.ecarts-row { display:grid; grid-template-columns:repeat(3,1fr); gap:24px; margin-bottom:30px; }
.ecart-box { background:white; border-radius:16px; padding:20px 24px; box-shadow:0 4px 20px rgba(0,0,0,0.03); text-align:center; transition:transform 0.2s ease; }
.ecart-box:hover { transform:translateY(-2px); }
.ecart-box .val { font-size:32px; font-weight:700; }
.ecart-box .lbl { font-size:13px; color:#64748b; margin-top:8px; font-weight:500; }
.ecart-box.sig .val { color:#ef4444; }
.ecart-box.nonsig .val { color:#f59e0b; }
.ecart-box.rem .val { color:#64748b; }
.ecart-note { grid-column: 1 / -1; font-size:12px; color:#94a3b8; text-align:center; padding-top:8px; font-style:italic; }

.grid2 { display:grid; grid-template-columns:1fr 1fr; gap:24px; margin-bottom:24px; }

.card { background:white; border-radius:16px; padding:28px; box-shadow:0 4px 20px rgba(0,0,0,0.03); }
.card h2 { font-size:16px; font-weight:600; color:#0a192f; margin-bottom:20px; padding-bottom:12px; border-bottom:1px solid #e2e8f0; }

table { width:100%; border-collapse:collapse; font-size:13px; }
th { background:#f8fafc; padding:12px 16px; text-align:left; font-weight:600; color:#475569; border-bottom:2px solid #e2e8f0; }
td { padding:14px 16px; border-bottom:1px solid #f1f5f9; vertical-align:top; }
tr:hover td { background:#f8fafc; }

.badge { display:inline-block; padding:4px 12px; border-radius:24px; font-size:11px; font-weight:600; text-transform:uppercase; letter-spacing:0.5px; }
.badge-red { background:#fee2e2; color:#b91c1c; }
.badge-orange { background:#fef3c7; color:#b45309; }
.badge-green { background:#d1fae5; color:#047857; }
.badge-blue { background:#dbeafe; color:#1d4ed8; }
.badge-gray { background:#f1f5f9; color:#475569; }

.stat-row { display:flex; justify-content:space-between; align-items:center; padding:10px 0; border-bottom:1px solid #f1f5f9; }
.stat-row:last-child { border-bottom:none; }
.stat-row span { color:#64748b; font-size:13px; }

.timeline { display:flex; flex-direction:column; gap:12px; }
.timeline-item { display:flex; gap:16px; align-items:flex-start; }
.timeline-dot { width:12px; height:12px; border-radius:50%; background:#3b82f6; margin-top:4px; flex-shrink:0; box-shadow:0 0 0 3px #dbeafe; }
.timeline-content { font-size:13px; color:#1e293b; }
.timeline-date { font-size:11px; color:#94a3b8; margin-top:2px; }

.verify-badge { background:#fef3c7; color:#b45309; padding:4px 12px; border-radius:24px; font-size:11px; font-weight:600; text-transform:uppercase; letter-spacing:0.5px; }

.perimetre-list { list-style:none; }
.perimetre-list li { padding:8px 0; border-bottom:1px solid #f1f5f9; font-size:13px; color:#334155; }
.perimetre-list li:last-child { border-bottom:none; }
.perimetre-list li::before { content:"▹ "; color:#3b82f6; font-weight:bold; margin-right:4px; }

.meth-badge { font-size:10px; padding:3px 8px; border-radius:6px; font-weight:600; text-transform:uppercase; letter-spacing:0.5px; }
.meth-regex { background:#dbeafe; color:#1d4ed8; }
.meth-llm { background:#f3e8ff; color:#7e22ce; }

/* Tabs Styles */
.tab-container { margin-top: 10px; }
.tabs { display: flex; gap: 16px; border-bottom: 2px solid #e2e8f0; margin-bottom: 24px; }
.tab-btn { padding: 14px 24px; background: none; border: none; border-bottom: 3px solid transparent; cursor: pointer; font-size: 15px; font-weight: 600; color: #64748b; font-family: inherit; transition:all 0.2s ease; }
.tab-btn:hover { color: #0a192f; }
.tab-btn.active { color: #0a192f; border-bottom-color: #3b82f6; }

.tab-content { display: none; }
.tab-content.active { display: block; }

/* Print Styles for PDF Export */
@media screen {
  #executive-summary { display: none; }
}

@media print {
  body { background: white; color: black; margin: 0; padding: 0; }
  .container { max-width: 100%; margin: 0; padding: 0; }
  header, .tabs, .btn-print { display: none !important; }
  
  /* =========================================
     IMPRESSION : On imprime UNIQUEMENT la Synthèse Exécutive
     (le Dashboard complet est caché à l'impression)
     ========================================= */
  body #dashboard-content { display: none !important; }
  body #executive-summary { display: block !important; margin-top: 0 !important; page-break-before: avoid !important; }
  
  /* Mode Noir et Blanc & épuré pour la Synthèse */
  body * { 
    color: black !important; 
    box-shadow: none !important; 
  }
  
  body #executive-summary {
    position: relative;
    z-index: 1;
  }

  body table { border-collapse: collapse; width: 100%; margin-top: 20px; background: rgba(255,255,255,0.9) !important; }
  body th, body td { border: 1px solid black !important; padding: 10px; background: transparent !important; }
  body th { font-weight: bold; border-bottom: 2px solid black !important; background: rgba(240,240,240,0.9) !important; }

  /* Fixes pagination */
  table { page-break-inside: auto; break-inside: auto; }
  tr { page-break-inside: avoid; page-break-after: auto; break-inside: avoid; }
  thead { display: table-header-group; }
  tfoot { display: table-footer-group; }
}
</style>
</head>
<body>

<header style="display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; gap: 20px;">
  <div style="display:flex; align-items:center;">
    <!-- Le logo sera chargé depuis le dossier 'static' que vous devrez créer à côté de dashboard.py -->
    <img src="/static/dgssi_logo.svg" alt="DGSSI" style="height: 60px; object-fit: contain; background: white; padding: 5px 10px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.3);" onerror="this.style.display='none'">
  </div>
  <div style="text-align: center;">
    <h1 style="margin:0; font-size:24px; font-weight:700; letter-spacing:-0.5px;">Plateforme de Conformité DGSSI</h1>
    <span style="color:#cbd5e1; font-size:14px;"></span>
  </div>
  <div style="display:flex; justify-content: flex-end; gap:10px;">
    <button class="btn-print" onclick="window.printExecutiveSummary()" style="background: white; color: #0a192f; border: none; padding: 10px 16px; border-radius: 8px; font-weight: 600; cursor: pointer; box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: all 0.2s ease;">
       Télécharger Synthèse Exécutive
    </button>
  </div>
</header>

<div class="container">

  <!-- BLOC SYNTHÈSE EXÉCUTIVE (Affiché uniquement via bouton dédié) -->
  <div id="executive-summary" style="padding-top: 20px;">
    <div style="display: flex; align-items: center; justify-content: flex-start; gap: 30px; margin-bottom: 20px; border-bottom: 2px solid #000; padding-bottom: 20px;">
      <img src="/static/dgssi_logo.svg" alt="DGSSI Logo" style="height: 90px; object-fit: contain;">
      <div style="text-align: left;">
        <h1 style="font-size: 28px; margin: 0 0 5px 0;">Synthèse de l'Audit</h1>
        <h2 style="font-size: 22px; margin: 0; color: #333;">{{ audit.iiv_nom }}</h2>
      </div>
    </div>

    <!-- Informations Générales de l'Audit (Sous la ligne) -->
    <div style="margin-bottom: 40px; display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 14px;">
      <div><strong>Date d'extraction :</strong> {{ audit.date_extraction.strftime('%d/%m/%Y') }}</div>
      <div><strong>Prestataire :</strong> {{ audit.prestataire_audit }}</div>
      <div><strong>Classification :</strong> {{ audit.classification }}</div>
      <div><strong>Taux de conformité global :</strong> {{ audit.taux_conformite_global }}%</div>
      <div><strong>Référentiel utilisé :</strong> 
        {% if audit.referentiels_utilises %}
          {{ audit.referentiels_utilises | join(', ') }}
        {% else %}
          DNSSI v2
        {% endif %}
      </div>
    </div>

    <div style="margin-top: 30px;">
      <table style="width:100%; border:1px solid #e2e8f0;">
        <thead>
          <tr style="background:#f8fafc;">
            <th style="width:25%">Chapitre</th>
            <th style="width:40%">Note d'audit (Synthèse)</th>
            <th style="width:35%">Constats</th>
          </tr>
        </thead>
        <tbody>
          {% for c in chapitres %}
          <tr>
            <td><strong>{{ c.nom_chapitre }}</strong></td>
            <td>
              {% if c.notes_audit_synthese %}
                <div style="font-size:13px; color:#334155;">{{ c.notes_audit_synthese }}</div>
              {% else %}
                <span style="color:#94a3b8; font-style:italic;">Pas de notes spécifiques</span>
              {% endif %}
            </td>
            <td>
              {% set ns = namespace(found=false) %}
              <ul style="padding-left:15px; margin:0; font-size:12px;">
                {% for nc in ecarts %}
                  {% if nc.chapitre_nom == c.nom_chapitre %}
                    {% set ns.found = true %}
                    <li style="margin-bottom:6px;">
                      {{ nc.resume_constat }}
                      {% if nc.a_verifier %}<br><span style="color:#b91c1c; font-weight:600;">[À vérifier]</span>{% endif %}
                    </li>
                  {% endif %}
                {% endfor %}
              </ul>
              {% if not ns.found %}
                <span style="color:#10b981; font-style:italic;">Conforme / Aucun écart</span>
              {% endif %}
            </td>
          </tr>
          {% endfor %}
        </tbody>
      </table>
    </div>

    <!-- Ajout du Volet Technique demandé dans la synthèse -->
    <div style="margin-top: 40px;">
      <h2 style="font-size: 20px; color: #0a192f; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; margin-bottom: 20px;">Synthèse de l'Audit de Configuration Technique</h2>
      <table style="width:100%; border:1px solid #e2e8f0;">
        <thead>
          <tr style="background:#f8fafc;">
            <th style="width:30%">Équipement Audité</th>
            <th style="width:14%; text-align:center;">CRITIQUE</th>
            <th style="width:14%; text-align:center;">ÉLEVÉE</th>
            <th style="width:14%; text-align:center;">MOYENNE</th>
            <th style="width:14%; text-align:center;">FAIBLE</th>
            <th style="width:14%; text-align:center;">Score global</th>
          </tr>
        </thead>
        <tbody>
          {% for r in resultats %}
          {% set score = r.critique*4 + r.elevee*3 + r.moyenne*2 + r.faible %}
          <tr>
            <td><strong>{{ r.element_audite }}</strong></td>
            <td style="text-align:center;">{% if r.critique > 0 %}<span style="color:#b91c1c; font-weight:bold;">{{ r.critique }}</span>{% else %}<span style="color:#cbd5e1">-</span>{% endif %}</td>
            <td style="text-align:center;">{% if r.elevee > 0 %}<span style="color:#b45309; font-weight:bold;">{{ r.elevee }}</span>{% else %}<span style="color:#cbd5e1">-</span>{% endif %}</td>
            <td style="text-align:center;">{% if r.moyenne > 0 %}<span style="color:#1d4ed8; font-weight:bold;">{{ r.moyenne }}</span>{% else %}<span style="color:#cbd5e1">-</span>{% endif %}</td>
            <td style="text-align:center;">{% if r.faible > 0 %}<span style="color:#475569; font-weight:bold;">{{ r.faible }}</span>{% else %}<span style="color:#cbd5e1">-</span>{% endif %}</td>
            <td style="text-align:center; font-weight:bold;">{{ score }}</td>
          </tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
  </div>

  <div id="dashboard-content" class="tab-container">
    <div class="tabs">
      <button class="tab-btn active" onclick="openTab(event, 'tab-general')">Vue d'Ensemble</button>
      <button class="tab-btn" onclick="openTab(event, 'tab-orga')">Volet Organisationnel — Conformité</button>
      <button class="tab-btn" onclick="openTab(event, 'tab-tech')">Volet Technique — Architecture</button>
    </div>

    <!-- ONGLET VUE GÉNÉRALE -->
    <div id="tab-general" class="tab-content active">
      <!-- KPIs principaux -->
      <div class="kpis" style="grid-template-columns: repeat(2, 1fr);">
        <div class="kpi {% if audit.taux_conformite_global >= 80 %}ok{% else %}danger{% endif %}">
          <div class="val">{{ audit.taux_conformite_global }}%</div>
          <div class="lbl">Taux de conformité global</div>
        </div>
        <div class="kpi ok">
          <div class="val">{{ couverture }}%</div>
          <div class="lbl">Couverture référentiel DNSSI v2 ({{ nb_clauses_total }} clauses, calculé)</div>
        </div>
      </div>

      <div class="grid2">
        <!-- Infos audit -->
        <div class="card">
          <h2>Informations de l'audit</h2>
          <div class="stat-row"><span>IIV auditée</span><strong>{{ audit.iiv_nom }}</strong></div>
          <div class="stat-row"><span>Secteur</span><span class="badge badge-gray">{{ audit.iiv_secteur }}</span></div>
          <div class="stat-row"><span>Prestataire</span><strong>{{ audit.prestataire_audit }}</strong></div>
          <div class="stat-row"><span>Classification</span><span class="badge badge-orange">{{ audit.classification }}</span></div>
          {% if eval %}
          <div class="stat-row"><span>Élément le plus exposé</span><span class="badge badge-red">{{ eval.element_le_plus_expose }}</span></div>
          {% endif %}
        </div>

        <!-- Historique versions -->
        <div class="card">
          <h2>Historique des versions du rapport</h2>
          <div class="timeline">
            {% for v in versions %}
            <div class="timeline-item">
              <div class="timeline-dot"></div>
              <div class="timeline-content">
                <strong>{{ v.version }}</strong> — {{ v.commentaire }}
                <div class="timeline-date">{{ v.date }}</div>
              </div>
            </div>
            {% endfor %}
          </div>
        </div>
      </div>
    </div>

    <!-- ONGLET ORGANISATIONNEL -->
    <div id="tab-orga" class="tab-content">
      <!-- Périmètre fonctionnel -->
      <div class="card" style="margin-bottom:20px;">
        <h2>Périmètre fonctionnel (§1.1 — audit de conformité)</h2>
        {% if audit.perimetre_fonctionnel %}
        <ul class="perimetre-list">
          {% for p in audit.perimetre_fonctionnel %}
          <li>{{ p }}</li>
          {% endfor %}
        </ul>
        {% else %}
        <p style="color:#999; font-size:13px;">Non disponible pour cet audit.</p>
        {% endif %}
      </div>

      <!-- Répartition officielle des écarts -->
      <div class="ecarts-row">
        <div class="ecart-box sig">
          <div class="val">{{ nb_ecarts_par_type.get('significatif', '—') }}</div>
          <div class="lbl">Significatifs (officiel rapport)</div>
        </div>
        <div class="ecart-box nonsig">
          <div class="val">{{ nb_ecarts_par_type.get('non_significatif', '—') }}</div>
          <div class="lbl">Non significatifs (officiel rapport)</div>
        </div>
        <div class="ecart-box rem">
          <div class="val">{{ nb_ecarts_par_type.get('remarque', '—') }}</div>
          <div class="lbl">Remarques (officiel rapport)</div>
        </div>
        <div class="ecart-note">
          
        </div>
      </div>

      <!-- Chapitres DNSSI -->
      <div class="card" style="margin-bottom:20px;">
        <h2>Conformité DNSSI v2 — Couverture par chapitre</h2>
        <table>
          <tr><th>#</th><th>Chapitre</th><th>Clauses couvertes</th><th>Codes DNSSI</th><th>Constats</th></tr>
          {% for c in chapitres %}
          {% set ns = namespace(vrais_constats=0) %}
          {% for nc in ecarts %}
            {% if nc.chapitre_id == c.id and 'Conforme' not in nc.resume_constat and 'Aucun écart' not in nc.resume_constat %}
              {% set ns.vrais_constats = ns.vrais_constats + 1 %}
            {% endif %}
          {% endfor %}
          <tr>
            <td style="color:#999;">{{ loop.index }}</td>
            <td><strong>{{ c.nom_chapitre }}</strong></td>
            <td><span class="badge badge-green">{{ c.nb_clauses }} clauses</span></td>
            <td style="font-size:11px; color:#666; max-width:350px;">{{ c.clauses_str }}</td>
            <td>
              {% if ns.vrais_constats == 0 %}
                <span class="badge badge-green">✓ CONFORME</span>
              {% else %}
                <span class="badge badge-orange">{{ ns.vrais_constats }} CONSTAT(S)</span>
              {% endif %}
            </td>
          </tr>
          {% endfor %}
        </table>
      </div>
      
      <!-- Détails par chapitre -->
      {% for c in chapitres %}
      <div class="card chapter-detail-card" style="margin-bottom:20px;">
        <h2 style="color: #0f3460; border-bottom: 2px solid #eee; padding-bottom: 10px; margin-bottom: 15px;">{{ c.nom_chapitre }}</h2>
        
        {% if c.notes_audit_synthese %}
        <div style="background: #f8f9fa; padding: 15px; border-left: 4px solid #0f3460; margin-bottom: 15px;">
          <p style="margin-top: 0; font-weight: 600; color: #333;">Notes d'audit :</p>
          <p style="font-size: 13px; color: #555; line-height: 1.5;">{{ c.notes_audit_synthese }}</p>
          {% if c.notes_audit %}
          <details style="margin-top: 10px;">
            <summary style="cursor: pointer; color: #0f3460; font-weight: 600; font-size: 11px;">Voir la source</summary>
            <div style="margin-top: 8px; padding: 10px; background-color: #fff; border: 1px solid #ddd; font-family: monospace; font-size: 11px; white-space: pre-wrap; word-break: break-word;">{{ c.notes_audit }}</div>
          </details>
          {% endif %}
        </div>
        {% endif %}

        {% set vrais_constats_chap = [] %}
        {% for nc in ecarts %}
          {% if nc.chapitre_id == c.id and 'Conforme' not in nc.resume_constat and 'Aucun écart' not in nc.resume_constat %}
            {% set _ = vrais_constats_chap.append(nc) %}
          {% endif %}
        {% endfor %}
        
        {% if vrais_constats_chap|length > 0 %}
          <table style="margin-top: 10px;">
            <tr><th>Constat</th><th>Statut</th></tr>
            {% for nc in vrais_constats_chap %}
            <tr>
              <td style="font-size:12px; max-width:450px;">
                <div style="font-weight: 600; margin-bottom: 8px; color: #333;">{{ nc.resume_constat }}</div>
                <details>
                  <summary style="cursor: pointer; color: #0f3460; font-weight: 600; font-size: 11px;">Voir le texte source extrait</summary>
                  <div style="margin-top: 8px; padding: 10px; background-color: #f8f9fa; border-left: 3px solid #0f3460; font-family: monospace; font-size: 11px; white-space: pre-wrap; word-break: break-word;">{{ nc.texte_source }}</div>
                </details>
              </td>
              <td>
                <span class="badge badge-orange">Écart</span>
              </td>
            </tr>
            {% endfor %}
          </table>
        {% else %}
          <p style="color: #28a745; font-size: 13px; font-weight: bold; margin-top: 10px;">✓ Conforme : Aucun écart de conformité relevé.</p>
        {% endif %}
      </div>
      {% endfor %}


    </div>

    <!-- ONGLET TECHNIQUE -->
    <div id="tab-tech" class="tab-content">
      <div class="grid2">
        <!-- Périmètre technique -->
        <div class="card">
          <h2>Périmètre technique (§4.1 — audit de configuration)</h2>
          {% if audit.perimetre_technique %}
          <ul class="perimetre-list">
            {% for p in audit.perimetre_technique %}
            <li>{{ p }}</li>
            {% endfor %}
          </ul>
          {% else %}
          <p style="color:#999; font-size:13px;">Non disponible pour cet audit.</p>
          {% endif %}
        </div>
        
        <!-- Référentiels techniques -->
        <div class="card">
          <h2>Référentiels Techniques Utilisés (§4.3)</h2>
          {% if audit.referentiels_utilises %}
          <ul class="perimetre-list">
            {% for ref in audit.referentiels_utilises %}
            <li>{{ ref }}</li>
            {% endfor %}
          </ul>
          {% else %}
          <p style="color:#999; font-size:13px;">Non disponible pour cet audit.</p>
          {% endif %}
        </div>
      </div>

      <!-- Résultats techniques -->
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
    </div>

  </div> <!-- end tab-container -->

</div>

<script>
function openTab(evt, tabId) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
    document.getElementById(tabId).classList.add('active');
    evt.currentTarget.classList.add('active');
}

function printFullDashboard() {
    document.body.classList.remove('print-summary');
    window.print();
}

function printExecutiveSummary() {
    document.body.classList.add('print-summary');
    window.print();
}
</script>
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

    cur.execute(
        "SELECT * FROM resultats_techniques WHERE audit_id = %s "
        "ORDER BY (critique*4+elevee*3+moyenne*2+faible) DESC",
        (audit["id"],),
    )
    resultats = cur.fetchall()

    cur.execute("""
        SELECT c.*,
               json_array_length(c.clauses::json) as nb_clauses,
               array_to_string(ARRAY(SELECT json_array_elements_text(c.clauses::json)), ', ') as clauses_str,
               (SELECT COUNT(*) FROM non_conformites nc WHERE nc.chapitre_id = c.id) as nb_constats
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

    ecarts = [nc for nc in non_conformites if not nc.get("est_note")]
    notes = [nc for nc in non_conformites if nc.get("est_note")]

    nc_total = len(ecarts)
    nc_a_verifier = sum(1 for nc in ecarts if nc.get("a_verifier"))

    # Couverture référentiel calculée par rapport au total officiel du YAML DNSSI v2
    exigences = obtenir_exigences()
    codes_couverts_normalises = set()
    for c in chapitres:
        if c.get("clauses"):
            # c["clauses"] is returned as list by RealDictCursor if cast to json in Postgres, or string. Secure parsing:
            clauses = c["clauses"] if isinstance(c["clauses"], list) else json.loads(c["clauses"])
            for code in clauses:
                codes_couverts_normalises.add(_normaliser(code))
                
    nb_couverts = sum(1 for e in exigences if _normaliser(e.code) in codes_couverts_normalises)
    nb_clauses_total = len(exigences)
    couverture = round(100 * nb_couverts / nb_clauses_total) if nb_clauses_total > 0 else 0

    nb_ecarts_par_type = audit.get("nb_ecarts_par_type") or {}

    db.close()

    return render_template_string(
        HTML,
        audit=audit, eval=eval_, versions=versions,
        resultats=resultats, chapitres=chapitres,
        ecarts=ecarts, notes=notes,
        nc_total=nc_total, nc_a_verifier=nc_a_verifier,
        couverture=couverture, nb_clauses_total=nb_clauses_total,
        nb_ecarts_par_type=nb_ecarts_par_type,
    )

@app.route("/api/alerts", methods=["POST"])
def recevoir_alerte():
    """Webhook Grafana Alerting — reçoit les notifications des alertes
    métier DGSSI (écarts critiques, taux de conformité bas). Log
    uniquement pour l'instant, pas de persistance ni d'action
    automatique — suffisant pour prouver que le canal fonctionne
    de bout en bout, une vraie action (email, ticket...) serait une
    extension future.
    """
    payload = request.get_json(silent=True) or {}
    alertes = payload.get("alerts", [])
    for alerte in alertes:
        nom = alerte.get("labels", {}).get("alertname", "inconnue")
        statut = alerte.get("status", "inconnu")
        app.logger.warning("Alerte Grafana reçue : %s (statut=%s)", nom, statut)
    return jsonify({"recu": True, "nb_alertes": len(alertes)}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
if __name__ == "__main__":
    app.run(debug=True, port=5000)