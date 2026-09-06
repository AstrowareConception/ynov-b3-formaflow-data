# Plan de clés Redis

| Clé | Type | TTL | Valeur | Réparation |
|---|---|---:|---|---|
| `formaflow:v1:session:SES-2027-0001:availability` | string | 60 s | `1` place indicative | recalcul SQL après absence/invalidation |
| `formaflow:v1:basket:BASKET-SYNTH-01` | hash | 1 800 s | session et participant opaques | abandon accepté à expiration |
| `formaflow:v1:idempotency:OP-SYNTH-01` | string | 86 400 s | résultat minimal `ENR-2027-000001` | unicité durable PostgreSQL reste décisive |
