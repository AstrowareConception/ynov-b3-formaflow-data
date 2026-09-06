# Release 1.0.0

## Portée

La release transforme la spécification enrichie V0.1.0 en quatre états pédagogiques : `course-start`, `checkpoint-relational`, `checkpoint-nosql` et `reference-final`. `data-v1.0.0` identifie le même commit final publiable. Les productions restent formatives ; l'unique évaluation est le QCM individuel contextualisé de 45 minutes, séparé du dépôt et représentant 100 % de la note.

## Sources et provenance

Le contenu initial courant du dépôt a été retenu comme spécification Data V0.1.0 officielle. `_inputs/ynov-b3-formaflow-data-v0.1.0.zip`, SHA-256 `a53295a77f758178bf960379e5b1c6b37b73f4a623773579531ad57da57f31d4`, a été écartée comme ancienne variante incomplète après comparaison fichier par fichier ; elle reste locale, ignorée et absente de la distribution. L'empreinte annoncée de l'archive de référence initiale était `ac5355ccc33ba5ea29c7de0880919afba07507b1f4fb3db4af89bd5f87b9e89a`.

Les dépendances canoniques ont été contrôlées strictement : FormaFlow Reference 1.0.0 au SHA-256 `9de0223729f0aa4b99c7d5d2ff260cd25f7540401566bb033b7a383c57b4d921` et CDAN Evidence Kit 1.0.0 au SHA-256 `845ff950bf6be288715b6edb0c4a84457c7827bb40caca238a411ba188e6665a`.

## Reproductibilité de la distribution

Le packageur classe explicitement les extensions et noms de fichiers texte du dépôt. Leur contenu est encodé en UTF-8 avec des fins de ligne LF avant compression ; les autres fichiers sont archivés sans modification. Cette normalisation ne dépend pas de la configuration Git locale. Le test d'intégration compare le ZIP construit depuis le checkout, depuis les blobs d'un `git archive`, depuis une copie simulant des fins de ligne CRLF et depuis l'extraction du ZIP précédent.

## Limites connues

Les diagrammes restent en source Mermaid car aucun moteur `mmdc` ou Graphviz n'était disponible pendant la construction ; les commandes exactes figurent dans `docs/models/README.md`. Le benchmark local illustre un plan et une mesure sur 10 000 lignes, sans généralisation. Cassandra est testé en mono-nœud pédagogique et ne prouve ni disponibilité distribuée ni comportement de production.
