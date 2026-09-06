# Exemples et contre-exemples

| Invariant | Exemple valide | Contre-exemple | Résultat attendu |
|---|---|---|---|
| Capacité | La deuxième inscription d'une session de capacité 2 est acceptée | Une troisième inscription active est tentée | refus atomique, y compris en concurrence grâce au verrou de session |
| Unicité | Un participant suit deux sessions différentes | Deux acheteurs inscrivent le même participant à la même session | refus par unicité du couple session/participant |
| Prix historique | Une ligne accepte 42 000 centimes, puis le tarif passe à 47 000 | Une ancienne commande est recalculée avec le tarif actuel | ligne inchangée à 42 000 et mise à jour directe interdite après confirmation |
| Financement | Une organisation achète pour un participant rattaché | L'organisation est déduite comme propriétaire définitif du participant | acheteur, bénéficiaire et rattachement restent séparés |
| Paiement incertain | `UNKNOWN` attend une réconciliation | Une inscription est confirmée dès le timeout | aucune confirmation prématurée |

Les identifiants et montants sont synthétiques. Ces exemples décrivent des faits à préserver, sans imposer leur forme dans un futur modèle de domaine.
