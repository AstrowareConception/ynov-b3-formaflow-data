# FormaFlow Data — Conception et architecture des données

> Version : 1.0.0  
> Statut : environnement pédagogique exécutable  
> Module : Conception et architecture des données — Bachelor 3 DEV  
> Volume : 14 heures — 7 h FFP + 7 h TDP

## Finalité du repository

`ynov-b3-formaflow-data` est le premier repository pédagogique exécutable de la chaîne FormaFlow. Il permet aux étudiants de passer d'un besoin métier à des modèles conceptuel, logique et physique, d'éprouver l'intégrité et les performances d'un schéma relationnel, de comparer quatre familles NoSQL, puis de concevoir une architecture de données polyglotte gouvernée.

Le dépôt applique strictement le syllabus sans préconstruire les réponses. Il fournit le contexte, les jeux de données synthétiques, les scénarios, les gabarits, les commandes et les états de reprise ; les étudiants produisent les modèles, décisions et preuves.

## Résultats pédagogiques attendus

À l'issue du module, l'étudiant doit pouvoir :

- concevoir un MCD puis le traduire en MLD et MPD ;
- justifier clés, contraintes, types et index ;
- normaliser un schéma et décider d'une dénormalisation maîtrisée ;
- lire un plan d'exécution simple et mesurer une hypothèse ;
- distinguer les modèles document, clé-valeur, colonne et graphe ;
- choisir un paradigme en fonction des accès, garanties et coûts ;
- composer une architecture SQL/NoSQL avec source de vérité et synchronisation explicites ;
- distinguer modèle de données, modèle de domaine et hypothèse d'ownership.

## Fil rouge

AstroData Hub est le volet données de FormaFlow Marketplace. Le corpus couvre formations, sessions, participants, organisations, inscriptions, commandes, factures, paiements, documents, consultations et recommandations.

Trois cas limites traversent le module : session complète, double inscription et tarif modifié après achat. Ils obligent à protéger la capacité, l'unicité et l'historique plutôt qu'à dessiner un schéma uniquement nominal.

## Parcours standard — TP refondus en 2026–2027

Le parcours de 14 heures conserve les **quatre séances**, les jeux de données, les commandes et les checkpoints. Les quatre cours théoriques ont été réorganisés ; leurs TP formatifs sont désormais progressifs et sont distribués en **Pages Moodle** :

1. **TP 1 — Merise et conception :** besoin métier, dictionnaire, cardinalités, MCD → MLD → premier MPD PostgreSQL.
2. **TP 2 — Normalisation et intégrité :** dépendances et anomalies, contraintes, concurrence, index, EXPLAIN et décision de dénormalisation.
3. **TP 3 — SQL / NoSQL :** quatre usages, modèles document / clé-valeur / colonnes larges / graphe, approfondissement d'un profil, décision multicritère.
4. **TP 4 — Composition et transmission :** source de vérité, outbox et reprise, mapping et migration, gouvernance, ADR, relais vers DDD.

**Guides et détails :** [parcours TP refondu](docs/pedagogie/TP-2026-2027.md) et [briefs de séance](briefs/). Chaque TP possède un corrigé HTML **enseignant séparé**, qui ne doit pas être publié dans le repo étudiant.

Les tags `course-start`, `checkpoint-relational`, `checkpoint-nosql` et `reference-final` sont **historiques et immuables** ; une refonte des consignes sur `main` ne les déplace pas. Les Page Moodle contiennent les consignes à jour, même lorsque le travail local repart d'un ancien tag. **Les étudiants remettent leurs productions au format ZIP sur Moodle, sans push vers le dépôt de l'enseignant.**

## Évaluation

Le repository ne contient aucune épreuve ni aucun corrigé d'évaluation.

Le module comporte une seule évaluation sommative : un QCM individuel contextualisé de 45 minutes représentant 100 % de la note. Les MCD, MLD, MPD, scripts, modèles NoSQL, benchmarks et décisions produits dans le dépôt restent formatifs.

Les variantes, feuilles de réponses et corrigés sont conservés dans un kit formateur privé distinct. Aucun tag `assessment-start` n'est nécessaire puisque le QCM n'exige pas d'exécuter le dépôt.

## Arborescence cible

```text
ynov-b3-formaflow-data/
├── README.md
├── CHANGELOG.md
├── manifest.yml
├── CHECKPOINTS.md
├── Makefile
├── compose.yml
├── .env.example
├── inputs/
│   └── formaflow-reference/
├── briefs/
├── fixtures/
│   ├── nominal/
│   ├── edge-cases/
│   ├── flawed-schema/
│   └── benchmark/
├── docs/
│   ├── glossary.md
│   ├── assumptions.md
│   ├── invariants.md
│   ├── models/
│   ├── adr/
│   └── cdan/transfer.md
├── diagrams/
├── sql/
│   ├── schema/
│   ├── constraints/
│   ├── indexes/
│   ├── reporting/
│   └── tests/
├── nosql/
│   ├── mongodb/
│   ├── redis/
│   ├── cassandra/
│   └── neo4j/
├── benchmarks/
│   ├── protocols/
│   └── results/
├── evidence/
└── handoff/
    └── data-reference/
```

Le tag `course-start` contient l'environnement, les corpus et les gabarits sans les solutions canoniques. Les corrections apparaissent progressivement dans les checkpoints formateur afin de préserver le déroulement des quatre séances.

## Technologies retenues

- PostgreSQL comme unique cible relationnelle exécutée et évaluée pendant les ateliers ;
- Docker Compose pour rendre l'environnement reproductible ;
- `psql` et un client graphique librement choisi ;
- outil de modélisation exportant un format partageable ou une image versionnée ;
- profils Docker Compose séparés pour MongoDB, Redis, Cassandra et Neo4j ;
- scripts SQL et outils locaux simples pour les fixtures et mesures.

Les versions d'images sont figées dans `compose.yml` et consignées dans `image-lock.yml`. Un digest n'est ajouté que lorsqu'il a réellement été résolu. La réussite ne dépend jamais du démarrage simultané des quatre moteurs NoSQL.

## Commandes contractuelles

| Commande | Effet attendu |
|---|---|
| `make setup` | Vérifier les prérequis et préparer les fichiers locaux |
| `make start` | Démarrer PostgreSQL et les services minimaux |
| `make stop` | Arrêter l'environnement sans supprimer les productions |
| `make reset-data` | Recréer un état de données synthétiques déterministe |
| `make seed DATASET=nominal` | Charger explicitement un jeu de données |
| `make smoke` | Vérifier connexion, schéma, données et requêtes essentielles |
| `make validate` | Contrôler le contrat documentaire et les durées du parcours |
| `make test` | Exécuter les contrôles SQL et validations documentaires automatisables |
| `make benchmark` | Lancer le protocole de mesure relationnel borné |
| `make nosql PROFILE=mongodb` | Démarrer un seul profil NoSQL identifié |
| `make quality` | Contrôler format, liens, manifests et fichiers attendus |
| `make package` | Produire l'archive pédagogique déterministe |
| `make clean` | Supprimer uniquement `build/` et `dist/` |

Chaque commande devra être idempotente ou documenter clairement ses effets destructifs. `make reset-data` ne manipulera que les volumes Docker explicitement nommés par ce projet.

## Travail local, tags et reprise

- travail étudiant : dossier local `FormaFlow_TP<n>_Groupe-XX/`, sans branche distante ni push ; remise du ZIP dans Moodle ;
- tag formateur initial : `course-start` ;
- reprise après le relationnel : `checkpoint-relational` ;
- reprise après la comparaison NoSQL : `checkpoint-nosql` ;
- état consolidé après le module : `reference-final`.

Les tags formateur sont immuables. Un étudiant bloqué peut repartir d'un checkpoint sans que son évaluation soit affectée, puisque les productions du repository ne sont pas notées.

## Entrée canonique

`inputs/formaflow-reference/` contient une copie figée de `ynov-b3-formaflow-reference` : vision, acteurs, glossaire, règles, cas limites et manifeste de version. Ce dossier est en lecture seule pendant les activités.

## Sortie canonique

Après le module, le formateur publie `handoff/data-reference/` au tag `reference-final`. Le paquet contient :

- glossaire consolidé ;
- invariants et exemples/contre-exemples ;
- MCD, MLD et MPD canoniques ;
- dictionnaire ciblé ;
- décisions de stockage, normalisation et dénormalisation ;
- résultats de mesure contextualisés ;
- hypothèses d'ownership explicitement présentées comme telles ;
- limites et questions ouvertes.

Le module Architecture hexagonale & DDD copie ce paquet dans `inputs/data-reference/`. Il ne récupère jamais un dossier étudiant.

## Sécurité et données

Toutes les données sont fictives. Aucun dump réel, secret, compte distant ou service cloud n'est nécessaire. Les scripts de génération doivent être déterministes, documenter leur volumétrie et rester compatibles avec les ressources des postes étudiants.

## Utilisation locale

Consulter `docs/getting-started.md` puis exécuter `make setup`, `make start`, `make reset-data` et `make smoke`. Les commandes directes `python scripts/manage.py <commande>` restent disponibles sur un poste Windows où GNU Make n'est pas installé.
