# PurrNet host vs dedicated — problèmes à chercher

Source d'inspiration pratique : skill `edgegap-purrnet` (https://github.com/edgegap/llm-agent-skills/tree/main/skills/edgegap-purrnet), `references/purrnet.md`, et guide officiel https://edgegap.com/integration/purrnet . Ne pas copier sa configuration sans utiliser Edgegap.

## Host ≠ dedicated

Un host exécute serveur **et** client local ; un serveur dédié n'exécute que le serveur. Une méthode `OnSpawned(bool asServer)` peut être appelée une fois par rôle dans un host. Du code `if (isHost)` ne convient généralement pas à un dedicated.

**Anti-bug critique :** un `[ObserversRpc]` peut envoyer une graine, initialiser une manche ou créer des objets en host grâce au client local, mais **ne pas exécuter son corps sur le dedicated**. Si le serveur doit exécuter la méthode, examiner `[ObserversRpc(runLocally: true, bufferLast: true)]` et sa compatibilité avec la version locale ; ou appeler explicitement la logique serveur dans une méthode non-RPC, puis envoyer la réplication aux clients. `runLocally` n'est pas nécessaire pour chaque RPC purement cosmétique.

## Contrôles avant build

1. Identifier `NetworkManager` et **Start Server Flags / Start Client Flags**, ne pas démarrer serveur/client deux fois ; le client connecté par matchmaking ne doit pas se connecter automatiquement à `127.0.0.1`.
2. Identifier les transports et ports. UDP PurrNet par défaut dans l'exemple Edgegap : `5000`, alors que **le template Edgegap utilise `7777`**. Ne jamais confondre les deux.
3. Chercher `[ObserversRpc]`, `isHost`, `Camera.main`, `AudioSource.Play`, `Input.*` et UI dans tout le chemin dédié : les éléments client-only ne doivent pas faire échouer le serveur headless.
4. Vérifier que joueurs/ressources sont générés par le serveur et que les scènes destinées au dedicated sont incluses dans le build.
5. Si connexion manuelle via `NetworkManager.StartClient`, laisser la transition d'état asynchrone démarrer ; ne pas annuler la tentative parce que `clientState` vaut encore `Disconnected` immédiatement après l'appel.
6. Ne pas changer les règles d'ownership sans analyser leurs conséquences. Un serveur dédié n'élimine pas automatiquement les abus côté client.
7. Prévoir arrêt du serveur, déconnexion, timeout et logs selon l'hébergeur. Aucun token secret dans le client Unity.

## Test de bout en bout

1. Un build headless démarre sans client local et logge le port configuré.
2. Deux builds clients se connectent en direct en utilisant le même transport et le bon port.
3. Un élément du monde créé **par le serveur** existe et est cohérent pour les deux clients.
4. Les clients peuvent jouer, se déconnecter, se reconnecter, et les nouvelles connexions reçoivent l'état requis.
5. La fermeture du serveur et les erreurs de transport sont contrôlées.

Pour création app/version Docker, allocation, matchmaking et cycle de vie Edgegap, charger `edgegap-purrnet` si elle existe. Ne pas dupliquer la logique de déploiement dans cette skill généraliste.

### Niveau de preuve

`edgegap-purrnet` déclare des tests en conditions réelles sur son **propre sample** PurrNet avec deux clients. Cela ne signifie pas que les exemples de `purrnet-expert` ont été compilés. Tout comportement doit être testé dans le projet de l'utilisateur.
