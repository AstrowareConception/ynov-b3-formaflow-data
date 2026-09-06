# Séance 3 - Comparer quatre paradigmes NoSQL

**Durée indicative :** 4 h, dont 2 h 15 FFP et 1 h 45 TDP.
**État de départ :** tag `checkpoint-relational`. Reprise possible depuis ce tag sur une branche dédiée.

## Objectifs

Identifier document, clé-valeur, colonnes larges et graphe ; comparer MongoDB, Redis, Cassandra et Neo4j à partir des accès, garanties, volumes, coûts et limites ; ne pas remplacer la source relationnelle sans justification.

## Contexte et fichiers fournis

Les usages étudiés sont : catalogue aux attributs variables, disponibilité éphémère, consultations query-first et recommandations par compétences. Utiliser `fixtures/nominal/`, `nosql/README.md`, `docs/templates/comparison-matrix.md` et les profils Compose séparés.

## Étapes proposées

1. Écrire pour chaque usage les lectures, écritures, latence, cohérence, volume et rétention attendus.
2. Proposer document et index MongoDB, convention de clés et TTL Redis, partition/clustering Cassandra, nœuds et relations Neo4j.
3. Identifier duplication, invalidation, taille, éviction, hot partitions et surinterprétation possibles.
4. Distinguer ce qui a été exécuté, modélisé ou observé via une trace préparée.
5. Remplir une matrice pondérée et formuler une recommandation réversible.

## Productions formatives attendues

Quatre modèles minimaux, données synthétiques, requêtes cibles, matrice comparative et recommandation argumentée.

## Critères de réussite

Chaque modèle part d'un accès ; Redis n'est source de vérité ni des inscriptions ni des paiements ; les garanties et coûts sont explicites ; un seul profil est lancé à la fois ; une technologie peut être écartée.

## Erreurs fréquentes

Comparer seulement la syntaxe, imbriquer sans limite de croissance, oublier TTL et invalidation, partitionner Cassandra par commodité d'écriture, déduire une causalité d'une proximité dans le graphe.

## Questions de synthèse

Quelle panne rend chaque projection obsolète ? Quelle duplication est assumée ? Quel signal ferait abandonner la technologie choisie ?
