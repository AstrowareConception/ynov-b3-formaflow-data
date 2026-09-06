# Dictionnaire de données ciblé

| Objet.attribut | Type PostgreSQL | Null | Sens / règle |
|---|---|---:|---|
| `organization.organization_id` | `text` | non | Identifiant synthétique opaque `ORG-*` |
| `participant.participant_id` | `text` | non | Bénéficiaire `LRN-*`, distinct d'un compte |
| `participant.organization_id` | `text` FK | oui | Organisation de référence éventuelle, pas preuve de financement |
| `training.training_id` | `text` | non | Offre sans date ni capacité |
| `tariff.amount_minor` | `integer` | non | Montant courant en unité mineure, positif ou nul |
| `training_session.capacity` | `integer` | non | Strictement positive ; comparée aux inscriptions actives |
| `training_session.current_tariff_id` | `text` FK | non | Tarif de référence actuel |
| `customer_order.buyer_participant_id` | `text` FK | oui | Acheteur individuel éventuel |
| `customer_order.organization_id` | `text` FK | oui | Organisation acheteuse éventuelle ; au moins un acheteur est requis |
| `order_line.accepted_unit_price_minor` | `integer` | non | Photographie contractuelle indépendante du tarif courant |
| `enrollment.(session_id, participant_id)` | `text`, `text` | non | Couple unique dans la version 1.0.0 |
| `payment.status` | enum | non | `PENDING`, `ACCEPTED`, `REFUSED` ou `UNKNOWN` |
| `document.storage_key` | `text` | non | Clé synthétique, pas un chemin contenant un secret |
| `consultation.profile_id` | `text` | oui | Profil opaque ; `NULL` représente une consultation anonyme |
| `training_skill.target_level` | `smallint` | non | Niveau cible entre 1 et 5 |
| `recommendation.generated_at` | `timestamptz` | non | Date de calcul de la projection reconstruisible |

Les identifiants restent des chaînes pour préserver les identifiants canoniques intermodules. Ce choix physique ne les transforme pas en value objects DDD.
