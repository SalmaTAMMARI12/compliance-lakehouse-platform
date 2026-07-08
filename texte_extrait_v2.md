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

## Preuves :

Constats d'actions associés.

## Désignation d'un responsable de la sécurité des SI (RSSI)

- -Le RSSI est le Directeur en charge de la Direction de Sécurité du SI rattachée à la Direction Centrale de la Sécurité du Groupe (DC). Ses missions sont définies au niveau de la note de service portant la création de la DC.

## Télétravail sécurisé :

- -Un guide de bonnes pratiques de gestions des accès logiques a été élaboré en 2020 en raison de la pandémie du COVID-19 et ce afin de  permettre  aux  différents  utilisateurs  d'accéder  aux  systèmes AUDITÉ  depuis  leurs  sites  de  télétravail  de  façon  sécurisée. T outefois,  après  la  pandémie,  l'accès  aux  systèmes  de  l'audité depuis des sites de télétravail a été restreint.
- Interview
- NS du 12-03-2008 Création de la Direction Centrale Sécurité Groupe
- Présentation de l'organisation DC V1.0
- Présentation de l'organisation du PSIG
- Présentation de la comitologie SSI AUDITÉ
- Compte rendu du comité opérationnel SSI (Mars 2023)
- Bonnes pratiques de gestion des accès logiques
- -Conforme aux exigences. Aucun écart relevé.

## 3.3 Sécurité des ressources humaines

| ## Clauses :  DNSSI  (RH-AVT-PERSON,  RH-AVT-COND,  RH-APRES-FORM,  RH-FIN- GEST)  ## Objectifs :  - S'assurer  que  le  personnel  et  les  contractuels  comprennent  leurs responsabilités  et  qu'ils  sont  compétents  pour  remplir  les  fonctions que l'entité ou l'IIV envisage de leur confier  - S'assurer que les employés et les contractuels sont conscients de leurs responsabilités en matière de sécurité des SI et qu'ils assument ces responsabilités.  - Protéger les intérêts de l'entité ou de l'IIV dans le cadre du processus de modification, de rupture ou de terme d'un contrat de travail.  ## Points de  contrôle :  - Personnel de confiance  - Termes et conditions d'embauche  - Formation et sensibilisation du personnel  - Gestion des mutations et départs  ## Notes d'audit : Personnel de confiance :  - Le processus de recrutement au sein de l'audité prévoit un tri de sélection et des tests de personnalité pour l'ensemble des candidats. Une attention particulière  est  adressée  au  candidats  critiques  appelés  à  occuper  des fonctions  sensibles  ou  à  exécuter  des  taches  sensibles  sur  des  sites critiques (conduite d'enquête d'environnement).   |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## Preuves :

Constats

## Termes et conditions d'embauche :

- -Avant leur prise de service, les nouvelles recrues sont tenues de signer un engagement de confidentialité ainsi que de prendre connaissance du code de déontologie et de la charte utilisateur.

## Formation et sensibilisation du personnel :

- -Une plateforme de formation et de sensibilisation E-learning est mise en place et pilotée par les équipes DC ;
- -Un programme de sensibilisation est établi annuellement. Ce programme englobe des modules SSI sur la plateforme E-learning et des sessions de sensibilisation  au  profit  des  nouvelles  recrues  et  des  collaborateurs  de l'audité ;
- -Un programme annuel de formation  au profit des développeurs et des équipes de la DC est établi.

## Gestion des mutations et départs

- -La  Direction  des  Habilitations  (DH)  est  chargée  de  la  gestion  des habilitations,  en  collaboration  avec  la  Direction  Générale  « Capital Humain » et les responsables métier, selon un processus bien défini au niveau de la procédure de gestion des habilitations ;
- -La  mise  à  jour  des  habilitations  se  fait  systématiquement  suite  à  la réception des états de décisions des ressources humaines notamment pour le  cas  des  désactivations  (démission,  départ  à  la  retraite,  changement d'affectation, licenciement etc. ) ;
- -Le processus de restitution des biens est établi et le retrait d'accès est assuré systématiquement en cas de départ ou de mouvement du personnel.
- Interview
- AUDITÉ Charte pour l'usage de ressources informatiques et de services
- Internet AUDITÉ Charte d'utilisation du service Accès distant v1.0
- AUDITÉ Charte utilisateur pour l ' usage des ressources informatiques et des services Internet -v2.1
- Code déontologie de l'audité
- Engagement de confidentialité
- Planning des compagnes de sensibilisation à la cybersécurité 2023
- Programme de formation en cybersécurité 2023
- Procédure de gestion des habilitations 2015.
- Exemple d'Etat récapitulatif des décisions de cessation communiqué par les RH.
- -Conforme aux exigences. Aucun écart relevé.

## Clauses :

## Objectifs :

## Points de contrôle :

DNSSI (ACTIF-RESP-INV, ACTIF-RESP-PROP, ACTIF-RESP-CHARTE, ACTIF-RESP-CARTO, ACTIF-CLASSIF-INFO, ACTIF-CLASSIF-MES, ACTIFCLASSIF-EXAM, ACTIF-SUP-AMOV, ACTIF-SUP-MOBIL, ACTIF-SUPNOMAD, ACTIF-SUP-REB)

- -I dentifier les actifs informationnels de l'entité ou de l'IIV et définir les responsabilités appropriées en matière de protection.
- -S'assurer que les actifs informationnels bénéficient d'un niveau de protection approprié conforme à leur importance pour l'entité ou pour l'IIV.
- -Empêcher la divulgation, la modification, le retrait ou la destruction non autorisé(e) de l'information de l'entité ou de l'IIV stockée sur des supports et assurer la sécurité de l'utilisation des appareils mobiles.
- Inventaire des actifs
- Propriétaires des actifs
- Charte d'utilisation du SI
- Cartographie SI
- Classification
- Mesures de protection des informations
- Examen de la classification
- Gestion des supports amovibles
- Politique en matière d'appareils mobiles
- Postes nomades
- Mise au rebut ou recyclage des supports

## Notes d'audit : Inventaire des actifs :

- -Chaque équipe au niveau de l'audité dispose d'un inventaire des actifs matériels dont elle est en charge.
- -La liste des logiciels installés avec version existe et sont placés sous la responsabilité de l'équipe PSIG ;
- -Le projet d'acquisition d'une CMDB afin de consolider l'ensemble des inventaires est en cours de réalisation.

## Charte d'utilisation du SI

- -L'audité  dispose  d' une  charte utilisateur  pour  l'usage  des  ressources informatiques et des services Internet, mise à jour en 2023 et qui prend en charge les exigences législatives et réglementaires en vigueur et qui contient une clause de confidentialité des données.
- -La  dernière  version  de  la  charte  est  en  cours  de  validation  par  la hiérarchie et sera mise à disposition de l'ensemble des collaborateurs au niveau du système SIRH ;

## Cartographie SI

- -Les cartographies réseaux et applicatives existent et sont régulièrement tenues à jour ;

## Classification des actifs informationnels :

## Preuves :

## Constats

- -L'audité a  élaboré  une  politique  de  classification  du  patrimoine informationnel qui définit les échelles de classification, la démarche de classification ainsi que les principes de marquages et de manipulation des données selon leur niveau de classification ;
- -L'exercice de classification du patrimoine informationnel de l'audité est inscrit dans le cadre du plan d'action pour l'année 2024 ;

## Mesures de protection des informations

- -Un guide de marquage et de manipulation des actifs informationnels selon leur sensibilité sera élaboré à l'issue de l'exercice de classification planifié pour 2024 ;
- -Des  sessions  de  sensibilisation  relatives  à  la  classification  et  aux mesures de protection des informations sont prévues dans les prochaines campagnes de sensibilisation ;

## Gestion des supports amovibles

- -L'utilisation sécurisée des appareil s mobiles est stipulée au niveau de la charte d'utilisation des ressources informatiques de l'audité ;

## Mise au rebut ou recyclage des supports

- -Une procédure de mise au rebut est élaborée. Elle identifie les différents intervenants et décrit les étapes et les contrôles nécessaires à la maitrise de la mise au rebut sécurisée des actifs informatiques de l'audité.
- Interview
- Architecture réseau et applicative
- Cartographie applicative
- Liste des logiciels
- AUDITÉ \_Charte pour l'usage de ressources informatiques et de services internet v2011
- AUDITÉ\_Charte utilisateur pour l ' usage des ressources informatiques et des services Internet -v2.1 2023
- Politique classification du patrimoine informationnel
- Procédure de mise au rebut
- Canevas Rapport d'homologation
- Canevas procédure d'exploitation de sécurité (pour les SIS)
- -Absence d'un  inventaire  complet,  consolidé  et  mis  à  jour  de l'ensemble des actifs (matériels et logiciels) avec leurs versions, les correctifs appliqués, les n° de License etc.
- -La dernière version de la charte est en cours de validation par la hiérarchie et le processus de sa communication et signature par l'ensemble  des  collaborateurs  et  personnes  concernées  est  en cours d'instauration ;
- -A  l'issue  de  l'exercice  de  classification  planifié  pour  2024, l'audité  procèdera  à  la déclaration  actualisée  des  SI  Sensibles conformément à la loi 05-20. L'exercice d'homologation des SI sensibles identifiés selon les canevas préalablement élaborés sera conduit à cet effet.

## 3.5 Contrôle d'accès

## Clauses :

DNSSI  (ACC-EXIG-POL,  ACC-UTILIS-ENREGIS/DESINSCRI,  ACC-UTILISIDF/AUTH, ACC-UTILIS-HABILIT, ACC-UTILIS-GENERIQ, ACC-UTILISREVUE, ACC-SYS/APP-ACC, ACC-SYS/APP-PRIVIL, ACC-SYS/APP-MDP)

## Objectifs :

## Points de contrôle :

- -Limiter  l'accès  à  l'information  et  aux  moyens  de  traitement  de l'information.
- -Maîtriser l'accès utilisateur par le biais d'autorisations et empêcher les accès non autorisés aux systèmes et services d'information
- -Empêcher les accès non autorisés aux systèmes et aux applications
- Politique de contrôle d'accès
- Enregistrement et désinscription des utilisateurs
- Identification et authentification
- Gestion des habilitations
- Gestion des comptes génériques
- Revue des droits d'accès
- Accès aux systèmes et applications
- Gestion des accès à privilèges
- Gestion des mots de passe

## Notes d'audit : Gestion de l'accès utilisateurs

## :

- -L'audité dispose d' une procédure de gestion des habilitations qui définit les  règles  à  mettre  en  place  afin  d'assurer le  traitement  et  la  prise  en charge des demandes d'accès validées par les responsables hiérarchiques habilités, de garantir la gestion des profils et des accès octroyés au SI ainsi que  d' avoir  une  vision  consolidée  des  habilitations  attribuées  aux différents utilisateurs ;
- -La  Direction  des  Habilitations  (DH)  est  chargée  de  la  gestion  des habilitations,  en  collaboration  avec  la  Direction  Générale  « Capital Humain » et les responsables métier, selon un processus bien défini au niveau de la procédure de gestion des habilitations ;
- -Au niveau des régions, des relais RH sont désignés en tant qu'interlocuteurs de la DH afin de faciliter la gestion des accès logiques conformément à la procédure en vigueur ;
- -Un projet d'optimisation du processus de gestion des accès est en cours de réalisation et a pour objectif entre autres de :
- Mettre à jour la procédure de gestion des habilitations
- Centraliser le traitement des demandes d'accès au niveau de la Direction des Habilitations en priorisant dans un 1 er lieu les SI critiques
- Mettre  en  œuvre  un  outil  pour  digitaliser  le  processus  de traitement des demandes et de l'octroi des accès

## Preuves :

## Accès aux systèmes et applications

- -L'attribution  des  droits  d'accès  aux  applications  se  fait  à  travers  une demande d'accès validée par les responsables hiérarchiques habilités ;
- -Une  matrice  d'habilitation  relative  aux  systèmes  et  équipement  de sécurité est établie ;
- -Les comptes à privilèges sont inventoriés et mis à jour régulièrement.

## Revue des droits d'accès

- -La revue des droits d'accès est assurée régulièrement et la mise à jour des habilitations  se  fait  systématiquement  suite  à  la  réception  des  états  de décisions des ressources humaines notamment pour le cas des désactivations (démission, départ à la retraite, changement d'affectation, licenciement etc.) ;

## Gestion des Mots de passe

- -La politique de gestion des mots de passe est appliquée via une stratégie de groupe GPO.
- Interview
- Politique de gestion des accès logiques 2023 (en cours de validation)
- Procédure de gestion des habilitations 2015
- Exemple de demande d'accès logique signé (septembre 2023)
- Matrice d'habilitation RH
- Matrice d'habilitation technique
- Extrait de la liste des comptes à privilège
- Politique de gestion des mots de passe (2023)

## Constats

- -La politique de gestion des accès logique élaborée en 2023 est toujours en cours de validation par la hiérarchie.
- -Les  règles  relatives  à  la  gestion  des  mots  de  passe  d'accès  aux applications sont définies au niveau d'une politique de gestion de mots de passe. Toutefois, cette politique n'est pas encore validée.

## 3.6 Cryptographie

| Clauses :  DNSSI (CRYPTO-MES-POL, CRYPTO-MES-GESTCLE).  Objectifs :  - Garantir l'utilisation correcte et efficace de la cryptographie en vue de protéger la confidentialité, l'authenticité et l'intégrité de l'information.  Points de  contrôle :  - Politique d'utilisation des mesures cryptographiques  - Gestion des clés cryptographiques   |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

| ## Notes d'audit :  - La Entreprise met en œuvre des mesures cryptographiques sur différents plans. En effet les équipes de sécurité ont élaboré un document détaillant quatorze différents  cas  d'usages  de  chiffrements  adoptés  au  sein  du Groupe.  Ceux-là couvrent aussi bien les données en stockage que les données et communications en transit.  - Tous les disques durs des postes de travail CAM sont chiffrés.  ## Preuves :  - Interview  - Politique de gestion des clés cryptographiques  - Use cases cryptographiques au sein de l'audité  ## Constats  - La politique de gestion des clés cryptographiques a été élaborée et est en cours de validation.   |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## 3.7 Sécurité physique

| ## Clauses :  DNSSI  (PHYS-ZONE-DELIMIT,  PHYS-ZONE-PROC,  PHYS-ZONE-DISPO, PHYS-ZONE-VIDEOPROT, PHYS-ZONE-INCEN, PHYS-ZONE -EAU, PHYS- MAT-CABL, PHYS-MAT-OND, PHYS-MAT-ELECTROG, PHYS-MAT-CLIM, PHYS-MAT-EQUIP, PHYS-MAT-HORSLOC).  ## Objectifs :  -  Empêcher tout accès physique non autorisé, tout dommage ou intrusion portant sur l'information et les moyens de traitement de l'information de l'entité ou de l'IIV.  - Empêcher la perte, l'endommagement, le vol ou la compromission des actifs informationnels et l'interruption des activités de l'entité ou de l'IIV .  ## Points de contrôle :  - Délimitation des zones  - Procédures de contrôle d'accès  - Dispositif de contrôle d'accès  - Vidéo protection  - Sécurité incendie  - Dégâts des eaux  - Sécurité du câblage  - Onduleurs  - Groupe électrogène  - Climatisation  - Entretien des équipements de sécurité environnementale  - Sécurité du matériel et des actifs hors les locaux  ## Notes d'audit :  ## Délimitation des zones :  - Les zones physiques de sécurité sont bien identifiées et regroupées en trois zones, à savoir : zones d'accès au public, zones d'accès contrôlé et zones sensibles ;  Procédure de contrôle d'accès :   |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## Preuves :

- -L'audité a mis en place un dispositif de sureté et de sécurité des sites du  siège.  Ce  dispositif  définit  le  rôle  et  les  responsabilités  des différents acteurs qui interviennent dans la sécurisation des sites du siège, les modalités d'accès pour les détenteurs de badges permanents et  non  permanents,  les  équipements  de  sureté  et  de  sécurité  qui équipent les bâtiments du siège ainsi que les consignes à suivre en cas de sinistre.
- -L'accès  à  la  salle  machine  de  l'audité  est  régit  par  une  procédure spécifique de gestion des accès ;
- -Au niveau des filiales, des guides et des consignes de sécurité sont élaborés et diffusés à l'ensemble des collaborateurs concernés.

## Dispositif de contrôle d'accès :

- -Les accès aux locaux de l'audité sont maitrisés via des dispositifs de contrôle d'ac cès individuel ;
- -Une note de  service  régissant  les  accès  des  visiteurs  aux  différents locaux de l'audité a été élaborée en 2017 ;
- -Les visiteurs sont amenés à déposer leurs cartes d'identité nationales chez l'agent de sécurité et se font attribuer un badge visiteur numéroté. Quant aux prestataires,  agents  de  service  et  stagiaires,  ils  se  voient attribuer un badge « Prestataire/Stagiaire » numéroté.  La traçabilité de leurs accès est assurée par le biais d'un registre chez l'agent d'accueil.
- -Les personnes tierces accèdent aux zones sensibles accompagnées du personnel de l'audité et doivent renseigner des registres à cet effet.

## Sécurité environnementale :

- -Un système de vidéo surveillance est mis en place et supervisé par un poste de contrôle de sécurité ;
- -Les  locaux  techniques  sont  équipés  de  mécanismes  de  sécurité environnementale  conformes  à  la  certification  TIER  III  Facility (délivrée en mars 2022) . L' ensemble est supervisé par le biais d'une plateforme de Gestion Technique Centralisée ;
- -Tous  les  équipements  de  sécurité  physique  sont  sous  contrat  de maintenance et le test de leur fonctionnement est assuré périodiquement ;
- -Le câblage électrique et câblage réseau sont bien identifiés (étiquetés),  et  séparés  (câbles  déroulés  en  faisceaux  clairs  et  non emmêlés) ;
- -L'audité dispose d'onduleurs et de groupes électrogènes adaptés aux besoins du groupe ;

## Sortie du matériel et des actifs hors locaux de travail :

- -La sortie des actifs fait l'objet un bon de sortie délivré aux agents de sécurité.
- Interview
- Visite des lieux
- Document Zoning des deux sites
- NS du 15.01.2016 Mise en place de la solution de contrôle d'accès et de gestion de temps de présence

Constats

- Procédure de gestion d ' accès à la salle machine V 1.2
- NS n° 5-1-D Gestion des clés des bureaux et locaux des sites du CAM
- NS N°-17-D Accès des visiteurs aux locaux de l'audité
- NS N°-19-D Dispositif de sécurité des sites du siège
- ARCHI05\_Rapport de test des installations techniques DC PROD AUDITÉ 2023
- ARCHI 06\_Rapport de test de la solution de détection incendie et d'extinction automatique 2023
- -Conforme. Aucun écart relevé.

## 3.8 Sécurité liée à l'exploitation

## Clauses :

## Objectifs :

## Points de contrôle :

DNSSI (EXP-PROC-CHANG, EXPPROC-CAP, EXP-PROC-ENVIR, EXPPROTEC-MALVEIL,  EXP-SAUV-PROC,  EXP-SAUV-RESTAUR,  EXP-SAUV-SEC, EXP-JOURN/SURV-JOURNAL,  EXP-JOURN/SURV-PRIVIL,  EXP-JOURN/SURVMAINT, EXP-JOURN/SURV-SYNCHRON, EXP-JOURN/SURV-DIST, EXPJOURN/SURV-CENTR, EXP-SYS-CONFIG, EXP-SYS-DURC, EXP-VULNINSTALL, EXP-VULN-GEST, EXP-VULN-CORRECT, EXP-AUDIT-MES).

- -S'assurer de l'exploitation correcte et sécurisée des moyens de traitement de l'information.
- -Garantir que l'information et les moyens de traitement de l'information sont protégés contre les logiciels malveillants.
- -Se protéger contre la perte de données.
- -Enregistrer les événements et générer des preuves
- -Garantir  l'intégrité  des  systèmes  en  exploitation  et  empêcher  toute exploitation des vulnérabilités techniques.
- -Réduire au minimum l'incidence des activités d'audit sur les systèmes en exploitation.
- Gestion des changements
- Gestion des capacités
- Séparation des environnements
- Protection contre les logiciels malveillants
- Procédures de sauvegarde
- Restauration
- Sécurité des sauvegardes
- Journalisation des événements
- Traçabilité des actions des comptes à privilège
- Traçabilité des actions de maintenance
- Synchronisation des horloges

## Notes

## d'audit :

- Administration à distance
- Centralisation
- Configuration système
- Durcissement des configurations
- Restrictions liées à l'installation de logiciels
- Gestion des vulnérabilités techniques
- Gestion des correctifs
- Mesures relatives à l'audit du système d'information

## Procédures et responsabilités liées à l'exploitation :

- -Une  équipe  dédiée  au  niveau  de  la  salle  de  surveillance  assure  une supervision 24/7 des réseaux et systèmes de l'audité et est chargée d'alerter les administrateurs en cas de problème. Des solutions telles que ZABBIX, SOLARWIND  et Dynatrace sont utilisées afin d'analyser le bon dimensionnement des systèmes et réseaux et garantir la disponibilité du SI.

## Protection contre code malveillants :

- -La  protection des serveurs et postes de travail contre les logiciels malveillants est assurée par la solution de protection TrendMicro déployée sur tout le parc informatique et mise à jour régulièrement ;

## Sauvegarde et restauration :

- -L'audité dispose d'une politique de sauvegarde qui précise pour chaque système la nature des sauvegardes à effectuer, leur fréquence ainsi que les types de supports utilisés. A cet effet des plans de sauvegarde sont élaborés pour chaque système ;
- -La sauvegarde est effectuée par le biais de deux solutions : IBM Spectrum pour les systèmes AIX et VEEAM pour les serveurs virtuels ;
- -Une procédure de restauration est élaborée pour les deux plateformes de sauvegarde utilisée ;
- -Les  tests  de  restauration  sont  effectués  de  façon  régulière  selon  un planning prédéfini et sont sanctionnés par des PV ;
- -Les supports de sauvegarde sont stockés dans des coffres forts au niveau du Datacenter et du site de Backup;

## Journalisation et surveillance :

- -Les logs des applications et systèmes sont collectés par la solution IBM QRADAR et sont supervisés et analysés  régulièrement  par  les  équipes SOC ;
- -L'audité dispose d'un serveur NTP pour la synchronisation des horloges ;

## Maitrise des logiciels en exploitation et gestion des vulnérabilités techniques :

## Preuves :

- -Les procédures d'administration et de configuration sont documentées et se  basent  sur  les  bonnes  pratiques  des  éditeurs  ainsi  que  les  dossiers d'ingénierie ;
- -Mes missions d'audit de sécurité sont effectuées avant le déploiement des configurations. Une attestation de sécurité est délivrée à cet effet ;
- -Les configurations des équipements réseaux et de sécurité sont sauvegardées quotidiennement ;
- -Le contrôle applicatif  est  assuré  via  l'outil  Trend  Micro  qui  permet  de maitriser l'installation et l'exécution des logiciels autorisés uniquement ;
- -La gestion centralisée des mises à jour des systèmes est assurée par le biais de  l'outil  SSCM.  Des  tests  et  des  qualifications  des  mises  à  jour  sont effectués dans un environnement préprod avant leur déploiement ;

## Gestion des vulnérabilités techniques :

- -L'équipe  SOC  assure  la  veille  technologique  et  le  suivie  global  des vulnérabilités  techniques.  Une  attention  particulière  est  accordée  aux alertes et vulnérabilités remontées par le maCERT ;
- -L'audité a  élaboré  une  procédure  qui  décrit  les  étapes  et  les  contrôles nécessaires pour l'identification, la classification et la réponse efficace aux vulnérabilités techniques de son système d'information. Cette procédure gère également le suivi et l'application des correctifs de sécurité.

## Considérations sur l'audit du système d'information :

- -L'audité dispose d'une méthodologie de déroulement des audits technique réalisées  par  les  équipes  de  la  Direction  Centrale  de  la  Sécurité  de l'information.
- Interview
- AUDITÉ\_Politique de sauvegarde\_v1.0
- Planning de test de restauration des environnements de production 2023
- AUDITÉ\_Procédure de Restauration des données\_v1.0
- APPORT DE TEST ET DE VERIFICATION DES sauvegarde - GED Production Windows 2000 - 23012023
- RAPPORT DE TEST ET DE VERIFICATION DES sauvegarde SOLARWINDS-BD -01022023
- RAPPORT DE TEST ET DE VERIFICATION DES sauvegarde -DA BD et APP- 24062023
- Procédure de gestion des vulnérabilités
- Méthodologie de déroulement des audits techniques

## Constats

- -Absence de procédure formelle de gestion des changements couvrant tous les types de changements aussi bien applicatifs que d'infrastructure et respectant le cycle : demande, validation, application et contrôle ;
- -L'audité dispose d'un réseau dédié pour les administrateurs. Toutefois, les postes utilisés à cet effet sont connectés à internet et sont utilisés pour des activités autres que l'administration ;
- -Les données sensibles sauvegardées ne sont pas chiffrées ;
- -Bien que les accès (distants et sur site) effectués par les prestataires soient contrôlés, aucun mécanisme n'est mis en place afin de vérifier leurs actions. Le projet d'acquisition et de mise en place du Bastion WALLIX est inscrit dans le plan d'action sécurité ;
- -Absence  de  procédures  et  de  guides  de  durcissement.  Un  projet d'élaboration d'un  référentiel de durcissement  est en cours de réflexion.

## 3.9 Sécurité des communications

## Clauses :

## Objectifs :

## Points de contrôle :

## Notes d'audit :

DNSSI (COM-MANAG-CLOISON, COM-MANAG-FILTRAGE, COM-MANAGSYSAUT, COM-MANAG-DISTANT, COM-MANAG-TUNEL, COM-MANAG-RSF, COM-TRANS-FICHIER, COM-TRANS-MESS, COM-TRANS-FILTR)

- -Garantir  la  protection  des  informations  sur  les  réseaux  et  des moyens de traitement de l'information sur lesquels elle s'appuie
- -Maintenir la sécurité de l'information transférée au sein de l'entité ou de l'IIV et vers l'extérieur .
- Cloisonnement du réseau
- Filtrage des flux
- Systèmes autorisés sur le réseau
- Accès distants
- Tunnelisation chiffrée
- Sécurité des réseaux sans fil
- Usage des transferts par fichiers
- Usage de la messagerie électronique
- Filtrage des mails

## Cloisonnement du réseau :

- -L'audité adopte une stratégie de cloisonnement conformément à la criticité des systèmes à protéger ;
- -Une  segmentation  par  VLAN  fonctionnel  (par  métier)  est adoptée au niveau du réseau AUDITÉ ;

## Preuves :

Constats

## Filtrage des flux :

- -Le filtrage des flux réseau x entrants et sortants de l'audité est assuré via des mécanismes de filtrage et de contrôle.

## Systèmes autorisés sur le réseau :

- -L' accès au réseau AUDITÉ est contrôlé via l'adresse MAC . Un projet d'acquisition d'une solution NAC est planifié.

## Accès distant :

- -L'accès externe au réseau de la direction se fait via VPN /IPSEC. L'authentification à double facteur/Multi facteur est obligatoire pour tous les accès distants ;
- -Un mécanisme de géolocalisation VPN est mis en place afin de contrôler les régions depuis lesquelles les connexions distantes sont effectuées. Une white liste est élaborée à cet effet et est partagée avec les équipes SOC ;
- -Un  état de supervision journalier des accès distants est communiqué par le SOC aux équipes de sécurité de la direction de la sécurité de l'information ;

## Usage de la messagerie électronique

- -Les  règles  de  bon  usage  de  la  messagerie  électronique  sont définies  au  niveau  de  la  charte  d'utilisation  des  ressources informatiques et des services internet ;

## Filtrage des mails

- -Le filtrage des  courriers émis et reçus est  assuré (Anti-spam, Scan des pièces jointes, …) .
- Interview
- Architectures réseaux
- Charte d'utilisation des ressources informatiques et des services internet ;
- Etat des accès distants communiqué par le SOC
- Procédure de gestion des accès distants
- -La matrice des flux n'est pas documentée ;

## 3.10 Acquisition, développement et maintenance des systèmes d'information

| Clauses :  DNSSI  (DEV-EXIG-PROJET,  DEV-EXIG-TRANSAC,  DEV-PROC-POL,  DEV- PROC-CHANG, DEV-PROC-ENVIR, DEV-PROC-TEST, DEV-PROC-CODE, DEV- PROC-DONNEE,)  Objectifs :  - Veiller à ce que la sécurité fasse partie intégrante des SI tout au long de leur cycle de vie.   |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## Points de contrôle :

## Preuves :

## Constats

-

S'assurer que la sécurité de l'information est mise en œuvre dans le cadre du  cycle  de  développement  des  SI  conformément  aux  référentiels  et guides en vigueur.

- -Sécurité de l'information dans la gestion de projet
- -Protection des transactions liées aux services d'application
- -Politique de développement sécurisé
- -Contrôle des changements apportés au système dans le cycle de développement
- -Environnement de développement sécurisé
- -Test de la sécurité du système
- -Protection des données de test

## Notes d'audit : Exigences de sécurité applicables aux systèmes d'information

- -L'audité dispose d'une charte de gestion de projet qui prend en charge la sécurité et les risques de sécurité dans toutes les étapes de l'exécution du projet depuis la planification jusqu'à la mise en production ;
- -Des audits de sécurité et tests d'intrusion sont effectués par les équipes de  la  direction  de  la  sécurité  de  l'information  avant  la  mise  en production et la livraison du projet ;

## Sécurité des processus de développement et d'assistance techniques

- -L'audité dispose d'un guide de bonnes pratiques pour le développement des applications web ;
- -Les environnements de développement, recette, et de production sont bien séparés ;
- -L'accès aux codes source est protégé par des outils de gestion et de versionning (SVN et GITLAB) ;
- -Les données utilisées lors des tests sont anonymisées ;
- Interview
- Charte de gestion des projets
- Guide de bonnes pratiques pour le développement des applications web
- -Des  pratiques  pour  la  gestion  des  changements  sont  appliquées systématiquement.  En  effet,  les  équipes  de  développement  dispose d'un  fichier  Excel  ou  sont  recensées  toutes  les  modifications  et changement  apportées  aux  applications  développées.  Cependant, au cune  procédure  formelle  n'est  en  vigueur  pour  la  gestion  des changements.

## 3.11 Relation avec les fournisseurs

## Clauses :

DNSSI (FOURNIS-REL-RISQ, FOURNIS-REL-POL, FOURNIS-REL-EXIG, FOURNIS-GEST-SURVEIL)

## Objectifs :

## Points de contrôle :

## Notes d'audit :

## Preuves :

- -Garantir la protection des actifs de l'entité ou de l'IIV accessibles aux fournisseurs
- -Maintenir un niveau convenu de sécurité de l'information et de prestation de services, conformément aux accords conclus avec les fournisseurs.
- Risques émanant des fournisseurs
- Politique de sécurité de l'information dans les relations avec les fournisseurs
- Exigences contractuelles
- Surveillance et revue des services des fournisseurs

## Sécurité de l'information dans les relations avec les fournisseurs

- -Les clauses de sécurité et de protection de l'information sont inclus dans les cahiers de charge depuis 2018 ;
- -Chaque prestataire doit  renseigner un questionnaire d'évaluation de niveau de sécurité. Selon les résultats de cette évaluation, les exigences de confidentialité et de protection de l'information ainsi que les délais d'intervention à mettre au niveau des contrats sont définit ;
- -Chaque prestataire ayant accès au SI de l'AUDITÉ est tenu de signer un engagement de confidentialité et de protection de l'information ;

## Gestion de la prestation de service

- -La direction de sécurité de l'information mène des audits de sécurité sur toutes les prestations délivrées par les prestataires afin d'assurer qu'elles ne présentent aucun risque de sécurité et délivre à cet effet une attestation de sécurité.
- Interview
- CPS\_AOO\_46\_11
- Contrat PASSI
- Exemple lettre d'engagement signée
- Attestation de conformité de sécurité- MAR202100049-
- Politique de sécurisation des relations avec les fournisseurs /prestataires
- Politique de sécurité Cloud
- Clauses contractuelles types (fournisseurs/prestataires)
- Clauses contractuelles sécurité Cloud.

## Constats

- -L'audité a élaboré une politique de sécurisation des relations avec les fournisseurs /prestataires , une politique de sécurité cloud ainsi qu'une liste  des  clauses  contractuelles  types  pour  toutes  les  prestations  de service y compris le cloud. Toutefois ces documents sont toujours en cours de validation.

## 3.12 Gestion des Incidents de cybersécurité

## Clauses :

## Objectifs :

## Points de contrôle :

## Notes d'audit :

DNSSI (INCID-GEST-PROC, INCID-GEST-CAT, INCID-GEST-SIGNAL, INCIDGEST-QUALIF,  INCID-GEST-REPONSE,  INCID-GEST-ALERT,  INCID-GESTREP, INCID-GEST-PREUV)

- -Garantir  une  méthode  cohérente  et  efficace  de  détection  et  de traitement des incidents de cybersécurité, incluant la communication des événements et des failles liés à la sécurité.
- Procédures et responsabilités en matière de gestion des incidents
- Catégorisation et classification des incidents
- Signalement des événements
- Qualification des événements
- Réponse aux incidents liés à la sécurité des SI
- Réaction aux alertes liés à la sécurité des SI
- Répertoire d'incidents
- Recueil des preuves

## Procédure et responsabilités en matière de gestion des incidents :

- -La gestion des incidents de sécurité au niveau de l'audité est soumise à une politique élaborée décrivant le processus de détection, de signalement, d'évaluation et de catégorisation des incidents de cybersécurité, les  mesures  d'intervention  et  de  traitement  y  afférentes , ainsi que les rôles et responsabilités des acteurs concernés ;

## Signalement des évènements :

- -Les utilisateurs sont tenus à travers la PSSI, la charte de sécurité ainsi que les différentes sessions de sensibilisation à la sécurité, à déclarer tout incident de sécurité par téléphone ou par email au service helpdesk ou à l'é quipe de la sécurité de l'Information Groupe ;
- -Les  incidents  de  sécurité  majeurs  sont  signalés  au  ma-CERT  et  au régulateur.

## Qualification des évènements :

- -L'équipe sécurité de la Direction Centrale de la Sécurité de l'information Groupe  est  chargé  de  la  qualification  et  de  la  catégorisation  des évènements avant de procéder à leur analyse et résolution en

## Preuves :

## Constats

collaboration  avec  les  équipes  en  charge  de  l'investigation  et  de  la réponse aux incidents de sécurité ;

## Réponse aux incidents liés à la sécurité des SI :

- -L 'analyse  et  l' investigation  ainsi  que  la  résolution  des  incidents  de sécurité  sont  la  responsabilité  d'une  équipe pouvant  faire  intervenir plusieurs  membres  notamment  l'équipe  SOC,  les  équipes  de  sécurité opérationnelle  ou  des  équipes  externes  mandatées  pour  l'analyse  et l'investigation dans le cadre de contrats établis avec l'audité ;
- -L'audité  dispose  de  plusieurs  modes  opératoires  de  réponse couvrant l'essentiel des incidents de sécurité envisageables ;
- -A l'issue de la résolution de l'incident de sécurité, une fiche est élaborée détaillant  tous  les  aspects  relatifs  à  l'incident  en  question  (sévérité, impact, source d'attaque, cause, résultat d'analyse, …)
- -Un  contrat  est  conclu  avec  PASSI  afin  de  réaliser,  à  la  demande  de l'audité,  de  missions  d'investigation  des  incidents  de  sécurité sur  tout type de système d'exploitation ;

## Répertoire d'incidents :

- -L'équipe sécurité de la Direction Centrale de la Sécurité de l'information Groupe dispose d'un répertoire des incidents de sécurité survenus avec leur typologie et description. L'audité prévoit l'acquisition d'un outil de ticketing pour la gestion des incidents.
- Interview
- Exemple de fiche d'incident résolu
- Politique de gestion des incidents de sécurité
- Mode opératoire « Phishing »
- Contrat d'investigation avec PASSI.
- -La politique de gestion des incidents n'est pas encore validée par la hiérarchie. Elle n'est pas conforme à la règlementation en vigueur. En effet, la politique fait référence au décret n°2-15-712 qui a été abrogé après la promulgation de la loi 05-20 ;

## 3.13 Gestion du plan de continuité de l'activité

| ## Clauses :  DNSSI (CONTINU-BIA, CONTINU-ACT, CONTINU-PLAN, CONTINU-EXERCICE)  ## Objectifs :  Neutraliser  les  interruptions  des  activités  de  l'entité,  protéger  les processus métier cruciaux des effets causés par les principales défaillances des systèmes d'information ou par des sinistres et garantir une reprise de ces processus dans les meilleurs délais.   |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## Points de contrôle :

## Preuves :

- Analyse BIA ;
- Plan de continuité et de reprise d'activité (PCA/PRA)
- Mise à l'essai des PCA/PRA
- Exercices et Scenarios

## Notes d'audit : Analyse d'impact sur l'activité :

- -Une  analyse d'impact  sur  l'activité  (BIA)  a  été  réalisée  afin  de recenser  l'ensemble  des  activités  et  processus  critiques  au  sein  de l'AUDITÉ, d'analyser les risques associés et de définir les objectifs de reprise RPO/RTO pour chaque processus métier.
- -La revue du BIA est assurée à une fréquence annuelle ou suite à des évolutions ou changements au niveau des activités et processus métier.

## Plan de continuité et de reprise d'activité :

- -L'audité dispose d'un dispositif de gestion du Plan de Continuité de l'Activité et du plan de continuité informatique qui définit l'organisation, les missions et les re sponsabilités des différents acteurs impliqués et qui est applicable à l'entreprise et toutes ses filiales ;
- -La gestion de ce dispositif relève des responsabilités de la direction PCA au sein du pôle développement,
- -L'audité dispose également de deux procédures de déclanchement du dispositif PCA/PCI au niveau du siège et au niveau des filiales. Ces procédures  décrivent  les  modalités  de  déclenchement  du  PCA,  les rôles et responsabilités des différents intervenants afin de garantir la poursuite et le rétablissement rapide du cours normal des activités de l'Entreprise en cas de sinistre.

## Tests du PCA :

- -Des tests de mise à l'essai du PCA sont effectués régulièrement à une fréquence trimestrielle afin de s'assurer de son efficacité. Chaque test donne lieu à un plan d'action d'amélioration ;
- Interview
- Liste des activités critiques de l'audité.
- Fiche BIA Leasing
- Fiche BIA Direction centrale Flux et Services
- Fiche BIA Direction centrale e
- Fiche BIA Direction Production SI
- Fiche BIA Direction Risque Marché
- Présentation du dispositif de continuité d'activité au sein de l'audité
- Dispositif de gestion du Plan de Continuité d'activité- Plan de Continuité Informatique
- NS n°84.D du 04.11.2017 Procédures de déclenchement du Plan de Continuité d'Activité PCA filiale et Siège
- Rapport test PCA Direction Risques Marché
- Rapport test PCA Filiale Leasing
- Rapport test PCA Filiale Rabat
- Rapport test PCA Filiale DR Rabat

Constats

## 3.14 Conformité

## Clauses :

DNSSI (CONF-OBLIG-IDF, CONF-OBLIG-CYBERSEC, CONF-OBLIG- INTELLECT, CONF-OBLIG-PERSO, CONF-OBLIG-CRYPTO , CONF-REVU-SSI)

## Objectifs :

-  Eviter toute violation des obligations légales, réglementaires, statutaires, ou contractuelles et des exigences de sécurité ;

- Garantir  que  la  sécurité  des  SI  est  mise  en  œuvre  et  appliquée conformément aux politiques et procédures organisationnelles

## Points de contrôle :

- Identification de la législation en vigueur

- Conformité à la réglementation liée à la cybersécurité

- Droits de propriété intellectuelle

- Protection des données personnelles

- Réglementation relative aux mesures cryptographiques

- Vérification de la conformité de la sécurité des SI

## Notes d'audit :

## Conformité aux obligations légales et réglementaires :

- -La protection du droit de la propriété intellectuelle est assurée à travers la mise en place d'un processus de contrôle de l'utilisation des logiciels sous licence ;
- -La mise en conformité à la loi 09-08 relative à la protection des données à caractère personnel en collaboration avec la CNDP est assuré ;
- -L'ensemble  des  exigences  réglementaires,  légales  et  contractuelles, notamment le cadre juridique applicable en matière de cyber sécurité, sont explicitement identifiées au niveau de la nouvelle politique globale de  sécurité  SI  et  leur  respect  est  mentionné  au  niveau  de  la  charte utilisateur des SI. Toutefois, ces documents sont en cours de validation par la hiérarchie.

## Revue de sécurité de l'information :

- -Des audits de sécurité sont effectués régulièrement conformément aux normes et directives en vigueur et selon un plan prédéfini.
- -Les sites de replis identifiés lors de la mise à l'essai du PCA ne sont pas dédiés à la reprise d'activité ce qui peut impacter la continuité d'activité en cas de sinistre majeur.
- -Un projet d'enrichissement du PCA/PCA est prévu et l'intégration de scénarios cyber au niveau des exercices de crise est planifiée pour T1-2024.

## Preuves :

- Interview

- Politique de sécurité des SI V 2015

- Politique Globale de Sécurité SI v2023

- Charte utilisation des SI V2011

- Charte utilisation des SI V2023

Constats

- Politique de gestion des clés cryptographiques
- Méthodologie de déroulement des audits techniques de sécurité v1.0
- Plan Audit Annuel Securité\_V1\_21092023
- Dernier rapport d'audit : PASSI\_AUDITÉ\_web CAM SERVICES\_v1.4\_20230804
- -Le document « AUDITÉ\_PA\_Audit Annuel Securité\_V1\_21092023 » fait référence à une directive qui n'est plus en vigueur. De plus il est à noter que la DGSSI relève uniquement de l'Administration de la Défense Nationale.

## 4. Constats et recommandations de l'audit technique

L'évaluation technique s'est principalement orientée vers l'analyse des architectures et l'audit des configurations en place.

## 4.1 Périmètre

Il s'agit d'une mission d'évaluation technique qui s'est principalement orientée vers l'analyse de l'architecture et l'audit des configurations en place.

Le périmètre de cette mission englobe les composantes SI ci-après énumérées :

- Le firewall central Forcepoint ;
- Le firewall Fortigate partenaire ;
- Le firewall Fortigate frontal ;
- Le switch fédérateur ;
- Le serveur de messagerie ;
- Le serveur web alpha.

## 4.2 Objectif et principe

L'audit des configurations vise à vérifier le bon durcissement des configurations en place. Pour ce faire, et afin d'appliquer les principes de défense en profondeur et de Confiance Zéro, chaque actif est considéré à part entière et de manière isolée sans tenir compte des contrôles présents au niveau des actifs sous-jacents.

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

## a. Etat des contrôles vérifiés par élément audité

| Elément audité  Critique  Elevée  Moyenne  Faible  Architecture  0  0  3  2  Firewall Central Forcepoint  2  0  5  1  Firewall Partenaire  3  4  9  1  Firewall Frontal  3  4  9  1  Switch fédérateur  2  2  7  1  Serveur de messagerie  0  16  6  2  Serveur web Alpha  6  14  7  0   |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## b. Répartition des contrôles non implémentés par criticité et par élément audité

<!-- image -->

1

1

1

## c. Points d'amélioration relatifs à l'architecture

L'étude de l'architecture a permis de remonter des points d'amélioration qui concernent principalement :

1

- Protection de l'accès au réseau :
- o Absence d'une solution NAC, toutefois on note l'utilisation de quelques mécanismes pour limiter l'accès non autorisé au réseau telle que la restriction des adresses MAC. On note aussi l'existence d'un projet pour la mise en place d'une solution NAC.
- Réseau d'administration :
- o Même si un réseau dédié aux administrateurs existe, les postes utilisés ne sont pas dédiés pour les tâches d'administration.
- Traçabilité des actions d'administration :
- o La traçabilité des actions d'administration n'est pas assurée ; toutefois il existe un projet pour la mise en place d'un bastion.
- Matrice des flux :
- o La matrice des flux n'est pas documentée.
- d. Points d'amélioration relatifs aux configurations

Les points d'amélioration proposés concernent principalement les axes suivants :

## Les équipements de sécurité et du réseau :

- L'utilisation d'une version à jour du firmw are ;
- L'utilisation des règles de filtrage restrictives ;
- L'utilisation d'algorithmes cryptographiques robustes ;
- La désactivation de l'installation automatique ;
- La désactivation du compte de maintenance ;
- L'utilisation des protocoles chiffrés pour l'administration ;
- La restriction des accès d'administration ;
- La journalisation des évènements ;
- La journalisation de la règle d'interdiction implicite ;
- L'activation de l'envoi des journaux importants par mail ;
- L'authentification des serveurs NTP ;
- L'activation du modèle AAA ;
- L'utilisation des comptes locaux nominatifs ;
- L'application d'une politique de mots de passe ;
- L'utilisation de la version sécurisée du protocole de supervision SNMP ;
- La configuration d'un serveur d'authentification pour les accès d'administration ;
- L'exigence de l'authentification pour accéder au mode privilégié ;
- L'exigence du stockage chiffré des mots de passe ;
- La configuration de la fermeture automatique des sessions d'administration ;

·

L'horodatage des évènements journalisés

;

- L'activation du mécanisme "port security" ;

- L'activation des mécanismes de protection du protocole STP ;
- La configuration de la fermeture automatique des sessions d'administration ;
- La configuration du verrouillage des comptes d'administration ;
- La configuration des bannières.

## Le serveur de messagerie :

- La configuration de la taille maximale des messages envoyés ;
- La configuration de la taille maximale des messages reçus ;
- La journalisation de l'activité SMTP pour les connecteurs d'envoi et de réception ;
- La journalisation des évènements de connectivité ;
- L'interdiction du transfert automatique ;
- La désactivation des réponses automatiques ;
- La désactivation de l'envoi des notifications de rejet ;
- La limitation des appareils mobiles qui peuvent utiliser ActiveSync ;
- La définition d'une période de rafraîchissement de la stratégie de sécurité ;
- L'utilisation  d'un  mot  de  passe  compliqué  pour  déverrouiller  les  appareils  mobiles  qui utilisent ActiveSync ;
- L'exigence du verrouillage automatique des appareils mobiles qui utilisent ActiveSync ;
- L'exigence de changer périodiquement les mots de passe et de ne pas réutiliser les anciens mots de passe pour les appareils mobiles qui utilisent ActiveSync ;
- L'exigence  du  verrouillage  des  appareils  mobiles  qui  utilisent  ActiveSync  après  des tentatives de déverrouillage échouées ;
- L'exigence du chiffrement des appareils mobiles qui utilisent ActiveSync ;
- La définition de la durée de rétention des éléments supprimés ;
- La conservation des éléments supprimés ;
- La désactivation de l'authentification de base.

## Le serveur web :

- L'emplacement des ressources web sur le disque ;
- L'utilisation de la fonctionnalité "host headers" ;
- L'activation du chiffrement pour l'authentification basée sur formulaire ;
- L'utilisation des cookies pour les formulaires d'authentification ;
- L'activation du  chiffrement  et de la validation des cookies  pour  les  formulaires d'authentification ;
- L'activation du chiffrement pour l'authentification de base ;
- L'utilisation des cookies pour le stockage des informations de sessions ;
- La protection des cookies ;
- La configuration de l'algorithme de validation des services ;
- L'activation des messages d'erreur personnalisés ;

- La désactivation de l'affichage des erreurs HTTP détaillées ;
- La désactivation du traçage de la pile ASP.Net ;
- La configuration des en-têtes envoyés par le serveur ;
- La configuration de la longueur maximale du contenu des requêtes ;
- La configuration de la longueur maximale des URL ;
- La configuration de la longueur maximale de la chaine des requêtes ;
- Le rejet des requêtes avec double encodage ;
- La désactivation de la méthode TRACE ;
- La limitation des requêtes autorisées par adresse IP ;
- L'activation de la journalisation avancée ;
- L'activation du mécanisme HSTS "HTTP Strict Transport Security" ;
- La désactivation des versions vulnérables du protocole SSL ;
- L'utilisation des versions sécurisées du protocole SSL ;
- La désactivation des suites cryptographiques "NULL" "DES" et "RC4" ;
- L'utilisation des suites cryptographiques "AES 256".