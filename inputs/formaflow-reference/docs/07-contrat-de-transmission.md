# Contrat de transmission intermodules

## Objectif

Un paquet de transmission fournit au module suivant suffisamment de contexte pour travailler, sans lui imposer une production étudiante, une connexion réseau ou l'historique complet du repository précédent.

## Structure minimale

Chaque paquet `handoff/<consumer>-reference/` contient :

```text
handoff/<consumer>-reference/
├── README.md
├── manifest.yml
├── source-version.txt
├── glossary.md
├── assumptions.md
├── known-limitations.md
├── decisions/
├── diagrams/
├── fixtures/
└── evidence/
```

Le contenu spécialisé — MCD, OpenAPI, événements, backlog, tests ou rapports — est ajouté selon le besoin du consommateur.

## Propriétés obligatoires

- origine et tag formateur identifiables ;
- fichiers consultables hors ligne ;
- données exclusivement synthétiques ;
- hypothèses et limites explicites ;
- absence de secret et de dépendance à un compte externe ;
- commandes de validation lorsque le paquet contient des éléments exécutables ;
- séparation entre faits de référence, décisions du module précédent et questions encore ouvertes.

## Publication

1. Le formateur consolide les productions et corrigés utiles.
2. Il génère le paquet destiné au consommateur.
3. Il vérifie les liens, formats, schémas et données.
4. Il publie un tag `reference-final` ou le tag canonique prévu par le repository.
5. Le paquet est copié dans `inputs/` du module suivant.
6. Le repository consommateur enregistre la version dans son propre manifeste.

## Interdictions

- dépendre directement d'une branche d'étudiant ;
- utiliser un sous-module Git vers un dépôt susceptible d'évoluer pendant le cours ;
- corriger silencieusement une règle métier pendant la copie ;
- inclure une solution à l'exercice que le module consommateur doit faire découvrir ;
- transmettre des données ou secrets réels.

