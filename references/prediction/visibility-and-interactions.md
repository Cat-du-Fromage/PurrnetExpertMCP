# Predicted visibility and identity interactions

**Sources** `client-side-prediction/predicted-visibility.md` (>=1.3.0), `multi-identity-interactions.md`, `predicted-state-machine/README.md`, `predicted-state-machine/predicted-state-node.md`, `built-in-components/predicted-parent.md`.

## Visibility
- The predicted visibility is **distinct from Network Visibility** classical. The calls `predictionManager.HideFrom/ShowTo` concern **dynamic objects created via hierarchy** and are applied **only by the server**. The predicted stage objects can always be visible (see version).
- Visibility applies to complete roots, not just one piece; attached objects can cause ancestor visibility, and owned objects can benefit from special rules. Hide can completely remove an object from the client world and interrupt status/input; not just disable Renderer.
- When a NetworkIdentity is mirrored in prefab predicted (>=1.4), its visibility and owner follow the predicted world, not the normal Network Visibility assembly.

## Multiple identities
- Store Stable IDs in STATE, lookup at playback time, mutation only during simulation; `[SimulationOnly]` possible according to installed source. Do not mutate an identity from a rendering callback or MonoBehaviour by ignoring timeline.
- `PredictedEvent` filter presentation/one shots, **is neither RPC nor network transcript**; all peers must be able to generate the occurrence in the simulation, and the STATE mutation must remain replayable.
- `PredictedStateNode`/state machine: state of movement/combat with predicted state (check hooks/active node and transitions according to version). Do not mix state classic UI machine and predicted timeline.
- `PredictedPlayers`: check APIs and events in the package; when deterministic initialization use events called on the simulated timeline.

## Tests
Two teams, fog of war, child object attached, owner, late join, collision between identities, dynamic states, and cross-client observation limits.
