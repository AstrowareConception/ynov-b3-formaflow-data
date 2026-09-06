# ADR-0003 - Outbox et projections reconstruisibles

- Statut : accepté pour la référence pédagogique 1.0.0
- Contexte : une double écriture PostgreSQL/NoSQL peut laisser une décision valide sans projection ou une projection sans décision.
- Options : double écriture synchrone ; CDC sur les tables ; outbox transactionnelle et consommateurs idempotents ; recalcul périodique seulement.
- Décision : utiliser conceptuellement une outbox dans la transaction PostgreSQL, publier au moins une fois, traiter par identifiant/version et conserver une voie de reprojection. Redis reçoit une invalidation ; les projections durables reçoivent un fait versionné. La CDC est une alternative documentée, pas une dépendance du laboratoire.
- Conséquences : pas de transaction distribuée ; une fenêtre d'incohérence existe et doit être observée. Les consommateurs doivent supporter duplication, ordre partiel et rejeu.
- Risques : croissance de l'outbox, événement poison, contrat couplé au schéma et effacement incomplet.
- Mesures : purge après rétention contrôlée, dead-letter, métrique d'âge, charges minimisées et tests de reconstruction.
- Réexamen : exigences de cohérence synchrone ou impossibilité opérationnelle de maintenir le relais.

Les noms de producteurs dans les exemples sont des responsabilités techniques indicatives, pas des bounded contexts définitifs.
