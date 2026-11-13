# Cycle de vie connexion/joueur/observation

**Source officielle** : `systems-and-modules/network-manager/connection-and-player-events.md`, `network-manager/authentication.md`, `network-identity/networkbehaviour.md`.

## Séquence et callbacks
1. État transport : `onServerConnectionState` / `onClientConnectionState` (`Connecting`, `Connected`, `Disconnecting`, `Disconnected`). Pas encore de `PlayerID` garanti.
2. Authentification acceptée : `onPlayerJoined(PlayerID, bool isReconnect, bool asServer)`. `isReconnect` indique qu'un identifiant déjà vu dans la session revient, pas que son monde est automatiquement restauré.
3. Scènes : `onPlayerLoadedScene` / `onPlayerUnloadedScene`; attendre chargement pertinent avant de supposer un objet de scène prêt. Écouter le côté client/serveur documenté.
4. Observation : callbacks `OnObserverAdded` / `OnObserverRemoved`, côté serveur; état de replication par joueur. Utiles pour late join et payload initial ciblé.
5. `onPlayerLeft` : nettoyer l'état selon stratégie reconnexion/persistance, sans effacer une session récupérable par erreur.

**Piège host** : `asServer` peut provoquer deux chemins distincts, un pour serveur et un pour client; vérifier explicitement le rôle. Abonner les handlers au bon moment (`OnSpawned` dans les comportements réseau selon docs) et les désabonner symétriquement; éviter les lambdas anonymes impossibles à détacher.

## Validation
Reconnexion par cookie, join tardif, changement de scène, visibilité gagnée/perdue, host/dédié, déconnexion pendant chargement. Mesurer l'ordre réel des événements dans les logs et garder les identifiants cohérents.
