# Carte des concepts et API — points d'entrée vérifiés

Ceci est un **annuaire de concepts**, pas un remplacement des signatures de la
version installée. Liens : `source-map.md`.

| Besoin | PurrNet | Point de vérification |
| --- | --- | --- |
| Entrée réseau | `NetworkManager`, transports, Network Prefabs, Network Rules | `systems-and-modules/network-manager/` |
| Script lié au réseau | `NetworkBehaviour`, `NetworkIdentity` | `systems-and-modules/network-identity/` |
| Côté serveur/client/host | `OnSpawned(bool asServer)` | `networkbehaviour.md` + source exact |
| Appel client → serveur | `[ServerRpc]` | `remote-procedure-call-rpc/README.md` |
| Appel vers observateurs | `[ObserversRpc]` | même page |
| Appel ciblé | `[TargetRpc]`, `PlayerID` | même page |
| État synchronisé | `SyncVar<T>`, `.value`, `.onChanged` | `sync-types/syncvar.md` |
| Listes / dictionnaires | `SyncList`, `SyncDictionary` | `network-modules/sync-types/` |
| Spawning | `Instantiate`, `Destroy`, Network Identity/Prefabs | `spawning-and-despawning/README.md` |
| Sécurité | `Network Rules`, `ServerStrict`, `ServerOwner`, `Unsafe` | `network-rules.md` |
| Mouvement / prediction | `PurrDiction` (package complémentaire) | `client-side-prediction/` |

## Mini-extrait conceptuel de la documentation officielle

À adapter aux règles d'autorité et à la révision locale :

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
        // Effet visuel côté observateurs.
    }
}
```

Source de référence des attributs :
https://github.com/PurrNet/PurrDocs/blob/main/systems-and-modules/remote-procedure-call-rpc/README.md

**Ne pas** dire que ce code a été compilé. `ServerRpc` dépend de l'objet
spawné, des règles réseau et de l'autorisation du client appelant.

## Alerte migrateur

- Mirror : ne pas utiliser automatiquement `[Command]` / `NetworkServer.Spawn()`.
- Unity Netcode for GameObjects : ne pas substituer `NetworkVariable<T>` ou
  `ServerRpcParams` sans confirmation explicite.
- FishNet : ne pas transposer des méthodes d'ownership ou des hooks portant
  un nom similaire sans vérification dans PurrNet.

## Conseils de synchronisation

- Une modification du gameplay critique doit avoir une autorité claire.
- L'interface utilisateur peut réagir à l'état répliqué ; l'UI n'est pas la
  source de vérité métier.
- Documenter le comportement lors d'un late join et après reconnexion.
- Séparer les appels ponctuels (RPC) de l'état durable (SyncVar ou autre
  mécanisme adapté).
- Ne pas synchroniser en boucle des `Transform`/`GameObject` à travers des
  sérialiseurs non vérifiés.
