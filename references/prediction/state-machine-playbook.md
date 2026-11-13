# PredictedStateMachine / PredictedStateNode — procedure

**Sources** : [State Machine](https://purrnet.dev/docs/client-side-prediction/predicted-state-machine), [Predicted State Node](https://purrnet.dev/docs/client-side-prediction/predicted-state-machine/predicted-state-node), [Flow](https://purrnet.dev/docs/client-side-prediction/flow), [Best Practices](https://purrnet.dev/docs/client-side-prediction/best-practices).

## Do not confuse

- `NetworkStateMachine` (PurrNet classic) replicates the state; `StateNode` is a `NetworkBehaviour` whose methods can differentiate `asServer`.
- The **predite** machine evolves in the PurrDiction timeline with simulation/conciliation. Transitions that influence gameplay must occur in a state that history can restore.
- `Enter`/`Exit` simulation should not send RPC, start an irreversible audio or write a backup at each replay. The `ViewEnter`/`ViewExit` functions (depending on version) are related to the presentation; check their signature before implementation.

## Example of liability (pseudo-code)

```text
State: Idle -> Move -> Jump -> Land
Input: move axis + jump edge collected by UpdateInput
STATE: activeMode, jumpTicks, velocity, lastInteraction
On StateSimulate: update STATE deterministically, ask transitions only on simulated timeline
On UpdateView / ViewEnter: change Animator pose / VFX as needed
On rollback: restore previous state + replay transitions, no duplicate score/SFX.
```

- Generic versions of `PredictedStateNode<INPUT,STATE>` and `PredictedStateNode<STATE>` do not necessarily have the same callbacks; read the local implementation.
- If the machine contains dynamic submodules, their creation/destruction belongs to the simulation and follows the roster of predicted modules.
- A local animation should not only determine a collision or cooldown server.

## Tests

Chained attacks, fast transition Idle→Jump→Land, correction during Enter/Exit, lower frame rate than tick rate, same multiple pass tick, late join mid-state, pool reset and invalidated authority.
