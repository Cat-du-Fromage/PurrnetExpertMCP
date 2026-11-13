# Contrat obligatoire PurrDiction (BP-01 à BP-10)

**Source** `client-side-prediction/best-practices.md` (clone local recommandé). **Lecture obligatoire** avec `references/purrdiction-best-practices.md` AVANT tout changement à la simulation. Ce document sert de routeur; la synthèse longue v0.3 reste normative dans la skill mais n'est pas une substitution à la doc du commit installé.

| BP | Exigence | Guide d'exécution / tests |
|---|---|---|
| 01 | Tout état mutable affectant futur tick est dans STATE | `input-and-state.md`, `lifecycle-and-rollback.md` |
| 02 | GetInitialState, GetUnityState, SetUnityState pour état Unity | `lifecycle-and-rollback.md` |
| 03 | Simulate/LateSimulate rejouables, effets différés | `lifecycle-and-rollback.md` |
| 04 | Pas de RPC/SyncVar/Instantiate/NetworkTransform au cœur du gameplay prédit | `hierarchy-and-parenting.md`, `visibility-and-interactions.md` |
| 05 | Delta/tick/RNG prédits, pas Time/Random classiques | `deterministic-identity.md` |
| 06 | Input capturé, sanitize, extrapolation edges effacés, serveur valide | `input-and-state.md`, `security.md` |
| 07 | FullPrediction / PredictedIfOwned / ServerRelay / SoftCorrection selon rôle | `prediction-policies.md` |
| 08 | Disposable buffers et snapshots copiés en profondeur | `memory-and-pooling.md` |
| 09 | Références PredictedObjectID/PredictedComponentID stables | `hierarchy-and-parenting.md` |
| 10 | Host, remote, dédié, pertes, rollback, pooling, teleports, late join | `references/purrdiction-test-matrix.md` |

**Nuance** : hors simulation, un RPC sur NetworkIdentity/mirror peut envoyer une demande au serveur. La création de predicted objects dans un tel ServerRpc est *server-driven* (latence) et ne doit pas être décrite comme prédite localement. Si version <1.4, vérifier bridge `PredictedIdentitySpawner` ; >=1.4 mirror automatique (voir source exacte).

Pour chaque réponse contenant du code de prédiction, produire BP-01...BP-10 : conforme prouvé / N/A motivé / non vérifié / défaut. Ne pas appeler le résultat « validé » si pas de compilation Unity ni de test rollback.
