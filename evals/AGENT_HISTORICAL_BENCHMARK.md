# Benchmark proposé v0.7 — incidents de Stray Help

**Non exécuté** : le pack contient des scénarios et des assertions, pas des résultats de modèle.

Pour mesurer des agents sur le même projet Unity verrouillé et les mêmes logs :

1. 10 prompts explicites (« PurrNet … »), 10 implicites (« mon host double… » dans projet `dev.purrnet.purrnet`) et 10 négatifs (UI Unity seul / FishNet). Fresh session pour chacun, éviter la fuite de contexte.
2. Comparer sans skill vs v0.6 vs v0.7, avec/sans consigne de projet `AGENTS.md`/`CLAUDE.md`.
3. Pour les 22 cas de `evals/v0.7-cases.json`, vérifier : **activation réellement constatée**, lecture des références, identification de la version de l'API, classification datée du bug, hypothèses concurrentes, reproductibilité, pas de recommandation de mise à jour aveugle, tests Unity/exécution.
4. Score manuellement ou via évaluateur extérieur : +1 activation quand attendue, +1 version correcte, +1 bon diagnostic différentiel, +1 APIs vérifiées, +1 test discriminant, -2 patch ancien non vérifié, -2 confusion PurrDiction vs PurrNet, -2 faux positif sur netcode tiers.
5. Les scores s'appuient sur des journaux (références réellement ouvertes) et des builds/testeurs quand possible ; *jamais* sur le seul résultat de `trigger_probe.py` ou `historical_issues.py`.

## Fixtures minimales utiles

- PurrNet release moderne (`packages-lock.json`, package Git commit) avec double `OnSpawned(bool asServer)` mais **sans bug RPC framework**.
- PurrNet version ancienne verrouillée juste avant une correction archive (si elle peut être compilée dans Unity cible) et un test du comportement historique documenté.
- `SyncList` avec ownerOnly et nouvelle scène, avec les trois événements joueur / scene loaded / observer.
- PurrDiction plus ancien que 1.4.0 dans projet utilisant PurrNet core récent.
- Message « Git not found », et cas « Dissonance impossible » : l'agent doit reconnaître le statut obsolète.

Aucun cas réel/Unity n'a encore été exécuté dans ce pack.
