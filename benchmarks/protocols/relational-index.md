# Protocole relationnel borné - consultations par formation

## Hypothèse

Sur le jeu synthétique retenu, un index composé `(training_id, occurred_at DESC)` peut réduire les pages examinées pour compter les consultations récentes d'une formation ciblée. Le protocole ne prétend pas que l'index est toujours préférable : il augmente le coût d'écriture et peut être ignoré sur une petite table ou une valeur peu sélective.

## Préconditions et commande

```bash
make start
make benchmark
```

Le script charge le profil `small` de 10 000 consultations avec le seed `20260906`, supprime l'index pour la variante `before`, exécute un échauffement puis cinq répétitions avec `EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)`. Il recrée ensuite l'index, relance `ANALYZE` et répète exactement la requête.

## Enregistrement

`build/benchmark/result.json` contient version PostgreSQL, OS/architecture/CPU/mémoire exposés par Docker, dataset, seed, date logique, volumétrie, requête, échauffement, répétitions, résultat fonctionnel, temps rapportés par PostgreSQL et chemins des plans JSON. Les tests vérifient présence, types et égalité fonctionnelle, jamais un seuil temporel.

## Interprétation

Comparer les nœuds de plan, lignes lues, buffers et dispersion. Une exécution locale courte est sensible au cache, à la virtualisation, aux tâches concurrentes et au coût fixe de planification. Le résultat est contextualisé et non généralisable à une production, une autre distribution ou un autre ratio lecture/écriture.
