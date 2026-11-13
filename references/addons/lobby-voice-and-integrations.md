# Addons optionnels : PurrLobby / PurrVoice / Dissonance / Steam

**Documentation** : `tools/purrlobby/README.md`, `getting-started.md`, `how-it-works.md`, `scene-setup.md`, `providers.md`, `custom-providers.md`, `in-game.md`, `tools/purrvoice-voice-chat/README.md`, `integrations/dissonance.md`, `integrations/unitask.md`, `systems-and-modules/transports/steam-transport.md`.

- **PurrLobby** : gérer matchmaking et lobbies est distinct de la connexion transport, de l'authentification et du spawn du joueur. Contrôler provider et compatibilité de version, credentials serveur, UI et transfert vers scène de jeu. Ne pas confondre `PurrLobby` et ancien dépôt `PurrNet-Lobby` sans vérifier.
- **PurrVoice** : voix, providers d'entrée/sortie, muted state, micro, lip sync. Tester permissions micro, latence, voix par équipe/proximité, interdiction de secrets et privacy; voix ne remplace pas la validation de session.
- **Dissonance** : intégration possible; ne pas reprendre une réponse Discord ancienne qui affirme « pas d'intégration officielle » sans confronter `integrations/dissonance.md` et le dépôt `PurrNet-Dissonance`.
- **Steam transport** : invit/identité/lobby Steam ≠ autorité serveur; vérifier plateforme et dépendances. **EOS transport** et autres add-ons ont leurs propres packages.
- **PurrUI/PurrLay/PurrOpus/PurrServices** : ne pas inventer les APIs; consulter package réellement installé et dépôt officiel correspondant.

Tests : 2 clients, reconnexion, autorisation d'entrée, changement de scène, timeout, interruption micro, late join, serveur dédié et builds de plateformes ciblées.
