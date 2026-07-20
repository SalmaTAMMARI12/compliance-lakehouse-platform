select
    id as non_conformite_id,
    chapitre_id,
    texte_source,
    resume_constat,
    recommandation,
    actifs_concernes,
    echeance,
    confiance,
    methode_extraction,
    a_verifier
from "dgssi"."public"."non_conformites"