# PredictedHierarchy, parts, spawn and PredictedParent

**Sources** `client-side-prediction/predicted-hierarchy.md`, `predicted-object-references.md`, `built-in-components/predicted-parent.md`, `built-in-components/predicted-identity-spawner.md`, `best-practices.md`.

- Predicted world creates/destructs parts with `predictionManager.hierarchy.Create/Delete`; `Instantiate`/`Destroy` classic in simulation create non-synchronized objects with rollback.
- A **piece** is a GameObject equipped with a `PredictedIdentity` within the prefab; a root can contain several parts. The IDs are `PredictedObjectID` or `PredictedComponentID`; store these IDs in STATE, **not** a GameObject reference/Transform between ticks, then solve to the use tick.
- The client creation that must be immediate must be caused by INPUT in `Simulate` to be executed also on the server; a simple IU click that calls `hierarchy.Create` on the client side can disappear at the next check. For one-shot action sensitive to repeat packages, consider action counter, rather than a constantly true boolean.
- Alternative **accepted**: the UI button requests via a ServerRpc on an authorized NetworkIdentity, the server creates the predicted object; no client-side prediction, appearance after RTT. Never send this RPC from each `Simulate` replay.
- `PredictedGameObject.SetActive` useful for reversible toggle; `Delete` performs a true part removal.
- To repair gameplay, add **`PredictedParent`** to the room. The attachment occurs during the simulation and is recorded in state, restored during rollback and sent to the late join. Without component, changing parent is purely a local decoration at best; parent under Imbricated Transform non-part not replicated identically.
- Prefabs predicted with `NetworkIdentity` for cat/IU: **>=1.4** mirror automatically, do not add obsolete `PredictedIdentitySpawner`; **<1.4** bridge distinct. Mirror follows the verified world, not speculative spawn, and visibility/ownership mirror derive from prediction, not ordinary Network Rules.

## Tests
Spawn client then reject server, projectile pool rollback, parent destroyed/recreated, repair cross-prefab, owner transfer, scene reload, late join and hidden visibility.
