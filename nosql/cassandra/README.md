# Cassandra - consultations query-first

## Usage et statut

Le besoin est de lire les consultations d'une formation sur une période récente et, séparément, l'activité récente d'un profil opaque. Les tables sont des projections de traces ; PostgreSQL conserve le catalogue, et la conservation brute doit respecter la rétention. `make nosql PROFILE=cassandra` exécute réellement le schéma et le petit dataset si les ressources le permettent. `prepared-trace.json` représente seulement une volumétrie supérieure et ne prétend pas avoir été exécuté.

## Query-first et duplication

`consultations_by_training_month` partitionne par `(training_id, bucket_month)` et ordonne par `occurred_at DESC, consultation_id`. La requête fournit toujours formation et mois. `consultations_by_profile_month` duplique les événements ayant un profil pour éviter un index secondaire et répondre à une seconde requête définie. L'ingestion doit écrire les deux vues de manière idempotente avec le même identifiant ; Cassandra n'est pas utilisé pour une transaction de commande.

## Taille, rétention et garanties

Un mois borne la partition ; l'exploitation surveille octets et cellules et peut passer à un bucket journalier si une formation chaude dépasse le seuil opérationnel retenu. `default_time_to_live = 7776000` limite les données à 90 jours. Les lectures utilisent la cohérence locale adaptée au laboratoire ; duplication et éventuelle divergence sont réparées par rejeu de la trace autoritative. Tombstones, compaction, réplication réelle, multi-DC et sauvegardes restent hors de la preuve locale mono-nœud.
