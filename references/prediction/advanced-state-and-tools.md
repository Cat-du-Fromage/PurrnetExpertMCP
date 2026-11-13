# Advanced PurrDiction: state machines, timers, callbacks, development shortcuts

Official: `client-side-prediction/predicted-state-machine/{README.md,predicted-state-node.md}`, `predicted-modules/predicted-timer-module.md`, `built-in-components/predicted-physics-callbacks.md`, `development-shortcuts.md`, `flow.md`.

- Predicted state-machine state and transition decisions must be replayable; differentiate `StateSimulate` from `ViewEnter/ViewExit` and prevent repeat of audio, save, network I/O. Confirm node generic variant and registration in Inspector.
- Predicted timers must live in tick state or documented predicted timer modules; don't use wall-clock coroutines as the authoritative cooldown during rollback.
- Physics callbacks: `PredictedPhysicsCallbacks` adds rollback-aware collision/trigger records without requiring predicted Rigidbody; supported event payloads and lifecycle vary at `>=1.4.0`. Use stable IDs (`otherId`) rather than retaining GameObject across replay.
- Dev shortcuts: server-only correction or spawn can be acceptable for **prototype** when the resulting snap/delay is documented and tested; do not claim it is strict deterministic or suitable for critical combat. Document the debt to remove before production.
- Mixed identities: use `PredictedEvent` for view/presentation, keep state mutations in every required replay, use stable `PredictedObjectID` and inspect cross-identity simulation ordering.
