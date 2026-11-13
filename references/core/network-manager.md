# NetworkManager, startup and sessions

**Official source**: `systems-and-modules/network-manager/README.md`, `systems-and-modules/network-manager/connection-and-player-events.md`, `systems-and-modules/network-manager/network-rules.md`, `systems-and-modules/transports/README.md`.

## Contract
- Inspect the `NetworkManager` of each scene and its server/client boot flags before adding `StartServer`, `StartClient` or `StartHost`. Editor + clone mode, a client build and a server build can start differently.
- Do not assume that a client can know the remote address at the time of initial loading. If connection after matchmaking, disable the self-start **before** the stage manager starts; check the signatures on the installed version.
- `StartClient` can perform the `Disconnected` → `Connecting` transition asynchronously: do not immediately conclude failure or run multiple simultaneous tests.
- Distinguish transport (socket/connection), authentication (entry authorization), `PlayerID` (accepted player), loaded scene (ready player), observed object (replicted). None of these states involves all others.
- Remove protocol version, reconnexion cookies, Network Rules, prefabs and registered assets, transport configuration and Platform/Build target.

## Check
Host, remote client, dedicated headless, reconnexion and launch of two build; no double managers and automatic connections to `127.0.0.1` not requested.
