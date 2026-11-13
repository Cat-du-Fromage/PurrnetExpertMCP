# Levels of evidence, checklist and definition of "completed"

| Niveau | Authorized expression | Expected evidence |
| --- | --- | --- |
| P0 | Assumption | Proposed code/symbol without verification |
| P1 | Documented | Link to official doc with date and version if possible |
| P2 | Verified code | Signature or file of the package installed / commit |
| P3 | Successful compilation | Unity compiles scripts in the project (log or build output) |
| P4 | Verified local behaviour | Scene with host + clone / multiple players, result observed |
| P5 | Audited dedicated behaviour | Build server headless + two clients, logs and world status confirmed |
| P6 | Verified deployment | Real hosting and same E2E tests (only if requested) |

The `assets/unity/*.cs` of this pack are **P1/P2 partial**: based on documented examples, **no Unity** compilation test is done here. An agent must validate them in the project and adjust the signatures if necessary.

## Essential tests according to functionality

- `host`: `OnSpawned` triggered once per role, no double event or double spawn.
- `client owner`: Allowed RPC and synchronized data.
- `client non-owner`: access correctly denied / read-only status if expected.
- `dedicated`: The server creates its world without a local client.
- `late join`: durable condition rebuilt; buffer RPC used only if appropriate.
- `disconnect/reconnect`: no consistent leakage/duplication, ownership and scene.
- `transport`: real ports and protocol, reconnection / latency / cut.
- `security`: invalid requests or spam do not change the status without permission.
- `build`: Asmdef, validated packages, codegen and target build.

Never turn an assertion of `evals/` into "evidence" if the test has not been performed.
