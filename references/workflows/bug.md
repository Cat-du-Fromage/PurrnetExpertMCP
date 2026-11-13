# Workflow B — Repair a bug without assigning a cause prematurely

## 0. Collecting evidence

Request/Search, without repetition: exact description, host/dedicated/client role, version PurrNet/PurrDiction, OS/build vs Editor, transport, minimal repro, separate logs `server.log` and `Player.log`, lock package. Capture "anticipated/observed" and number of players.

## 1. Controlled reproduction

Set the matrix: Editor host (server+local client), remote client, dedicated (without local client), late client; compare logs. A plausible correction without replicated scenario must be presented as a hypothesis.

## 2. Decision tree of symptoms

| Symptoms | First check, then docs |
|---|---|
| RPC missing | spawn, ownership, observers, connections, channel and host/client role ; `core/messaging-and-mtu.md` |
| RPC doubled | `OnSpawned(bool asServer)` host, repeated subscriptions, `runLocally`, server call + client |
| World empty on dedicated | `isHost`, client-only `ObserversRpc` that initializes the server, spawn server, scenes in build |
| Connect loop instantly | `StartClient` async; transitional `Disconnected` state, auto-start and port |
| Transform jitter | more than one writer, ownership, sync buffer, Rigidbody patch, transport, FPS/latency |
| Empty state on late join | `SyncVar/SyncList` initial status, observers, stage loading, pooling, late subscription |
| Build IL2CPP | .asmdef, stripping, packer/codegen type, installed versions, log exact |
| Predicted correction | unrestored state, external input in `Simulate`, non-idempotent effect, policy, versions |

See `references/tools/troubleshooting-playbook.md`, `references/dedicated-server.md` and `references/historical/triage-playbook.md`.

## 3. History = track, not diagnosis

`python scripts/historical_issues.py "<SYMPTOM>" --project <PROJECT> --json`. Compare the historical fix with the installed version and the current code. A bug "corrected in 1.2.1" **does not explain** the same symptom in 1.25.0 without proof of regression.

## 4. Isolate and fix the cause

Produce a testable cause: `“Server state is missing before the RPC is sent”`, not `“PurrNet issue”`. Change the minimum area. Do not place `runLocally: true` on all RPC without discernment; often prefer an explicit call from server logic + RPC purely client. Avoid replacing transport/dependence if logs point to a double subscription.

## 5. Regression

Even reproduce BEFORE, host+dedicated if applicable, two clients, late join, network loss and version. If impossible, provide reproduction script and logging steps. Results observed and not observed according to `references/validation/acceptance.md`.
