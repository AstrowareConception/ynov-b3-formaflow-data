# Redis - disponibilité éphémère et idempotence

## Usage et statut

Redis expose une disponibilité indicative du catalogue et une clé d'idempotence courte. Il n'est jamais source de vérité des inscriptions, commandes ou paiements. `make nosql PROFILE=redis` exécute réellement `init.redis` lorsque l'image est disponible ; `keys.md` décrit le modèle hors moteur.

## Convention, TTL et invalidation

- `formaflow:v1:session:<session-id>:availability` : chaîne entière, TTL 60 s ;
- `formaflow:v1:basket:<opaque-id>` : hash de panier synthétique, TTL 1 800 s ;
- `formaflow:v1:idempotency:<operation-id>` : résultat minimal, TTL 86 400 s.

Après une transaction PostgreSQL d'inscription, le consommateur invalide la disponibilité avec `DEL`; la prochaine lecture recalcule depuis la source. Une mise à jour opportuniste peut utiliser `SET ... EX`, mais n'accorde jamais une place. L'absence de clé signifie « inconnu, recalcul requis », pas « zéro ».

## Persistance, éviction et limites

Le profil de cours désactive RDB et AOF et utilise `allkeys-lru` avec 64 Mo : toute clé peut disparaître. Une éviction provoque un cache miss ou la perte d'une protection d'idempotence courte ; l'opération autoritative doit donc disposer aussi d'une unicité durable côté PostgreSQL. En production, politique d'éviction, mémoire, persistance et isolation des usages seraient réévaluées.
