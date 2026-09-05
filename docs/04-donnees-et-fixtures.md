# Données et fixtures

## Principes

Toutes les données sont synthétiques, déterministes et documentées. Un seed identique doit produire le même nombre d'enregistrements, les mêmes identifiants de référence et les mêmes cas limites.

## Jeux prévus

### `nominal`

Petit corpus lisible destiné à comprendre les relations : formations, sessions, participants, organisations, commandes, inscriptions, factures, paiements et documents.

### `edge-cases`

Corpus ciblé contenant notamment : session complète, double demande d'inscription, changement de tarif, participant financé par une organisation, paiement refusé ou incertain et données facultatives absentes.

### `flawed-schema`

Export volontairement redondant mélangeant inscription, participant, organisation, formation, session, tarif, facture et paiement. Il doit rendre observables les anomalies d'insertion, modification et suppression sans rendre la correction triviale.

### `benchmark`

Jeu de taille paramétrable destiné à comparer une requête avant et après indexation, réécriture ou matérialisation. Trois tailles sont prévues : petite pour la salle, moyenne pour la démonstration et trace préparée pour une volumétrie supérieure.

## Contraintes de conception

- aucune donnée personnelle réelle ;
- aucune dépendance à un générateur en ligne ;
- identifiants stables pour les scénarios cités dans les supports ;
- horodatages et montants cohérents ;
- génération compatible avec un poste étudiant standard ;
- procédure de réinitialisation explicite ;
- inventaire des volumes produit après chargement.

