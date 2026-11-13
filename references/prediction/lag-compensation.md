# Lag compensation and hit validation

**Sources** `client-side-prediction/lag-compensation.md` (frontmatter >=1.4.0), `systems-and-modules/collider-rollback.md`, `client-side-prediction/security.md`.

- Two different paths: PurrNet classic can use `rollbackTick` of NetworkIdentity and RPC + `RollbackModule`, while PurrDiction >=1.4 provides `lagCompensationTick` **in `Simulate`** and `predictionManager.lagCompensation` (Raycast/CircleCast/etc.). Do not confuse the tick spaces.
- Interesting targets must have `ColliderRollback`; the system records their history. The server uses its own history and bounds the offset requested via `Max Lag Compensation Seconds` (documented failure 0.15s in some versions).
- The attack input contains the intention (`fire`), not a "I touched this enemy for 80 damage"; result from the predictable raycast + server validation in STATE. The input does not send `rollbackTick` for the modern PurrDiction path.
- `Forward View Offsets` facilitates matching results on remote clients at additional bandwidth cost; choose according to gameplay.
- Avoid the raycast making an audio/analytic effect on each replay; use filtered events/views.

## Tests
High latency shooting on moving target, false offset, hidden target, despawn target before impact, modified client, 2D and 3D Hitscan, late join.
