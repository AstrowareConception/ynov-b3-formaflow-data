# Référence de données vers Architecture hexagonale & DDD

Ce snapshot autonome provient de `ynov-b3-formaflow-data` 1.0.0 au tag `reference-final`. Il transmet le sens des données, les invariants démontrés, les modèles conceptuel/logique/physique, les décisions de stockage, les mesures contextualisées, les hypothèses et les limites.

## Utilisation

Copier ce dossier dans `ynov-b3-formaflow-hexagonal/inputs/data-reference/`, sans sous-module ni dépendance dynamique. Lire `glossary.md`, `invariants.md`, `examples-and-counterexamples.md` et `open-questions.md` avant de confronter les faits au modèle de domaine.

Le MPD est autonome et rejouable avec `psql -v ON_ERROR_STOP=1 -f models/mpd.sql <base_vide>`. Les données ne sont pas embarquées dans le MPD ; les exemples restent documentaires et synthétiques.

## Limite de responsabilité

Ce paquet ne définit aucun agrégat, entité DDD, value object, bounded context, port, adapter ou architecture applicative. Une table n'est pas automatiquement une entité de domaine et une base n'est pas automatiquement un bounded context. `ownership-hypotheses.md` contient uniquement des hypothèses à discuter.
