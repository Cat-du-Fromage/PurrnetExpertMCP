# Predictive policies and scopes

**Source** `client-side-prediction/prediction-policies.md`, `views-and-interpolation.md`, `flow.md`.

| Policy | Client | Good case | Danger |
|---|---|---|---|
| `FullPrediction` | Simule+rollback/replay | Local gameplay with exact interactions | Cost CPU/history |
| `PredictedIfOwned` | Full for owner, ServerRelay for remote | Pawn, vehicle | Remote more late |
| `ServerRelay` | Follow verified ticks without predicting ahead | Hazards and remote server-driven objects | Visible latency |
| `SoftCorrection` | Simulate and converge without live rollback | Debris, non-critical props | State not historically identical |
| `PredictedIfOwnedWithSoftFallback` | Full owner, soft remote si support | Remote more fluid actors | Fallback ServerRelay possible |

- `SoftCorrection` supported by verified components (PredictedTransform, PredictedRigidbody 2D/3D, PredictedProjectile3D); some others, and `DeterministicIdentity`, return **silently** to ServerRelay on clients. Do not choose it for collidable gameplay critical.
- `PredictionPolicyScope` applies to descendants; children's scopes, inheritance, overrides, change of owner can recalculate policy.
- `identity.SetPredictionPolicy` only changes the application (future scope can overwrite). `identity.SetPredictionPolicyOverride` defines the persistent override. `identity.UsePredictionPolicyScope` removes override and re-resolves thescope. Versions must be checked in the source.
- Avoid changes in policy in the middle of a critical phase; validate reconciliation after ownership changes and uses the pool.
- Do not use a soft correction to hide non-deterministic mutations; first correct STATE/simulation.

## Tests
Local vs remote player, ragdoll, projectile hitbox, change of ownership, reparenting under policy scope, pooling, unsupported soft fallback, network jitter.
