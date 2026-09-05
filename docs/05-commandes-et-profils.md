# Commandes et profils d'exécution

## Interface commune

Le `Makefile` constitue l'interface pédagogique stable. Il masque les détails répétitifs sans cacher les commandes SQL importantes étudiées en cours.

Chaque cible doit :

- afficher clairement ce qu'elle exécute ;
- échouer avec un message actionnable ;
- documenter ses préconditions ;
- éviter toute action sur un volume non créé par le projet ;
- fonctionner hors ligne après récupération initiale des images.

## PostgreSQL

`make start` démarre uniquement PostgreSQL et les outils minimaux. `make reset-data` recrée la base pédagogique depuis des scripts versionnés. `make smoke` vérifie la connexion, la présence des objets attendus, le chargement des fixtures et quelques résultats stables.

## NoSQL

Les profils sont indépendants :

```text
make nosql PROFILE=mongodb
make nosql PROFILE=redis
make nosql PROFILE=cassandra
make nosql PROFILE=neo4j
```

Un profil peut fournir un moteur réel, un script d'initialisation ou seulement une trace préparée selon le coût de démarrage. Le support indique toujours si l'étudiant observe, modélise ou exécute réellement.

## Benchmark

`make benchmark` enregistre au minimum version, dataset, requête, répétitions, plan et résultats. Il ne produit pas automatiquement une recommandation : l'interprétation reste une activité étudiante.

