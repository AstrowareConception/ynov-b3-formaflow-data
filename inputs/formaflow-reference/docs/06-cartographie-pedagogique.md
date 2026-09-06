# Cartographie pédagogique

## Chaîne FormaFlow

| Ordre | Module | Repository | Entrée principale | Sortie canonique |
|---:|---|---|---|---|
| 1 | Conception et architecture des données | `ynov-b3-formaflow-data` | Corpus métier et cas limites | Glossaire consolidé, invariants, MCD/MLD/MPD, stockage et hypothèses d'ownership |
| 2 | Architecture hexagonale & DDD | `ynov-b3-formaflow-hexagonal` | `inputs/data-reference/` | Langage ubiquitaire, context map, frontières, événements, diagrammes et ADR |
| 3 | Échange de données & interopérabilité | `ynov-b3-formaflow-interop` | `inputs/architecture-reference/` | Contrats, mappings, compatibilité, incident et dossier d'évolution vulgarisé |
| 4 | Participation projet & agilité | `ynov-b3-formaflow-agility` | `inputs/interop-reference/` | Vision, story map, backlog, tranche verticale, critères, DoD, risques et workflow |
| 5 | Développement backend & microservices | `ynov-b3-formaflow-distributed` | `inputs/agility-reference/` | Gateway et services de référence, contrats, identité, données, journaux et scénarios de panne |
| 6 | Sécurité applicative & RGPD | `ynov-b3-formaflow-security-lab` | `inputs/backend-reference/` | Corrections, tests, cartographies RGPD, constats et paquet méthodologique |

## Chaîne AtlasLegacy

`ynov-b3-atlaslegacy` constitue une rupture volontaire. Le module de rétro-ingénierie reçoit le tag `audit-start`. Le formateur publie ensuite `audit-reference`, puis `communication-start`, `communication-reference` et `refactor-start` afin d'alimenter successivement Communication technique et Clean Code & Refactoring.

La sécurité transmet éventuellement un paquet méthodologique expurgé, mais aucun code FormaFlow ne devient un prérequis d'AtlasLegacy.

## Portefeuille CDAN

Chaque module produit une trace courte dans `docs/cdan/transfer.md`. Le repository `ynov-b3-cdan-evidence-kit` fournit les gabarits communs : contexte, décision, preuve, limite, compétence mobilisée et action suivante.

## Principe de reprise

Un module consommateur ne télécharge pas dynamiquement l'état du précédent. Le formateur copie et fige le paquet validé dans `inputs/`. Cette duplication contrôlée garantit la reproductibilité de l'année pédagogique et évite les cascades d'échec.

