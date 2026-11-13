# Hosting, déploiement et exemples de jeu

**Docs** : `game-server-hosting/`, `full-game-guides/`, `community-guides/`, `guides/setting-up-a-server.md`, `readme/performance/`.

- Distinguer host joueur/P2P, relay, dédié. Préférer serveur autoritaire selon risque de triche, coûts et latence; valider connexion/ports avant matchmaking.
- L'hébergement Edgegap et la configuration cloud détaillée relèvent de `edgegap-purrnet` lorsqu'elle est installée; la présente skill doit rester focalisée sur architecture PurrNet et correctifs réseau.
- La skill `edgegap-purrnet` documente notamment l'auto-start `NetworkManager`, `StartClient()` asynchrone et `[ObserversRpc(runLocally: true)]` pour logique exécutée sur serveur dédié. Appliquer les corrections **seulement** après vérification de la version et du besoin.
- Les exemples GitHub sont une source intermédiaire : un sample peut viser `dev`, une autre Unity version, des Network Rules permissives ou un API depuis remplacée. Ne pas considérer compilation du sample = compilation du projet utilisateur.
- Les réponses Stray Help (Discord) sont historiques, utiles au diagnostic, et doivent être confirmées contre la version installée.

Livraison : séparer preuve D1 documentation, D2 API installé, D3 compilation Unity, D4 deux clients, D5 dédié, D6 perte/jitter. Présenter seulement les niveaux réellement obtenus.
