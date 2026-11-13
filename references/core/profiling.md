# Performance, bande passante, profils de test

**Sources officielles** : `systems-and-modules/bandwidth-profiler.md`, `readme/performance/`, `systems-and-modules/bitpacker-serialization/`, `plug-n-play-components/network-transform.md`, `network-transform/adaptive-sync.md`, `client-side-prediction/disposable-collections.md`.

- Mesurer avant d'optimiser : octets/s par catégorie/objet, nombre RPC, ticks, correction freq, taille de history, GC, CPU serveur et client. `NetworkTransform` est différent de `PredictedTransform`.
- Réduire les messages à haute fréquence : choisir le bon Sync Type/SyncInput, intervalle/delta, une voie unreliable uniquement si perte acceptable, payloads compressibles et observer sets petits.
- Utiliser visibility et ownerOnly pour **ne pas envoyer** les données non nécessaires. Vérifier fuite de valeurs privées lors des transferts d'owner.
- En PurrDiction, les états volumineux sont dupliqués lors de reconciliation : `Disposable*`, `IDuplicate`, `Dispose`, policy adaptée et de vrais tests rollback.
- Ne pas faire confiance à un benchmark ancien de Stray Help; comparer dans les conditions de build du projet.

## Matrice
2/4/8 clients selon cible, 60/120 ms ping, 0/1/5% pertes, jitter, tick 30/60, FPS 30/144, dédié headless, spikes d'entités, late joins. Reporter les mesures réellement observées, sans inventer de chiffres.
