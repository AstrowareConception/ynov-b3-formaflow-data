# Vision produit

## Proposition de valeur

FormaFlow Marketplace est une plateforme fictive permettant à des particuliers et à des organisations de découvrir des formations professionnelles, de choisir une session disponible, de commander des inscriptions et de suivre les principales étapes administratives associées.

Le produit a été choisi parce qu'il offre un domaine compréhensible sans être trivial. Il associe catalogue, planification, capacité, identité, commande, paiement simulé, inscription, facturation, notification et protection des données. Ces préoccupations peuvent être observées selon plusieurs modèles sans qu'une architecture unique s'impose naturellement.

## Problème pédagogique

Les étudiants rencontrent souvent des sujets sans lien entre les matières. FormaFlow fournit au contraire un vocabulaire stable et des situations récurrentes. L'objectif n'est pas de développer neuf fois la même application, mais de montrer qu'un même système peut être décrit par :

- un modèle conceptuel et physique de données ;
- un modèle de domaine protégeant des invariants ;
- des contrats d'échange et des stratégies de compatibilité ;
- un backlog organisé autour de la valeur ;
- une architecture backend distribuée ;
- une cartographie des risques et des traitements de données.

## Parcours de référence

Le parcours central est le suivant :

1. une formation est publiée ;
2. une ou plusieurs sessions sont planifiées ;
3. un client choisit une session ouverte ;
4. une commande d'inscription est créée ;
5. un paiement fictif est accepté, refusé ou laissé dans un état incertain ;
6. la commande confirmée déclenche la création de l'inscription ;
7. le participant et les équipes concernées sont notifiés ;
8. les traces nécessaires à l'administration, au support et à la conformité sont conservées selon des règles explicites.

## Qualités recherchées

Le système doit rester explicable, testable, reproductible localement et suffisamment riche pour révéler les compromis. Il doit également permettre d'observer des pannes, des incompatibilités, des erreurs de modélisation et des vulnérabilités sans contacter un service réel.

## Non-objectifs

FormaFlow n'a pas vocation à devenir une marketplace commerciale prête pour la production. Le fil rouge n'inclut pas de paiement réel, de messagerie réelle, de fournisseur d'identité externe, de cloud obligatoire, de Kubernetes, de recommandation par intelligence artificielle ni de traitement de données réelles.

