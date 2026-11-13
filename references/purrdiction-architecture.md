# PurrDiction — architecture, cycles, choix et incompatibilités de version

S'appuyer sur **l'ensemble** des pages `client-side-prediction/` dans la copie synchronisée. Source du chemin : https://purrnet.dev/docs/client-side-prediction . Ce document développe les points critiques, pas toute la doc.

## Cycle déterminant

1. Entrée : le contrôleur recueille input dans `GetFinalInput`, capte les fronts entre ticks dans `UpdateInput`, vérifie/normalise par `SanitizeInput`. Les peers et le serveur rejouent des **INPUT historiques**, pas l'Input System live.
2. Tick : PurrDiction sauvegarde avant simulation, exécute `Simulate`, physiques, `LateSimulate`, snapshot puis réseau. Les callbacks peuvent se réexécuter.
3. Réconciliation : réception d'état vérifié, rollback, replay de ticks non vérifiés, correction des composants Unity avec bridge ou composants prédits intégrés.
4. Frame : `UpdateView(viewState, verified)` pour visuels ; `LateUpdateView` pour caméra, IK ou composants dépendant d'autres views. `ResetInterpolation` pour téléportations et erreurs trop importantes.

Sources : `flow.md`, `input-handling.md`, `state-handling.md`, `views-and-interpolation.md`.

## DATA et types

- `PredictedIdentity<INPUT, STATE>` vs `PredictedIdentity<STATE>` selon nécessité d'input. `STATE` doit couvrir toutes les décisions futures. `IPredictedData<STATE>`, math/packing auto ou custom selon version.
- `PredictedModule<STATE>` pour état modulaire, mais coût de snapshots/CPU/traffic additionnel. **Modules statiques créés dans même ordre sur tous les pairs** ; jamais conditionnés à `isServer` ou `isOwner`, sinon `PredictedModuleRosterMismatchException` et réplication suspendue. **Modules dynamiques** pendant simulation, recréables par constructeur public `(PredictedIdentity, autres paramètres optionnels)` ; configuration influant gameplay doit appartenir à l'état et non à ces paramètres.
- `DeterministicIdentity` pour bit-à-bit strict avec `sfloat`, policies/desync séparées ; `SimulationStart` sur la timeline (pas mutations dans Awake). Ne pas confondre avec le rollback physique Unity.

Sources : `predicted-identities.md`, `predicted-modules/README.md`, `deterministic-identity.md`.

## Politiques (vérifier la version)

| Policy | Timelines | Recommandation |
| --- | --- | --- |
| FullPrediction | tick futur local + rollback des vérifiés | interactions critiques exactes |
| PredictedIfOwned | full owner / relay non-owner | acteurs contrôlés |
| ServerRelay | ticks vérifiés, derrière la latence | objets pilotés serveur |
| SoftCorrection | correction convergente sans replay du vivant | prop/cosmétique *si supporté* |
| PredictedIfOwnedWithSoftFallback | owner full / autres soft sinon relay | selon version/composant |

Ne pas utiliser `SoftCorrection` sur hit validation. Un fallback automatique sans erreur peut masquer une hypothèse erronée. `PredictionPolicyScope`, `SetPredictionPolicy`, `SetPredictionPolicyOverride`, `UsePredictionPolicyScope` ont des durées différentes ; tester transfert de propriété et pooling.

## Spawn, hierarchy, references

- `predictionManager.hierarchy.Create/Delete` et ID au lieu de `Instantiate/Destroy` en simulation. Pièces d'un prefab peuvent être parentes, enfants, déplacées ou supprimées ; topologie se restaure pendant replay. `TryCreateAndGet` n'assure une référence que dans le tick courant.
- `PredictedObjectID` pour objet, `PredictedComponentID` pour identité spécifique ; lookup après rollback peut retourner `false`.
- Mirroring de `NetworkIdentity` **>=1.4.0** : automatique dans prefab prédit, server-driven/verified, hors spawn et visibilité classiques PurrNet, ownership conforme à topologie prédite ; pour UI/chat/nom, pas gameplay prédictible. `PredictedIdentitySpawner` ancien est obsolète en >=1.4.0 ; sur version antérieure se référer à la page versionnée.

Sources : `predicted-hierarchy.md`, `predicted-object-references.md`, `built-in-components/predicted-identity-spawner.md`.

## Physics, events, lag compensation

- `PredictedTransform`, `PredictedRigidbody`, `PredictedRigidbody2D` : pipeline physique rollback et view ; ne pas superposer NetworkTransform sur le même transform.
- `PredictedEvent` ou view verified pour effets uniques. Contacts/callbacks physiques temporaires ne pas conserver entre ticks.
- Lag compensation avec `ColliderRollback`, `predictionManager.lagCompensation` et `lagCompensationTick` depuis `Simulate`, **>=1.4.0** selon doc consultée ; `rollbackTick` du networking traditionnel désigne autre chose. Max Lag Compensation Seconds borne l'offset client, serveur fait le hit test.
- Pooled collections deep-copy, `Dispose`, `IDuplicate<T>` ; pas de double dispose.

Sources : `predicted-physics-callbacks.md`, `built-in-components/predicted-transform.md`, `built-in-components/predicted-rigidbody-2d-and-3d.md`, `lag-compensation.md`, `disposable-collections.md`.

## Points d'attention d'implémentation

- `PredictionManager` par scène, `PredictionPolicyScope` / configs par objet ; scènes/additive, visibilité, propriété, interpolation et det. exigeant vérification contextuelle.
- Input réseau de petite taille, front d'action consommé une fois, extrapolation prudente. Ne pas forcer `Repeat Input Factor` énorme pour cacher les corrections.
- Documentation `main` peut mentionner des systèmes plus récents que la version de package. Inspecter `package.json` exact (PurrDiction) et sources locales avant snippet ; ne pas « mettre à jour » un package automatiquement sans permission.
