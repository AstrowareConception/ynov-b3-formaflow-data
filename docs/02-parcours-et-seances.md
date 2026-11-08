# Parcours pédagogique — quatre TP refondus

Le module comporte quatre séances dont l'enchaînement suit désormais l'ordre **besoin → modèle → garantie → choix → composition**. Les TP sont formatifs et associés aux cours théoriques refondus. Il n'y a **ni chronogramme de micro-exercices, ni correction intégrée aux supports étudiants**.

| Séance | Apport théorique structurant | TP de consolidation | Point de reprise |
|---|---|---|---|
| 1 | Besoin métier, Merise, MCD, MLD, premier MPD | Décrire et modéliser le parcours FormaFlow ; expliciter les cardinalités et trois invariants | `course-start` |
| 2 | Anomalies, 1NF–3NF approfondies, intégrité, index, mesure, dénormalisation | Reprendre un export fragile, justifier contraintes et index et qualifier un benchmark | dossier local TP1 ; secours `checkpoint-relational` |
| 3 | Quatre familles NoSQL, garanties, comparaison par usage | Quatre modèles minimaux et un seul profil approfondi ; matrice incluant PostgreSQL | `checkpoint-relational` |
| 4 | Sources et copies, outbox, contrats, migrations, exploitation | Architecture justifiée, scénarios de reprise, mapping, ADR, dossier DDD | `checkpoint-nosql` |

## Règles communes aux productions

- Ne pas modifier le corpus figé `inputs/formaflow-reference/`.
- Réutiliser les trois cas limites : capacité, doublon d'inscription, prix historique.
- Séparer **preuve exécutée**, **trace observée** et **hypothèse ou modèle seulement proposé**.
- Conserver une source éditable pour les schémas et l'architecture, ainsi qu'une trace de décision / contribution. Dépôt des productions en ZIP sur Moodle, sans push vers GitHub.
- Ne pas inclure les corrigés dans les archives ZIP déposées par les étudiants.
- Le travail reste possible à partir de diagrammes et traces en cas de poste bloqué.

Les étapes exactes, critères et livrables sont présentés dans les Pages Moodle. Voir `briefs/session-01` à `session-04`, ainsi que `docs/pedagogie/TP-2026-2027.md`.

Les modalités de notation préexistantes restent décrites séparément dans `docs/09-evaluation.md` ; les TP ne créent pas une nouvelle épreuve.
