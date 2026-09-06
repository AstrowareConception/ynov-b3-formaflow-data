# Statut d'exécution des profils

Ce fichier est mis à jour uniquement à partir de contrôles réellement exécutés. Les quatre modèles et leurs scripts sont toujours validés statiquement par `make quality`.

| Profil | Modélisé | Initialisation réelle | Trace préparée | Source de vérité |
|---|---|---|---|---|
| MongoDB 8.0.29 | oui | oui, 3 documents et lecture par slug = 1 | non | PostgreSQL |
| Redis 7.4.11 | oui | oui, disponibilité = 1 ; TTL = 60/1800/86400 s | non | PostgreSQL |
| Cassandra 5.0.9 | oui | oui, 2 tables et partition cible = 1 ligne | oui, 1 000 000 événements non exécutés | trace autoritative à définir / PostgreSQL pour le catalogue |
| Neo4j 5.26.30 Community | oui | oui, écarts recommandés = 1, 2, 3 | non | PostgreSQL |

Environnement d'exécution : Docker Desktop 29.7.2, Windows hôte, images Linux `amd64`, le 2026-09-06. Chaque validation finale a été précédée d'un arrêt explicite de tous les profils du projet. Un premier essai Redis a révélé que `compose down` sans activation des profils laissait MongoDB actif ; le script a été corrigé pour inclure les quatre profils, tous les conteneurs ont été arrêtés, puis Redis, Cassandra et Neo4j ont été rejoués en isolation.
