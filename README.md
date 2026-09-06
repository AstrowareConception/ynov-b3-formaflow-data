# FormaFlow Data — Conception et architecture des données

> Version documentaire : 0.1.0  
> Statut : spécification initiale, repository non encore implémenté  
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

## Parcours standard

1. **Séance 1 — Modéliser :** besoin, glossaire, hypothèses, MCD, MLD et premier MPD PostgreSQL.
2. **Séance 2 — Garantir et mesurer :** normalisation, contraintes, index, `EXPLAIN`, benchmark borné et décision de dénormalisation.
3. **Séance 3 — Comparer :** modèles MongoDB, Redis, Cassandra et Neo4j construits à partir des accès et des garanties.
4. **Séance 4 — Composer :** source de vérité, synchronisation, architecture polyglotte, gouvernance, trace CDAN et QCM individuel.

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

Cette V0.1.0 documente l'arborescence sans fournir encore les fichiers exécutables, les datasets complets ou les solutions.

## Technologies retenues

- PostgreSQL comme unique cible relationnelle exécutée et évaluée pendant les ateliers ;
- Docker Compose pour rendre l'environnement reproductible ;
- `psql` et un client graphique librement choisi ;
- outil de modélisation exportant un format partageable ou une image versionnée ;
- profils Docker Compose séparés pour MongoDB, Redis, Cassandra et Neo4j ;
- scripts SQL et outils locaux simples pour les fixtures et mesures.

Les versions majeures, images et digests seront figés lors de l'implémentation. La réussite ne dépendra jamais du démarrage simultané des quatre moteurs NoSQL.

## Commandes contractuelles

| Commande | Effet attendu |
|---|---|
| `make setup` | Vérifier les prérequis et préparer les fichiers locaux |
| `make start` | Démarrer PostgreSQL et les services minimaux |
| `make stop` | Arrêter l'environnement sans supprimer les productions |
| `make reset-data` | Recréer un état de données synthétiques déterministe |
| `make seed DATASET=nominal` | Charger explicitement un jeu de données |
| `make smoke` | Vérifier connexion, schéma, données et requêtes essentielles |
| `make test` | Exécuter les contrôles SQL et validations documentaires automatisables |
| `make benchmark` | Lancer le protocole de mesure relationnel borné |
| `make nosql PROFILE=mongodb` | Démarrer un seul profil NoSQL identifié |
| `make quality` | Contrôler format, liens, manifests et fichiers attendus |

Chaque commande devra être idempotente ou documenter clairement ses effets destructifs. `make reset-data` ne manipulera que les volumes Docker explicitement nommés par ce projet.

## Branches, tags et reprise

- branche étudiante : `work/<team-id>` ;
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

Le module Architecture hexagonale & DDD copie ce paquet dans `inputs/data-reference/`. Il ne récupère jamais une branche étudiante.

## Sécurité et données

Toutes les données sont fictives. Aucun dump réel, secret, compte distant ou service cloud n'est nécessaire. Les scripts de génération doivent être déterministes, documenter leur volumétrie et rester compatibles avec les ressources des postes étudiants.

## État de la version 0.1.0

Cette version fixe le contrat du repository. Restent à produire lors de la spécification détaillée : `compose.yml`, `Makefile`, datasets, briefs, schéma volontairement fragile, tests SQL, protocoles de benchmark, gabarits de modèles, checkpoints réels, handoff complet et kit formateur.
