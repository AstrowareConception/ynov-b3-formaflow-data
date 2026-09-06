# FormaFlow — Référentiel pédagogique commun

> Version documentaire : 1.0.0  
> Statut : référentiel approuvé  
> Année pédagogique cible : 2026-2027

## Finalité du repository

`ynov-b3-formaflow-reference` constitue la source de vérité sémantique du fil rouge FormaFlow utilisé dans plusieurs enseignements de Bachelor 3 Informatique Développement.

Il décrit le produit fictif, ses acteurs, ses parcours, son vocabulaire, ses règles métier stables, ses cas limites et les informations transmises entre les modules. Il permet à chaque cours de travailler sur le même univers sans dépendre du code, des choix techniques ou des productions d'un groupe précédent.

Ce repository est documentaire. Il ne contient ni application exécutable, ni solution d'exercice, ni modèle de données imposé, ni découpage DDD présenté comme définitif.

## Principes directeurs

1. **Un même domaine, plusieurs regards.** Les modules observent FormaFlow sous l'angle des données, du domaine, des échanges, de l'organisation du travail, du backend distribué ou de la sécurité.
2. **Une continuité sans dépendance étudiante.** Chaque repository pédagogique embarque une copie figée des documents dont il a besoin. Une absence ou une erreur dans un module ne bloque jamais le suivant.
3. **Le sens précède la technologie.** Le référentiel stabilise les termes, scénarios et invariants, mais laisse les étudiants concevoir les modèles et architectures demandés par chaque syllabus.
4. **Les états canoniques appartiennent au formateur.** Les productions étudiantes nourrissent l'apprentissage ; les passages de relais reposent sur des versions consolidées et publiées par le formateur.
5. **Aucune donnée réelle.** Les personnes, organisations, paiements, factures, traces et incidents sont entièrement fictifs.

## Périmètre fonctionnel

FormaFlow est une marketplace fictive de formations professionnelles. Elle permet notamment de :

- publier des formations et planifier leurs sessions ;
- consulter un catalogue et les disponibilités ;
- gérer des comptes individuels et des organisations clientes ;
- commander une ou plusieurs inscriptions ;
- simuler le paiement, produire les éléments de facturation et créer les inscriptions ;
- notifier les participants et les équipes concernées ;
- exporter certaines informations et traiter les demandes liées aux données personnelles.

Le parcours transversal de référence est : **choisir une session, confirmer une commande, créer l'inscription et notifier le participant**.

## Hors périmètre

Le référentiel ne tranche pas à lui seul :

- le MCD, le MLD ou le MPD attendu dans le module Données ;
- les agrégats, bounded contexts et frontières transactionnelles du module DDD ;
- le choix définitif entre communication synchrone et asynchrone ;
- le découpage final des microservices ;
- l'implémentation de la sécurité ou du RGPD ;
- l'organisation des équipes étudiantes ;
- les réponses aux évaluations.

Les documents distinguent donc soigneusement les **faits métier stabilisés**, les **hypothèses pédagogiques** et les **décisions laissées aux étudiants**.

## Utilisateurs du référentiel

- **Formateur :** maintient les versions canoniques, prépare les instantanés et arbitre les évolutions.
- **Étudiant :** consulte les extraits fournis dans le repository de son module ; il n'a pas besoin de cloner ce référentiel directement.
- **Concepteur des cours :** s'assure que scénarios, exemples, exercices, QCM et corrigés emploient les mêmes termes.
- **Mainteneur des repositories :** vérifie que les fixtures, contrats, événements et données restent conformes à la version annoncée du référentiel.

## Arborescence cible

```text
ynov-b3-formaflow-reference/
├── README.md
├── CHANGELOG.md
├── manifest.yml
├── VERSION
├── Makefile
├── CONTRIBUTING.md
├── catalog/
│   ├── actors.json
│   ├── glossary.json
│   ├── business-rules.json
│   ├── state-models.json
│   ├── traceability.json
│   └── journeys/purchase-enrollment.json
├── events/
│   ├── catalog.json
│   └── examples/
├── fixtures/
│   ├── reference-dataset.json
│   └── edge-cases.json
├── handoff/template/
├── docs/
│   ├── README.md
│   ├── 01-vision-produit.md
│   ├── 02-acteurs-et-parcours.md
│   ├── 03-glossaire.md
│   ├── 04-regles-metier-et-invariants.md
│   ├── 05-cas-limites.md
│   ├── 06-cartographie-pedagogique.md
│   ├── 07-contrat-de-transmission.md
│   ├── 08-gouvernance-et-versionnement.md
│   ├── 09-identifiants-etats-evenements.md
│   └── 10-tracabilite-et-validation.md
├── scripts/
│   ├── validate_reference.py
│   └── package_reference.py
└── schemas/
    ├── README.md
    ├── event-envelope.schema.json
    ├── handoff-manifest.schema.json
    ├── reference-dataset.schema.json
    └── events/
```

## Repositories consommateurs

| Repository | Usage principal du référentiel |
|---|---|
| `ynov-b3-formaflow-data` | Besoin, vocabulaire, invariants, cas limites et données synthétiques |
| `ynov-b3-formaflow-hexagonal` | Corpus consolidé du module Données à confronter au modèle de domaine |
| `ynov-b3-formaflow-interop` | Faits métier candidats, consommateurs, mappings et contraintes d'évolution |
| `ynov-b3-formaflow-agility` | Demande d'évolution, acteurs, valeur, risques et critères d'acceptation |
| `ynov-b3-formaflow-distributed` | Parcours e-commerce, responsabilités, contrats et scénarios de panne |
| `ynov-b3-formaflow-security-lab` | Actifs, rôles, données personnelles, surfaces exposées et scénarios autorisés |
| `ynov-b3-cdan-evidence-kit` | Terminologie et catégories de preuves transférables |

`ynov-b3-atlaslegacy` demeure volontairement autonome. Il peut réutiliser des méthodes pédagogiques, mais pas le domaine ni le code de FormaFlow.

## Distribution et versionnement

Le référentiel suit un versionnement sémantique documentaire :

- **PATCH** : clarification sans modification du sens métier ;
- **MINOR** : ajout compatible d'un acteur, scénario, règle ou attribut ;
- **MAJOR** : modification incompatible d'un terme, d'un invariant ou d'un parcours.

Les tags prennent la forme `reference-vX.Y.Z`. Les repositories consommateurs copient les fichiers nécessaires dans leur propre dossier `inputs/` et consignent la version utilisée. Aucun sous-module Git n'est imposé.

## Commandes

| Commande | Effet |
|---|---|
| `make validate` | Vérifier les JSON, identifiants, références, règles, événements, données, liens et marqueurs interdits |
| `make package` | Produire une archive du référentiel approuvé après validation |
| `make clean` | Supprimer uniquement les fichiers générés par le packaging |

La validation ne nécessite ni service externe, ni Docker, ni accès réseau.

## État de la version 1.0.0

Cette version fixe le vocabulaire, les règles, les identifiants, les cycles d'état, le parcours canonique, les trois événements d'intégration, les jeux de données synthétiques, le gabarit de handoff et la matrice de traçabilité. Elle constitue la première source distribuable aux repositories consommateurs sous le tag `reference-v1.0.0`.

## Auteur et cadre d'utilisation

Référentiel conçu pour les enseignements de Térence FERUT, AstroWare Conception, à Ynov Campus. Les situations professionnelles sont fictives ou reconstruites ; aucune architecture, donnée ou information confidentielle d'un client réel n'est reproduite.
