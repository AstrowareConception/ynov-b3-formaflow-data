# Séance 1 - Du besoin au schéma physique

**Durée indicative :** 4 h, dont 2 h 15 FFP et 1 h 45 TDP.
**État de départ :** tag `course-start`. Reprise possible avec `git switch --detach course-start`, puis création d'une branche `work/<team-id>`.

## Objectifs

À partir du snapshot FormaFlow, délimiter le besoin AstroData Hub, produire un glossaire ciblé, expliciter hypothèses et invariants, puis proposer un MCD, un MLD et un premier MPD PostgreSQL. Distinguer modèle de données, modèle de domaine, base physique, ownership supposé et bounded context.

## Contexte et fichiers fournis

Le parcours relie formations, sessions, participants, organisations, commandes, inscriptions, tarifs, factures, paiements et documents. Consulter `inputs/formaflow-reference/`, `fixtures/nominal/dataset.json`, `fixtures/edge-cases/dataset.json`, `docs/templates/` et `sql/course-start/`.

## Étapes proposées

1. Raconter le parcours nominal et les trois invariants transversaux sans parler de tables.
2. Construire le glossaire et le registre d'hypothèses ; signaler les termes encore ambigus.
3. Dessiner les concepts et cardinalités du MCD, puis traduire en relations dans le MLD.
4. Choisir clés, types et nullabilité dans un extrait de MPD ; relier chaque contrainte à un scénario.
5. Confronter le modèle à une session complète, un doublon et une évolution tarifaire.

## Productions formatives attendues

Glossaire, hypothèses, invariants, sources textuelles MCD/MLD, premier MPD et liste des questions ouvertes. Utiliser les gabarits sans consulter de correction canonique.

## Critères de réussite

Chaque terme a un sens stable ; les cardinalités couvrent acheteur et bénéficiaire ; le prix historique est représentable ; les trois invariants ont exemple et contre-exemple ; les hypothèses d'ownership ne sont pas présentées comme des faits DDD.

## Erreurs fréquentes

Confondre formation et session, compte et participant, paiement et commande ; transformer chaque table en entité DDD ; conserver seulement le tarif courant ; employer `NULL` sans sémantique explicite.

## Questions de synthèse

Quelle règle relève du schéma, d'une transaction ou d'une décision applicative ? Quelle information décrit un fait historique ? Quel choix resterait à arbitrer dans le cours DDD ?
