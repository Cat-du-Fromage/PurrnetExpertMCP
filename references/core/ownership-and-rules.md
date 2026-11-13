# Autorité, ownership et Network Rules

**Source officielle** : `systems-and-modules/network-manager/network-rules.md`, `systems-and-modules/network-identity/ownership.md`, `network-identity/spawning-and-despawning/client-spawning-validation.md`, `terminology/server-auth-safe.md`, `terminology/client-auth-everyone-unsafe.md`.

- Chaque mécanisme doit définir initiateur, acteur autorisé, validation, données autoritaires et récepteurs. Être owner n'implique pas être autorisé à faire *toutes* les opérations sur les enfants/identités.
- `Network Rules` influencent spawn, despawn, ownership, RPC et synchronisation. Une règle `Everyone` ou `Unsafe` accélère le prototypage mais ne garantit **aucune protection anti-triche**; pour une économie/PvP, utiliser validation serveur et permissions restrictives.
- `ServerRpc(RequireOwnership: false)` ouvre plus largement les appels; valider explicitement auteur et conditions. Les options `RequireOwnership` et `RunLocally` peuvent surcharger les rules : vérifier l'attribut réellement installé.
- Spawns client possibles selon rules : vérifier et rejeter préfabs/positions/ownership illégitimes via la validation de spawning; ne pas faire confiance à un `NetworkIdentity` transmis par le client.
- Changement d'owner : traiter initialisation, observateurs, données `ownerOnly`, nettoyage et persistance côté serveur. Pour `ownerOnly` voir `sync-types.md` : l'ancien owner conserve localement sa dernière valeur.
- Les policies PurrDiction règlent **la timeline client**, pas l'autorité serveur; ne pas les confondre avec `Network Rules`.

## Revue hostile
Client non owner appelle RPC, falsifie paramètre, tente achat négatif, spawn un prefab non permis, spamme plusieurs fois le même message. Vérifier serveur dédié et hôte.
