# MongoDB - projection documentaire du catalogue

## Usage et statut

Le modèle sert la lecture d'une fiche de formation dont les attributs, prérequis et modalités varient. PostgreSQL reste la source de vérité des formations, tarifs et sessions ; MongoDB est une projection reconstruisible. `make nosql PROFILE=mongodb` exécute réellement `init.js` lorsque l'image est disponible. `model.json` reste la représentation lisible sans moteur.

## Structure et accès

Une formation est un document avec résumé, attributs variables, compétences et modules imbriqués. Les sessions ne sont pas imbriquées : leur nombre peut croître sans borne et leur capacité change selon un cycle transactionnel. Le document conserve seulement `nextSessionIds`, projection bornée à trois identifiants opaques.

Accès cibles : fiche par `slug`, recherche de formations publiées par compétence, filtre sur `attributes.level`. Les index sont unique sur `slug`, composé sur `status` et `skills.code`, et partiel sur le niveau.

## Garanties et limites

La mise à jour atomique d'un document suffit pour son contenu éditorial, pas pour une commande multi-objet. Les doublons de libellés de compétences sont acceptés dans la projection et recalculés depuis la source. Une limite de taille documentaire et le maximum de trois prochaines sessions préviennent une croissance silencieuse ; historique, inscriptions et paiement restent hors du document.

La projection peut être en retard pendant une fenêtre cible de 60 secondes. Une outbox PostgreSQL et un consommateur idempotent sont proposés dans l'architecture finale ; un recalcul complet par `training_id` répare les écarts.
