# Glossaire consolidé AstroData Hub

Ce glossaire complète le snapshot FormaFlow 1.0.0 pour le périmètre données. Il ne constitue ni un langage ubiquitaire DDD définitif ni une liste d'agrégats.

| Terme | Définition retenue | Distinction importante |
|---|---|---|
| Formation | Offre pédagogique décrivant une promesse et un contenu | N'a ni date ni capacité ; celles-ci appartiennent à la session |
| Session de formation | Occurrence planifiée d'une formation | Porte dates, capacité, état et tarif courant de référence |
| Participant | Personne physique bénéficiaire d'une inscription | Peut différer de l'acheteur et du responsable d'organisation |
| Organisation cliente | Structure susceptible de financer des participants | Le financement ne transfère pas automatiquement tous les droits d'accès |
| Tarif | Prix de référence d'une formation sur une période | Une évolution ne réécrit jamais le prix accepté |
| Commande | Engagement commercial d'un individu ou d'une organisation | Regroupe une ou plusieurs lignes et possède son propre état |
| Ligne de commande | Choix d'une session pour un bénéficiaire | Photographie montant et devise acceptés |
| Inscription | Droit d'un participant à suivre une session | Une place est consommée par les états `PENDING` et `CONFIRMED` |
| Facture | Document comptable fictif associé à une commande | N'est ni la commande ni un paiement |
| Paiement | Tentative financière simulée | Plusieurs tentatives peuvent concerner une commande ; `UNKNOWN` exige une réconciliation |
| Document | Métadonnée d'un document synthétique | Le stockage binaire n'est pas modélisé comme une colonne SQL |
| Consultation | Observation d'accès au catalogue | Peut être anonyme et suit une rétention distincte |
| Compétence | Capacité décrite par un libellé stable | Relie profils et formations sans prouver une causalité |
| Recommandation | Projection calculée et datée | N'est pas une source de vérité sur le profil ou la formation |
| Source de vérité | Système autorisé à décider la valeur de référence | Une projection ou un cache peut être reconstruisible sans devenir autoritatif |
| Ownership pressenti | Hypothèse sur une responsabilité future | Ne définit pas un bounded context ni un agrégat DDD |
