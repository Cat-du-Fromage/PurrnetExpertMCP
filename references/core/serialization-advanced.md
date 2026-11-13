# Custom and asynchronous serialization, delta and large payloads

Official: `systems-and-modules/bitpacker-serialization/networking-custom-classes-structs-and-types.md`, `async-serialization-packing.md`, `delta-packers.md`, `systems-and-modules/network-modules/syncbigdata/README.md`, `synctexturefile.md`.

- Prefer generated serializers for supported types. `IPackedAuto` helps codegen registration/packing; `IPackedSimple` and `IPacked` support custom pathways. **Do not invent generic method signatures**: look at the installed Packer/BitPacker code and generated packers.
- `IAsyncPackable` has `PrepareForPackAsync` before sending and `PrepareAfterUnpackAsync` after unpack; both return `Task<IAsyncPackable>` per current docs. `[DontPack]` excludes non-serializable fields; resolving local references in `PrepareAfterUnpackAsync` requires stable identifiers, not scene-name lookups in production.
- Delta packers: evaluate baseline correctness, equality/diff behavior and schema evolution. Check IL2CPP/AOT, registration and assembly codegen; test cold startup and late join.
- **SyncBigData** is a rate-limited asynchronous module for larger byte arrays; receiver readiness is delayed. It handles ownership loss/reconnect as documented. `SyncTextureFile` is a related specialized wrapper; inspect installed API before coding.
- Large files do not belong in repeated standard RPC calls. Consider security: max size, data validation, malicious compression ratios, quotas and cancellation; profile throughput before tuning.
- Troubleshooting: serializer hash/registration errors → **Type Hash Resolver**, actual namespace/assembly/packer; MTU/drops → Bandwidth Profiler.
