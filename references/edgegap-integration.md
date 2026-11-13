# Cooperation with the skill beggap-purrnet

Source : https://github.com/edgegap/llm-agent-skills/tree/main/skills/edgegap-purrnet

`purrnet-expert` intervenes on gameplay C#, RPC, synchronization modules, authority, bugs host/dedicated, serialization, addon PurrDiction, version and debugging.

`edgegap-purrnet` (if installed) takes over for: dedicated Linux, standalone bootstrap, plug-in/build Docker, deployments to Edgegap, matchmaking, connection panel, cloud ports, lifecycle and server destruction. Do not force it for a self-hosted server or host/relay project.

## Flux de collaboration

1. `purrnet-expert` inspects the Unity/PurrNet version and the logic of the game; notes the host-only changes required.
2. `edgegap-purrnet` configures its bootstrap, server/client templates and local steps → Docker → cloud → matchmaking.
3. `purrnet-expert` rereads game logic changes and authority risks, and checks that the world state exists without local client.
4. Both pass the test matrix; do not present the Edgegap sample as proof of the user project.

Never integrate Edgegap secrets into the client or project files. For any action on a real account or invoiced service, follow the confirmation expected by the tool concerned.

## v0.8 — Transfer Operational Contract

For an Edgegap request, load `references/workflows/edgegap-handoff.md` and then, if the Edgegap skill is available, let it take the lead role in the deployment. Forward `Unity version`, `PurrNet version/commit`, `NetworkManager/scene`, `start flags`, `transport/port`, `callbacks host-only`, `build evidence` and `risks`. Expected return: logs of a server **without local client**, two real clients, direct deployment before matchmaker, auto-stop and stop billing resources. Never turn a validation reported on the Edgegap sample into proof on the user project.

Detailed comparison and location of reviews Edgegap : `references/edgegap-comparison.md`.
