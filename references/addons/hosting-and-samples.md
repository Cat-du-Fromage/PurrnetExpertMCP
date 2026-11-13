# Hosting, deployment and game examples

**Docs** : `game-server-hosting/`, `full-game-guides/`, `community-guides/`, `guides/setting-up-a-server.md`, `readme/performance/`.

- Distinguish host player/P2P, relay, dedicated. prefer authoritative server according to risk of cheating, costs and latency; validate connection/ports before matchmaking.
- Edgegap hosting and the detailed cloud configuration are the responsibility of `edgegap-purrnet` when installed; this skill must remain focused on PurrNet architecture and network patches.
- The `edgegap-purrnet` skill documents the `NetworkManager` autostart, `StartClient()` asynchronous, and `[ObserversRpc(runLocally: true)]` for logic executed on dedicated server. Apply the corrections **only** after checking the version and need.
- GitHub examples are an intermediate source: a sample can target `dev`, another Unity version, permissive Network Rules or an API since replaced. Do not consider compilation of sample = compilation of user project.
- The Stray Help (Discord) answers are historical, useful for diagnosis, and must be confirmed against the installed version.

Delivery: separate proof D1 documentation, D2 API installed, D3 compilation Unity, D4 two clients, D5 dedicated, D6 loss/jitter. Show only the levels actually achieved.
