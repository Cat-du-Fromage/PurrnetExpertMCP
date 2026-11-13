# Workflow D — Predicted gameplay with PurrDiction

**Condition**: check `dev.purrnet.purrdiction` separately from `dev.purrnet.purrnet` and read `references/purrdiction-best-practices.md` (BP-01 to BP-10). Open docs `client-side-prediction/{best-practices,input-handling,state-handling,flow,prediction-policies,views-and-interpolation}.md` according to the tasks; API and version in the local package.

## Phase P0 — Separate input, simulation, state and view

- INPUT `IPredictedData`: `GetFinalInput` by tick; `UpdateInput` for button edges (`GetKeyDown`), `SanitizeInput` on server + client, `ModifyExtrapolatedInput` for one-time events. Do not read Input components in the middle of the replay.
- STATE `IPredictedData<T>`: any mutable state that influences simulation. `GetInitialState`, `GetUnityState` and `SetUnityState` for Unity components to restore.
- `Simulate`/`LateSimulate`: keep ordinary RPCs, analytics, audio, particles and standard Instantiate outside replay. Use predicted time and randomness.
- View: `UpdateView`, `LateUpdateView`, `PredictedEvent` depending on the nature of the presentation, verify when effects run on the confirmed timeline.

## Phase P1 — Topology and Policy

Choose `PredictedIdentity<STATE>` / `<INPUT,STATE>` / `StatelessPredictedIdentity` / `PredictedModule` / `DeterministicIdentity` as required. Instances via `PredictedHierarchy.Create/Delete`, `PredictedObjectID` references, `PredictedParent` and predicted visibility rules. Select FullPrediction / PredictedIfOwned / ServerRelay / SoftCorrection; account for ownership, bots, interactions with historical state and replay cost. NetworkIdentity components are version dependent; do not conclude that there is absolute incompatibility.

## Phase P2 — Minimum integration

Avoid competing writers `NetworkTransform` and `PredictedTransform`, undisposed collections, static modules created conditionally by peer, direct references to objects recreated during rollback. See `references/prediction/real-world-recipes.md`, `prediction/predicted-modules.md`, `prediction/physics-and-collisions.md`.

## Phase P3 — Verify

- **Prove compilation and Inspector settings** PredictionManager, physics providers, predicted prefabs, tick.
- Test A: one-tick input, client/server state, correction and visibility without duplicate audio or UI effects.
- Test B: latency and packet loss, replay, one-shot input stays cleared in extrapolation.
- Test C : projectile / spawn, ownership change, parenting, deletion, pooling, late join.
- Test D: policy fallback/soft correction, out-of-order, tick frequency and different FPS.
- For BP-01 through BP-10, record verified, justified N/A, failed or unverified. Without Unity access, the maximum evidence level is D2.
