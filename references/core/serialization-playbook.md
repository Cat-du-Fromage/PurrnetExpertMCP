# Serialization PurrNet: diagnostic path and recipes

**Docs** : [Custom types](https://purrnet.dev/docs/systems-and-modules/bitpacker-serialization/networking-custom-classes-structs-and-types), [Async](https://purrnet.dev/docs/systems-and-modules/bitpacker-serialization/async-serialization-packing), [Delta](https://purrnet.dev/docs/systems-and-modules/bitpacker-serialization/delta-packers), [SyncBigData](https://purrnet.dev/docs/systems-and-modules/network-modules/syncbigdata), [Type Hash Resolver](https://purrnet.dev/docs/tools/type-hash-resolver).

## Which mechanism to choose?

- Primitive, struct or supported class: packer/codegen automatically if actually saved.
- `IPackedAuto`: Explain support for a type that needs to be auto-packed, including Broadcast outside NetworkBehaviour.
- `IPackedSimple` / `IPacked`: manual serializer when format is under control. Inspect `Packer` and `BitPacker` installed for real signature; do not invent overloads.
- `IAsyncPackable`: prepack preparation and rehydration after a pack, e.g. Addressables; `[DontPack]` removes nontransferable references from payload.
- `SyncBigData` / `SyncTextureFile`: large and asynchronous bytes with configured flow rate; reception is not immediate, provide download/cancell status.

## Pseudo-flux explicite `IAsyncPackable`

1. Encode a stable and authorized **identifier** (not only the name of a GameObject that can be repeated).
2. `PrepareForPackAsync()` recovers and prepares data before emission; do not hold a lock Unity during a wave.
3. Only packable fields cross the network; `[DontPack]` fields are missing.
4. `PrepareAfterUnpackAsync()` retrieves the local resource, manages cancellation/unavailability and restores recipient-side references.
5. Load failure tests, missing asset, platform difference/Addressable catalog, AOT/IL2CPP, reconnect.

## Debugging type hash / not registered

Tools → PurrNet → Analysis → **Type Hash Resolver**: enter id decimal signed/unsigned or `0x...`; check type, assembly, record. The resolver does not change code or register: it identifies. For an AOT error, look at the assembly and packager generated before adding an expensive runtime reflection.

## Safety constraints

Size limits, nested structure, unreliable content, quotas, timeouts, memory; do not send arbitrary `Transform`/`GameObject` out of a registered NetworkIdentity. For predicted objects, state/input transmit `PredictedObjectID` IDs rather than GameObject references that can be recreated by rollback.

## Test

Cold join, late join, ownership transfer, payload > MTU, truncated file, interrupted download, release Addressables, code/branch change and platform. Measure allocations and bitrate with Bandwidth Profiler.
