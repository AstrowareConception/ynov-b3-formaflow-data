# Séance 2 - Normaliser, contraindre et mesurer

**Durée indicative :** 3 h, dont 1 h 30 FFP et 1 h 30 TDP.
**État de départ :** travail de séance 1 ; reprise possible depuis `checkpoint-relational` uniquement après la phase de recherche prévue.

## Objectifs

Diagnostiquer un schéma redondant, mobiliser 1NF, 2NF et 3NF, présenter BCNF lorsque les déterminants le justifient, choisir contraintes et index à partir des accès, puis mesurer une hypothèse sans conclusion universelle.

## Contexte et fichiers fournis

Le fichier `fixtures/flawed-schema/enrollment-export.csv` mélange plusieurs granularités. Les profils de volume sont dans `fixtures/benchmark/profiles.json`; les gabarits de dépendances et de benchmark sont dans `docs/templates/`.

## Étapes proposées

1. Identifier granularité, clé candidate et dépendances fonctionnelles de l'export.
2. Démontrer une anomalie d'insertion, de modification et de suppression.
3. Proposer une décomposition progressive jusqu'à 3NF et discuter BCNF sur un cas justifié.
4. Associer contraintes et index aux écritures et requêtes attendues.
5. Écrire un protocole avec dataset, seed, échauffement, répétitions, plans et limites.
6. Comparer résultats fonctionnels avant toute interprétation du temps.

## Productions formatives attendues

Registre de dépendances, schéma normalisé, SQL, tests positifs et négatifs, requêtes de reporting, plans `EXPLAIN`, fiche benchmark et décision de dénormalisation éventuelle.

## Critères de réussite

La décomposition n'est pas arbitraire ; les trois invariants sont testés ; les écritures autorisées restent possibles ; les résultats de reporting sont cohérents ; aucune assertion ne dépend d'un seuil temporel absolu.

## Erreurs fréquentes

Découper une table sans citer de dépendance, créer un index sans requête cible, tester seulement les refus, prendre un plan unique pour une vérité générale, confondre duplication historique justifiée et redondance accidentelle.

## Questions de synthèse

Quelle dépendance motive chaque relation ? Quel invariant nécessite de la concurrence ou un verrouillage ? Dans quelles conditions une dénormalisation contrôlée serait-elle réexaminée ?
