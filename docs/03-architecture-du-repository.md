# Architecture du repository

## Séparation des zones

- `inputs/` : références figées et non modifiables par les étudiants ;
- `briefs/` : besoins, scénarios, volumes et consignes propres aux séances ;
- `fixtures/` : données synthétiques reproductibles ;
- `docs/` : vocabulaire, hypothèses, invariants, modèles et décisions ;
- `diagrams/` : sources éditables et rendus versionnés ;
- `sql/` : schéma, contraintes, index, reporting et tests ;
- `nosql/` : propositions ou prototypes séparés par famille ;
- `benchmarks/` : protocoles et résultats, jamais conclusions isolées ;
- `evidence/` : sorties de commandes et preuves sélectionnées ;
- `handoff/` : paquet canonique publié uniquement par le formateur.

## Formats

Les documents humains sont rédigés en Markdown. Les modèles doivent être conservés dans un format source lorsque l'outil le permet, accompagnés d'un export PNG, SVG ou PDF consultable sans licence propriétaire.

Les scripts SQL sont ordonnés, rejouables et séparés des résultats de mesure. Les sorties volumineuses, caches et volumes de bases ne sont pas versionnés.

## Règle de neutralité

Le repository décrit les données sans transformer automatiquement une table en entité DDD, une base en bounded context ou une relation en agrégat. Les fichiers d'ownership sont nommés comme hypothèses et seront remis en question dans le module suivant.

## Kit formateur

Les solutions, variantes du QCM, corrigés et scripts de démonstration sensibles vivent dans un repository privé distinct. Les tags de reprise distribués aux étudiants ne contiennent que les éléments nécessaires à la continuité pédagogique.

