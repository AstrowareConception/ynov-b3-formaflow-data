# Traçabilité et validation

## Source et représentation

Les documents Markdown expliquent le domaine à un lecteur humain. Les fichiers JSON en fournissent une représentation contrôlable par les repositories consommateurs. En cas d'écart, la version ne peut pas être publiée avant arbitrage : aucun format n'est silencieusement déclaré supérieur à l'autre.

## Matrice de traçabilité

`catalog/traceability.json` relie chaque module aux règles, cas limites, événements et productions qu'il peut mobiliser. Cette matrice remplit trois fonctions :

- vérifier qu'un exercice reste ancré dans le socle commun ;
- éviter qu'un QCM évalue un fait absent des cours et des dossiers fournis ;
- mesurer l'impact d'une modification du référentiel.

La matrice n'impose pas qu'un cours utilise tout le domaine. Chaque module sélectionne un sous-ensemble compatible avec son syllabus et annonce ce périmètre.

## Validation locale

`make validate` effectue notamment les contrôles suivants :

1. tous les JSON sont lisibles et leurs identifiants sont uniques ;
2. le manifeste, `VERSION` et le tag canonique annoncent la même version ;
3. acteurs, termes, règles, cas limites et événements cités existent ;
4. les transitions d'état ont une origine et une destination déclarées ;
5. les exemples d'événements respectent les contrats publiés ;
6. les lignes de commande, paiements et inscriptions des fixtures référencent des objets existants ;
7. les montants utilisent `EUR` et des unités mineures entières ;
8. les adresses pédagogiques utilisent le domaine réservé `.test` ;
9. les liens Markdown locaux sont résolus ;
10. aucun marqueur de secret ou donnée manifestement réelle n'est présent.

Le validateur utilise la bibliothèque standard Python et ne contacte aucun service externe.

## Publication

Une publication formateur suit l'ordre : revue, `make validate`, mise à jour du changelog, création de l'archive, vérification de son empreinte, puis tag immuable. Les repositories consommateurs copient seulement les fichiers dont ils ont besoin et enregistrent l'origine exacte dans leur manifeste d'entrée.
