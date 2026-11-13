# PurrLobby: menu → lobby → session → game → return

Official: `tools/purrlobby/{README.md,getting-started.md,scene-setup.md,providers.md,how-it-works.md,in-game.md,custom-providers.md,customizing-the-ui.md}`.

## Quick starting point (current docs, verify installed addon)
1. Open shipped `Assets/PurrLobby/Scenes/MenuScene.unity`, include both MenuScene and GameScene in **Build Settings** and test a lobby with two peers.
2. Set `LobbyManager`'s `GameOrchestrator` asset (preconfigured `Orchestrator.PurrNet`, `Orchestrator.Steam`, `Orchestrator.Nakama` are described in docs); configure provider slots and **Game Allocator → Game Scene**.
3. Game scene needs a `NetworkManager`; allocator handles transport setup and creates `GameSession`. Optional `SessionManager` prefab adds pause UI and game-over flow.
4. **PurrLobby suppresses NetworkManager auto-start temporarily** during its scene load; do not disable flags globally without checking that this behavior exists in your addon version.
5. Providers have different capabilities: CreateLobby, JoinLobbyById/Code, JoinRandom, QueryLobbies, PrivateLobbies. The UI exposes only supported ones. Do not invent features for an unsupported provider.
6. PurrNet backend requires PurrServices and PurrTransport; Steam backend requires Steamworks.NET and uses Steam relay sockets; Nakama requires Nakama configuration and backend. Matchmaking, lobby metadata and actual game transport are distinct layers.
7. `GameSession` coordinates return to menu, exit reason and client reconnect attempts. Default docs mention client reconnect timeout and interval; verify installed values. Handle listen host differently from disconnected client.

Tests: one/two/four players; private lobby/join code; ready state; invite; game scene startup without double network auto-start; leave, game over, disconnect/reconnect, remote vs host and server-only mode where supported. Never assume PurrLobby implies dedicated-server matchmaking by itself.
