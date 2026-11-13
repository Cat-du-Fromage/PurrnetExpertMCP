# Mandatory contract PurrDiction (BP-01 to BP-10)

**Source** `client-side-prediction/best-practices.md` (recommended local clone). **Required reading** with `references/purrdiction-best-practices.md` BEFORE any change to the simulation. This document serves as a router; the long synthesis v0.3 remains normative in the skill but is not a substitution for the doc of the installed commit.

| BP | Exigence | Implementation Guide / Tests |
|---|---|---|
| 01 | Any mutable state affecting future tick is in STATE | `input-and-state.md`, `lifecycle-and-rollback.md` |
| 02 | GetInitialState, GetUnityState, SetUnityState for state Unity | `lifecycle-and-rollback.md` |
| 03 | Simulate/LateSimulate replayable, delayed effects | `lifecycle-and-rollback.md` |
| 04 | No RPC/SyncVar/Instantiate/NetworkTransform at the heart of the predicted gameplay | `hierarchy-and-parenting.md`, `visibility-and-interactions.md` |
| 05 | Delta/tick/RNG predicted, not Classic Time/Random | `deterministic-identity.md` |
| 06 | Captured input, sanitize, deleted edge extrapolation, valid server | `input-and-state.md`, `security.md` |
| 07 | FullPrediction / PredictedIfOwned / ServerRelay / SoftCorrection by Role | `prediction-policies.md` |
| 08 | Available buffers and snapshots copied in depth | `memory-and-pooling.md` |
| 09 | References PredictedObjectID/PredictedComponentID stable | `hierarchy-and-parenting.md` |
| 10 | Host, remote, dedicated, loss, rollback, pooling, teleports, late join | `references/purrdiction-test-matrix.md` |

**Nuance**: Without simulation, a RPC on NetworkIdentity/mirror can send a request to the server. The creation of predicted objects in such a ServerRpc is *server-driven* (latency) and should not be described as predicted locally. If version <1.4, check bridge `PredictedIdentitySpawner`; >=1.4 automatic mirror (see exact source).

For each response containing prediction code, produce BP-01...BP-10: proven conform / N/A motivated / unverified / default. Do not call the result "validated" if no Unity compilation or rollback test.
