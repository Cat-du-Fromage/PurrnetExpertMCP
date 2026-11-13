# PredictedHierarchy: authority, ID, creating and parenting

Official: `client-side-prediction/{predicted-hierarchy.md,predicted-object-references.md,predicted-visibility.md}`, `built-in-components/{predicted-parent.md,predicted-identity-spawner.md}`.

- Use `predictionManager.hierarchy.Create/Delete` in the simulated timeline for predicted prefabs. Every piece with a PredictedIdentity has a stable `PredictedObjectID`; use `PredictedComponentID` for a specific predicted component.
- Client-side `Create` outside simulation can appear briefly then disappear on server reconciliation; it is only a guess. For responsive creates: express action as replayable INPUT, validate server authoritative state and execute Create in Simulate. Documented advice: counters are safer for fire/spawn events than bools that repeat or vanish under extrapolation.
- When immediate response is unimportant, UI can request a server `ServerRpc` **outside Simulate**, which performs authoritative Create and clients learn through state; this is not prohibited by Best Practices.
- Avoid saving raw GameObject/Transform/component pointers in STATE; objects may be recreated/pool swapped. `TryCreateAndGet` component is immediate-use, retain ID for future ticks.
- `PredictedParent` is required when reparenting affects rollback state. Parent directly to a registered predicted piece for portable results; plain nested transform is view-only/local attachment.
- For reversible enable/disable prefer `PredictedGameObject.SetActive` when appropriate, not full Delete/Recreate.
- Predicted visibility is **server-controlled**, separate from classic Network Visibility; scene predicted objects have different visibility behavior. Test fog-of-war, inheritance of attached instances, owner guarantees.
- `NetworkIdentity` mirrored into predicted prefab changes at PurrDiction 1.4.0; older `PredictedIdentitySpawner` may be needed, newer version uses automatic mirroring and marks that component obsolete. Never guess from a tutorial.

End-to-end tests: remote predicted spawn, server reject, rollback rollback-delete/recreate, pool reuse, late join and owning change; verify exact IDs and no leaked classic identity.
