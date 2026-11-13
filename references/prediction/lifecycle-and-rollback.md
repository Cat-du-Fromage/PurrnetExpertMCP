# Timeline, hooks, replay, presentations

**Sources** `client-side-prediction/flow.md`, `state-handling.md`, `views-and-interpolation.md`, `predicted-identities.md`, `best-practices.md`.

## Chronologie
Setup / `LateAwake` (initialization view, no deterministic mutations untracked) → preparation INPUT → snapshot pre-stick → `Simulate` → predicted physics → `LateSimulate` → snapshot/network frames → possibly rollback/verified tick/replay → interpolation `UpdateView` then `LateUpdateView`.

- `Simulate` and `LateSimulate` can be called MORE times for the same tick during reconciliation. The invocations must be replayable; do not execute `AudioSource.Play`, particles, `PlayerPrefs`, analytics, HTTP query, files, ordinary RPC.
- For punctual effects: use `PredictedEvent`, `predictionManager.isVerifiedView` or suitable callbacks view; the state simulation should not be ignored during `isCatchingUpFrames`.
- Unity objects mutated during simulation must be captured via `GetUnityState` and restored via `SetUnityState`; otherwise rollback only restores a piece of truth. Physical/transform build-ins have their own bridge.
- The `UpdateView(STATE viewState, STATE? verified)` presentation can be read; inter-identity cameras/IKs in `LateUpdateView` if available in version. `ResetInterpolation()` for teleport.
- `StatelessPredictedIdentity` has different view signatures according to PurrDiction <1.4 and >=1.4; check the version source code.
- Profile: correction rate, length history, forward/after replay position, memory leaks and snap thresholds.

## Anti-pattern
`if (!isCatchingUpFrames) state.ammo--;` = divergence. Instead, mutate ammo always, filter only the shooting visual effect.

## Tests
Client identity without authority, 150ms + jitter, multi-ticks resimulation, frame loss, teleport and reparenting; compare verified and returned statements.
