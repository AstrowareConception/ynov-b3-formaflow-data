# Commandes étudiantes

| Commande | Précondition | Résultat |
|---|---|---|
| `make setup` | Python, Docker CLI/Compose | vérifie et prépare `.env` et les fixtures |
| `make start` | daemon Docker actif | démarre PostgreSQL uniquement |
| `make stop` | Docker | arrête les conteneurs du projet, conserve les volumes |
| `make reset-data` | PostgreSQL disponible | recrée l'état pédagogique déterministe |
| `make seed DATASET=nominal` | schéma prêt | charge le petit jeu lisible |
| `make seed DATASET=edge-cases` | schéma prêt | charge les cas limites ciblés |
| `make seed DATASET=benchmark` | schéma prêt | génère et charge le petit profil de mesure |
| `make smoke` | données chargées | vérifie connexion, objets et résultats stables |
| `make validate` | Python | contrôle le contrat documentaire et les durées du parcours |
| `make test` | données chargées | lance validations et tests SQL |
| `make benchmark` | checkpoint relationnel | enregistre protocole, plans et mesures |
| `make nosql PROFILE=<nom>` | profil disponible | lance un seul moteur et son initialisation |
| `make quality` | Python, Docker Compose | valide fichiers, liens, contrats et configuration |
| `make package` | état final valide | construit le ZIP déterministe |
| `make clean` | aucune | supprime seulement `build/` et `dist/` |
