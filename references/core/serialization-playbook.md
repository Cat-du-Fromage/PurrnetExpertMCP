# Sérialisation PurrNet : parcours de diagnostic et recettes

**Docs** : [Custom types](https://purrnet.dev/docs/systems-and-modules/bitpacker-serialization/networking-custom-classes-structs-and-types), [Async](https://purrnet.dev/docs/systems-and-modules/bitpacker-serialization/async-serialization-packing), [Delta](https://purrnet.dev/docs/systems-and-modules/bitpacker-serialization/delta-packers), [SyncBigData](https://purrnet.dev/docs/systems-and-modules/network-modules/syncbigdata), [Type Hash Resolver](https://purrnet.dev/docs/tools/type-hash-resolver).

## Quel mécanisme choisir ?

- Primitive, struct ou classe supportée : packer/codegen automatiquement si réellement enregistré.
- `IPackedAuto` : expliciter la prise en charge d'un type qui doit être auto-packed, y compris Broadcast hors NetworkBehaviour.
- `IPackedSimple` / `IPacked` : serializer manuel quand le format est sous contrôle. Inspecter `Packer` et `BitPacker` installés pour la vraie signature ; ne pas inventer les surcharges.
- `IAsyncPackable` : préparation avant pack et réhydratation après unpack, par exemple Addressables; `[DontPack]` retire les références non transférables du payload.
- `SyncBigData` / `SyncTextureFile` : octets volumineux et asynchrones à débit configuré ; la réception n'est pas immédiate, prévoir état de téléchargement/annulation.

## Pseudo-flux explicite `IAsyncPackable`

1. Encoder un **identifiant stable et autorisé** (pas seulement le nom d'un GameObject susceptible de se répéter).
2. `PrepareForPackAsync()` récupère et prépare les données avant émission; ne pas tenir un lock Unity pendant un await.
3. Seuls les champs packables traversent le réseau; les champs `[DontPack]` sont absents.
4. `PrepareAfterUnpackAsync()` retrouve la ressource locale, gère annulation/non-disponibilité et rétablit les références côté destinataire.
5. Tests sur échec de chargement, asset manquant, différence de plateforme/Addressable catalog, AOT/IL2CPP, reconnect.

## Debugging type hash / non-registered

Tools → PurrNet → Analysis → **Type Hash Resolver** : entrer id decimal signé/non-signé ou `0x...`; vérifier type, assembly, enregistrement. Le resolver ne modifie ni code ni registres : il identifie. Pour une erreur AOT, regarder l'assemblage et le packer généré avant d'ajouter une réflexion runtime coûteuse.

## Contraintes de sécurité

Limites de taille, structure imbriquée, contenu non fiable, quotas, timeouts, mémoire; ne pas envoyer des `Transform`/`GameObject` arbitraires hors d'un NetworkIdentity enregistré. Pour les objets prédits, état/input transmettent des IDs `PredictedObjectID` plutôt que des références GameObject susceptibles d'être recréées par rollback.

## Test

Cold join, late join, ownership transfer, payload > MTU, fichier tronqué, téléchargement interrompu, release Addressables, changement de code/branches et plateforme. Mesurer allocations et débit avec Bandwidth Profiler.
