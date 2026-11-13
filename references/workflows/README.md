# Workflows, in minimum order

An agent must not read the entire package at each request. Choose **a course**, then open only the references that his/her need triggers. Official pages remain priority for signatures and branches.

| Player/developer's intention | Route | Criterion that proves a useful purpose |
|---|---|---|
| "Add Network Feature" | [feature.md](feature.md) | Two peers observe the same result, with permissions and late join |
| « My RPC doesn't work / jitter / bug » | [bug.md](bug.md) | Localized cause, reproduction before/after and counter-test |
| « Works as a host, not as a dedicated server » | [dedicated.md](dedicated.md) | The server without local client has the world and two clients play |
| "I want rollback / prediction" | [prediction.md](prediction.md) | Reconciled simulation, unplayed effects and degraded network testing |
| « Deploy on Edgegap / matchmaking » | [edgegap-handoff.md](edgegap-handoff.md) | Delegation to `edgegap-purrnet`, check interfaces between skills |

For each route: inspect first, preserve the existing one, check APIs on the local package, document the steps Unity, **do not declare a validated step without an artifact of proof**. See [acceptance.md](../validation/acceptance.md).

Evidence: D0 hypothesis, D1 doc, D2 signatures, D3 build, D4 two clients, D5 dedicated, D6 stress/security. A regex control is a signal, never a D3+ result.
