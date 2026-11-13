# Performance, bande passante, profils de test

**Official sources**: `systems-and-modules/bandwidth-profiler.md`, `readme/performance/`, `systems-and-modules/bitpacker-serialization/`, `plug-n-play-components/network-transform.md`, `network-transform/adaptive-sync.md`, `client-side-prediction/disposable-collections.md`.

- Measure before optimizing: bytes/s by category/object, number RPC, ticks, freq correction, history size, GC, server CPU and client. `NetworkTransform` is different from `PredictedTransform`.
- Reduce messages to high frequency: choose the right Sync Type/SyncInput, interval/delta, a path that can only be linked if acceptable loss, compressible payloads and small sets.
- Use visibility and ownerOnly for **do not send** data not required. Check private values leak when transferring owner.
- In PurrDiction, the bulky states are duplicated during reconciliation: `Disposable*`, `IDuplicate`, `Dispose`, adapted policy and real rollback tests.
- Do not trust an old Stray Help benchmark; compare under project build conditions.

## Matrice
2/4/8 clients according to target, 60/120 ms ping, 0/1/5% losses, jitter, tick 30/60, FPS 30/144, dedicated headsless, entity spikes, late joins. Report the measures actually observed, without inventing numbers.
