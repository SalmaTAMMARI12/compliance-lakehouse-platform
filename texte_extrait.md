## AUDIT DE SECURITE DES SYSTEMES D'INFORMATION DU XXXXXXXXXX

## Informations relatives au document

| Auteur  AAAAAAAAA  Classification  Confidentiel  Titre du document  Audit de sécurité des systèmes d'information de l'auditéAUDITÉXXX  Type de document  Rapport d'audit  Equipe d'audit  M  AAAA BBBBB : Responsable Audit de conformité  M CCCC DDDD: Responsable Audit technique  M EEEEE FFFFF : Auditeur   |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

| Visa du chef d'équipe  Visa du Chef  Visa du Directeur   |
|----------------------------------------------------------|

## Historique des mises à jour

| Version  Commentaires  Date  Auteur  V1.0  Version initiale  15/11/2023  AAAAAAAAA  V1.1  Modifiée et partagée avec l'auditer  09/02/2024  AAAAAAAAA  V 1.2  Intègre les remarques de l'Auditer  02/05/2024  AAAAAAAAA   |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## Table des matières

| 1. CONTEXTE GENERAL ...................................................................................... 4  1.1  Périmètre de l'audit  ................................................................................................................  4  1.2  Déroulement de l'audit  ..........................................................................................................  4  1.3  Référentiels ............................................................................................................................  5  1.4  Echelles d'évaluation  .............................................................................................................  6  2. SYNTHESE DES RESULTATS ............................................................................... 7  2.1  Aperçu général  .......................................................................................................................  7  2.2  Niveau de conformité par rapport à la DNSSI  .......................................................................  9  2.3  Écarts dressés par type :  .......................................................................................................  10  3. PISTES SIGNIFICATIVES D  '  AUDIT DE CONFORMITE A LA DNSSI ................................. 12  3.1     Politique de sécurité des systèmes d'information  ................................................................  12  3.2  Organisation de la sécurité  ...................................................................................................  14  3.3  Sécurité des ressources humaines ........................................................................................  16  3.4  Gestion des actifs informationnels  .......................................................................................  17  3.5  Contrôle d'accès  ..................................................................................................................  20  3.6  Cryptographie ......................................................................................................................  21  3.7  Sécurité physique  .................................................................................................................  22  3.8  Sécurité liée à l'exploitation  ................................................................................................  24  3.9  Sécurité des communications  ...............................................................................................  27  3.10  Acquisition, développement et maintenance des systèmes d'information  ..........................  28  3.11  Relation avec les fournisseurs  ..............................................................................................  30  3.12  Gestion des Incidents de cybersécurité  ................................................................................  31  3.13  Gestion du plan de continuité de l'activité  ..........................................................................  32  3.14  Conformité ...........................................................................................................................  34  4. CONSTATS ET RECOMMANDATIONS DE L  '  AUDIT TECHNIQUE .................................... 35  4.1  Périmètre  ..............................................................................................................................  35  4.2  Objectif et principe ..............................................................................................................  35  4.3  Référentiels utilisés  ..............................................................................................................  36  4.4  Echelle d'évaluation  ............................................................................................................  36  4.5  Résultats  ...............................................................................................................................  36   |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## 1. Contexte général

Le PASSI FFFFFF a procédé à un audit de la sécurité du système d'information DE

L'AUDITÉXXX conformément à la loi 05.20 sur la cybersécurité et du Décret n°2-21-406 du 4 hija 1442 (15 juillet 2021) pris pour son application.

L'objectif de cet audit a été de :

- Identifier le niveau de conformité du SI par rapport aux exigences de sécurité énoncées dans la Directive Nationale de la Sécurité des Systèmes d'Information (DNSSI) et le Décret n°2-21406 du 4 hija 1442 (15 juillet 2021) pris pour l'application de la loi 05.20 sur la cybersécurité ;
- Assurer l'analyse de l'architecture réseau et l'audit des configurations ;
- Proposer  des  recommandations  à  même  de  permettre  d'améliorer  et  de  consolider  la sécurité du SI.

Ce rapport a pour objet de restituer les résultats de cette mission d'audit.

## 1.1 Périmètre de l'audit

Le périmètre de cet audit concerne les systèmes d'information de l'audité ci-après énumérés :

- Les Systèmes d'Information métier ;
- Les systèmes support (Messagerie, Active Directory, etc.) ;
- L'infrastructure réseaux et sécurité supportant ces systèmes.
- Le Datacenter.

## 1.2 Déroulement de l'audit

La mission d'audit s'est déroulée en trois étapes :

Étape 1 : Cadrage

- Réunion de cadrage tenue avec les responsables de la Direction Générale pour définir le périmètre et fixer les modalités d'intervention ;
- Recueil de la documentation disponible (Politiques, procédures, organigrammes et fiches de postes, documents d'architecture, configuration des équipements, etc.).

## Étape 2 : Exécution

- Revue documentaire ;
- Entretiens avec les acteurs identifiés. Il s'agit principalement des responsables SI ci -après :
- Directeur DC : Direction Centrale Sécurité Groupe
- o Directeur sécurité de l'information (RSSI)
- o Responsable Département Audit et veille Sécurité
- o Responsable Département GRC : Gouvernance Sécurité, Risques et Conformité
- Directeur Pôle Système d'Information Groupe (PSIG)
- o Directeur Central systèmes et infrastructures
- o Responsable sécurité opérationnelle
- Directeur Pôle Digital
- o Directeur Central Etudes et Développements
- Directeur de Domaine Audit Interne
- Directeur PMO
- Directeur central Organisation, en charge de la gestion des habilitations fonctionnelles
- Directeur Central des achats
- o Directeur Achats IT
- Représentant de l'Equipe PCA, Gestion de la continuité d'activité
- Représentant de la Direction RH
- Analyse approfondie de l'architecture ;
- Choix de l'échantillon des équipements qui feront l'objet de l'audit des configurations ;
- Audit des configurations (manuellement ou via l'utilisation d'outils) ;
- Évaluation des écarts constatés.

## Étape 3 : Rapport et recommandations

- Rédaction du rapport d'audit qui regroupe l'analyse des constats et les recommandations émises par l'équipe d'audit ;
- Restitution des résultats de l'audit ;
- Clôture de l'audit.

## 1.3 Référentiels

Les référentiels retenus pour mener cette mission d'audit de la sécurité sont :

- La Directive Nationale de la Sécurité des Systèmes d'Information (DNSSI) basée sur la norme ISO/IEC 27002 :2013 et qui s'articule autour de 14 chapitres, décrivant les mesures de sécurité organisationnelles et techniques qui doivent être appliquées par les

administrations et les organismes publics ainsi que les infrastructures d'importance vitale, à savoir :

- o Politique de sécurité des systèmes d'information ;

- o Organisation de la sécurité des systèmes d'information ;

- o Sécurité des ressources humaines ;

- o Gestion des actifs informationnels ;

- o Contrôle d'accès ;

- o Cryptographie ;

- o Sécurité physique et environnementale ;

- o Sécurité liée à l'exploitation ; -

- o Sécurité des communications ;

- o Acquisition, développement et maintenance des systèmes d'information ;

- o Relations avec les fournisseurs ;

- o Gestion des incidents de cybersécurité ;

- o Gestion de la continuité de l'activité ;

- o Conformité
- Les  dispositions  du  Décret  °2-21-406  du  4  hijja  1442  (15  juillet  2021)  pris  pour l'application de la loi 05.20 sur la cybersécurité.

## 1.4 Echelles d'évaluation

- L'évaluation de la conformité par rapport à la DNSSI se fait en fonction de l'échelle suivante :
- Les écarts (non-conformité à la DNSSI) constatés sont classés en 3 catégories en fonction de leur type et leur criticité :
- Les écarts de type « écart significatif » sont susceptibles de remettre à eux seuls en cause les activités de l'objet de l'audit.
- Les écarts de type «  écart non significatif » sont des écarts nécessitant une action corrective, mais qui ne peuvent pas à eux seuls porter atteinte aux activités ou aux engagements de l'objet de l'audit.
- Les remarques correspondent à des écarts n'engendrant pas de risques pour l'objet de l'audit.  Il  peut  s'agir  d'écarts  par  rapport  aux  bonnes  pratiques  ou  d'évolutions permettant d'améliorer la qualité de service.

Tableau 1: Échelle de notation du niveau de conformité du SI selon la DNSSI

| Niveau de conformité  Description  N/A  L'entité ou l'IIV n'est pas concernée par la règle. (à justifier)  Conforme  L'entité ou l'IIV répond à toutes les exigences de la règle  Non conforme  L'entité ou l'IIV ne répond pas aux exigences de la règle   |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## 2. Synthèse des résultats

## 2.1 Aperçu général

Le PASSI a procédé à un audit de la sécurité du système d'information  de l'audité dans l 'objectif d'évaluer sa posture de sécurité et de dégager d'éventuelles pistes d'amélioration à même d'améliorer cette posture.

Outre  la  conformité  par  rapport  aux  normes  et  référentiels  en  vigueur,  notamment  la Directive  Nationale  de  la  Sécurité  des  Systèmes  d'Information  (DNSSI),  cet  audit  a  été  aussi l'occasion d'identifier des axes d'amélioration par rapport aux bonnes pratiques sur les aspects te chniques relatifs à l'architecture et la configuration du Système d'Information en question en plus d'une évaluation des vulnérabilités visibles depuis le réseau Internet.

## Conformité à la DNSSI :

L'audit de conformité a permis de vérifier le niveau d'implémentation des différentes règles de sécurité  édictées  par  la  DNSSI. Les  constats  faits  par  l'équipe  d'audit,  suite à  l'analyse  de  la documentation  fournie  par  le  AUDITÉX,  aux  entretiens  conduits  avec  les  différentes  équipes concernées et aux visites sur les lieux, se résument comme suit :

## Gouvernance de la sécurité :

- -L'audité a procédé en 2018 à une refonte de l'organisation des structures en charge de la sécurité des systèmes d'information permettant ainsi une bonne gouvernance de la sécurité au sein du groupe.  De plus un projet de mise à jour de la feuille de route sécurité des SI élaborée en 2017 a été lancé . Il a pour objectif d'évaluer le niveau de maturité de la sécurité SI de l'audité et d'aligner les orientations stratégiques du groupe en matière de sécurité SI aux référentiels en vigueur et aux exigences réglementaires. Dans ce sens, une nouvelle politique de sécurité des SI, en instance de validation, a été élaborée.
- -L'exercice d'analyse des risques réalisé par le département GRC (Gouvernance, Risque et Conformité) concerne uniquement les plateformes sensibles et ne couvre pas l'ensemble du système d'information de l'audité.

## Gestion des ressources et des actifs informationnels :

- -L'audité a élaboré une politique de classification du patrimoine informationnel qui définit les  échelles  de  classification,  la  démarche  de  classification  ainsi  que  les  principes  de marquages et de manipulation des données selon leur niveau de classification. L 'exercice de classification du patrimoine informationnel de l'audité est inscrit dans le cadre du plan d'action pour l'année 2024 ;
- -Les  inventaires  mis  en  place  par  les  différentes  équipes  de  l'audité  méritent  d'être complétés  et  consolidés  au  niveau  d'une  base  commune  de  gestion  des  configurations (CMDB) pour une meilleure gestion des actifs et des vulnérabilités y associées.

- -La dernière version de la charte , en instance de validation, prend en charge l'ensemble des mesures de sécurité à adopter en alignement avec les nouvelles orientations stratégiques. L e  processus  de  sa  communication  et  signature  par  l'ensemble  des  collaborateurs  et personnes concernées est en cours d'instauration .

## Gestion de l'exploitation :

- -L'exploitation est régie en général par des processus opérationnels bien établis et maitrisés aussi bien par les équipes opérationnelles que par les équipes de sécurité (Supervision des environnement,  Mise  à  jour,  Sauvegarde,  etc..).  Toutefois,  la  gestion  des  changements requière davantage d'attention et doit être encadrée par une procédure formelle pour une mise en œuvre structurée et efficace des modifications à la suite de toute évolution, mise à jour ou nouveau déploiement.
- -La  traçabilité  des  actions  de  tiers  prestataires  aussi  bien  dans  le  cadre  de  nouveaux développements  que  dans  celui  de  la  maintenance  du  système  d'information, doit  être assurée à travers la mise en place de contrôles spécifiques pour encadrer toutes les étapes de leurs interventions et pour s'assurer de leur respect des exigences de sécurité mises en place.
- -L'audité dispose d'une charte de gestion de projet qui prend en charge la sécurité et les risques de sécurité dans toutes les étapes de l'exécution du projet depuis la planification jusqu'à la mise en production. Toutefois, il est nécessaire d'élaborer et de mettre en œuvre une politique spécifique relative à la sécurité du développement.

## Gestion des incidents et de la continuité d'activité :

- -La gestion des incidents de sécurité au niveau de l'audité est soumise à une politique , en instance de validation, décrivant le processus de détection, de signalement, d'évaluation et de catégorisation des incidents de cybersécurité, les mesures d'intervention et de traitement y afférentes, ainsi que les rôles et responsabilités des acteurs concernés.
- -Les sites de replis identifiés lors de la mise à l'essai du PCA ne sont pas dédiés à la reprise d'activité ce qui peut impacter la continuité d'activité en cas de sinistre majeur. Un projet d'enrichissement du PCA/P R A est prévu et l'intégration de scénarios cyber au niveau des exercices de crise est planifiée pour T1-2024.

## Analyse de l'architecture

L'analyse de l'architecture du système d'information de l'audité fait  état  de  plusieurs  constats positifs dont notamment :

- -Une maitrise de la sécurité périmétrique ;
- -La segmentation du réseau ;
- -La mise en place de plusieurs solutions techniques indispensables pour la sécurité du SI et qui couvrent plusieurs domaines de risque (protection antivirale, administration et mise à jour  centralisées,  d étection  d'intrusions ,  supervision  réseau,  filtrage  web  et  email  et sauvegarde).

Par ailleurs, il est recommandé de renforcer la sécurité de cette architecture par les actions ciaprès :

- La protection de l'accès au réseau ;
- La mise en place d'un réseau d'administration ;
- La mise en place d'une solution de traçabilité des actions d'administration ;
- La formalisation d'une matrice des flux ;

## Audit des configurations :

En ce qui concerne l'audit des configurations, il a concerné le firewall central, le firewall frontal WAN, le firewall frontal internet et le switch fédérateur en plus du serveur web et de messagerie. Sur la base de 199 contrôles vérifiés, plusieurs constats ont été établis dont 18 majeurs. Les points d'amélioration  proposés  au  regard  des  constats  identifiés  concernent  principalement  les  axes suivants :

- -L'utilisation d'une version à jour du firmware ;
- -L'utilisation des règles de filtrage restrictives ;
- -L'utilisation d'algorithmes cryptographiques robustes ;
- -La désactivation de l'installation automatique ;
- -La désactivation du compte de maintenance ;
- -L'utilisation des protocoles chiffrés pour l'administration ;
- -La restriction des accès d'administration ;
- -La configuration de la taille maximale des messages ;
- -La désactivation de l'authentification de base ;
- -La désactivation des versions vulnérables du protocole SSL ;
- -La désactivation des suites cryptographiques faibles ;
- -L'activation du chiffrement pour l'authentification basée sur formulaire et l'authentification de base ;
- -L'utilisation des cookies pour les formulaires d'authentification ;

## 2.2 Niveau de conformité par rapport à la DNSSI

Le taux de conformité du système d'information de l'audité par rapport à la DNSSI a été évalué à 76,70% Ce taux de conformité est calculé en ne prenant en considération que les règles totalement mises en œuvre (note =4). La finalisation de l'implémentation des règles dont la mise en œuvre actuelle est partielle (note=3), améliorerait substantiellement ce taux.

<!-- image -->

Figure 1 : Répartition des contrôles par conformité

| Chapitre / Conformité  Conformité  totale  Conformité  partielle et  totale  1. POLITIQUE DE SECURITE DES SYSTEMES D'INFORMATION  50,00%  100,00%  2. ORGANISATION DE LA SECURITE DES SYSTEMES D'INFORMATION  0,00%  100,00%  3. SECURITE DES RESSOURCES HUMAINES  0,00%  100,00%  4. GESTION DES ACTIFS INFORMATIONNELS  54,55%  100,00%  5. CONTROLE D'ACCES  22,22%  100,00%  6. CRYPTOGRAPHIE  50,00%  100,00%  7. SECURITE PHYSIQUE ET ENVIRONNEMENTALE  0,00%  100,00%  8. SECURITE LIEE A L'EXPLOITATION  10,53%  78,95%  9. SECURITE DES COMMUNICATIONS  0,00%  100,00%  10. ACQUISITION, DEVELOPPEMENT ET MAINTENANCE DES SI  0,00%  71,43%  11. RELATION AVEC LES FOURNISSEURS  25,00%  100,00%  12. GESTION DES INCIDENTS DE CYBERSECURITE  12,50%  87,50%  13. GESTION DE LA CONTINUITE DE L'ACTIVITE  25,00%  75,00%  14. CONFORMITE  0,00%  100,00%   |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

Tableau 2 : Moyenne de conformité par chapitre de DNSSI

| ## Taux de conformité à la DNSSI  (Taux des règles mises en œuvre totalement)  76,70%   |
|-----------------------------------------------------------------------------------------|

## 2.3 Écarts dressés par type :

L'audit  a  permis  de  relever 19 fiches  d'écarts  dont  1 1  significatif,  07  non  significatifs  et  une remarque.

Le schéma ci-dessous illustre le pourcentage des écarts dressés par type :

Figure 2 : Illustration graphique des écarts dressés par type

<!-- image -->

## 3. Pistes significatives d'audit de conformité à la DNSSI

## 3.1 Politique de sécurité des systèmes d'information

Clauses :

DNSSI (POL-RISQUE, POL-FORMEL, POL-PAS, POL-TDB)

Objectifs :

Apporter à la sécurité des systèmes d'information (SI) une orientation et un soutien de la part de la Direction de l'entité ou l'IIV , conformément aux exigences métier et aux lois, règlements, directives et référentiels en vigueur.

Points de

contrôle :

- Analyse de risque

- Politique de sécurité des systèmes d'information

- Plan d'actions de la sécurité des SI

- Tableau de bord de la sécurité des SI

## Notes d'audit : Analyse de risque :

- -L'audité adopte une méthodologie de gestion des risques de sécurité SI propre  au  groupe,  définie  au  niveau  de  la  Politique  de  Gestion  des Risques de Sécurité des Systèmes d'Information élaborée en 2023 ;
- -Le département GRC (Gouvernance, Risque et Conformité) a réalisé en 2023, des analyses des risques de sécurité relatives à l'ensemble des plateformes critiques de l'audité, notamment les systèmes A, B, C, et D;
- -L'exercice d'analyse des risques a permis de dresser une cartographie de risque couvrant l'ensemble des systèmes sensibles du groupe ainsi que de définir un plan d'action pour le traitement des risques identifiés ;
- -Les besoins de sécurité en termes de de DICT (Disponibilité, Intégrité, Confidentialité  et  Traçabilité)  ont  été identifiés  pour  l'ensemble  des plateformes critiques du groupe.

## Politique de sécurité des systèmes d'information :

- -L'audité dispose d'une Politique de Sécurité des Systèmes d'Information (PSSI) élaborée en 2012 et mise à jour en 2015, validée et approuvée par le top management ;
- -Un projet de mise à jour de la feuille de route sécurité des SI élaborée en 2017 est en cours de réalisation. Ce projet est mené en partenariat avec  un  cabinet  externe.  Il  a  pour  objectif  d'évaluer  le  niveau  de maturité  de  la  sécurité  SI  de  l'audité  et  d'a ligner  les  orientations stratégiques  du  groupe  en  matière  de  sécurité  SI  aux  référentiels  en vigueur et aux exigences réglementaires ;
- -Une nouvelle Politique Globale de Sécurité des systèmes d'information (PGSSI) de l'audité est élaborée et est en cours de finalisation. Elle vise à intégrer les nouvelles orientations stratégiques du groupe et s'aligner aux différentes exigences réglementaires notamment celles introduites par la loi 05-20 et ses directives. Elle se veut aussi comme politique globale applicable à l'échelle du groupe .

## Preuves :

## Constats

## Plan d'actions de la sécurité des SI

- -L'audité dispose d'un plan d'action annuel global de la sécurité SI. Le suivi de l'implémentation de l'ensemble des projets qui y sont inscrits est assuré régulièrement par les équipes de la DC ;
- -La  feuille  de  route  sécurité  2024-2026  est  élaborée  et  comprend l'ensembles des projets à réaliser ainsi que le budget y associé ;

## Tableaux de bord de sécurité :

- -La  Direction  Centrale  de  Sécurité  assure  le  suivi  permanant  de l'implémentation  des  projets  inscrits  dans  le  cadre  du  plan  d'action globale de sécurité SI ;
- -Des indicateurs de suivi SSI sont régulièrement générés notamment par rapport à la sécurité opérationnelle, la conformité, la gouvernance ainsi qu'à l'audit et la veille sécurité et sont regroupés au niveau du tableau de bord de suivi de la sécurité SI ;
- -L'auto -évaluation de la conformité du SI AUDITÉ aux exigences de la DNSSI est effectuée régulièrement et le suivi de la mise en conformité à la DNSSI est assuré par le biais d'un outil propre à la DC.
- Interview
- Politique de gestion des risques de sécurité SI (Juin 2023)
- Cartographie des risques SSI des plateformes critiques et plan d'action pour le traitement des risques (Juillet 2023)
- PSSI AUDITÉ Version 2015
- Politique Globale de SSI 2023
- Plan d'action Global SSI 2023
- Suivi des projets DC T3 2023
- Feuille de route SSI 2024-2026
- Tableau de bord avec indicateurs -bilan septembre 2023
- Outil d'évaluation de la maturité DNSSI
- -L'exercice  d'analyse  de  risque  concerne  uniquement  les  plateformes sensibles  et  ne  couvre  pas  l'ensemble  du  système  d'information  de l'audité ;
- -Les besoins de sécurité en matière de DCIT ne sont pas identifiés pour l'ensemble des composantes du SI de l'audité ;
- -La politique globale de sécurité des systèmes d'information de l'audité élaborée en 2023 n'est pas validée par le top management.

## 3.2 Organisation de la sécurité

Clauses :

DNSSI (ORG-INTER-GOUV, ORG-INTER-RSSI, ORG-INTER-RESP, ORG-TELETRAV-SEC)

## Objectifs :

- Établir un cadre de gestion pour engager, puis vérifier la mise en œuvre et le fonctionnement de la sécurité du SI au sein de l'entité ou de l'IIV.

- Assurer la sécurité du système d'information de l'entité ou de l'IIV en cas d'adoption du télétravail.

## Points de

contrôle :

- Gouvernance de la sécurité des SI

- Désignation d'un responsable de la sécurité des SI (RSSI)

- Attribution des rôles et responsabilités

- Télétravail sécurisé

## Notes d'audit : Gouvernance de la sécurité des SI :

- -Une nouvelle organisation des structures en charge de la sécurité des systèmes d'information a été adoptée depuis Mars 2018. Cette refonte de l'organisation a donnée naissance à la Direction Centrale de la Sécurité dont les missions et composition sont définies par une note de service émanant de la présidence du directoire ;
- -Rattaché à la DC,  la Direction de Sécurité des Systèmes d' I nformation Groupe assure la sécurité SI à l'échelle de l'entreprise et de ses filiales ;
- -La Direction de Sécurité des SI est composée d'un Département de Gouvernance  de  sécurité,  risques  et  conformité  réglementaires, d' un Département d' Audit et de veille sécurité et d'un Département de Continuité Informatique ;
- -La sécurité opérationnelle relève hiérarchiquement du Pôle Systèmes d'Information Groupe (PSIG) ;
- -Plusieurs comités sont mis en place pour assurer le suivi global des projets SI et des actions de sécurité, notamment :
- o Le Comité stratégique de Sécurité de l'Information : l'instance de  direction  qui  valide  les  grandes  décisions  en  matière  de sécurité de l'information ainsi que  les décisions sur les évaluations et la surveillance des risques du Groupe ;
- o Le Comité des Risques Sécurité Groupe joue un rôle essentiel dans la protection des données, des systèmes et des infrastructures technologiques du Groupe contre les menaces et les  attaques  informatiques.  Il  assure  une  gestion  proactive  et structurée  des  risques  en  matière  de  sécurité  des  systèmes d'information en suivant les directives de la politique Globale de la SSI.
- -En ce qui concerne le suivi de la sécurité au niveau des filiales, il est prévu de mettre en place un comité de sécurité filiale dont la mission est d'assurer au sein de la filiale, le respect des politiques de  sécurité  locales  et  du  groupe  ainsi  que  le  suivi  des  plans

est considéré à part entière et de manière isolée sans tenir compte des contrôles présents au niveau des actifs sous-jacents.

## 4.3 Référentiels utilisés

Cet audit se base, pour chaque typologie d'actif et chaque technologie, sur un certain nombre de contrôles sélectionnés selon leur pertinence principalement à partir des référentiels ci-après :

- CIS Benchmarks
- DISA Security Technical Implementation Guides (STIGs)
- Guides de durcissement des configs et guides DGSSI
- Recommandations des éditeurs

## 4.4 Echelle d'évaluation

Les constats sont classés selon l'échelle de criticité ci -après détaillée. Cela reflète le niveau de risque introduit par la non implémentation ou la défaillance du contrôle associé.

| Niveau de criticité  Description  CRITIQUE  Il est impératif que des mesures soient prises immédiatement  pour réduire les risques de cette catégorie  ÉLEVÉE  Il est impératif que des mesures soient prises dans un court délai  pour réduire les risques de cette catégorie  MOYENNE  Des mesures doivent être prises dans un délai moyen pour réduire  les risques de cette catégorie  FAIBLE  Il s'agit de notes d'information sur des pratiques peu  recommandées, sans impact prouvé sur la sécurité   |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## 4.5 Résultats

Les  contrôles  vérifiés  dans  le  cadre  de  l'audit  technique  ainsi  que  le  résultat  de  cette vérification  figurent  dans  les  grilles  jointes  en  annexe.  Ces  résultats  peuvent  être synthétisés comme suit :