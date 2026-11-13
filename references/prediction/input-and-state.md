# INPUT, STATE, validation and repetition

**Sources** `client-side-prediction/input-handling.md`, `state-handling.md`, `security.md`, `flow.md`, `predicted-identities.md`.

- `PredictedIdentity<INPUT,STATE>` collects local intent via `GetFinalInput(ref INPUT)` **once by tick**; the fronts `GetKeyDown` must be accumulated in `UpdateInput(ref INPUT)` between the ticks to avoid being lost.
- INPUT is a `IPredictedData` struct, STATE a struct `IPredictedData<STATE>`; store in STATE all data that changes future ticks (position, speed, cooldown, ammo, mode, RNG, IDs). Inspector = parameters *constant* or transferred to the state when they change.
- `SanitizeInput(ref INPUT)` to limit movement, unfinished numbers, love and sizes; valid EN PLUS cooldown server, resources, ownership, collision, speed and permissions. A "well-trained" input is not "legitimate".
- `ModifyExtrapolatedInput(ref INPUT)` neutralizes one-shot events (fire, jump, interact, purchases) if input repeats for lack of package. The `Repeat Input Factor` too small stoppe removes actors; too big does them overshoot. Choose according to RTT and policy.
- In `Simulate(INPUT input, ref STATE state, float delta)`, never read `Input`, `PlayerInput`, a `InputHandler` MonoBehaviour, frames Unity or a RPC. Simulation should depend on INPUT+STATE+predictable sources only.
- `GetInitialState` full snapshot; `GetUnityState/SetUnityState` for Unity physics/transform/caches that impact the future tick. `UpdateView` uses viewState interpole but should not alter the gameplay verdict.
- The rendering events use `PredictedEvent`/verified view, no state mutation to audio callback.

## Tests
Press/release between ticks, loss of a package containing a fire, falsified input, cooldown, input stable, rollback, late join and policy change. Check that server status always wins.
