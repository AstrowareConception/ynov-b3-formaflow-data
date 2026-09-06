# Normalisation et dénormalisation contrôlée

## Diagnostic de l'export fragile

La ligne de `fixtures/flawed-schema/enrollment-export.csv` mélange les granularités inscription, participant, organisation, session, formation, ligne de commande, facture et tentative de paiement. Une valeur atomique par cellule satisfait superficiellement la 1NF, mais la relation reste impropre à représenter plusieurs paiements ou plusieurs lignes par commande sans répétition.

Avec une clé composée candidate incluant au moins commande, ligne et paiement, des attributs dépendent seulement de fragments : `order_line_id -> session_id, participant_id, accepted_price`, `payment_id -> payment_status`, `participant_id -> participant_name, participant_email`. Cela viole la 2NF. Les dépendances `session_id -> training_id -> training_title` et `participant_id -> organization_id -> organization_name` rendent les dépendances transitives visibles et violent la 3NF.

## Décomposition de référence

Le MPD sépare `participant`, `organization`, `training`, `tariff`, `training_session`, `customer_order`, `order_line`, `enrollment`, `invoice` et `payment`. Chaque fait non-clé dépend de la clé, de toute la clé et de rien d'autre dans sa relation. Les relations d'association compétence/formation et compétence/profil utilisent leur couple comme clé.

## BCNF

Les relations canoniques visent BCNF lorsque tout déterminant fonctionnel non trivial est une super-clé. Le cas pédagogique utile est l'export : `participant_email -> participant_id` peut être un déterminant métier candidat alors que `participant_id` est la clé technique. La contrainte `UNIQUE(email)` rend les deux clés candidates explicites. Si le métier autorisait le partage ou le changement ambigu d'adresse, cette dépendance disparaîtrait : BCNF ne doit donc pas être affirmée sans hypothèse métier.

## Dénormalisations intentionnelles

- `order_line.accepted_unit_price_minor` et `currency` dupliquent la valeur tarifaire pour préserver un fait historique ; ce n'est pas une anomalie à « corriger » par jointure dynamique.
- `reporting.daily_consultations` matérialise un agrégat reconstruisible. Sa fraîcheur est explicite et un `REFRESH` répare la projection.
- Les modèles NoSQL du checkpoint suivant assument d'autres duplications orientées lecture, sans déplacer automatiquement la source de vérité.

Toute nouvelle dénormalisation doit citer accès, volume, mesure, mécanisme de reconstruction et condition de réexamen.
