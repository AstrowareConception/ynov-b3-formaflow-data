# Gouvernance et versionnement

## Responsabilité

Le formateur est responsable de la version canonique du référentiel. Toute évolution doit préserver la cohérence entre progressions pédagogiques, cours intégraux, repositories, exercices, QCM et corrigés.

## Statuts documentaires

- `draft` : proposition encore modifiable ;
- `review` : contenu soumis à une revue transversale ;
- `approved` : version retenue pour préparer les repositories ;
- `frozen` : version figée pour une année pédagogique ;
- `deprecated` : version conservée pour l'historique mais non utilisée.

## Règles de versionnement

- Une clarification orthographique ou rédactionnelle produit une version PATCH.
- Un ajout compatible de scénario, règle ou donnée produit une version MINOR.
- Un changement de sens, d'identifiant, d'unité, d'invariant ou de parcours produit une version MAJOR.
- Une version déjà utilisée dans un tag de cours n'est jamais réécrite.
- Chaque repository consommateur indique explicitement la version importée.

## Processus de modification

1. Décrire le besoin et les repositories affectés.
2. Identifier les documents, fixtures, contrats, exercices et évaluations concernés.
3. Modifier le référentiel et son `manifest.yml`.
4. Vérifier les incohérences terminologiques et les liens de transmission.
5. Mettre à jour le journal des versions.
6. Publier un tag.
7. Régénérer uniquement les instantanés nécessaires.

## Critères de validation

Une version peut être déclarée `approved` lorsque :

- le parcours de référence peut être raconté sans contradiction ;
- chaque terme important possède une définition stable ;
- les invariants sont illustrables par un exemple et un contre-exemple ;
- aucun document ne révèle prématurément une solution pédagogique ;
- les repositories consommateurs et paquets de transmission sont identifiés ;
- les données restent fictives et les dépendances externes optionnelles ou simulées.

## Décisions arrêtées en 1.0.0

- les identifiants canoniques utilisent un préfixe métier, l'année lorsqu'elle est utile et une séquence lisible ;
- les états et transitions de Session, Commande, Paiement, Inscription et Notification sont publiés dans `catalog/state-models.json` ;
- les jeux partagés utilisent du JSON et le domaine réservé `.test` ;
- les événements et manifestes de handoff possèdent un schéma JSON versionné ;
- le référentiel est diffusé dans le cadre pédagogique Ynov 2026-2027, sans donnée ni secret réel ;
- chaque année conserve ses tags immuables et ses archives de référence.

Une évolution ultérieure pourra préciser une licence publique ou ajouter des événements compatibles. Elle ne devra jamais réécrire `reference-v1.0.0`.
