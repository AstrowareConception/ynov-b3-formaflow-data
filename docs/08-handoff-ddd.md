# Transmission vers Architecture hexagonale & DDD

## Destination

Le formateur construit `handoff/data-reference/` puis le copie dans `inputs/data-reference/` de `ynov-b3-formaflow-hexagonal`.

## Contenu minimal

```text
handoff/data-reference/
├── README.md
├── manifest.yml
├── source-version.txt
├── glossary.md
├── invariants.md
├── assumptions.md
├── data-dictionary.md
├── models/
│   ├── mcd.*
│   ├── mld.*
│   └── mpd.sql
├── decisions/
├── evidence/
└── known-limitations.md
```

## Information à préserver

- sens des termes ;
- règles et contre-exemples ;
- décisions de données déjà démontrées ;
- contraintes physiques utiles ;
- questions ouvertes ;
- hypothèses d'ownership ;
- limites des mesures.

## Information à ne pas imposer

Le paquet ne définit pas les agrégats, entités, value objects, ports, adapters ou bounded contexts. Il ne présente pas le schéma relationnel comme un modèle de domaine et n'inclut aucune branche étudiante.

## Validation

Avant publication, le formateur vérifie les liens, exécute le MPD sur une base vide, charge les fixtures, lance les tests d'intégrité et confirme que les hypothèses sont explicitement distinguées des faits.

