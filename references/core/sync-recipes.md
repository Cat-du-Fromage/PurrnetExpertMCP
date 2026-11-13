# Sync Types Recipes: Choose, Implement, Validate

**Sources** : [SyncVar](https://purrnet.dev/docs/systems-and-modules/network-modules/sync-types/syncvar), [ValidatedSyncVar](https://purrnet.dev/docs/systems-and-modules/network-modules/sync-types/validated-syncvar), [Owner Only](https://purrnet.dev/docs/systems-and-modules/network-modules/owner-only), [SyncInput](https://purrnet.dev/docs/systems-and-modules/network-modules/sync-types/syncinput), [SyncEvent](https://purrnet.dev/docs/systems-and-modules/network-modules/sync-types/syncevent), [Common Pitfalls](https://purrnet.dev/docs/systems-and-modules/network-modules/common-pitfalls). See also `core/sync-types.md` and `core/serialization-advanced.md`. The examples were not compiled in Unity. Verify signatures in the installed package.

## 1. Decide on the object to be replicated

| Nature de l'information | First choice | Rejection/control |
|---|---|---|
| Health, score, persistent condition | `SyncVar<T>` | Update by the authority, snapshot for late join |
| Table of objects/inventory | `SyncList<T>` or other sync collections | Serializable elements; never a **module list** `List<SyncVar<...>>` |
| Immediate local change with server validation | `ValidatedSyncVar<T>` | Reject callback; actual server authority |
| One-time event without condition to be kept | `SyncEvent<T>` | Do not replace last state for late join |
| Continuous inputs to server logic | `SyncInput<T>` | Accepts network delay without client-side prediction |
| Countdown | `SyncTimer` | Tick/reconciliation interval and authority |
| Private value of the owner | `ownerOnly: true` on a module | Don't forget an already disclosed value |
| Input and state to predict/rollback | PurrDiction `INPUT/STATE` | Do not put `SyncVar` in the predicted simulation |

## 2. Synchronized Health: Minimum example from documented APIs

```csharp
using PurrNet;
using UnityEngine;

public class ExampleHealth : NetworkBehaviour
{
    private SyncVar<int> _health = new(100);

    protected override void OnSpawned(bool asServer)
    {
        _health.onChanged += HealthChanged;
        if (asServer) _health.value = 100;
    }

    private void HealthChanged(int newHealth)
    {
        Debug.Log($"Health updated: {newHealth}");
    }
}
```

Do not copy this snippet as it is into a real system: provide a subscriber according to the available callback, limited public access, authenticated damage request, respawn conditions and host test (double callback `OnSpawned(bool)`). Damage should not **never** be accepted as a new value decreed by a client. Do not reset health to 100 if a polarized or reconnected object should keep its state: explicitly choose an initialization policy.

## 3. `ownerOnly`: example and privacy trap

```csharp
private SyncList<int> _inventory = new(ownerOnly: true);
private SyncVar<int> _gold = new(0, ownerOnly: true);
```

The module is invisible to non-owners, even if the object is observed. **During a ownership transfer**, the previous owner retains his local copy of the last state. Do not transfer ownership on the assumption that the client's memory is erased; first purg the sensitive data or re-build the property model (a private identity per player), with a real transfer test. A value sent to the client can be copied even after cleaning; never transmit a secret that must not be discovered.

## 4. ValidatedSyncVar: workflow to test

- The owner client writes optimistically; the server authority checks with `serverValidation` and confirms or rejects; `onValidationFail` is owner-side.
- A range validation is not business validation: purchases check money, stock, cooldown, transaction and owner in the server state.
- Tester owner absent, transfer owner, old quick changes/ACK, latency and falsified client.

## 5. Conditions of validity for each recipe

1. Module declared **in a field/property of identity**, initialized before connection/spawn (`OnInitializeModules()` possible). It cannot be replaced after spawn, nor placed in a collection of modules.
2. Compare `ownerAuth` (power to write) and `ownerOnly` (recipients), and Network Rules/Network Visibility.
3. For an event, specify whether a late join should see an earlier state, otherwise use an extra durable Sync Type.
4. Check serializer, observe, permissions, initial status, server-only, host, two clients, late join and reconnection.
