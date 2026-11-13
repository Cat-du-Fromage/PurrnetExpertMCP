# Sérialisation et BitPacker

**Sources officielles** : `systems-and-modules/bitpacker-serialization/networking-custom-classes-structs-and-types.md`, `async-serialization-packing.md`, `delta-packers.md`, `systems-and-modules/code-stripping.md`, `systems-and-modules/network-manager/network-assets.md`.

- PurrNet peut générer des packers au compile time; valider la version, les assemblies et le codegen avant d'implémenter un packer manuel.
- `IPackedAuto` : types automatiques pour data personnalisée; `IPackedSimple` / `IPacked` quand la doc et la signature exigent une sérialisation contrôlée. Ne pas inventer de packer pour une classe avec références Unity ou cycles sans vérifier les limites.
- Packer/BitPacker manuel : lecture et écriture **dans le même ordre**, tailles bornées, entrées non fiables et versioning des messages. Sur réseau unreliable, traiter fragmentation/MTU et payloads trop gros.
- Les collections peuvent allouer et affecter le delta; mesurer la taille des snapshots dans Bandwidth Profiler et tester des mutations intermédiaires, la suppression et le late join.
- `NetworkId`, objets Unity et références de classes : vérifier sérialisation supportée dans le package, pas de `Transform` arbitraire à travers RPC. Les types `IPredictedData` ont en plus des contraintes de copie/dispose propres à l'historique.
- Examiner `Code stripping` pour build IL2CPP/AOT et les types/packers générés; un succès en Editor ne suffit pas.

## Tests
Round-trip binaire, mauvais payload, valeurs extrêmes, enums/version de structure, allocations, IL2CPP, grande collection, plusieurs clients et late join.
