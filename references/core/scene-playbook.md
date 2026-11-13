# Scènes Unity, prefabs et assets réseau — playbook

**Docs** : [Network Assets](https://purrnet.dev/docs/systems-and-modules/network-manager/network-assets), [Scene Scoped](https://purrnet.dev/docs/systems-and-modules/network-manager/scene-scoped-prefabs-and-assets), [Scene Module](https://purrnet.dev/docs/systems-and-modules/scene-module), [Addressables](https://purrnet.dev/docs/systems-and-modules/addressables), [Connection/Player Events](https://purrnet.dev/docs/systems-and-modules/network-manager/connection-and-player-events).

## 1. Table de diagnostic

| Symptom | À inspecter |
|---|---|
| Client connecté mais ne voit pas prefab | NetworkIdentity, registre, Network Rules, visibility, scène chargée |
| Le nouveau joueur n'a pas de monde | onPlayerLoadedScene, observers, état durable, snapshots, scène réellement présente |
| Instantiation fonctionne en Editor mais pas en build | asset inclus, Addressables catalog, scène au Build Settings, résolution par registry |
| Le même prefab existe deux fois | host/server `asServer`, spawn path, auto-start flags, startup idempotent |
| Perf mémoire se dégrade à chaque scène | registre global trop large, `NetworkScenePrefabs/NetworkSceneAssets`, pooling |

## 2. Checklist Inspector

1. Dans la scène de démarrage : `NetworkManager`, transport, règles de spawn/autorité, registres `NetworkPrefabs`/`NetworkAssets` selon le jeu.
2. Dans une scène de gameplay non globale : créer ses ScriptableObjects de registre avec `Folder / Scene` défini sur cette scène ; placer `NetworkScenePrefabs` et `NetworkSceneAssets` dans une GameObject de cette scène.
3. Éviter les doublons avec registre global : global gagne. Les objets doivent être créés dans **la scène qui possède le registre** ; sinon fallback sur autre scène et risques pour des clients qui ne l'ont pas chargée.
4. Charger la scène réseau **avant** de supposer que tous les joueurs reçoivent l'objet, vérifier les événements `onPlayerLoadedScene`/`onPlayerUnloadedScene` et la visibilité.
5. Addressables : enregistrer les prefabs Addressables et tenir compte du caractère asynchrone pour spawn, RPC et scene; tester le chargement lent, l'annulation, le cleanup/release sur clients et serveur.

## 3. Timing et callbacks

- Transport `Connected` est antérieur à l'auth et à l'attribution d'un `PlayerID`.
- `onPlayerJoined` est appelé **après** authentification, mais pas nécessairement après toutes les scènes.
- Les callbacks avec `asServer` s'exécutent pour serveur et client d'un host : garder le contrôle serveur dans la branche `asServer`.
- `OnObserverAdded` / `OnObserverRemoved` sont côté serveur et permettent de produire un état ciblé. Ne jamais utiliser leur seule occurrence pour l'état durable global.
- Des objets peuvent exister sur le serveur sans être visibles par un client, en raison des règles ou de la scène.

## 4. Tests obligatoires

Host + clone / deux builds clients / client tardif, rejoin avec cookie, chargement additif dans un ordre différent, unload d'une scène sous observation, connexion qui échoue durant chargement, prefab du registre scene-only, destruction + respawn pool, sérialisation d'un asset dynamique (par exemple AudioClip).
