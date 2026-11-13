# Workflow E — Collaboration with edgegap-purrnet, not duplication

The `edgegap/llm-agent-skills` study shows that his project tested on Edgegap validates a concrete chain `local dedicated -> Docker -> deploy direct -> matchmaker -> 2 clients -> shutdown`, with Unity assets, logs and assertions. Our skill is **general**: maintain its role of gameplay analysis and let `edgegap-purrnet` manage the Edgegap product. Read `references/edgegap-comparison.md`.

## Interface de transfert

**purrnet-expert transmits to edgegap-purrnet**: Unity exact, version PurrNet/package lock, stage name/NetworkManager, existing auto start flags, transport and port present, `isHost`/`ObserversRpc` suspicious, authoritative world validation scenario, permission limits. Produce a small `HANDOFF.md` or summary with paths and lines of code, without secrets.

**edgegap-purrnet product**: plugin/SDK configuration, dedicated startup, internal vs external port, Linux build, Dockerfile/.dockerignore, registry and allocation, client connector, matchmaker, auto-stop, log result and tests. **Do not assume** that Edgegap, Docker or Unity access exists; separate local changes and manual steps. Do not send Edgegap tokens to client, project, logs or versioned files.

**purrnet-expert then checks** that server changes do not break ownership, local host, authoritative gameplay, late join and RPCs; repeat the D2-D5 criteria. Do not reintroduce logic `isHost` just to satisfy a prefab Editor.

## Route of choice (examples)

- "My `SyncVar` does not sync" → purrnet-expert only.
- "The world is empty on dedicated without any mention Edgegap" → purrnet-expert, with audit dedicated generic.
- "I want Find Match on Edgegap with PurrNet" → edgegap-purrnet owner of deployment; purrnet-expert consulted for gameplay changes if needed.
- "I need a self-hosted Linux server PurrNet" → purrnet-expert (and generalist workflows), not Edgegap imposed.
- « Mirror or FishNet on Edgegap » → corresponding skills, **not** purrnet-expert.

## Definition of finished

The Edgegap project must **really be tested** by a headless server, two clients, cloud/external assignment, matchmaker and shutdown. A cloud access failure must not be disguised: deliver ready-to-test modifications and `HANDOFF.md` with remaining steps, not a "successful deployment".
