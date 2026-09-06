# Hypothèses et questions ouvertes

| ID | Nature | Formulation | Impact et validation attendue |
|---|---|---|---|
| `HYP-DATA-01` | hypothèse | `PENDING` et `CONFIRMED` consomment une place, contrairement à `CANCELLED` et `COMPLETED` | À confirmer avec les règles de gestion ; le trigger de capacité matérialise cette hypothèse |
| `HYP-DATA-02` | hypothèse | Une inscription annulée reste unique pour le couple participant/session | La contrainte conserve l'historique ; un besoin de réinscription exigerait un identifiant de tentative ou une règle révisée |
| `HYP-DATA-03` | hypothèse | Les montants sont stockés en unités mineures et une commande reste monodevise | Simplifie les totaux ; fiscalité et conversion sont hors périmètre |
| `HYP-DATA-04` | hypothèse | Un participant peut être rattaché à zéro ou une organisation de référence | Le financement réel reste porté par la commande, évitant d'en déduire des droits permanents |
| `HYP-DATA-05` | fait pédagogique | Toutes les identités et organisations sont synthétiques | Vérifié par les identifiants, libellés et domaines `.test` |
| `HYP-OWN-01` | ownership pressenti | Catalogue/planification pourrait posséder formations, sessions et tarifs | À remettre en question dans le module DDD ; aucune frontière définitive n'en découle |
| `HYP-OWN-02` | ownership pressenti | Commerce pourrait posséder commandes, lignes, factures et paiements simulés | Une hypothèse de travail, pas un bounded context imposé |
| `HYP-OWN-03` | ownership pressenti | Suivi pédagogique pourrait posséder inscriptions et documents | Doit être confronté aux invariants transactionnels et aux parcours du futur modèle de domaine |

Questions ouvertes : politique exacte de réinscription après annulation, fiscalité, changement de devise, purge des documents, durée de rétention des consultations et gouvernance des libellés de compétences.
