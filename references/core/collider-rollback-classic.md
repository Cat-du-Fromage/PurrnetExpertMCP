# Collider Rollback classic versus Lag Compensation from PurrDiction

**Sources**: `systems-and-modules/collider-rollback.md` and `client-side-prediction/lag-compensation.md`, `client-side-prediction/security.md`.

## Choose without mixing the timelines

| Architecture de gameplay | Mechanism | Where to solve the impact? |
| --- | --- | --- |
| `NetworkIdentity` Classic + Authoritative Server Move | `ColliderRollback` and Tick/Latency Server Control | On the server, after checking the request |
| `PredictedIdentity` with PurrDiction | `predictionManager.lagCompensation`, `lagCompensationTick` during `Simulate` | Predicted timeline, authoritative server result |
| Totally own-auth and not validated | None guarantees the anti-cheat alone | Review the authority before dealing with the hit |

## Classic hit-validation fireworkflow

1. Enable the `ColliderRollback` component on the affected colliders and set the history according to the docs and package.
2. The client transmits a **shooting intent** (direction and tick/latency), never a "I touched X" decision accepted directly.
3. The server checks `RPCInfo.sender`/owner, ammunition, cooldown, old bounded tick and plausible origin.
4. The server performs the test via `ColliderRollback` of its version. Do not import an old signed copy of a Discord message.
5. The damage is calculated and applied on the server side. Visual impact is diffused without confusing feedback and decision.

## Anti-patterns

- Compare two locally rendered positions and announce a validated hit.
- Make two simultaneous rollbacks (ColliderRollback Classic and LagCompensation PurrDiction) for the same actor without a conversion plan.
- Trust an arbitrarily old tick transmitted by client: limited clearing window.
- Apply the damage to an observer RPC so that "all see the same".

## Scenarios

A valid 100 ms shot, a shot beyond the allowed window, a hidden player, a changing stage player, a malicious owner and a hit in the presence of loss of packages. Measure the gap between rendered client and verdict server.

**status**: decision guide; no complete scratchcast code is guaranteed compileable without checking the installed version.
