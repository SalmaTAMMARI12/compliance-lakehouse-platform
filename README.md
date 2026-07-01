
# DGSSI — Plateforme d'ingénierie et d'analyse des données réglementaires
Plateforme Data Engineering pour l'automatisation de l'analyse documentaire des rapports
d'audit de cybersécurité et des dossiers d'homologation des Infrastructures d'Importance
Vitale (IIV), dans le cadre des obligations réglementaires suivies par la DGSSI.

## Statut du projet

🚧 Socle technique en construction. Les extracteurs métier réels (DNSSI v2, homologation)
seront implémentés lorsque les rapports anonymisés seront fournis.

## Architecture

Clean Architecture / Ports & Adapters :

- `domain/` — cœur métier pur, zéro dépendance externe
- `infrastructure/` — adapters techniques (parsing, extraction, stockage, base de données, IA)
- `application/` — orchestration des cas d'usage
- `shared/` — configuration et logging centralisés