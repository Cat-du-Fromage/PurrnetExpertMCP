# Memory, History and Predicted Pooling

**Source** `client-side-prediction/disposable-collections.md`, `best-practices.md`, `predicted-hierarchy.md`, `predicted-modules/README.md`.

- States and buffers are duplicated and arranged at high frequency. Use adapted collections `DisposableList<T>`, `DisposableDictionary<K,V>`, `DisposableArray<T>`, manufactured by `Create(...)` and released via `STATE.Dispose`.
- Do not make `var second = first;` then two `Dispose()` from the shared struct collection. Use `.Duplicate()` and implement `IDuplicate<T>` on composite states with buffers. `IEquatable<T>` can help packers/delta for expensive states.
- Scratch allocations use pools with `Instantiate`/`Destroy` specific to local collections; do not confuse with `Instantiate` Unity network objects.
- `PredictedObjectID` are persistent handles, a GameObject/Component reference can be invalidated by reconciliation, suppression or re-pool. Solve for each relevant use.
- Collections of physical contacts are valid in the callback, not beyond. Do not keep external callback/event to a dynamic module whose life has ended.
- `PURR_LEAKS_CHECK` in Editor allows tracking allocations on certain versions; compile and verify the directive before recommending.

## Tests
1000 repeated spawns/despawns, rollback every 3 ticks, long replay, pool, double disposes, collision contact expired, heap allocation delta and profile history.
