# Addons optionnels : PurrLobby / PurrVoice / Dissonance / Steam

**Documentation** : `tools/purrlobby/README.md`, `getting-started.md`, `how-it-works.md`, `scene-setup.md`, `providers.md`, `custom-providers.md`, `in-game.md`, `tools/purrvoice-voice-chat/README.md`, `integrations/dissonance.md`, `integrations/unitask.md`, `systems-and-modules/transports/steam-transport.md`.

- **PurrLobby**: Manage matchmaking and lobbies is distinct from the player's transport connection, authentication and spawn. Control provider and version compatibility, server credentials, UI and transfer to game scene. Do not confuse `PurrLobby` and old `PurrNet-Lobby` repository without checking.
- **PurrVoice**: voice, input/output providers, muted state, microphone, lip sync. Test micro permissions, latency, team/proximity voice, secrecy ban and privacy; voice does not replace session validation.
- **Dissonance**: possible integration; do not repeat an old Discord response that states "no official integration" without confronting `integrations/dissonance.md` and the `PurrNet-Dissonance` repository.
- **Steam transport**: invit/identity/lobby Steam, server authority; check platform and dependencies. **EOS transport** and other add-ons have their own packages.
- **PurruI/PurrLay/PurrOpus/PurrServices**: do not invent APIs; see actually installed package and corresponding official repository.

Tests: 2 clients, reconnection, entry authorization, scene change, timeout, microphone interruption, late join, dedicated server and targeted platform build.
