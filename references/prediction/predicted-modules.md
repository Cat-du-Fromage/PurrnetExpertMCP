# PredictedModule and Dynamics

**Source** `client-side-prediction/predicted-modules/README.md`, `predicted-modules/predicted-timer-module.md`, `flow.md`.

- `PredictedModule<TState>` integrates a sub-state and a simulation to the identity: delta/history/automatic reconciliation, but snapshot cost and additional simulation.
- **static** modules created before first tick (typically `LateAwake`): the same **list and order** must be created on ALL peers. Never condition the static roster to own/serve, otherwise `PredictedModuleRosterMismatchException` suspends replication for this identity.
- Modules **dynamics** created during simulation: existence is itself reconciled. The constructor must be public, first parameter `PredictedIdentity`, other optional parameters; dynamic gameplay parameters in STATE, not only ctor args.
- `Dispose()` of a dynamic module during simulation triggers the reconciled deletion; `Dispose` of a static is invalid/no-op + error. Callback `onDisposed` to use to clean external references.
- A dynamic reference cached off STATE can point to an old instance after rollback. Prefer `TryGetModule<T>` / current lookup; check method signatures in package.
- Not to be confused with classic `NetworkModule`s: they are never created as a list on execution and are not reconciled via history.

## Tests
Roster mismatch simulated, dynamic created and deleted during rollback, constructor with unpersistent config, pool, duplicated state and two different FPS clients.
