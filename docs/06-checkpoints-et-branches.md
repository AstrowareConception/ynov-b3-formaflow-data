# Checkpoints et branches

## Branches étudiantes

Chaque binôme travaille dans `work/<team-id>`. Les commits doivent séparer autant que possible modèle, scripts, tests et documentation afin de rendre la progression lisible.

## Tags formateur

| Tag | Contenu | Usage |
|---|---|---|
| `course-start` | Corpus, briefs, fixtures, gabarits et environnement initial | Début du module |
| `checkpoint-relational` | Schéma relationnel de référence, contraintes, données et scripts de reprise | Déblocage avant NoSQL |
| `checkpoint-nosql` | Corpus relationnel stabilisé et gabarits NoSQL prêts pour la synthèse | Déblocage avant l'architecture polyglotte |
| `reference-final` | Version consolidée et paquet de transmission | Préparation du module DDD |

## Règles

- les tags formateur ne sont jamais déplacés ;
- repartir d'un checkpoint n'entraîne aucune pénalité automatique ;
- les productions d'un autre binôme ne servent pas de solution de reprise ;
- les solutions détaillées ne sont publiées qu'au moment compatible avec le déroulement ;
- chaque checkpoint passe `make smoke` et `make test` avant publication.

