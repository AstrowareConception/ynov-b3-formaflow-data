# Architecture de données polyglotte gouvernée

Cette synthèse est une architecture pédagogique de référence, pas une obligation de déployer cinq moteurs. PostgreSQL suffit au parcours transactionnel ; chaque projection NoSQL doit prouver une valeur supérieure à son coût avant adoption. Les propriétaires mentionnés sont des hypothèses destinées au cours Architecture hexagonale & DDD.

## Sources de vérité et lectures

| Information | Source de vérité | Lecture spécialisée | Ownership pressenti, non définitif | Fraîcheur cible | Reprise |
|---|---|---|---|---|---|
| Formations, sessions, tarifs | PostgreSQL `core` | catalogue MongoDB | gestion de l'offre | moins de 60 s | reprojection par `training_id` |
| Participants, organisations | PostgreSQL `core` | identifiants minimisés dans les projections | identité/clients | selon usage | relecture autorisée et purge ciblée |
| Commandes, lignes, prix accepté | PostgreSQL `core` | vues SQL de reporting | commerce | transactionnelle | sauvegarde/restauration et journal |
| Inscriptions, capacité | PostgreSQL `core` | disponibilité Redis indicative | suivi pédagogique | cache 60 s | `DEL`, cache miss puis recalcul |
| Factures, paiements simulés | PostgreSQL `core` | vues SQL de facturation | administration commerciale | transactionnelle | réconciliation des paiements `UNKNOWN` |
| Documents | PostgreSQL pour métadonnées | stockage d'objet hypothétique hors périmètre | administration | selon document | inventaire et restauration coordonnés |
| Consultations | trace autoritative à définir ; copie SQL de laboratoire | Cassandra par formation/mois | analytique pressentie | minutes | rejeu avec même `consultation_id` |
| Compétences | PostgreSQL `core` | graphe Neo4j | référentiel pédagogique | moins de 5 min | reconstruction complète |
| Recommandations | calcul versionné | Neo4j et table analytique | expérimentation | datée, non autoritative | recalcul, jamais correction manuelle silencieuse |

## Synchronisation et incohérence

Les transactions PostgreSQL qui modifient un fait projeté écrivent dans la même transaction une ligne d'outbox avec identifiant, type versionné, clé d'agrégation technique, date et charge minimale. Un relais publie au moins une fois ; chaque consommateur enregistre l'identifiant traité ou remplace idempotemment sa projection par version source. La CDC reste une alternative d'exploitation lorsque l'outbox applicative n'est pas disponible, mais son contrat doit être stabilisé hors du format interne des tables.

MongoDB et Neo4j tolèrent une courte fenêtre d'incohérence visible par `projectedAt` et `sourceVersion`. Redis est invalidé après décision ; l'expiration borne naturellement l'écart et un cache miss relit PostgreSQL. Cassandra reçoit des événements de consultation idempotents ; la duplication query-first peut diverger et un job de comparaison/rejeu la répare. Une notification ou projection en panne ne revient jamais sur une commande ou inscription déjà décidée.

## Reprise et observabilité

- Compteurs : retard d'outbox, âge de la plus ancienne ligne, événements traités/échoués, dead letters, cache hit/miss et âge des projections.
- Corrélation : `event_id`, `correlation_id`, identifiant opaque du fait et version source ; aucune adresse ou nom dans les événements de référence.
- Reprise : backoff borné, dead-letter inspectable, rejeu idempotent, reprojection complète et comparaison de comptes/empreintes.
- Alertes : backlog croissant, partition Cassandra trop grande, évictions Redis, échec de refresh matérialisé, écart de version MongoDB/Neo4j.

## Gouvernance, rétention et minimisation

Le glossaire, les identifiants d'événements et les propriétaires pressentis sont versionnés. Une évolution incompatible crée une nouvelle version de contrat. Les consultations ont une TTL proposée de 90 jours ; la disponibilité Redis vit 60 secondes, le panier 30 minutes et l'idempotence 24 heures. Les profils analytiques utilisent des identifiants opaques, et les événements excluent noms et emails. Documents, factures et demandes d'effacement nécessitent une politique légale validée avant production ; aucune durée réelle n'est inventée dans ce laboratoire.

Les sauvegardes PostgreSQL sont la priorité : sauvegarde logique testée, restauration périodique et objectifs RPO/RTO à définir. Les projections reconstruisibles peuvent être sauvegardées pour accélérer la reprise, mais leur restauration ne doit pas masquer une version source obsolète. Les clés Redis éphémères ne sont pas sauvegardées dans le profil de cours.

## Coût, réversibilité et risques

Chaque moteur ajoute image, correctifs, supervision, sauvegarde éventuelle, compétences et procédures d'incident. Cassandra est le coût le plus difficile à justifier à petite échelle ; Neo4j n'est pertinent que si les traversées et leur explicabilité apportent une valeur mesurable. MongoDB peut être remplacé par une projection JSONB ou une recherche SQL, Redis par un recalcul direct, Cassandra par un stockage analytique plus simple, et Neo4j par des jointures ou un calcul batch. Cette réversibilité repose sur PostgreSQL et les traces autoritatives, jamais sur une double écriture non journalisée.

Risques principaux : perte ou duplication d'événement, projection silencieusement périmée, cache pris pour une autorité, partition chaude, graphe surinterprété, effacement incomplet, exposition de données, inflation des coûts et ownership prématurément figé. Les mitigations sont versionnement, idempotence, fraîcheur visible, réconciliation, minimisation, budgets d'exploitation et conditions explicites de retrait.
