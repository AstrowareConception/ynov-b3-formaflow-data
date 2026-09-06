# Neo4j - recommandations par compétences

## Usage et statut

Le graphe relie profils opaques, compétences et formations pour expliquer des recommandations par écart de niveau. PostgreSQL reste source de vérité des formations et du référentiel de compétences ; les recommandations sont recalculables. `make nosql PROFILE=neo4j` exécute réellement `init.cypher` si l'image est disponible. Les requêtes sont également lisibles sans moteur.

## Nœuds, relations et contraintes

Nœuds : `Training`, `Skill`, `Profile`. Relations : `(:Training)-[:REQUIRES {level}]->(:Skill)` et `(:Profile)-[:HAS_SKILL {level}]->(:Skill)`. Les identifiants sont uniques par label. Les propriétés temporelles de projection permettent de diagnostiquer la fraîcheur sans inclure de nom ou d'adresse.

## Limites

Un chemin ou une compétence commune indique une proximité définie par le modèle, jamais une causalité ni une aptitude réelle. Le score simple ne prend en compte ni préférence, ni disponibilité, ni biais de catalogue. Les traversées sont bornées, les profils restent opaques, et un recalcul complet répare une projection obsolète. Le choix du graphe doit être réexaminé si les requêtes restent de simples jointures bornées ou si son coût d'exploitation dépasse la valeur d'explication.
