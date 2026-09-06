# Parcours et séances

## Séance 1 — Du besoin au schéma physique

**Durée :** 4 h, dont 2 h 15 FFP et 1 h 45 TDP.

**État de départ :** `course-start`.

**Dossiers mobilisés :** `inputs/formaflow-reference/`, `briefs/session-01/`, `fixtures/nominal/`, `docs/`, `diagrams/` et `sql/schema/`.

**Productions :** glossaire, registre d'hypothèses, invariants, MCD, MLD, extrait de MPD et premier script SQL.

**Point de contrôle :** les scénarios session complète, double inscription et tarif modifié après achat peuvent être racontés et reliés à des choix explicites.

## Séance 2 — Normaliser, indexer et mesurer

**Durée :** 3 h, dont 1 h 30 FFP et 1 h 30 TDP.

**État de départ :** branche du binôme ou `checkpoint-relational` en cas de reprise.

**Dossiers mobilisés :** `fixtures/flawed-schema/`, `fixtures/benchmark/`, `sql/constraints/`, `sql/indexes/`, `sql/reporting/`, `sql/tests/` et `benchmarks/`.

**Productions :** dépendances fonctionnelles, schéma normalisé, contraintes, index, plans d'exécution, protocole, résultats et décision de dénormalisation.

**Point de contrôle :** toute affirmation de performance mentionne le dataset, la requête, le contexte d'exécution et la limite de généralisation.

## Séance 3 — Comparer les paradigmes NoSQL

**Durée :** 4 h, dont 2 h 15 FFP et 1 h 45 TDP.

**État de départ :** `checkpoint-relational`.

**Dossiers mobilisés :** `nosql/`, `fixtures/nominal/`, `briefs/session-03/` et `benchmarks/`.

**Productions :** cartographie des accès, document MongoDB, plan de clés Redis, table Cassandra, graphe Neo4j, matrice pondérée et recommandation.

**Point de contrôle :** chaque modèle expose son chemin d'accès principal, ses duplications, ses garanties et son coût d'exploitation.

## Séance 4 — Architecture polyglotte et validation individuelle

**Durée :** 3 h, dont 1 h FFP et 2 h TDP. Le QCM individuel contextualisé de 45 minutes est inclus dans ces 2 h de TDP.

**État de départ :** `checkpoint-nosql`.

**Dossiers mobilisés :** ensemble des productions, `docs/adr/`, `diagrams/`, `evidence/` et `docs/cdan/`.

**Productions formatives :** architecture, ownership pressenti, source de vérité, synchronisation, mappings, risques, contrôles et fiche CDAN.

**Évaluation :** QCM individuel séparé du repository. Après le cours, le formateur construit `reference-final` et `handoff/data-reference/`.
