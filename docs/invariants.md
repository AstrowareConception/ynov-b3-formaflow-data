# Invariants de données

## `INV-CAPACITY` - capacité d'une session

Le nombre d'inscriptions consommant une place (`PENDING` ou `CONFIRMED`) ne dépasse jamais `training_session.capacity`.

- Exemple autorisé : une session de capacité 2 avec une place occupée accepte une seconde inscription.
- Contre-exemple : un autre participant tente de prendre une troisième place.
- Protection : verrou de ligne sur la session et trigger `core.guard_session_capacity()` ; le verrou sérialise les concurrents pour la dernière place.
- Preuve : `sql/tests/010_integrity.sql` teste écriture autorisée puis refus `check_violation`.

## `INV-ENROLLMENT-UNIQUE` - absence de double inscription

Un participant ne possède qu'une inscription pour une même session.

- Exemple autorisé : le même participant est inscrit à deux sessions différentes.
- Contre-exemple : une autre commande tente d'inscrire le participant à une session déjà associée.
- Protection : contrainte `UNIQUE (session_id, participant_id)` indépendante de l'acheteur ou de l'organisation financeuse.
- Preuve : `sql/tests/010_integrity.sql` attend une `unique_violation`.

## `INV-PRICE-SNAPSHOT` - prix accepté historique

Une ligne de commande conserve le montant et la devise acceptés ; modifier le tarif courant ne modifie jamais cette photographie.

- Exemple autorisé : le tarif passe de 42 000 à 47 000 centimes tandis que la ligne reste à 42 000.
- Contre-exemple : recalculer une ancienne commande par jointure avec le seul tarif courant.
- Protection : colonnes non nulles sur `order_line` et trigger interdisant leur modification après confirmation.
- Preuve : fixture `EDGE-PRICE-HISTORY`, test SQL et vue `reporting.accepted_price_history`.

Ces protections décrivent le stockage PostgreSQL. Elles ne déterminent pas automatiquement l'emplacement de règles dans un futur modèle de domaine.
