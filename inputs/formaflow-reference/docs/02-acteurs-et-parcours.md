# Acteurs et parcours

## Acteurs principaux

### Visiteur

Il consulte le catalogue public, recherche une formation et examine les prochaines sessions. Il ne peut ni commander ni accéder aux données d'un participant.

### Client individuel

Il possède un compte, commande une inscription pour lui-même, consulte ses commandes et exerce ses droits sur ses données personnelles.

### Responsable d'organisation

Il commande des inscriptions pour des collaborateurs autorisés. Son pouvoir d'action reste limité à son organisation et ne lui donne jamais un accès global aux autres comptes.

### Participant

Il est la personne inscrite à une session. Un participant peut être le client ayant effectué la commande ou un bénéficiaire distinct.

### Gestionnaire de formation

Il publie les formations, planifie les sessions, ajuste leur capacité selon les règles autorisées et consulte les inscriptions nécessaires à l'organisation.

### Agent administratif

Il traite les dossiers d'inscription, les documents, les demandes de correction et certains exports. Ses actions doivent être traçables et limitées à sa mission.

### Administrateur technique

Il exploite la plateforme sans disposer par principe d'un accès métier illimité. Les privilèges techniques et fonctionnels restent distingués.

### Services simulés

Le prestataire de paiement, la messagerie et les dépendances externes sont remplacés par des simulateurs locaux déterministes. Ils permettent de reproduire succès, refus, lenteur, indisponibilité et réponse incertaine.

## Parcours fonctionnels

### Publication d'une session

Un gestionnaire associe une session à une formation, définit ses dates, sa capacité, son tarif de référence et son état initial. Une session ne devient réservable que si les informations indispensables sont cohérentes.

### Commande et inscription

Un client sélectionne une session, désigne le participant, confirme les informations nécessaires et déclenche un paiement simulé. La commande conserve une photographie du prix et des informations contractuelles utiles. L'inscription est créée uniquement lorsque les conditions métier retenues sont satisfaites.

### Annulation et remboursement

Le client ou un agent autorisé demande l'annulation. Le résultat dépend de l'état de l'inscription, de la date de la session et de la politique applicable. L'annulation ne signifie pas automatiquement remboursement intégral.

### Notification

Une notification informe le participant d'un fait déjà décidé. Son échec ne doit pas effacer la décision métier qui l'a précédée.

### Exercice des droits

Une personne peut demander accès, rectification, portabilité, limitation, opposition ou effacement. La réponse doit distinguer données supprimables, données temporairement conservées pour une obligation justifiée et informations pouvant être anonymisées.

