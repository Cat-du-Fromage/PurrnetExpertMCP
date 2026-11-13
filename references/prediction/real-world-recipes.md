# PurrDiction Recipes — controller, shooting, rollback, spawn and view

**Sources**: [Best Practices](https://purrnet.dev/docs/client-side-prediction/best-practices), [Input](https://purrnet.dev/docs/client-side-prediction/input-handling), [State](https://purrnet.dev/docs/client-side-prediction/state-handling), [Hierarchy](https://purrnet.dev/docs/client-side-prediction/predicted-hierarchy), [Lag Compensation](https://purrnet.dev/docs/client-side-prediction/lag-compensation), [View](https://purrnet.dev/docs/client-side-prediction/views-and-interpolation). The code here is **Illustrative and not compiled** in Unity; check package and version (including `>=1.4.0`).

## 1. Controller INPUT vs STATE

```csharp
using PurrNet.Prediction;
using UnityEngine;

public struct MoveInput : IPredictedData
{
    public Vector2 move;
    public bool jump;
    public void Dispose() { }
}

public struct MoveState : IPredictedData<MoveState>
{
    public Vector3 position;
    public Vector3 velocity;
    public float cooldown;
    public void Dispose() { }
}
```

`INPUT` is an intention collected on the controller. `STATE` is all that influences a future result, even when the data is also present on a Transform or Rigidbody. Inspector fields must be immutable or copied to STATE before influencing a simulation.

**Skeleton of Responsibilities** (not compilable as is):

```text
UpdateInput: accumulate frame-level edge (jump |= WasPressedThisFrame).
GetFinalInput: collect continuous axes once per simulation tick.
SanitizeInput: clamp [-1,1], reject NaN/Inf; enforce server-side move limits.
ModifyExtrapolatedInput: jump=false, fire=false when repeating missing remote input.
GetInitialState: complete snapshot, incl. cooldown and random state.
Simulate(INPUT, ref STATE, delta): deterministic tick state mutation; NEVER Input.GetKeyDown.
GetUnityState/SetUnityState: bridge Rigidbody/Transform not already covered by built-ins.
UpdateView(viewState, verified): render pose/Animator/FX; do not change gameplay.
```

The simulation can be called several times for the same tick. `Time.deltaTime`, `Time.time`, `UnityEngine.Random` and irreversible effects are prohibited in the replayable path. Audio/particles/achievements: view callbacks, `PredictedEvent`, verified view. Avoid effects in `LateSimulate` as well.

## 2. Projectile / hit-scan

**Reactive spawning**: the fire request must be in INPUT, verified by STATE (munitions, cooldown, owner); create by `predictionManager.hierarchy.Create` **during** `Simulate`. For a creation event, a monotonous meter in the input can withstand repetitions better than a Boolean. A `Create` call from a client's UI button outside of the simulation does not make creation authoritative: it can disappear at the correction.

**Spawning not predicted**: an IU button can trigger a `ServerRpc` on a conventional network identity, and the server creates the predicted object; the client sees it when the checked state returns. Do not send regular RPC *from the replay*.

**Hitscan (modern API)**: `predictionManager.lagCompensation.Raycast(lagCompensationTick, ray, out hit, range, mask)` during `Simulate`, target with `ColliderRollback` configured, server-bound view delay. The predicted `lagCompensationTick` is not the classic `NetworkIdentity.rollbackTick`. Hit success must change STATE; shooting sound remains in view.

## 3. Interaction with an object

- In STATE, a persistent target is `PredictedObjectID` or `PredictedComponentID`, **pas** `GameObject`/`Transform` likely to be destroyed or recycled to rollback.
- Solve the handle in the current world just before the interaction (`TryGetGameObject`, `TryGetIdentity` depending on the version). A missing lookup is normal if the partner no longer exists.
- `PredictedParent` makes parent changes replayable; repairing from simulation, using recognized pieces.
- `PredictedGameObject.SetActive` may be preferable to temporarily hide an object, without cost of destruction/recreation.

## 4. Prediction policies: an example of a decision

| Role | Policy indicative | Pourquoi |
|---|---|---|
| Local player | `PredictedIfOwned` | local predictive, remote copies verified |
| Combat interactif | `FullPrediction` | historical coherence of collisions |
| Cosmetic decor / ragdoll | `SoftCorrection` if supported | visual convergence, no historical collision guarantee |
| Server-controlled Enemies | `ServerRelay` si latence acceptable | no unnecessary replay client |
| Voiture locale + remote douce | `PredictedIfOwnedWithSoftFallback` if supported | soft fallback according to component |

Test `NetworkIdentity` mirroring according to the version: before PurrDiction 1.4 `PredictedIdentitySpawner` may be required; from 1.4 the mirror is automatic and the old component is obsolete.

## 5. Receipt / Replay Test

- Two client build, host vs dedicated, 0/100/250ms RTT, jitter 30ms, simulated losses.
- Repeat the fire/jump inputs under loss, check neither double-fire nor double-fired after correction.
- Replay spawn/delete/reparent, pool user, ownership transfer, reconnect, teleport (ResetInterpolation if necessary).
- Compare `currentState`, `verifiedState`, `viewState` at the same time; measure correction and cost history.
