# Workflow C — Host/client to dedicated server

## Livrable cible

A **server process without local client** starts, generates its world and has authoritative systems. Two DISTANT clients load the scene, play and recover state mutations. The test is not validated by a simple `Connected` event.

## Phase D0 — Audit of the existing project

`python scripts/audit_dedicated_readiness.py <PROJECT> --json`; then manually check the finds. Inspect all scenes and NetworkManager, Start Server/Client Flags, transports (UDP/WebTransport/Composite), port and `Application.targetFrameRate`; search `isHost`, `StartHost`, `[ObserversRpc]`, `[TargetRpc]`, `runLocally`, `StartClient`, `clientState`, `OnSpawned(bool asServer)`, `Camera.main`, audio, `Input.*`, client-only components. Search scripts that trigger `StartServer()` or `StartClient()` twice. No static results are enough to conclude.

## Phase D1 — Adapt Without rewriting the scenes

- **Preserve the Editor/host+clone cycle** as long as the user does not want to replace it; avoid changing all the start flags of a scene for a dedicated test.
- A single maintainer triggers the server; do not start a local host/client in the dedicated process.
- Any score logic, seed, spawn or round conditioned by `isHost` must work on `isServer` without a local client.
- An ordinary `[ObserversRpc]` may not execute its own body on dedicated. If it initializes the server, separate server initialization and diffusion, OR examine `runLocally: true` after checking the signature and semantics.
- Disable/avoid camera/IU/audio/Unity Input server-side dependencies; do not remove the collision/physics logic useful on dedicated.
- Network settings: binding the server on its interface, port **internal**; client to external address and port, compatible protocols. **Do not copy the default ports of the Edgegap template** into a generic project.
- `StartClient()` is asynchronous: do not interpret its initial state `Disconnected` as immediate failure.

## Phase D2 — Validation locale

1. Unity compiles a Linux Dedicated Server build (or dedicated target), all necessary scenes in Build Settings.
2. The server starts ONLY, loads the world and logs its port, an authoritative timer/score/resource exists before the first connection.
3. Two clients (separate buildings, not just clone Editor) join with a configurable address/port; world initialization, score, controlled interaction.
4. A client is refused for an unauthorized transfer; late join recovers status/synchronization.
5. Logout and stop clean, timeout and log; if cloud host, check corresponding lifecycle.

## Phase D3 — Handoff cloud

If the target is Edgegap, **fall to `edgegap-purrnet`** for Docker/SDK/plugin/credentials/ cloud port/matchmaker and run the steps in `edgegap-handoff.md`. Do not assume that its tested sample proves the user project's compilation. WebGL requires a browser transport, to be checked and tested directly.
