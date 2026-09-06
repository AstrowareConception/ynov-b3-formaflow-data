# Preuves d'intégrité relationnelle

Commande exécutée sur PostgreSQL 16.15 : `python scripts/manage.py test` après `reset-data` et seed nominal.

Résultats observés le 2026-09-06 :

- la dernière place autorisée est insérée ;
- une place au-delà de la capacité produit une `check_violation` ;
- un doublon session/participant produit une `unique_violation` ;
- le tarif courant peut évoluer sans changer le montant accepté ;
- la modification du snapshot d'une commande confirmée est refusée ;
- chiffre d'affaires, remplissage, facturation et historique retournent les valeurs nominales attendues.

Limite : le verrouillage concurrent est mis en œuvre par verrou de ligne et testé fonctionnellement, mais ce fichier ne contient pas un stress test multi-client.
