# Règles métier et invariants

Les règles ci-dessous constituent un socle commun. Leur traduction en contraintes SQL, objets métier, contrats, critères d'acceptation ou tests dépend du module.

## Sessions

- Une session appartient à une seule formation de référence.
- Sa date de fin ne peut pas précéder sa date de début.
- Sa capacité est un entier strictement positif lorsqu'elle devient réservable.
- Une session annulée ne peut plus accepter de nouvelle inscription.
- La modification d'une formation ne doit pas réécrire silencieusement l'historique contractuel des commandes déjà confirmées.

## Commandes et prix

- Les montants monétaires sont exprimés en centimes d'euro dans les contrats techniques de référence.
- Une ligne confirmée conserve une photographie du prix convenu, même si le tarif courant change ensuite.
- Une commande possède un identifiant stable et un cycle de vie explicite.
- Une même demande idempotente ne doit pas créer plusieurs commandes équivalentes.
- Un paiement réel n'est jamais effectué : les résultats proviennent exclusivement d'un simulateur local.

## Inscriptions

- Un même participant ne peut pas posséder deux inscriptions actives à la même session.
- Une inscription consommant une place ne peut pas conduire à dépasser la capacité autorisée.
- Une inscription appartient à un participant et à une session identifiables.
- La création, la confirmation, l'annulation et le remboursement éventuel sont des décisions distinctes.
- Une notification échouée ne doit pas annuler silencieusement une inscription déjà confirmée.

## Identité et autorisation

- Être authentifié ne suffit jamais à accéder à une commande, une inscription ou un export.
- Un client individuel n'accède qu'aux ressources auxquelles il est légitimement rattaché.
- Le responsable d'une organisation ne peut agir que pour les participants relevant du périmètre autorisé.
- Les contrôles d'autorisation sont effectués côté serveur, indépendamment de l'interface utilisateur.

## Données personnelles

- Chaque donnée collectée doit être reliée à une finalité explicite.
- Les événements, journaux et exports ne transportent que les données nécessaires à leur usage.
- Les secrets, mots de passe en clair et jetons complets ne sont jamais consignés dans les journaux.
- Une demande d'effacement produit un résultat traçable et distingue suppression, anonymisation et conservation justifiée.
- Les jeux de données pédagogiques restent synthétiques et réinitialisables.

## Échanges

- Un événement d'intégration décrit un fait passé ; il ne commande pas implicitement au consommateur une décision cachée.
- Chaque événement publié possède un identifiant, une version, un horodatage et un identifiant de corrélation.
- La compatibilité d'une évolution est analysée du point de vue des producteurs et consommateurs identifiés.
- Un consommateur doit pouvoir rencontrer un doublon sans produire un effet métier incontrôlé.

