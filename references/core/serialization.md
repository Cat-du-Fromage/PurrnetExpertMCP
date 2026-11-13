# Serialization and BitPacker

**Official sources**: `systems-and-modules/bitpacker-serialization/networking-custom-classes-structs-and-types.md`, `async-serialization-packing.md`, `delta-packers.md`, `systems-and-modules/code-stripping.md`, `systems-and-modules/network-manager/network-assets.md`.

- PurrNet can generate packers at the time compile; validate version, assembly and codegen before implementing a manual packer.
- `IPackedAuto`: automatic types for custom data; `IPackedSimple` / `IPacked` when doc and signature require controlled serialization. Do not invent a packer for a class with Unity references or cycles without checking the limits.
- Manual Packer/BitPacker: read and write **in the same order**, bounded sizes, unreliable input and message versioning. On unreliable network, handle fragmentation/MTU and payloads too big.
- Collections can allocate and affect the delta; measure the size of snapshots in Bandwidth Profiler and test intermediate mutations, suppression and late join.
- `NetworkId`, Unity objects and class references: check serialization supported in the package, no arbitrary `Transform` through RPC. `IPredictedData` types have in addition copy/dispose constraints specific to history.
- Examine `Code stripping` for build IL2CPP/AOT and generated types/packers; Editor success is not enough.

## Tests
Round-trip binary, bad payload, extreme values, enums/structural version, allocations, IL2CPP, large collection, multiple clients and late join.
