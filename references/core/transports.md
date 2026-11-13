# Transports, hébergement et diagnostic réseau

**Sources officielles** : `systems-and-modules/transports/README.md`, `udp-transport.md`, `web-transport.md`, `steam-transport.md`, `purr-transport.md`, `composite-transport.md`, `local-transport.md`, `eos-transport.md`, `simulating-latency.md`; `guides/test-with-friends/`.

- Distinguer transport sélectionné (UDP, WS/WSS, Steam, relay, composite, local), plateforme et contraintes du navigateur. **WebGL ne peut pas ouvrir de socket UDP**; choisir un transport Web compatible et une configuration TLS valide.
- Ne pas présumer que les transports ont les mêmes propriétés `address`/`serverPort`, le même NAT traversal ou la même sécurité. PurrTransport relayer et relay tiers ont leurs limitations et coûts; vérifier la doc actuelle.
- Inspecter adresse d'écoute serveur (souvent `0.0.0.0`), port interne, protocole, endpoint/port **externe** renvoyé par hébergeur; attention Firewall/NAT/IPv6.
- Un serveur dédié est distinct d'un host joueur : éviter les initialisations seulement sur client, les appels camera/audio/UI, et observer RPC dont le corps doit aussi être exécuté sur le serveur.
- Avant recommander une infrastructure, clarifier (si inconnu) plateforme, topologie, nombre joueurs, modèle d'autorité et matchmaking; pour Edgegap déléguer à `edgegap-purrnet` si installé.

## Diagnostic minimal
Server started? port listen? authenticator accepted? `PlayerID` created? scene loaded? observer? state? Test loopback, LAN, réseaux différents, pertes simulées et headless; séparer ces phases dans les logs.
