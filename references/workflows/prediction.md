# Workflow D — Gameplay prédit et PurrDiction

**Précondition** : vérifier `dev.purrnet.purrdiction` séparément de `dev.purrnet.purrnet` et lire obligatoirement `references/purrdiction-best-practices.md` (BP-01 à BP-10). Ouvrir docs `client-side-prediction/{best-practices,input-handling,state-handling,flow,prediction-policies,views-and-interpolation}.md` selon les tâches ; API et version dans le package local.

## Phase P0 — Séparer entrée, simulation, état et vue

- INPUT `IPredictedData` : `GetFinalInput` par tick ; `UpdateInput` pour fronts (`GetKeyDown`), `SanitizeInput` sur serveur + client, `ModifyExtrapolatedInput` pour événements ponctuels. Ne pas lire les composants d'Input au milieu du replay.
- STATE `IPredictedData<T>` : tout état mutable qui influence la simulation. `GetInitialState`, `GetUnityState` et `SetUnityState` pour les composants Unity à restaurer.
- `Simulate`/`LateSimulate` : purs du point de vue des effets non rejouables ; pas de RPC, analytics, audio, particules/Instantiate standard, Time/Random Unity direct.
- View : `UpdateView`, `LateUpdateView`, `PredictedEvent` selon nature de la présentation, vérifier apparition des événements sur timeline vérifiée.

## Phase P1 — Topologie et politiques

Choisir `PredictedIdentity<STATE>` / `<INPUT,STATE>` / `StatelessPredictedIdentity` / `PredictedModule` / `DeterministicIdentity` selon besoin. Instances via `PredictedHierarchy.Create/Delete`, références `PredictedObjectID`, `PredictedParent` et règles de visibilité prédites. Sélectionner FullPrediction / PredictedIfOwned / ServerRelay / SoftCorrection ; justifier owner, bots, interactions historiques et coût de replays. Les composants NetworkIdentity miroirs dépendent de la version ; ne pas conclure à une incompatibilité absolue.

## Phase P2 — Intégration minimale

Éviter le double writer `NetworkTransform` et `PredictedTransform`, les collections non disposées, les modules statiques créés de façon conditionnelle par peer, les références directes à des objets recréés en rollback. Voir `references/prediction/real-world-recipes.md`, `prediction/predicted-modules.md`, `prediction/physics-and-collisions.md`.

## Phase P3 — Prouver

- **Prouver la compilation et les Inspector settings** PredictionManager, providers physics, predicted prefabs, tick.
- Test A : input 1 tick, état client vs serveur, corrected state, visibilité sans double effet audio/UI.
- Test B : latence et perte de paquets, replay, extrapolation d'input ponctuel non répétée.
- Test C : projectile / spawn, ownership change, parentage, suppression, pooling, late join.
- Test D : policy fallback/soft correction, out-of-order, fréquence de tick et FPS différents.
- Statuer chaque BP-01..BP-10 : OK démontré / N/A justifié / défaut / non vérifié. Si aucun Unity accessible, s'arrêter au niveau de preuve D2 au maximum.
