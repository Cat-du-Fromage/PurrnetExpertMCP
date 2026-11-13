# PurrNet classique — contrat technique et anti-patterns

Sources vérifiées :
- https://purrnet.dev/docs/systems-and-modules/network-modules/common-pitfalls
- https://purrnet.dev/docs/systems-and-modules/network-manager/network-rules
- https://purrnet.dev/docs/systems-and-modules/remote-procedure-call-rpc
- https://purrnet.dev/docs/systems-and-modules/network-modules/sync-types/syncvar
- https://purrnet.dev/docs/systems-and-modules/network-identity/spawning-and-despawning

**Attention** : ces recommandations visent le modèle `NetworkIdentity` normal. Pour `PredictedIdentity`, lire `purrdiction-best-practices.md` avant d'utiliser un sync type ou un RPC.

## Modules : règles documentées obligatoires

1. `NetworkModule`/`SyncVar`/`SyncList`/`SyncDictionary`/etc. sont des **champs ou propriétés** de `NetworkIdentity`/`NetworkBehaviour` (ou des modules statiquement imbriqués) ; pas de `List<SyncVar<T>>`, tableaux de modules, instanciation dynamique comme technique de collection de modules.
2. Valeur par défaut et initialisation via constructeur/déclaration ou `OnInitializeModules()` **avant attribution réseau** ; ne **jamais** remplacer un objet module après son spawn.
3. Imbrication possible, mais **acyclique** (pas de module A→B→A). La sérialisation Inspector exige public ou `[SerializeField]` selon module.
4. Événements `OnSpawned`, `OnOwnerChanged`, `OnDespawned` et abonnements/désabonnements respectent leur cycle ; vérifier signature exacte en package. Ne pas supposer un callback unique en host.
5. `ownerAuth`, `ownerOnly`, intervalles, callbacks `onChanged`, sync types avancés : lire **chaque** page correspondante et ses restrictions, pas une généralisation naïve à tous les modules.

## RPC / autorité / événements

- `[ServerRpc]`: requête client→serveur ; `[ObserversRpc]`: vers observateurs ; `[TargetRpc]`: vers `PlayerID` ciblé. Conditions (`RequireOwnership`, `RequireServer`, `RunLocally`, `BufferLast`, `Channel`, `CompressionLevel`, `MtuExceeded`, `Immediate`) varient par attribut ; vérifier signatures/version.
- RPC **événement** non équivalent à état durable : pour late join, état persistant répliqué ou solution buffer adaptée. Ne pas supposer que `BufferLast` reconstruit tout l'historique.
- `Network Rules` contrôlent spawn, despawn, propriété, visibilité, appel et autorisation de sync ; la permission d'appeler ne valide **pas** la distance d'interaction, l'argent, les dommages ni les cooldowns. Cas client-owner/non-owner/server/host/dedicated à tester.
- Dedicated server ≠ host : pas de client local ; un `[ObserversRpc]` sans `RunLocally` ne lance pas automatiquement son corps sur le serveur. Pour initialisation serveur, préférer branche serveur dédiée ou `RunLocally` justifié ; documenter les risques de double exécution host.

## Spawn, scene, visibility et références

- `Instantiate()` / `Destroy()` suivent les règles PurrNet pour objets avec `NetworkIdentity`, network prefab/scene et droits ; vérifier `NetworkManager`/Network Prefabs et visibilité avant de diagnostiquer.
- Les `NetworkId` ou types supportés servent de références répliquées lorsqu'un GameObject/Transform n'est pas packable tel quel ; inspecter BitPacker réel.
- Scene Management, Addressables, network visibility (distance/whitelist), owner-only data, scene-scoped assets, pooling et reconnection ont des pages distinctes. Vérifier chaque sous-système utilisé plutôt que supposer un comportement identique au modèle NGO/Mirror.
- Tester scene load/unload, joueur rejoignant tard, déconnexion/reconnexion et identités dormantes ; subscriptions propres.

## Transport, sécurité et performance

- Vérifier protocole réel (UDP / WebTransport WS/WSS / Steam / composite), ports internes/externes, scénarios WebGL et réseau local. `StartClient` peut rester initialement Disconnected avant de passer Connecting ; éviter les retries instantanés (cf. Edgegap).
- Pas de secrets côté client ou dans repo ; authentification, rate limiting et validation d'actions server. `Unsafe`/`Everyone` = tolérance prototypage, non validation de sécurité.
- Profiling/BitPacker/Compression/MTU : limiter messages répétés et payloads ; choisir channel selon sémantique, ne pas optimiser sans mesures.
- Respecter les frontières PurrDiction : modules/objets `NetworkIdentity` peuvent exister pour chat/UI autour d'un prefab prédit sur versions compatibles, **pas** pour son état réconcilié.

## Revue avant PR

Pour chaque script : package exact + classe parent + côté exécution + autorité du write + type état/événement + régime late join + ownership + serialized references + test 2 clients + config inspector + version source.
