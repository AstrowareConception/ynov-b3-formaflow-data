# ADR-0002 - Les modèles NoSQL restent des projections spécialisées

- Statut : accepté pour la référence pédagogique 1.0.0
- Contexte : quatre usages de lecture illustrent document, clé-valeur, colonnes larges et graphe, tandis que capacité, unicité et historique exigent une source transactionnelle cohérente.
- Options : déplacer chaque domaine vers son moteur « naturel » ; ne conserver que PostgreSQL ; conserver PostgreSQL comme source et rendre les projections NoSQL optionnelles et reconstruisibles.
- Décision : MongoDB projette le catalogue, Redis met en cache une disponibilité indicative, Cassandra projette les consultations et Neo4j projette compétences/recommandations. Aucun n'accorde une inscription ni ne confirme un paiement.
- Conséquences : les accès spécialisés deviennent explicites, mais synchronisation, observation, reprise et exploitation ont un coût. Un déploiement réel peut retenir moins de moteurs.
- Risques : dérive silencieuse, duplication de données, surcoût opérationnel, rétention divergente et fausse confiance dans un score de graphe.
- Réexamen : absence de valeur mesurable, exigences de cohérence plus fortes, volumes insuffisants ou équipe incapable d'exploiter le moteur.

Cette répartition technique ne définit pas de bounded contexts.
