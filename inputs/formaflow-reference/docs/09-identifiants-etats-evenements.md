# Identifiants, états et événements

## Identifiants canoniques

Les exemples utilisent des identifiants lisibles et opaques du point de vue métier. Ils facilitent les traces pédagogiques sans imposer la stratégie technique définitive.

| Objet | Forme de référence | Exemple |
|---|---|---|
| Formation | `TRN-####` | `TRN-0001` |
| Session | `SES-YYYY-####` | `SES-2027-0001` |
| Compte | `ACC-####` | `ACC-0001` |
| Participant | `LRN-####` | `LRN-0001` |
| Organisation | `ORG-####` | `ORG-0001` |
| Commande | `ORD-YYYY-######` | `ORD-2027-000001` |
| Ligne de commande | `OLN-YYYY-######` | `OLN-2027-000001` |
| Paiement simulé | `PAY-YYYY-######` | `PAY-2027-000001` |
| Inscription | `ENR-YYYY-######` | `ENR-2027-000001` |
| Facture | `INV-YYYY-######` | `INV-2027-000001` |
| Notification | `NTF-YYYY-######` | `NTF-2027-000001` |

Ces formes servent aux fixtures et aux échanges. Une implémentation peut employer UUID ou ULID en interne à condition de conserver l'opacité, la stabilité et une représentation documentée aux frontières.

## États et transitions

`catalog/state-models.json` définit les transitions autorisées pour Session, Commande, Paiement, Inscription et Notification. Il fixe les mots partagés, pas la structure des tables ou des classes.

Les transitions importantes du parcours canonique sont :

1. la session passe de `SCHEDULED` à `OPEN` lorsqu'elle devient réservable ;
2. la commande passe de `DRAFT` à `AWAITING_PAYMENT` ;
3. le paiement simulé produit `ACCEPTED`, `REFUSED` ou `UNKNOWN` ;
4. seul un résultat accepté autorise la confirmation de la commande dans le scénario nominal ;
5. la confirmation de commande permet la création d'une inscription ;
6. la notification peut échouer sans annuler l'inscription confirmée.

## Événements d'intégration

Trois événements sont canoniques en 1.0.0 :

- `TrainingSessionCreated.v1` annonce la création d'une session planifiée ;
- `OrderConfirmed.v1` annonce qu'une commande est devenue confirmée avec ses lignes et photographies de prix ;
- `EnrollmentCreated.v1` annonce la création d'une inscription pour un participant et une session.

Chaque événement possède `eventId`, `eventType`, `version`, `occurredAt`, `correlationId`, `causationId`, `producer` et `payload`. Les dates sont en UTC ISO 8601, les montants en centimes d'euro et les personnes sont référencées par identifiant opaque. Un événement exprime un fait passé ; il ne demande pas implicitement au consommateur d'exécuter une commande cachée.

## Compatibilité

Un ajout de champ facultatif reste compatible lorsque les consommateurs tolèrent les champs inconnus. La suppression d'un champ requis, le changement d'unité ou la modification du sens exige une nouvelle version de contrat. Un producteur et un consommateur doivent tester séparément leurs hypothèses.
