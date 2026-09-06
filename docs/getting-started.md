# Installation locale

## Prérequis

- Python 3.10 ou plus récent ;
- Docker Desktop sur Windows/macOS, ou Docker Engine avec le plugin Compose sur Linux ;
- GNU Make pour les commandes contractuelles ; sous Windows, utiliser WSL, Git Bash avec Make, Chocolatey/Scoop, ou exécuter directement `python scripts/manage.py <commande>` si Make n'est pas installé ;
- au moins 2 Go libres pour PostgreSQL ; prévoir davantage pour Cassandra ou Neo4j.

## Démarrage

```bash
make setup
make start
make reset-data
make smoke
```

`make start` ne lance que PostgreSQL. Les ports sont liés à `127.0.0.1`. Aucun compte distant ni secret n'est requis. `make stop` conserve les volumes ; `make clean` ne touche qu'à `build/` et `dist/`.

## Préconditions des commandes

`setup` exige le client Docker mais pas un serveur démarré pour générer les fixtures ; la validation Compose exige le plugin. Les commandes SQL exigent Docker actif. Chaque commande NoSQL télécharge puis démarre un seul profil et peut demander plusieurs minutes, surtout Cassandra.

## Réinitialisation sûre

`make reset-data` recrée uniquement les schémas de la base `formaflow` dans le conteneur du projet. Il ne supprime aucun volume externe. Pour retirer explicitement les volumes de ce projet, utiliser une commande Docker consciente du projet après inspection ; aucune cible pédagogique ne le fait automatiquement.
