# TP 1 — Du besoin au MCD, MLD et MPD (parcours refondu)

## Intentions pédagogiques

La séance 1 reconstruit les fondamentaux de Merise sans supposer leur maîtrise préalable. Le TP suit le cours : **besoin → règles et dictionnaire → MCD et cardinalités → MLD → premier MPD → épreuve des invariants**. Les consignes détaillées, destinées aux étudiants, sont distribuées par une **Page Moodle** distincte.

## État de départ

- Télécharger le tag immuable `course-start` sur son ordinateur : https://github.com/AstrowareConception/ynov-b3-formaflow-data/archive/refs/tags/course-start.zip . Le dépôt sert uniquement de documentation et de point de départ : **aucun fork, branche, commit ni push n'est demandé**.
- Créer sur son poste un dossier `FormaFlow_TP1_Groupe-XX/` séparé du corpus, puis remettre les productions sous la forme d'un ZIP dans Moodle.
- Référentiel : `inputs/formaflow-reference/docs/02-acteurs-et-parcours.md`, `03-glossaire.md`, `04-regles-metier-et-invariants.md`, `05-cas-limites.md`.
- Jeux : `fixtures/nominal/dataset.json`, `fixtures/edge-cases/dataset.json`.
- Ne pas utiliser les dossiers canoniques d'un état plus avancé comme corrigé pendant la recherche.

## Missions

1. Raconter le parcours d'une organisation qui finance l'inscription d'un bénéficiaire ; séparer formation, session, client, commande, ligne, paiement et inscription.
2. Définir au moins dix données métier, leurs unités, leurs absences permises et six règles de gestion vérifiables.
3. Dessiner le MCD du noyau, **lire chaque association dans les deux sens**, justifier minimum et maximum ; représenter une formation sans session et une commande sans inscription.
4. Traduire les liens en MLD, identifier PK, FK et unicités métier ; inclure le lien N,N Formation–Compétence avec `target_level`.
5. Produire dans un schéma de travail isolé un extrait de MPD PostgreSQL montrant PK/FK, `NOT NULL` et `CHECK`.
6. Examiner dernière place, doublon de participant et changement du prix après commande.

## Productions

`docs/glossary.md`, `docs/data-dictionary.md`, `docs/assumptions.md`, `docs/invariants.md`, sources éditables MCD/MLD, extrait SQL du MPD et tableau « règle → mécanisme → preuve ».

## Critères

Le dessin exprime le **métier**, non les tables. L'acheteur est distinct du bénéficiaire, le prix accepté reste historique, la PK technique ne remplace pas l'unicité métier. Les garanties de concurrence non encore implémentées sont **signalées** plutôt qu'inventées.

**En cas de poste bloqué :** fournir les modèles et une analyse des tests, en distinguant explicitement prévu, observé sur trace et exécuté.

> Les solutions de référence et corrigés Moodle sont réservés au formateur et ne doivent pas être ajoutés au rendu des étudiants.

## Remise Moodle

Un fichier `FormaFlow_TP1_Groupe-XX.zip` par groupe : modèles éditables et exports lisibles, documents métier, script SQL, `README.md` indiquant membres, contributions et degré de preuve. Aucun lien de commit n'est demandé.
