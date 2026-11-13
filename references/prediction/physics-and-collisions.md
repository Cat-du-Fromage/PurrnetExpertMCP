# Physics prédite, collisions, projectiles

**Sources** `client-side-prediction/built-in-components/predicted-transform.md`, `predicted-rigidbody-2d-and-3d.md`, `predicted-physics-callbacks.md`, `predicted-projectile-3d.md`, `predicted-parent.md`, `client-side-prediction/lag-compensation.md`.

- Utiliser `PredictedTransform` pour pose, `PredictedRigidbody` ou `PredictedRigidbody2D` pour physique; ne pas ajouter `NetworkTransform` qui écrirait le même état et provoquerait une lutte entre systèmes.
- `PredictedPhysicsCallbacks` fournit des collisions/triggers rollback-aware, y compris CharacterController/colliders cinématiques **sans** `PredictedRigidbody`; activer les providers Physics du Prediction Manager compatibles avec le projet.
- À partir des versions documentées >=1.4, utiliser `onPredictedCollisionEnter/Exit/Stay` et `onPredictedTriggerEnter/Exit/Stay`, avec les payloads `otherId` stables; les événements GameObject-only historiques sont obsolètes et peuvent manquer les exits déclenchés par deletion.
- Ne pas conserver un contact/collision list temporaire hors callback. Les callbacks de physique peuvent être rejoués : gameplay dans STATE, effets physiques/son visuels filtrés en view/verified events.
- `PredictedProjectile3D` requiert `PredictedTransform`, pas un Rigidbody/Collider; ses sphere casts, gravité, event mask et collision layers ont un coût et des contraintes; `AddImpulse` depuis simulation seulement. Ne pas supposer même API en version ancienne.
- Pour hitscan voir `lag-compensation.md` : utiliser history serveur avec `lagCompensationTick` au lieu d'accepter les hits du client.

## Test
Deux clients avec vitesses différentes, low/high tick, 2D/3D selon projet, touch/exit pendant delete, collisions pendant resim, projectile fast, téléports et pool.
