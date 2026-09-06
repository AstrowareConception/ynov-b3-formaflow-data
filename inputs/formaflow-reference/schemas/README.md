# Schémas machine-lisibles

Les schémas publiés avec `reference-v1.0.0` décrivent les formats canoniques distribués aux repositories consommateurs.

| Schéma | Usage |
|---|---|
| `event-envelope.schema.json` | Enveloppe commune des événements d'intégration |
| `events/training-session-created.v1.schema.json` | Contrat `TrainingSessionCreated.v1` |
| `events/order-confirmed.v1.schema.json` | Contrat `OrderConfirmed.v1` |
| `events/enrollment-created.v1.schema.json` | Contrat `EnrollmentCreated.v1` |
| `reference-dataset.schema.json` | Structure minimale du jeu de données synthétique |
| `handoff-manifest.schema.json` | Métadonnées d'un paquet de transmission intermodules |

Les schémas utilisent JSON Schema Draft 2020-12. La commande `make validate` vérifie leur syntaxe, leurs références locales, les exemples et les invariants transversaux sans accès réseau.

Les contrats d'événements sont figés en version 1. Toute évolution incompatible doit publier un nouveau nom versionné ; un fichier v1 déjà distribué n'est jamais réécrit silencieusement.
