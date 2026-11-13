# Concepts and API map — ports of entry verified

This is a ** concept directory**, not a replacement of signatures of the
installed version. Links: `source-map.md`.

| Need | PurrNet | Verification point |
| --- | --- | --- |
| Network input | `NetworkManager`, transports, Network Prefabs, Network Rules | `systems-and-modules/network-manager/` |
| Network Script | `NetworkBehaviour`, `NetworkIdentity` | `systems-and-modules/network-identity/` |
| Server/client/host side | `OnSpawned(bool asServer)` | `networkbehaviour.md` + source exact |
| Client to server call | `[ServerRpc]` | `remote-procedure-call-rpc/README.md` |
| Call to observers | `[ObserversRpc]` | same page |
| Targeted call | `[TargetRpc]`, `PlayerID` | same page |
| Synchronised status | `SyncVar<T>`, `.value`, `.onChanged` | `sync-types/syncvar.md` |
| Listes / dictionnaires | `SyncList`, `SyncDictionary` | `network-modules/sync-types/` |
| Spawning | `Instantiate`, `Destroy`, Network Identity/Prefabs | `spawning-and-despawning/README.md` |
| Security | `Network Rules`, `ServerStrict`, `ServerOwner`, `Unsafe` | `network-rules.md` |
| Mouvement / prediction | `PurrDiction` (additional package) | `client-side-prediction/` |

## Mini-conceptual extract from official documentation

To be adapted to the rules of authority and local revision:

```csharp
using PurrNet;

public class ExampleRpc : NetworkBehaviour
{
    [ServerRpc]
    private void RequestAction()
    {
        NotifyObservers();
    }

    [ObserversRpc]
    private void NotifyObservers()
    {
        // Play the visual effect on observing clients.
    }
}
```

Attribute reference source:
https://github.com/PurrNet/PurrDocs/blob/main/systems-and-modules/remote-procedure-call-rpc/README.md

**Do not** say this code has been compiled. `ServerRpc` depends on the object
Check that the object has spawned and that the Network Rules authorize the calling client.

## Alerte migrateur

- Mirror: Do not automatically use `[Command]` / `NetworkServer.Spawn()`.
- Unity Netcode for GameObjects: do not substitute `NetworkVariable<T>` or
  `ServerRpcParams` without explicit confirmation.
- FishNet: Do not transpose ownership methods or hooks carrying
  a similar name without verification in PurrNet.

## Conseils de synchronisation

- A change to the critical gameplay must have clear authority.
- The user interface can react to the replicated state; the IU is not the
  a source of professional truth.
- Document behavior during late join and after reconnexion.
- Separate one-time calls (RPC) from durable (SyncVar or other)
  adapted mechanism).
- Do not loop sync `Transform`/`GameObject` through the
  unverified serializers.
