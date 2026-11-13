# Politiques et scopes de prédiction

**Source** `client-side-prediction/prediction-policies.md`, `views-and-interpolation.md`, `flow.md`.

| Policy | Client | Bon cas | Danger |
|---|---|---|---|
| `FullPrediction` | Simule+rollback/replay | Local gameplay avec interactions exactes | Coût CPU/history |
| `PredictedIfOwned` | Full pour owner, ServerRelay pour remote | Pawn, véhicule | Remote plus en retard |
| `ServerRelay` | Suit ticks vérifiés, sans futur spéculatif | Hazards, serveur/remote | Latence visible |
| `SoftCorrection` | Simule et converge sans rollback live | Débris, props non critiques | État pas historiquement identique |
| `PredictedIfOwnedWithSoftFallback` | Full owner, soft remote si support | Remote acteurs plus fluides | Fallback ServerRelay possible |

- `SoftCorrection` pris en charge par composants vérifiés (PredictedTransform, PredictedRigidbody 2D/3D, PredictedProjectile3D); certains autres, et `DeterministicIdentity`, retournent **silencieusement** à ServerRelay sur clients. Ne pas le choisir pour gameplay collidable critique.
- `PredictionPolicyScope` s'applique aux descendants; scopes enfants, héritage, overrides, changement d'owner peuvent recalculer la policy.
- `identity.SetPredictionPolicy` ne change que l'appliquée (scope futur peut écraser). `identity.SetPredictionPolicyOverride` définit l'override persistant. `identity.UsePredictionPolicyScope` retire override et re-résout le scope. Les versions doivent être vérifiées dans la source.
- Éviter les changements de policy au milieu d'une phase critique; valider reconciliation après ownership change et reuse du pool.
- Ne pas employer une soft correction pour cacher des mutations non déterministes; d'abord corriger STATE/simulation.

## Tests
Local vs remote player, ragdoll, projectile hitbox, changement d'owner, reparenting sous policy scope, pooling, unsupported soft fallback, network jitter.
