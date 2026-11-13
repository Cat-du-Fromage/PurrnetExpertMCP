# Agreement of acceptance by evidence — PurrNet Expert

**A validation must be an observed result.** Python scripts, parsing logs and signatures do not replace the compilation or multiplayer test. Respect dependencies: never declare D4 "clients play" without log/observation D3 "build compiled" on the same revision.

## Levels of evidence

| Gate | What needs to be proven | Eligible evidence | Trap to avoid |
|---|---|---|---|
| D0 | Assumption and plan | Files/symptoms, reproduction project | "probably corrected" as a result |
| D1 | Official documentation consulted | URL+section+revision/branche, gate version | Archive Historical Discord taken for current API |
| D2 | Exact API present | Path source/commit package, signature, parameters, namespaces | grep on a comment only |
| D3 | Compilation Unity | commande Editor/Unity, exit code, log + plateforme/Unity version | Python `py_compile` presented as building C# |
| D4 | Game of 2 clients | 2 processes/builds, server and client logs, observed gameplay action | Connected without world/authority |
| D5 | Real dedicated server | build server without local client, 2 clients, logs world init + interaction | success in host only |
| D6 | Resilience and security | perte/jitter, late join, reconnect, owner transfer, tests d'inputs malveillants | no proof, "production ready" labels |

## Mini task contract before modification

```
FEATURE        : both clients can fire and see the impact
PROJECT        : Unity path and version, package commits, scene
AUTHORITY      : owner input -> server validation -> state -> observers
CHANGES        : files changed and rationale
RISKS          : RPC/host/dedicated/late join/prediction/MTU
REQUIRED GATES : D1 through D6 as applicable
```

## Output to be delivered

- Changes by path; scripts/Inspector/assembly required; old behavior preserved.
- PurrNet version and addons, accurate official references, API actually verified.
- Table of gates **successes / failed / not executed / not applicable** + proof (commands, logs, manual procedure).
- Cases tested: host, two remote clients, dedicated, late join, permissions, transport, prediction according to range.
- Open problems with reproducible diagnosis; never hide the absence of Unity/cloud.

## Manifeste machine-readable (optionnel)

To save **observed** results, use `assets/validation/evidence.example.json` and launch:

```bash
python scripts/check_evidence.py evidence.json --project <PROJECT>
```

Control rejects "pass" statuses without legible proof paths, and high-level gates without lower gates; it does not judge the truth of logs, nor the Unity semantics. Do not present it as an E2E test. Fill the values only after completing the steps.

To launch a Unity compilation/import in batch **explicitly**: `python scripts/unity_compile_check.py <PROJECT> --unity-exe <UNITY_EXE> --log-file <LOG> --run`. Without `--run`, the command simply displays its plan. A `0` return without compiler errors validates the import of scripts, **not** building a dedicated client or server.

## Edgegap

The Edgegap skill has examples and an announced validation on its Incremental sample. Its proof is about **its test project**, not about this user project and not about `assets/unity` of this package. Do not use its identifiers/tokens in this manifest. In cloud, record non-sensitive allocation identifier, build version, direct/matchmaker/autostop results, costs/resources stopped.
