# Network State Machine vs Predicted State Machine

Official: `plug-n-play-components/state-machine-auto-networked.md`, `client-side-prediction/predicted-state-machine/README.md`, `.../predicted-state-node.md`.

## Classic
- `PurrNet.StateMachine.StateNode` / `StateNode<T>` live under classic `NetworkStateMachine`. Nodes have `Enter(bool asServer)`, `Exit(bool asServer)`, `StateUpdate(bool asServer)`; controller can `machine.Next()`, `Previous()`, `SetState(specificState)`.
- Inspector default is server auth, can be owner auth; confirm who may transition. Persistent phase state should replicate to late joiners.
- Graph/controller scene configuration is mandatory; don't generate code while ignoring the Inspector state list.

## Predicted
- `PredictedStateNode` is a different prediction-timeline system. Transitions must survive rollback and replays; separate `StateSimulate`, state payload, presentation hooks such as `ViewEnter` / `ViewExit` (verify installed signatures).
- Do not mix the classic machine as the sole authoritative source for a predicted character's simulated state.

Test: transition under packet loss, late join, rollback, state entry side effects (no duplicate sound), host/dedicated behavior.
