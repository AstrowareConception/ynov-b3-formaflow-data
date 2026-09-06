# ADR-0001 - PostgreSQL comme source relationnelle et photographie du prix

- Statut : accepté pour la référence pédagogique 1.0.0
- Contexte : les commandes, inscriptions, factures et paiements exigent contraintes, transactions et historique cohérent.
- Options : conserver seulement le tarif courant ; versionner les tarifs et recalculer ; photographier montant/devise sur chaque ligne tout en gardant la référence au tarif.
- Décision : PostgreSQL 16 porte la source de vérité transactionnelle. La ligne conserve montant et devise acceptés ; la référence au tarif explique leur origine mais ne les recalcule pas.
- Conséquences : une duplication intentionnelle protège l'historique et simplifie l'audit ; elle impose de nommer précisément la sémantique et de protéger la valeur après confirmation.
- Risques : fiscalité, remises, remboursements et multidevise ne sont pas couverts.
- Réexamen : nouvelle exigence comptable ou commerciale affectant la granularité du prix.

Cette décision de stockage ne fixe aucune frontière DDD.
