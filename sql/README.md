# Zone SQL

Ce dossier contient le schéma PostgreSQL ordonné, les contraintes transactionnelles, les index reliés aux usages, les vues de reporting, les seeds et les tests d'intégrité.

L'ordre exécuté par `make reset-data` est `schema/000`, `schema/010`, `schema/020`, `constraints/030`, `indexes/040`, `reporting/050`, puis `seed/nominal.sql`. Les corrections de référence sont absentes du tag `course-start` et apparaissent à `checkpoint-relational`.
