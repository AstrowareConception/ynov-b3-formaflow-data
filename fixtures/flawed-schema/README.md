# Schéma volontairement fragile

`enrollment-export.csv` mélange dans une même relation participant, organisation, formation, session, inscription, tarif, commande, ligne, facture et paiement. Le fichier est synthétique et déterministe.

Les groupes doivent identifier les dépendances fonctionnelles et expliquer au moins :

- l'impossibilité d'ajouter proprement une formation sans commande ;
- la multiplication des mises à jour lors d'un renommage d'organisation ou de formation ;
- la perte d'informations de session lors de la suppression de sa dernière ligne ;
- les dépendances transitives `participant_id -> organization_id -> organization_name` et `session_id -> training_id -> training_title` ;
- les faits de granularités différentes autour de la commande, de la facture et des tentatives de paiement ;
- l'ambiguïté des valeurs absentes, qui peuvent signifier « non applicable », « pas encore produit » ou « inconnu » ;
- la différence entre `current_price_minor` et `accepted_price_minor`, indispensable à l'historique.

Le fichier ne prescrit pas une correction unique. Toute décomposition doit annoncer ses hypothèses, ses clés, les dépendances préservées et les jointures nécessaires aux usages.
