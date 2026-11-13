# Predicted physics, collisions, projectiles

**Sources** `client-side-prediction/built-in-components/predicted-transform.md`, `predicted-rigidbody-2d-and-3d.md`, `predicted-physics-callbacks.md`, `predicted-projectile-3d.md`, `predicted-parent.md`, `client-side-prediction/lag-compensation.md`.

- Use `PredictedTransform` for installation, `PredictedRigidbody` or `PredictedRigidbody2D` for physics; do not add `NetworkTransform` that would write the same state and cause a struggle between systems.
- `PredictedPhysicsCallbacks` provides rollback-aware collisions/triggers, including CharacterController/Cinetics Colliders **without** `PredictedRigidbody`; activate the Prediction Manager's Physics providers compatible with the project.
- From documented versions >=1.4, use `onPredictedCollisionEnter/Exit/Stay` and `onPredictedTriggerEnter/Exit/Stay`, with stable `otherId` payloads; historical GameObject-only events are obsolete and may miss exits triggered by deletion.
- Do not keep a contact/collision temporary list out of callback. Physics callbacks can be replayed: gameplay in STATE, visual physical/physical effects filtered in view/verified events.
- `PredictedProjectile3D` requires `PredictedTransform`, not a Rigidbody/Collider; its casts, gravity, event mask and collision layers have cost and constraints; `AddImpulse` since simulation only. Do not even assume API in old version.
- For hitscan see `lag-compensation.md`: use server history with `lagCompensationTick` instead of accepting client hits.

## Test
Two clients with different speeds, low/high tick, 2D/3D depending on project, touch/exit during delete, collisions during resim, fast projectile, teleports and pool.
