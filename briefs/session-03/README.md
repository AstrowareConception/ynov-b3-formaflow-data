# TP 3 — Choisir un paradigme SQL / NoSQL (parcours refondu)

## Intention

Passer de « connaître quatre technologies » à **justifier un moteur par un accès réel**, ses garanties, ses coûts et une solution plus simple à comparer.

## Point de départ

Tag immuable `checkpoint-relational` téléchargé sur le poste ou production consolidée autorisée. Consulter `nosql/README.md`, `nosql/execution-status.md` et `docs/templates/comparison-matrix.md`.

## Missions

1. Définir les **quatre fiches d'accès** : catalogue variable, disponibilité indicative, consultations par formation/mois, écarts de compétences par profil.
2. Proposer quatre modèles minimaux avec question, données, clés, requête dominante, duplications, fraîcheur, rétention, panne et stratégie de reconstruction :
   - **MongoDB** : document de catalogue et imbrication bornée ; comparer avec PostgreSQL JSONB.
   - **Redis** : convention de clés, type, TTL, cache miss, éviction et source d'autorité.
   - **Cassandra** : clé de partition `(training_id, bucket_month)` et clustering temporel ; expliquer hotspots et lectures multi-buckets.
   - **Neo4j** : nœuds Profile/Skill/Training, liens HAS_SKILL/REQUIRES, niveaux portés par les liens et score interprétable.
3. **Approfondir un seul profil exécutable** si le poste le permet. Pour les autres, l'analyse des modèles suffit ; pas de démarrage des quatre profils simultanément.
4. Réaliser une **matrice de choix par usage**, en incluant PostgreSQL seul, contraintes éliminatoires et coût total d'exploitation.
5. Formuler une recommandation réversible : bénéfice, risque, preuve ou hypothèse, condition de réexamen.

## Livrables

Quatre fiches, quatre modèles, une trace ou un essai réellement qualifié, une matrice multi-usages et une recommandation.

## Garde-fous

La capacité et l'unicité des inscriptions demeurent décidées en PostgreSQL. Une exécution mono-nœud ne démontre aucune garantie de cluster. La source autoritative des consultations peut rester à **définir**, sans inventer un pipeline. Recommander **zéro moteur supplémentaire** est acceptable.

> Le détail des questions et les critères sont dans la Page Moodle ; aucune réponse canonique n'est publiée dans le rendu étudiant.

## Remise

Rendu ZIP sur Moodle ; aucun envoi vers GitHub.
