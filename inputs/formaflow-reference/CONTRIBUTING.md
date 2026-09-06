# Contribuer au référentiel FormaFlow

## Principe

Une modification du référentiel peut affecter plusieurs cours, contrats, fixtures, exercices et QCM. Toute contribution commence donc par décrire le besoin, la compatibilité attendue et les repositories consommateurs concernés.

## Marche à suivre

1. Créer une branche `change/<sujet-court>` depuis le dernier tag approuvé.
2. Modifier d'abord les fichiers de référence machine-lisibles, puis leur explication documentaire.
3. Mettre à jour `catalog/traceability.json` lorsque la règle, le scénario ou l'événement change.
4. Ajouter ou adapter un exemple synthétique et, si nécessaire, son schéma.
5. Exécuter `make validate` sans accès réseau.
6. Faire relire l'impact pédagogique avant de fusionner.
7. Mettre à jour `CHANGELOG.md` et choisir PATCH, MINOR ou MAJOR.

## Règles de sûreté

- aucune donnée, URL privée, clé, jeton ou information client réelle ;
- aucun corrigé d'évaluation ni solution d'exercice ;
- aucune architecture de données, DDD ou microservices présentée comme l'unique réponse ;
- aucun changement silencieux d'un identifiant, d'une unité ou d'un invariant ;
- aucune réécriture d'un tag déjà utilisé pendant une année pédagogique.

## Critère d'acceptation

Une contribution est acceptable lorsque le parcours reste racontable sans contradiction, que les exemples passent les schémas, que les références sont résolues et que le changement peut être expliqué à un intervenant qui n'a pas participé à sa conception.
