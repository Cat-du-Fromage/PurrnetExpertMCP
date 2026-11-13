# NetworkTransform: pose, authority, interpolation

Official: `plug-n-play-components/network-transform.md` and `plug-n-play-components/network-transform/adaptive-sync.md`.

## Decision
- Use **NetworkTransform** for classic PurrNet `NetworkIdentity` pose (position/rotation/scale and optionally parent). For physics-driven pose choose **NetworkRigidbody** (2D/3D), and for PurrDiction choose **PredictedTransform** / **PredictedRigidbody** instead. Do not let two components simultaneously control one transform.
- Inspector: select **Owner Auth** deliberately (true: controlling owner; false: server). Align with Network Rules and validation. Select local vs world position/rotation; `Sync Parent` only supports an appropriate `NetworkIdentity` parent.
- Choose interpolation timing phase matching movement consumers. Tune min/max buffer with latency/jitter; extra buffer reduces jitter but introduces view latency. Avoid a second CharacterController.Move on observer peers.
- Character Controller Patch has changed on `dev`: older variants can toggle controllers and cause repeated trigger callbacks; re-check package implementation before claiming fix.

## Adaptive sync
- Enabled by default in current docs. It preserves simulation tick rate while skipping reconstructible sends; erratic motion falls back to regular syncing. Built-in max update interval ~0.3 s in documented implementation.
- `networkTransform.adaptiveSync = true/false` enables/disables; `networkTransform.hasSyncStrategy` indicates strategy; `SetSyncStrategy(...)` accepts custom `NetworkTransformSyncStrategy`, `null` resets to built-in.
- Custom strategy requires verified override `TryReconstruct` signature from installed source. Use custom strategy only after profiler evidence.

## Verify
1. Host, remote 2 clients, late join: pose and parent agree.
2. Authority: non-controller cannot drive authoritative pose through this component.
3. 100ms latency + jitter/loss: motion fluid, no stale drift, buffer latency acceptable.
4. Compare adaptive sync on/off in bandwidth profiler and report numbers.
