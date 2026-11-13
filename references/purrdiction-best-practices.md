# PurrDiction Best Practices

**Primary source** is the [official Best Practices page](https://purrnet.dev/docs/client-side-prediction/best-practices), also available in [PurrDocs](https://github.com/PurrNet/PurrDocs/blob/main/client-side-prediction/best-practices.md). Read the synchronized page at `references/cache/official-docs/client-side-prediction/best-practices.md` and verify symbols against the installed version. The checks below summarize and apply the official guidance.

## BP-01 — Store everything that affects future simulation in STATE

- Use struct `INPUT` and `STATE` with the relevant `IPredictedData` interfaces, including `IPredictedData<STATE>` for state. Implement `Dispose()` and check the version's packing and math contracts.
- Include position, velocity, rotation, cooldowns, ammo, gameplay or animation modes, combo counters, targets, RNG and stable IDs in STATE. Capture mutable Inspector settings that affect later ticks in STATE or change them through a predicted operation.
- Return a complete snapshot from `GetInitialState`. Use `GetUnityState(ref STATE)` and `SetUnityState(STATE)` when Unity components such as Transform or Rigidbody own part of the state. Check how built-in components already do this.
- Check `IMath<T>` and `Interpolate` for quaternions and nonlinear state. Keep presentation-only fields outside STATE.
- List each value mutated by simulation and show where it is captured or restored.

## BP-02 — Initialize and restore Unity state explicitly

- Keep predicted state changes on the timeline. For `DeterministicIdentity`, use simulation initialization such as `SimulationStart` for state that would otherwise depend on peer-specific `Awake`, `Update` or `OnEnable` callbacks.
- Ensure physics reads and writes can be restored. Unity physics can support rollback without guaranteeing bit-identical results across platforms.
- Verify each component that affects a future tick returns to the expected state after correction.

## BP-03 — Keep Simulate and LateSimulate replay-safe

- Keep irreversible effects out of replayed simulation, including audio, particles, achievements, saves, analytics, HTTP, currency changes, notifications and ordinary RPCs.
- Verify `PredictedEvent`, view callbacks such as `UpdateView` and `LateUpdateView`, or `predictionManager.isVerifiedView` for one-shot effects. Make server rewards idempotent.
- Preserve deterministic mutations during catch-up. Skipping them based on `isCatchingUpFrames` changes the replay result.
- Replay the same tick and check that rewards, external costs, RPCs and effects are not duplicated.

## BP-04 — Use one object model for predicted gameplay

| Classic mechanism | Predicted gameplay equivalent |
| --- | --- |
| `[ServerRpc]`, `[ObserversRpc]`, `[TargetRpc]` to change gameplay | Simulate actions from `INPUT` and restore `STATE` |
| `SyncVar`, `SyncList` and other Sync Types | Predicted `STATE` fields |
| `Instantiate` and `Destroy` for predicted objects | `predictionManager.hierarchy.Create/Delete` and stable IDs |
| Classic `NetworkTransform` or `NetworkRigidbody` writing the same state | `PredictedTransform`, `PredictedRigidbody` or `PredictedRigidbody2D` |
| `NetworkAnimator` for the same simulation | Drive `Animator` from `UpdateView` |
| `GameObject`, `Transform`, `PredictedIdentity` references in INPUT or STATE | `PredictedObjectID` or `PredictedComponentID`, resolved at use |

Use classic RPCs and Sync Types on a separate or mirrored `NetworkIdentity` for chat, lobby and display names. Starting with PurrDiction 1.4.0, identities inside predicted prefabs mirror automatically and follow predicted topology and visibility. Classic spawn and visibility rules do not govern the mirror. Earlier versions use the distinct `PredictedIdentitySpawner` mechanism. Confirm the version before choosing a mechanism.

## BP-05 — Use predicted time and randomness

- Use callback `delta`, `PredictedTime` and a replayable `PredictedRandom` stream. Check the installed API.
- Keep `Time.deltaTime`, `Time.time`, `Time.frameCount`, `DateTime.Now`, `Stopwatch` and `UnityEngine.Random` out of gameplay ticks.
- Use `DeterministicIdentity`, `sfloat` or fixed-point math for stronger determinism. Test separately from classic Unity physics.

## BP-06 — Validate INPUT on the server

- Verify how `GetFinalInput(ref INPUT)` provides tick input. Capture one-shot edges in `UpdateInput(ref INPUT)` so a press between ticks is retained. Simulate from recorded INPUT.
- Use `SanitizeInput(ref INPUT)` to clamp movement, aim and sizes and reject non-finite values. Validate cooldown, range, ammo, stamina, permissions, rate and hits against authoritative state.
- Remove one-shots such as jump, fire, interact and purchase in `ModifyExtrapolatedInput(ref INPUT)`. Tune Repeat Input Factor against actual loss. Too little repetition can stall remote players and too much can cause overshoot and snaps.
- The server remains responsible for authoritative positions and damage under every prediction policy.

## BP-07 — Choose the least expensive policy that preserves correctness

- `FullPrediction` supports critical interactions and exact rollback at higher replay cost.
- `PredictedIfOwned` predicts for the owner and relays to remote peers. Consider it for a player or vehicle with noncritical remote interactions.
- `ServerRelay` follows verified server state with latency.
- `SoftCorrection` converges on supported noncritical objects. Unsupported objects can fall back to `ServerRelay`. Investigate simulation defects directly.
- Check whether `PredictedIfOwnedWithSoftFallback` exists in the installed version and how it selects soft correction or relay for non-owners.
- Verify policy scope, overrides, ownership changes and pool reuse.

## BP-08 — Manage snapshot memory

- Create and dispose `DisposableList<T>`, `DisposableDictionary<K,V>` and `DisposableArray<T>` according to ownership. Dispose owned state in `STATE.Dispose`.
- A shallow struct copy shares owned buffers. Use `Duplicate` and implement `IDuplicate<T>` for composite state. Use `IEquatable<T>` when comparison is expensive or ambiguous.
- Release `CollisionContactList` and other temporary contacts according to the version's callback contract. Keep them within callback lifetime.
- Test snapshots, cleanup, resimulation and pooling for leaks, double disposal and mutations of earlier snapshots.

## BP-09 — Use stable predicted IDs

- Store `PredictedObjectID` or `PredictedComponentID` for references that may change during creation, deletion, pooling or rollback. Resolve at use and handle failure.
- Treat objects returned by `TryCreateAndGet` as valid for the current tick. Resolve again after rewind.
- Let `PredictedHierarchy` manage parent-child relationships, ownership and topology. Check the documented protocol before changing a predicted hierarchy.

## BP-10 — Exercise failures

- Test with a remote client. Cover latency, jitter, loss, ownership changes, reconnect, teleport, large corrections, late join, spawn and despawn during rollback, pool reuse, and different frame and tick rates.
- Measure snapshot volume, tick cost, correction frequency and input redundancy with bandwidth and prediction profilers.
- Use the [test matrix](purrdiction-test-matrix.md) for acceptance criteria.

Record evidence for BP-01 through BP-10 with code paths and test outcomes. Mark justified exceptions and unverified checks. Full compliance requires the applicable docs, installed API, Unity build and remote tests. Use `scripts/guard_predicted_code.py` as a heuristic alongside review.
