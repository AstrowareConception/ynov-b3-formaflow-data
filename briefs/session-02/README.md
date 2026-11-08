# TP 2 — Normalisation, intégrité et performances (parcours refondu)

## Intention

Poursuivre la séance 1 : **diagnostiquer → normaliser → protéger → mesurer → arbitrer**. La normalisation n'est pas un simple découpage mécanique ; elle préserve les faits et le passé contractuel.

## Point de départ

Productions du TP 1 enregistrées dans un dossier local. Reprise d'appoint via `checkpoint-relational` seulement quand le formateur l'autorise. Export fragile : `fixtures/flawed-schema/enrollment-export.csv`. Gabarits : `docs/templates/functional-dependencies.md`, `docs/templates/benchmark.md`. Benchmark de référence : `benchmarks/results/reference-small/result.json`.

## Missions

1. Repérer granularités mélangées et données absentes ; relever **au moins six dépendances fonctionnelles** motivées par les règles métier.
2. Illustrer les anomalies de modification, d'insertion et de suppression.
3. Décomposer progressivement : **1NF, 2NF, 3NF**, clés candidates, dépendances partielles/transitives, **reconstruction sans perte**.
4. Distinguer une duplication incorrecte d'une **photographie historique justifiée** (prix accepté et devise).
5. Justifier `NOT NULL`, `CHECK`, `UNIQUE`, FK, et la nécessité d'un **contrôle transactionnel** de la capacité. Les `PENDING` et `CONFIRMED` occupent une place dans ce corpus ; le MPD existant rend `(session_id, participant_id)` unique tous statuts confondus.
6. Formuler la requête consultations par formation et période, proposer l'index composé, lire `EXPLAIN` et, si possible, exécuter un protocole `EXPLAIN ANALYZE` contrôlé.
7. Comparer calcul SQL, vue matérialisée et table de synthèse. Nommer source, fraîcheur, réparation et coût avant toute copie.

## Livrables

Table de dépendances, MLD normalisé argumenté, SQL/tests ou traces qualifiées, requête et index, fiche benchmark (données, chauffe, répétitions, équivalence fonctionnelle, médiane, limites), décision de dénormalisation.

## Exigences de preuve

La trace 10 000 lignes du dépôt est une mesure historique locale ; **1 million** correspond à une **trace préparée, non une exécution**. Un plan seul ou une baisse de latence isolée ne prouve pas un SLA. Un test séquentiel ne démontre pas nécessairement la concurrence à deux connexions.

> La Page Moodle détaille les étapes et les critères. Les corrigés restent hors du dépôt étudiant.

## Remise

Rendu ZIP sur Moodle ; aucun envoi vers GitHub.
