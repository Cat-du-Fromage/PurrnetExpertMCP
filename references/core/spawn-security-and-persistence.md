# Spawning client, server validation and persistent objects

**Official source**: `systems-and-modules/network-identity/spawning-and-despawning/client-spawning-validation.md`, `systems-and-modules/network-identity/dont-destroy-on-load.md`, `systems-and-modules/network-manager/network-rules.md`.

## When to use and when to avoid it

- If the rules allow the Spawn client, **record a server validator** for prefabs, quotas and permissions. Do not consider the fact that an object is observed as proof of authorization.
- If only the servers are spawning, keep the Intent validation on the server side (RPC, command, INPUT); do not add a useless client spawn validator.
- `SpawnPacket` can represent a **partial creation** of identities: `TryGetRawPrefab` confirms simple creation before giving the prefab. Reject or explicitly treat partial packages according to design; do not interpret them as a simple guaranteed prefab.
- The `Network Rules` have several presets: `Unsafe` is useful for prototypes **unreliable**, `ServerStrict` for authoritative server, `ServerOwner` as compromise. The exact names must be checked in the installed package.

## Official example adapted — minimum validator, NOT production

```csharp
using PurrNet;
using PurrNet.Modules;
using UnityEngine;

public sealed class BasicSpawnGate : MonoBehaviour
{
    [SerializeField] private NetworkManager manager;

    private void OnEnable()
    {
        if (manager != null)
            manager.onClientSpawnValidate += Validate;
    }

    private void OnDisable()
    {
        if (manager != null)
            manager.onClientSpawnValidate -= Validate;
    }

    private bool Validate(PlayerID player, SpawnPacket packet)
    {
        if (!packet.TryGetRawPrefab(manager, out var prefab))
            return false;

        // Check the allowlist, quota, player permissions, scene and gameplay rules before accepting a spawn.
        return false;
    }
}
```

**Important**: it is a *signature sketch*, not a ready-to-paste solution: no client spawn passes until the permission policy is implemented. You must verify in Unity that `onClientSpawnValidate` exists on the version actually installed. Examples of the official documentation allow any simple prefab: this is not a sufficient security policy.

## `DontDestroyOnLoad` and Not Spawned

- A `NetworkIdentity` moved to the DDOL scene must be moved there **before starting the network**, for example during `Awake` according to the doc.
- If the `NetworkManager` does not reside itself in the DDOL scene, activate `NetworkRules.alwaysIncludeDontDestroyOnLoadScene` in the stage rules. Otherwise the persistent object can display **Not Spawned**.
- Additive scene deletion and reconnection require specific tests: do not duplicate a NetworkManager and do not persist two copies of the same identity.

## Validation observable

1. Authorized client: registered prefab and valid quota; both clients see the object.
2. Unauthorized client: the server refuses the package, the locally speculative object disappears, no persistent data leaks.
3. Partial Spawn: explicitly designed behavior (refusal or treatment), without crash.
4. Change of scene: DDOL identity always `spawned`, no duplicate; reverse test with DDOL rule disabled.
5. Reconnect/late join: durable condition and correct observations.

**Compilation status**: adapted example of the doc, not compiled with Unity in this pack.
