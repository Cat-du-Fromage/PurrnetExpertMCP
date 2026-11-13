# Études de cas : symptôme → test qui départage les causes

Chaque exemple est un **protocole**, non une déclaration de bug courant. Version officielle et signature locale restent obligatoires.

## Cas A — « Mes RPC s'exécutent deux fois sur l'hôte »

**Archives** : Stray `QUICK_REFERENCE` note un fix `ObserversRpc(runLocally: true)` en v1.2.0 et changelog d'autres fixes RPC host.

- Trois hypothèses : (1) vieux bug sur package effectivement antérieur ; (2) code invoqué une fois pour client ET une fois serveur sur host ; (3) deux appels au RPC, ou deux NetworkManagers.
- Tracer log à *l'invocation* et *à l'exécution*. Pour un `NetworkBehaviour` avec `OnSpawned(bool asServer)`, vérifier les deux chemins; tracer `runLocally` et destinataire; vérifier que les effets serveur nécessaires ne sont pas uniquement dans un ObserversRpc côté clients.
- Test : même code en host + dedicated + deux clients. **Ne jamais** retirer `runLocally` sans vérifier si le dedicated dépend de la méthode : le monde pourrait devenir vide.
- Validation : méthode appelée pour les bons destinataires; état authoritative ne dépend pas d'un client local.

## Cas B — « Un nouveau client rejoint mais son inventaire est vide »

**Archive** : note historique v1.5.0 SyncList late join, plus correctifs SyncVar/collections jusqu'à v1.20.0.

- Capturer le contenu serveur **avant** le join, le propriétaire, `ownerOnly`, l'autorité d'écriture, les types sérialisés, l'existence de l'objet sur l'observer et le chargement de la scène.
- Test discriminant : client propriétaire vs client non-owner; client arrivé avant/après spawn; `ownerOnly` doit cacher les données au non-owner ; `OnObserverAdded`/snapshot doivent servir le destinataire autorisé.
- Pour changement d'ownership : l'ancien propriétaire peut **conserver localement la dernière valeur vue** — le secret doit être nettoyé avant transfert si besoin; ne présumer aucune purge automatique côté ancien owner.
- Validation : inventaire correct pour nouveau propriétaire, pas de divulgation au tiers, pas de vieux état après pooling.

## Cas C — « Le player spawne dans une mauvaise scène / RPC reçu avant scène »

**Archive** : spawner-scene v1.3.3, buffered RPC trop tôt v1.9.3, révision plus large 1.20.0.

- Séparer : appartenance scène (`onPlayerJoinedScene`), **scène chargée** (`onPlayerLoadedScene`), observation d'objet (`OnObserverAdded`) et première donnée de spawn.
- Vérifier NetworkScenePrefabs et NetworkSceneAssets, scène d'instanciation, Build Settings, et registre global prioritaire.
- Éviter un `WaitForSeconds` « magique » : préférer événement de readiness, un état durable ou l'inclusion des données dès le spawn via `OnSerialize`/`OnDeserialize` si l'API installée le permet.
- Validation : deux clients ayant des scènes chargées dans des ordres différents, late join, unload/reload, client sans l'objet caché.

## Cas D — « Mon joueur tremble : WebTransport, NetworkRigidbody, NetworkTransform »

**Archive** : WebTransport/NetworkTransform fix 1.2.1; non-controller update 1.10.2; rework 1.20.0.

- Distinguer de la *prédiction* PurrDiction : si `PredictedTransform`, charger `prediction/best-practices.md`, pas uniquement `NetworkTransform` classique.
- Mesurer : writer owner/server, double writer (`NetworkTransform`, Rigidbody/CharacterController), buffers/jitter, packet loss, transport WebSocket vs UDP, update phase, payload MTU.
- Test : un objet qui bouge en ligne droite, puis changement de parent, teleport et changement owner ; comparer host, remote, WebGL.
- Validation : taux de corrections/jumps, exactitude sur remote après late join et reconnexion; profiler enregistré.

## Cas E — « Les nouveaux plugins/compilations ne marchent pas : Steam CS1061, GetClientPayload, IL2CPP »

**Archive** : FAQ propose un redémarrage pour SteamWorks CS1061; changelog 1.13.2 renomme un override d'auth et 1.19.1 note correctifs build.

- Capturer le **texte et la localisation** de l'erreur C#/ILPP, la version Unity, les asmdefs, packages, backend Mono/IL2CPP; ne pas choisir un remède par nom d'exception seul.
- Dans un authenticator, `GetClientPayload` remplace un ancien typo `GetClientPlayload` à partir d'une révision historique : contrôler la signature de la classe réellement résolue.
- Un redémarrage Unity/Hub peut rafraîchir l'import Steamworks, mais ne répare pas une API absente ni une version de package contradictoire.
- Validation : compilation Editor + build target, chargement runtime, test de la fonction après compilation.

## Cas F — « Une balle predicted apparaît puis disparaît »

**Archive** : PurrDiction a des fixes de hierarchy, pooling et inputs dans la période v1.2.x–v1.3.x, mais ce n'est pas une explication automatique de tout despawn.

- Vérifier que le spawn est demandé via `INPUT`, exécuté dans `Simulate` et confirmé par la **simulation serveur**; un clic Unity/UI hors simulation peut créer un objet purement spéculatif.
- Assurer `STATE` restaurable, `PredictedObjectID`, `PredictedHierarchy`, extrapolation des one-shot, politique et trajectoire déterministe.
- Vérifier les composants miroirs NetworkIdentity selon la version PurrDiction distincte de PurrNet.
- Validation : host, client distant, pertes/jitter, late join, spawn/replay/delete, et collision pendant rollback.
