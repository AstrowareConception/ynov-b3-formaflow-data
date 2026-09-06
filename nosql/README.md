# Zone NoSQL

Les propositions MongoDB, Redis, Cassandra et Neo4j sont séparées par profil. Chaque sous-dossier décrit le besoin, les accès, la structure, les duplications, les garanties, la rétention, le coût d'exploitation et ce qui est réellement exécuté ou seulement modélisé.

La présence d'un modèle n'implique pas que le moteur soit retenu dans l'architecture finale. Un seul profil est démarré à la fois avec `make nosql PROFILE=<mongodb|redis|cassandra|neo4j>`. Le statut factuel des essais figure dans `execution-status.md`.
