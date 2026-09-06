# Glossaire commun

Ce glossaire fixe un vocabulaire transversal. Il ne constitue pas encore un langage ubiquitaire DDD ni une décision sur les bounded contexts.

| Terme métier | Identifiant technique indicatif | Définition de référence |
|---|---|---|
| Formation | `Training` | Offre pédagogique décrivant une promesse, des objectifs et un contenu ; elle ne porte pas à elle seule une date de réalisation. |
| Session de formation | `TrainingSession` | Occurrence planifiée d'une formation, avec dates, capacité, tarif de référence et état. |
| Compte | `Account` | Moyen d'authentifier une personne et de gérer ses accès ; il ne se confond pas nécessairement avec un participant. |
| Participant | `Learner` | Personne physique destinée à suivre une session. |
| Organisation cliente | `CustomerOrganization` | Structure pouvant financer ou administrer des inscriptions pour des participants autorisés. |
| Commande | `Order` | Engagement commercial regroupant les informations nécessaires à l'achat d'une ou plusieurs inscriptions. |
| Ligne de commande | `OrderLine` | Élément d'une commande conservant notamment la session, le bénéficiaire et la photographie du prix convenu. |
| Inscription | `Enrollment` | Droit accordé à un participant de suivre une session déterminée, avec un cycle de vie propre. |
| Paiement | `Payment` | Tentative ou résultat financier simulé associé à une commande. |
| Facture | `Invoice` | Document comptable fictif produit selon les règles du scénario pédagogique. |
| Notification | `Notification` | Message préparé pour informer un destinataire d'un fait métier déjà établi. |
| Capacité | `Capacity` | Nombre maximal de places que la session peut accueillir selon la règle retenue. |
| Place disponible | `AvailableSeat` | Résultat calculé à partir de la capacité et des inscriptions qui consomment effectivement une place. |
| Consentement | `Consent` | Manifestation libre, spécifique, éclairée et univoque utilisée uniquement lorsqu'elle constitue la base légale appropriée. |
| Événement de domaine | `DomainEvent` | Fait significatif exprimé à l'intérieur d'un modèle de domaine. |
| Événement d'intégration | `IntegrationEvent` | Contrat versionné publié afin d'informer d'autres composants d'un fait déjà décidé. |
| État canonique | `ReferenceState` | Version consolidée par le formateur et utilisée comme point d'entrée ou de reprise. |
| Preuve | `Evidence` | Élément reproductible reliant une affirmation à une observation, un test, un résultat ou une décision. |

## Termes à ne pas confondre

- une **formation** n'est pas une **session** ;
- une **commande** n'est pas une **inscription** ;
- un **client** n'est pas nécessairement le **participant** ;
- une **confirmation de commande** n'est pas une **confirmation de notification** ;
- la **suppression d'un compte** n'entraîne pas mécaniquement l'effacement immédiat de toutes les données ;
- un **schéma de données** ne décide pas automatiquement des frontières du **modèle de domaine**.

