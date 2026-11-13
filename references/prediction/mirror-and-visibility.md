# PurrDiction mirror identities and versioned visibility

**Official sources** include `client-side-prediction/built-in-components/predicted-identity-spawner.md`, `client-side-prediction/predicted-visibility.md`, `client-side-prediction/predicted-hierarchy.md` and `client-side-prediction/security.md`.

## Version gate

| PurrDiction version | Documented behavior |
| --- | --- |
| **>= 1.4.0** | A `NetworkIdentity` inside a predicted prefab mirrors automatically. Remove the obsolete `PredictedIdentitySpawner`. |
| **< 1.4.0** | A prefab that needs a `NetworkIdentity` may require the legacy `PredictedIdentitySpawner` bridge. Check the exact installed version and documentation. |
| Missing version or conflicting assemblies | Inspect the package before generating mirroring code. |

Starting in 1.4.0, the predicted world controls the mirror lifecycle.

- The client creates the `NetworkIdentity` after the server verifies the topology. IDs, owners and observers come from the predicted world.
- The mirror follows `PredictedHierarchy` and its pooling. Leave its classic spawn/despawn to the predicted lifecycle. A buffered RPC waits for the observer to be ready.
- Classic spawn and visibility `Network Rules` do not govern manually managed mirrors. Filter visibility on the predicted root.
- Use RPCs and Sync Types on the mirror for data outside replayed gameplay, such as display names, chat or UI interactions. Keep one writer for the simulation.
- Each mirrored projectile or piece of debris adds identity, observer, RPC and sync costs.

## Predicted visibility

- The server calls `predictionManager.HideFrom/ShowTo` for dynamic objects created by the hierarchy system. According to current docs, predicted scene objects have their own lifecycle and this API does not hide them.
- Hiding a root removes its state and inputs from the client. Showing it again acts like a fresh network spawn. Test the view and its caches.
- An owned descendant can force visibility of itself and the ancestors it needs. A parent attached through `PredictedParent` can affect both ancestor and descendant visibility. Test the complete hierarchy.

## Example: predicted avatar with a display name

1. Use `PredictedIdentity<INPUT, STATE>` for movement, stamina and collisions and `PredictedTransform` for corrections.
2. Use a mirror `NetworkIdentity` for the display name if the installed version supports it. Give the predicted component sole responsibility for the pose.
3. Use an authorized Sync Type for the display name outside simulation. Let the predicted world manage ownership and topology.
4. To hide the avatar from a team, have the server call `HideFrom` on the predicted root.
5. Test rejected speculative spawns, corrections, ownership transfer, team changes, late join, pool reuse and destruction.

**Evidence** comes from the documentation. Confirm APIs against the installed version. The prefab example was not compiled in Unity.
