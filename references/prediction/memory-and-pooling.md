# Mémoire, historiques et pooling prédit

**Source** `client-side-prediction/disposable-collections.md`, `best-practices.md`, `predicted-hierarchy.md`, `predicted-modules/README.md`.

- States et buffers sont dupliqués et disposés à fréquence élevée. Utiliser les collections adaptées `DisposableList<T>`, `DisposableDictionary<K,V>`, `DisposableArray<T>`, fabriquées par `Create(...)` et libérées via `STATE.Dispose`.
- Ne pas faire `var second = first;` puis deux `Dispose()` de la collection struct partagée. Utiliser `.Duplicate()` et implémenter `IDuplicate<T>` sur les états composites possédant des buffers. `IEquatable<T>` peut aider packers/delta pour états coûteux.
- Scratch allocations utilisent pools avec `Instantiate`/`Destroy` propres aux collections locales; ne pas confondre avec `Instantiate` Unity d'objets réseau.
- Les `PredictedObjectID` sont des handles persistables, une référence GameObject/Component peut être invalidée par réconciliation, suppression ou re-pool. Résoudre à chaque usage pertinent.
- Des collections de contacts physiques sont valides dans le callback, pas au-delà. Ne pas conserver de callback/event externe vers un module dynamique dont la vie a fini.
- `PURR_LEAKS_CHECK` dans Editor permet la traque d'allocations sur certaines versions ; compiler et vérifier la directive avant de recommander.

## Tests
1000 spawns/despawns répétés, rollback tous les 3 ticks, long replay, pool reuse, double dispose, collision contact expired, heap allocation delta et profil history.
