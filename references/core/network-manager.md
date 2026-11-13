# NetworkManager, startup et sessions

**Source officielle** : `systems-and-modules/network-manager/README.md`, `systems-and-modules/network-manager/connection-and-player-events.md`, `systems-and-modules/network-manager/network-rules.md`, `systems-and-modules/transports/README.md`.

## Contrat
- Inspecter le `NetworkManager` de chaque scène et ses flags de démarrage serveur/client avant d'ajouter `StartServer`, `StartClient` ou `StartHost`. Le mode Editor + clone, une build client et une build serveur peuvent démarrer différemment.
- Ne pas supposer qu'un client peut connaître l'adresse distante au moment du chargement initial. Si connexion après matchmaking, désactiver l'auto-start **avant** que le manager de scène s'initialise; vérifier les signatures sur la version installée.
- `StartClient` peut effectuer la transition `Disconnected` → `Connecting` de manière asynchrone : ne pas conclure immédiatement à l'échec ni lancer plusieurs essais simultanés.
- Distinguer transport (socket/connexion), authentification (autorisation d'entrée), `PlayerID` (joueur accepté), scène chargée (joueur prêt), objet observé (répliqué). Aucun de ces états n'implique tous les autres.
- Relever version du protocole, cookies de reconnexion, Network Rules, prefabs et assets enregistrés, configuration des transports et Platform/Build target.

## Vérifier
Host, client distant, dédié headless, reconnexion et lancement de deux builds; absence de doubles managers et de connexions automatiques à `127.0.0.1` non demandées.
