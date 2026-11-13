# Diagnostic PurrNet — arbre de décision

D'abord demander/inspecter : version et commit, modèle host/dédié, transport,
Network Rules, prefab ou scène, logs et étapes de reproduction.

## RPC n'arrive pas

1. Confirmer que l'objet porteur d'une `NetworkIdentity` est bien spawné et
   observable par le destinataire.
2. Identifier l'appelant : serveur, client owner, client non owner, host.
3. Vérifier `Network Rules` et les restrictions des attributs RPC de la version.
4. Confirmer la direction (`ServerRpc`, `ObserversRpc`, `TargetRpc`) et le canal.
5. Ajouter temporairement des logs de rôles, d'identité réseau et de moment
   d'appel, puis tester en serveur dédié + deux clients.

## Double exécution en host

`OnSpawned(bool asServer)` peut être appelé côté serveur ET client dans un
host. Ne pas diagnostiquer automatiquement un bug de duplication : vérifier
le rôle, les `RunLocally` RPC et la logique de callback.

## Objet invisible, disparu ou dupliqué

1. Confirmer prefab enregistré (Network Prefabs) ou identité de scène.
2. Contrôler les règles de spawn/despawn et la visibilité.
3. Vérifier qui appelle `Instantiate()`/`Destroy()`, combien de fois,
   et le modèle de scène/late join.
4. Ne pas ajouter de `Spawn()` emprunté à Mirror sans preuve dans PurrNet.

## SyncVar ou state incorrect

1. Vérifier l'autorité d'écriture (server/owner) et les options (`ownerAuth`,
   `ownerOnly`) prises en charge par la version.
2. Vérifier la sérialisation effective du type.
3. Vérifier le moment de souscription aux événements, les initialisations
   et le démarrage réseau.
4. Tester les valeurs initiales, les changements, puis l'arrivée tardive.

## Références réseau et sérialisation

Ne pas supposer que `Transform` ou `GameObject` se sérialisent directement.
Consulter le code actuel du `BitPacker`, les identifiants réseau et le type
attendu. Le Quick Reference historique suggère `NetworkId` pour certains cas,
mais confirmer le nom/type et les API actuelles.

## Transport / performances

Diagnostiquer latence, perte de paquets, tailles de payload, canaux RPC et
les limites MTU documentées. Adapter la fréquence et le mode de transmission.
Ne pas recommander un transport ou relay « production » sur la seule foi
d'une réponse Discord datée.

## Vérifier un problème historique

Consulter d'abord le changelog officiel de **la version installée** :
https://github.com/PurrNet/PurrNet/blob/release/Assets/PurrNet/CHANGELOG.md
Puis vérifier l'ancienne FAQ :
https://github.com/nmban/Purrnet-Stray_Help/blob/e6140a571228044fe670b500e245f6bb370b2e06/docs/QUICK_REFERENCE.md
Ne pas proposer de « fix de v1.2.1 » comme si ce bug était encore présent.
