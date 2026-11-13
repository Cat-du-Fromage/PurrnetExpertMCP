# Network Modules classiques

**Official sources**: `systems-and-modules/network-modules/README.md`, `common-pitfalls.md`, `owner-only.md`, `sync-types/README.md`.

- Modules are **fields or properties of NetworkIdentity** (or an embedded module); no array/module list, no undeclared dynamic creation.
- `OnInitializeModules()` for initialization/reconfiguration before assigning IDs and first sending. Never reassign a module after its spawn.
- Imbracation of authorized modules into shafts, cycles prohibited. `public`/`[SerializeField]` for exposure Inspector according to type and version.
- Review `NetworkModule`-specific callbacks (`OnSpawned`, `OnOwnerChanged`, `OnDespawned`) and ensure event subscription/unsubscribe; do not assume the same signature as `NetworkBehaviour`.
- `ownerOnly` in a custom module must remain stable; hot change does not erase the previously released state.
- **Do not confuse** with `PredictedModule`, which has *dynamic* modules reconciled during simulation and static roster rules.

## Tests
Embedded module, host/dedie activation, late-join serialization, ownership, pooling, attempt to reassign after spawn and forbidden structure cases.
