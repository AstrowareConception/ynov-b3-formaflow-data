# Séance 4 - Composer une architecture polyglotte gouvernée

**Durée indicative :** 3 h, dont 1 h FFP et 2 h TDP. Le QCM individuel contextualisé de 45 minutes est inclus dans ces 2 h de TDP.
**État de départ :** tag `checkpoint-nosql`. Reprise possible depuis ce tag avant la synthèse.

## Objectifs

Composer les modèles retenus, désigner les sources de vérité et modèles de lecture, expliquer synchronisation et reprise, intégrer gouvernance et coût, puis sélectionner une trace formative compatible avec l'Evidence Kit 1.0.0.

## Contexte et fichiers fournis

Mobiliser les décisions relationnelles et NoSQL, `docs/templates/polyglot-architecture.md`, `docs/templates/adr.md` et `docs/cdan/transfer.md`. L'ownership est une hypothèse à transmettre au module Architecture hexagonale & DDD, pas un bounded context définitif.

## Étapes proposées

1. Cartographier chaque information avec sa source de vérité, ses lectures et son propriétaire pressenti.
2. Décrire flux, outbox/CDC/recalcul éventuel, fenêtre d'incohérence, idempotence et reprise.
3. Examiner rétention, minimisation, sauvegarde, observabilité, exploitation, coût et réversibilité.
4. Rédiger un ADR avec options, décision, conséquences, risques et condition de réexamen.
5. Sélectionner une ou deux preuves et compléter la fiche CDAN en distinguant contribution et socle fourni.

## Productions formatives attendues

Architecture polyglotte, matrice source de vérité, ADR, risques, hypothèses d'ownership et fiche CDAN formative.

## Critères de réussite

Chaque copie a une origine et une stratégie de réparation ; les incohérences temporaires sont bornées ; aucune donnée réelle ou secrète n'est présente ; la fiche CDAN annonce outils, vérifications et limites ; aucune seconde notation n'est créée.

## Erreurs fréquentes

Dessiner une base par bounded context, oublier la reconstruction d'une projection, appeler « événement » une commande non décidée, masquer le coût d'exploitation, présenter une hypothèse d'ownership comme décision définitive.

## Questions de synthèse

Que se passe-t-il si une projection manque un événement ? Quelle donnée doit être minimisée ? Quelle décision devra explicitement être remise en question dans le prochain module ?
