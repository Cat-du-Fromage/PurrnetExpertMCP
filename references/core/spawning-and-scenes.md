# Spawning, prefabs, pooling, scènes, Addressables

**Sources officielles** : `systems-and-modules/network-identity/spawning-and-despawning/README.md`, `pooling.md`, `network-manager/network-prefabs.md`, `network-manager/scene-scoped-prefabs-and-assets.md`, `systems-and-modules/scene-module.md`, `systems-and-modules/addressables/README.md`, `addressable-spawning-and-despawning.md`, `addressable-scene-handling.md`.

- PurrNet classique prend en charge `Instantiate`/`Destroy` d'objets avec `NetworkIdentity` **si les Network Rules le permettent** et si prefab/scene sont enregistrés selon la configuration. Ne pas importer `NetworkServer.Spawn()` de Mirror.
- Spawn/destroy côté serveur : valider prefab, owner et données; un objet non observé n'est pas forcément détruit sur le serveur. Late join doit reconstruire l'état durable par synchronisation/scene, non par un événement éphémère.
- Différencier objets de scène, objets instanciés avant démarrage, prefabs globaux, asset scope et scene scope. `Include Instantiated Scene Objects` n'est sûr que si les clients produisent les mêmes racines dans le même ordre.
- Pour scènes additives : vérifier qui déclenche chargement/déchargement, quel NetworkManager opère, quand les clients sont prêts, et le comportement lors de la reconnexion. Ne pas supposer que `SceneManager.LoadScene` local synchronise les peers.
- Addressables : vérifier les API dédiées pour chargement et RPC; ne pas deviner les signatures; tester erreurs d'adresse et chargements concurrents.
- Pooling : réinitialiser modules/effets/timers; les pièces enfant peuvent être poolées séparément et perdre leurs références. Voir `Reference<>` documentée dans `pooling.md` lorsque pertinent.
- Objets **prédits** : utiliser `PredictedHierarchy`, `PredictedParent`, et les règles spécifiques de rollback; ne pas appliquer la recette ci-dessus.

## Validation
Spawn/despawn dans scène additive, late join, changement de scène, perte de visibilité, pool reuse, host + deux clients + serveur dédié.
