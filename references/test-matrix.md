# Matrice minimale de tests multijoueurs

| Test | To be checked |
| --- | --- |
| Host seul | `OnSpawned` can be invoked for both roles: no dual business logic |
| Two clients + dedicated server | Client owner/non-owner, RPC sent to the right target |
| Client 2 rejoint tard | Spawning, durable condition, visibility and correct initial values |
| Logout / Reconnection | Clean-up, identities and possible reconnection cookies |
| Unauthorised client | Unable to invoke critical action or write unauthorised state |
| Despawn / change of scene | No ghost object or duplicate event |
| Build standalone | Same behavior off Unity Editor, not just host |
| Simulated latency/loss | No implicit assumption of order or reliability for unreliable channels |

Always mention what has actually been tested and what remains only
proposed. A C# compilation is not network validation.

## Additional PurrDiction tests v0.3

For all `PredictedIdentity` / `PredictedModule` / rollback / prediction, the above matrix is not enough: read **`references/purrdiction-test-matrix.md`** (PD-01..PD-23). Replay the ticks, change ownership, simulate losses and RTT, pools and spawn/despawn, check prediction/conciliation and memory, and control the use of the website for installed versions.
