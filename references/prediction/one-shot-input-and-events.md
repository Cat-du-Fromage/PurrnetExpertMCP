# PurrDiction: one-shot commands, extrapolation and replayable effects

**Sources** : `client-side-prediction/input-handling.md`, `best-practices.md`, `multi-identity-interactions.md`, `flow.md`, `security.md`.

## The concrete risk

`Input.GetKeyDown` only runs on certain Unity frames; `GetFinalInput` only runs by tick. If the input is read only in `GetFinalInput`, a strike between two ticks can be lost. Conversely, if `fire=true` is repeated during the extrapolation of a lost packet, a one-time action can be played several times.

## Diagram from official documentation (illustrative)

```csharp
// INPUT must be an IPredictedData struct with Dispose.
protected override void UpdateInput(ref PlayerInput input)
{
    input.jump |= Input.GetKeyDown(KeyCode.Space);
}

protected override void GetFinalInput(ref PlayerInput input)
{
    input.move = new Vector2(
        Input.GetAxisRaw("Horizontal"),
        Input.GetAxisRaw("Vertical"));
}

protected override void SanitizeInput(ref PlayerInput input)
{
    input.move = Vector2.ClampMagnitude(input.move, 1f);
}

protected override void ModifyExtrapolatedInput(ref PlayerInput input)
{
    input.jump = false;
}
```

These partial overrides were not compiled in Unity. Verify `PlayerInput`, the base class and the installed PurrDiction version.

## A Robust Fire Sequence

1. Local capture: `UpdateInput` can capture the button edge, or a command counter can distinguish two successive shots without repeated boolean.
2. `GetFinalInput` collects continuous axes; an input sent must remain **compact and serialisable**.
3. `SanitizeInput` clamps magnitude and rejects non-finite values; the server also checks cooldown, ammunition, ownership and range **in its simulation**.
4. `ModifyExtrapolatedInput` removes the one-shots on repeated inputs; do not remove the STATE mutation from `Simulate` during rollback.
5. Create a projectile by `PredictedHierarchy.Create` during the tick, with a stable sequence if necessary.
6. Play audio, trails and UI effects through `PredictedEvent`, `UpdateView` or a view guard verified for the installed version. Keep effects in presentation.

## Tests

- Press and release between two ticks.
- Drop the input packet for a shot and verify that recovery neither duplicates nor incorrectly discards the shot.
- Keep the button pressed with the high repeat factor.
- Replay three times the reward tick: no RPC/FX/additional upgrade.
- A malicious client sends `move=(Infinity, NaN)` and `fire` to each tick; no illegal damage.

**Status**: partial examples not compiled in Unity in this pack.
