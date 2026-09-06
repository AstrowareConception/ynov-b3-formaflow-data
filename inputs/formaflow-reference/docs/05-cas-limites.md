# Cas limites de référence

Ces situations doivent alimenter exercices, tests, QCM et démonstrations. Elles ne prescrivent pas une solution unique.

## Données et domaine

1. La dernière place d'une session est demandée presque simultanément par deux clients.
2. Un participant déjà inscrit est ajouté par une organisation différente.
3. Le tarif d'une session change après la confirmation d'une commande.
4. Une session est reportée après l'émission de documents administratifs.
5. Une formation est archivée alors que des sessions historiques doivent rester consultables.
6. Une organisation finance l'inscription d'un participant qui possède déjà un compte individuel.

## Interopérabilité

7. Un ancien consommateur reçoit une nouvelle version d'un événement contenant un champ inconnu.
8. Un producteur omet un champ autrefois obligatoire ou change son unité sans changer de nom.
9. Un message est livré deux fois après un redémarrage du consommateur.
10. Un webhook est reçu après expiration du délai de réponse du système appelant.
11. Le service de notification est indisponible lorsque la commande est confirmée.

## Backend distribué

12. Le simulateur de paiement répond lentement puis accepte la demande après expiration du timeout client.
13. Une erreur transitoire déclenche plusieurs retries susceptibles de répéter un effet.
14. Un consommateur empoisonné échoue systématiquement et le message rejoint une file dédiée.
15. Une instance malsaine continue momentanément à recevoir du trafic.
16. L'écriture métier réussit mais la publication de l'événement échoue.

## Sécurité et RGPD

17. Un utilisateur modifie l'identifiant d'une inscription dans l'URL et tente d'accéder à celle d'un autre compte.
18. Une valeur affichée dans le client contient une charge XSS inoffensive de démonstration.
19. Une action sensible utilisant un cookie est déclenchée depuis une origine non autorisée.
20. Un export ou un journal contient davantage de données personnelles que nécessaire.
21. Une demande d'effacement concerne des données également présentes dans une projection, un cache, un message ou une sauvegarde.

## Usage pédagogique

Chaque repository sélectionne seulement les cas compatibles avec son syllabus. Les variantes d'évaluation doivent employer des situations équivalentes mais inédites, et non recopier à l'identique les ateliers formatifs.

