# PurrDiction — architecture, cycles, choice and version incompatibilities

Rely on **the set** of the `client-side-prediction/` pages in the synchronized copy. Path Source: https://purrnet.dev/docs/client-side-prediction . This document develops the critical points, not the entire doc.

## Determining cycle

1. Input: The controller collects input in `GetFinalInput`, captures the fronts between ticks in `UpdateInput`, checks/normalizes by `SanitizeInput`. Peers and the server replays historical **INPUT**, not the Input System live.
2. Tick: PurrDiction backup before simulation, executes `Simulate`, physics, `LateSimulate`, snapshot and then network. Callbacks can run again.
3. Reconciliation: verified status reception, rollback, unverified tick replay, correction of Unity components with built-in bridge or predicted components.
4. Frame: `UpdateView(viewState, verified)` for visuals; `LateUpdateView` for camera, IK or components dependent on other views. `ResetInterpolation` for teleports and errors too big.

Sources : `flow.md`, `input-handling.md`, `state-handling.md`, `views-and-interpolation.md`.

## DATA and types

- `PredictedIdentity<INPUT, STATE>` vs `PredictedIdentity<STATE>` depending on input requirement. `STATE` should cover all future decisions. `IPredictedData<STATE>`, math/packing auto or custom depending on version.
- `PredictedModule<STATE>` for modular state, but additional snapshot/CPU/traffic cost. **Static models created in the same order on all peers**; never conditioned to `isServer` or `isOwner`, otherwise `PredictedModuleRosterMismatchException` and suspended replication. **Dynamic models** during simulation, re-createable by public constructor `(PredictedIdentity, other optional parameters)`; influent gameplay configuration must belong to the state and not to these parameters.
- `DeterministicIdentity` for strict bit-to-bit with `sfloat`, separate policies/desync; `SimulationStart` on the timeline (not mutations in Awake). Do not confuse with physical rollback Unity.

Sources : `predicted-identities.md`, `predicted-modules/README.md`, `deterministic-identity.md`.

## Policies (check version)

| Policy | Timelines | Recommandation |
| --- | --- | --- |
| FullPrediction | local future tick + checked rollback | interactions critiques exactes |
| PredictedIfOwned | full owner / relay non-owner | Controlled actors |
| ServerRelay | ticks checked, behind latency | server controlled objects |
| SoftCorrection | convergent correction without replay of the living | prop/cosmetic *if supported* |
| PredictedIfOwnedWithSoftFallback | owner full / other soft otherwise relay | according to version/component |

Do not use `SoftCorrection` on hit validation. An error-free automatic fallback can mask an erroneous hypothesis. `PredictionPolicyScope`, `SetPredictionPolicy`, `SetPredictionPolicyOverride`, `UsePredictionPolicyScope` have different durations; test ownership transfer and pooling.

## Spawn, hierarchy, references

- `predictionManager.hierarchy.Create/Delete` and ID instead of `Instantiate/Destroy` in simulation. Parts of a prefab can be parent, child, moved or deleted; topology is restored during replay. `TryCreateAndGet` only provides a reference in the current tick.
- `PredictedObjectID` for object, `PredictedComponentID` for specific identity; lookup after rollback can return `false`.
- `NetworkIdentity` Mirroring **>=1.4.0**: automatic in prefab predicted, server-driven/verified, out of spawn and classic visibility PurrNet, ownership according to predicted topology; for UI/chat/name, not predictable gameplay. `PredictedIdentitySpawner` old is obsolete in >=1.4.0; on earlier version refer to versioned page.

Sources : `predicted-hierarchy.md`, `predicted-object-references.md`, `built-in-components/predicted-identity-spawner.md`.

## Physics, events, lag compensation

- `PredictedTransform`, `PredictedRigidbody`, `PredictedRigidbody2D`: Rollback physical pipeline and view; do not overlay NetworkTransform on the same transform.
- `PredictedEvent` or view verified for unique effects. Temporary physical contacts/callbacks do not store between ticks.
- Lag compensation with `ColliderRollback`, `predictionManager.lagCompensation` and `lagCompensationTick` from `Simulate`, **>=1.4.0** according to doc consulted; `rollbackTick` traditional networking means something else. Max Lag Compensation Seconds terminal the client offset, server does the hit test.
- Pooled collections deep-copy, `Dispose`, `IDuplicate<T>`; no double has.

Sources : `predicted-physics-callbacks.md`, `built-in-components/predicted-transform.md`, `built-in-components/predicted-rigidbody-2d-and-3d.md`, `lag-compensation.md`, `disposable-collections.md`.

## Implementation Attention Points

- `PredictionManager` per scene, `PredictionPolicyScope` / configs per object; scenes/additive, visibility, property, interpolation and det. demanding contextual verification.
- Small network input, once consumed action front, cautious extrapolation. Do not force `Repeat Input Factor` huge to hide corrections.
- Documentation `main` may mention more recent systems than the package version. Inspect `package.json` exact (PurrDiction) and local sources before snippet; do not "update" a package automatically without permission.
