# Niveaux de preuve, checklist et définition du « terminé »

| Niveau | Expression autorisée | Preuve attendue |
| --- | --- | --- |
| P0 | Hypothèse | Code/symbole proposé sans vérification |
| P1 | Documenté | Lien vers doc officielle avec date et version si possible |
| P2 | Code vérifié | Signature ou fichier du package installé / commit précis |
| P3 | Compilation réussie | Unity compile les scripts dans le projet (log ou sortie de build) |
| P4 | Comportement local vérifié | Scène avec host + clone / plusieurs joueurs, résultat observé |
| P5 | Comportement dedicated vérifié | Build serveur headless + deux clients, logs et état monde confirmé |
| P6 | Déploiement vérifié | Hébergement réel et mêmes tests E2E (seulement si demandé) |

Les `assets/unity/*.cs` de ce pack sont **P1/P2 partiel** : inspirés des exemples documentés, **aucun test de compilation Unity** fait ici. Un agent doit les valider dans le projet et ajuster les signatures si nécessaire.

## Tests indispensables selon la fonctionnalité

- `host`: `OnSpawned` déclenché une fois par rôle, aucun double event ou double spawn.
- `client owner`: RPC autorisé et données synchronisées.
- `client non-owner`: accès correctement refusé / état en lecture seule si attendu.
- `dedicated`: le serveur crée son monde sans client local.
- `late join`: état durable reconstruit ; buffer RPC utilisé seulement si approprié.
- `disconnect/reconnect`: aucune fuite/duplication, ownership et scene cohérents.
- `transport`: ports et protocole réels, reconnexion / latence / coupure.
- `security`: requêtes invalides ou spam ne modifient pas l'état sans permission.
- `build`: asmdef, packages, codegen et build cible validés.

Ne jamais transformer une assertion d'`evals/` en « preuve » si le test n'a pas été exécuté.
