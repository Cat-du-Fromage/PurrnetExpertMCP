# RPC et Broadcasts

**Sources officielles** : `systems-and-modules/remote-procedure-call-rpc/README.md`, `generic-rpc.md`, `static-rpc.md`, `awaitable-rpc.md`, `fully-local-rpc.md`, `pre-post-processors.md`, `systems-and-modules/broadcast.md`.

## Décision
- **`ServerRpc`** : intention client → serveur, puis autorisation/validation; ne pas transmettre directement « dégâts appliqués » comme faits établis.
- **`ObserversRpc`** : serveur → observers de l'identité (ou autre selon Network Rules); la logique appelée sur observers ne s'exécute pas automatiquement sur serveur dédié; `RunLocally` ou traitement serveur explicite pour le state serveur.
- **`TargetRpc`** : vers un client ciblé, `PlayerID` paramètre selon signature de la version. Les appels bufferisés peuvent aider certaines notifications de late join, mais ne remplacent pas la synchronisation d'un état durable.
- **Broadcast** : message non lié à une identité (ex. lobby/connexion); abonnement/désabonnement au NetworkManager, distinguer scope Connection vs Player (avant/après authentification).

Les RPC peuvent être **statiques, génériques, awaitables et coroutine** selon version/codegen. Examiner `RequireOwnership`, `RequireServer`, `RunLocally`, `BufferLast`, `Channel`, `CompressionLevel`, `MtuExceeded`, `Immediate`, arguments et la policy de Network Rules. `Unreliable` ne convient pas aux événements dont la perte modifie durablement le gameplay. Décréter explicitement l'idempotence et la validation des retries.

**PurrDiction** : jamais envoyer un RPC ordinaire depuis `Simulate` sur chaque replay. Une demande RPC depuis une UI hors simulation peut déclencher un spawn serveur de predicted hierarchy, mais n'est pas une prédiction locale; voir `references/prediction/hierarchy-and-parenting.md`.

## Tests
Latence/perte sur Reliable/Unreliable, message à non-observer, absence d'owner, host doublonnage, dédié et late join; inspecter bande passante pour RPC fréquents.
