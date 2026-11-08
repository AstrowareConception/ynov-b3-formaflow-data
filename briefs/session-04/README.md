# TP 4 — Composer et transmettre une architecture de données (parcours refondu)

## Intention

Faire aboutir les séances précédentes : **responsabilités → synchronisation → transformation et migration → exploitation → transmission à DDD**. Le TP est formatif ; l'évaluation individuelle éventuelle est organisée séparément.

## Point de départ

Productions consolidées ou tag `checkpoint-nosql` si la reprise est nécessaire ; `docs/templates/polyglot-architecture.md`, `docs/templates/adr.md`, `docs/cdan/transfer.md`, modèles et hypothèses des autres séances.

## Missions

1. Cartographier les **sources autoritatives**, caches, projections et consommateurs. Couvrir commande, inscriptions, prix historique, disponibilité indicative, catalogue, consultations, compétences.
2. Montrer le risque de **double écriture**. Décrire transaction locale + **outbox**, relais, livraison au moins une fois, déduplication durable et reprise. **Ne pas présenter ce pipeline comme implémenté dans le dépôt.**
3. Définir une migration compatible des champs de montant `amount` vers `amount_minor` et `currency` : **expand → migrate → observe → contract**, mapping, unités, erreurs, versions, lineage et backfill.
4. Prévoir minimisation, droits, observabilité, sauvegarde et **test de restauration**, gestion des retards et coûts d'exploitation.
5. Rédiger un **ADR** explicitant alternatives, preuves, conséquences, risque et condition de réexamen.
6. Préparer un dossier court de **transmission à Architecture hexagonale & DDD** : vocabulaire, invariants, décisions, limites, hypothèses d'ownership encore ouvertes.

## Livrables

Diagramme éditable, matrice source/copie/fraîcheur/réparation, scénario de synchronisation, contrat de mapping, ADR, fiche CDAN et liens vers les preuves des séances 1 à 3.

## Points non négociables

Une table n'est pas un agrégat DDD ; un stockage n'est pas un bounded context. L'événement `order.confirmed` représente un fait, non une commande cachée. Un événement dupliqué ou une notification en échec ne doit pas modifier la décision métier déjà validée. Plusieurs moteurs ne sont **jamais** obligatoires.

> Les corrigés et toute épreuve sommative restent dans un espace enseignant distinct.

## Remise

Rendu ZIP sur Moodle depuis les fichiers du dossier local ; aucun envoi vers GitHub.
