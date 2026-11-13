# PurrDiction test matrix (excluding Unity tests as long as not performed)

| ID | Reproducible scenario | Observable Criterion / Fault Searched |
| --- | --- | --- |
| PD-01 | Two remote clients + server (not only host) | INPUT owner→server, STATE checked consistent, invalid actions refused |
| PD-02 | `UpdateInput` front jump/fire between two ticks | Action captured once, not lost or duplicated |
| PD-03 | Loss of packages on one-shot action | `ModifyExtrapolatedInput` removes repetition from front |
| PD-04 | Modified input: NaN/speed > allowed / spam purchase | `SanitizeInput` + business rules server block |
| PD-05 | Rollback/replay repeated from the same ticks | No double audio, analytics, RPC, reward, backup |
| PD-06 | Mutation Transform/rigidbody pendant simulation puis correction | `GetUnityState`/`SetUnityState` or integrated component actually restore state |
| PD-07 | Teleport and large correction | `ResetInterpolation` if relevant; no permanent drift |
| PD-08 | Pool reuses object during rollback | Stable ID solved to good object; no dead reference |
| PD-09 | `PredictedHierarchy.Create/Delete` and reparenting during replay | Server and client topology match. A late joiner reconstructs the hierarchy. |
| PD-10 | `PredictedModule` static all-peers | Identical order; none `PredictedModuleRosterMismatchException` |
| PD-11 | `PredictedModule` dynamic created/destructed in `Simulate` | Recreatable state after correction; no cached pointer expired |
| PD-12 | DATA with `DisposableList`/buffers | deep copy independent, good `Dispose`, no double free/leak under stress |
| PD-13 | Ownership switch and reconnection | Resolved policy and input controller transferred, no double sim |
| PD-14 | FullPrediction vs PredictedIfOwned vs ServerRelay | Timelines and cost/corrections match the need for gameplay |
| PD-15 | SoftCorrection and fallback on unsupported component | Relay behaviour identified, no hit validation not accurate |
| PD-16 | 30/60/120 Hz rendering and variable tick rates | stable gameplay; no `Time.deltaTime` dependency in sim |
| PD-17 | Ping 0/100/250ms + jitter/perte | Input extrapolation set, overshoot/correction measured |
| PD-18 | Client arrives late, then loses a connection | Prefab predicted and durable data reconstructable |
| PD-19 | PurrDiction >=1.4 with `NetworkIdentity` mirror | UI RPC OK, isolated predicted gameplay, visibility/ownership mirrored corrects |
| PD-20 | PurrDiction <1.4 as a separate fixture | Do not automatically copy new mirroring or recent lag-compensation |
| PD-21 | Lag offset Hitscan (compatible version) | Server checks ray on history, offset bounded, no trust on client hit |
| PD-22 | Mesure bandwidth/prediction profiler | Cost per tick/snapshots, observed corrections and transmissions |
| PD-23 | 2 different architecture machines, strict determinism | `DeterministicIdentity` and sfloat/fixed; no raw float affecting tick |

## Gates de livraison

- Static: `scripts/guard_predicted_code.py <PROJECT>` does not report any obvious prohibition (heuristic tool) **and** manual review BP-01..BP-10.
- Compilation Unity actual: exact package + addons, asmdef, codegen and target build.
- Performance Test: PD-01, PD-02, PD-03, PD-04, PD-05, PD-07, PD-08, PD-13, PD-17, PD-18 depending on the feature. Add all lines related to the components used.
- "Production ready" : impossible to confirm by a skill alone; profiler, automated tests, load, security and validation on target platforms required.
