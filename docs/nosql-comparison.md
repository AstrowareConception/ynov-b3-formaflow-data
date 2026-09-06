# Comparaison des paradigmes NoSQL

Les notes de 1 (défavorable) à 5 (favorable) répondent uniquement aux quatre usages pédagogiques décrits. Elles ne constituent pas un classement général des moteurs.

| Critère / poids | MongoDB catalogue | Redis disponibilité | Cassandra consultations | Neo4j recommandation |
|---|---:|---:|---:|---:|
| Accès cible naturel / 5 | 5 | 5 | 5 | 5 |
| Garantie adaptée sans source autoritative / 5 | 2 | 1 | 2 | 2 |
| Maîtrise de la croissance / 4 | 4 si imbrication bornée | 5 avec TTL/limite mémoire | 4 avec bucket et TTL | 3 avec traversées bornées |
| Cohérence transactionnelle multi-objets / 4 | 2 | 1 | 1 | 2 |
| Reconstruction / réversibilité / 3 | 4 | 5 | 4 | 4 |
| Coût d'exploitation pédagogique / 3 | 3 | 5 | 1 | 2 |

## Lecture par besoin

- MongoDB convient à la fiche catalogue variable si les sessions non bornées restent référencées et si PostgreSQL reconstruit la projection.
- Redis convient à une indication éphémère ou une protection courte ; une éviction ne doit jamais attribuer ou retirer une inscription autoritative.
- Cassandra illustre le query-first et une volumétrie d'événements, mais un cluster exploitable est coûteux et injustifié pour le petit dataset nominal.
- Neo4j explique des chemins de compétences, mais le graphe ne transforme ni corrélation ni proximité en recommandation causalement juste.

Les garanties, volumes et coûts conduisent donc à une architecture sélective : chaque moteur peut rester un prototype ou une projection optionnelle. PostgreSQL suffit au parcours transactionnel et demeure le point de reprise.
