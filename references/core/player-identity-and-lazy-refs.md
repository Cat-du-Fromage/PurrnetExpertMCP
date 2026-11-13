# PlayerIdentity, SyncLazyRef, ordre des événements

**Sources officielles** : `systems-and-modules/network-identity/playeridentity.md`, `systems-and-modules/network-modules/sync-types/synclazyref.md`, `systems-and-modules/network-manager/connection-and-player-events.md`.

## Choix rapide

| Besoin | Privilégier | Attention |
| --- | --- | --- |
| Retrouver la représentation d'un `PlayerID` | `PlayerIdentity<T>.TryGetPlayer` | Joueur authentifié n'implique pas forcément scène prête |
| Retrouver le joueur local | `PlayerIdentity<T>.TryGetLocal` | Peut être indisponible avant l'attribution locale |
| Énumérer les joueurs | `PlayerIdentity<T>.allPlayers` | Registry vivant; gérer spawn/déspawn/reconnect |
| Référence d'identité entre scènes | `SyncLazyRef<T>` | Référence résolue plus tard, peut redevenir `null` |
| Référence d'objet prédit | `PredictedObjectID` | Ne pas mélanger avec `SyncLazyRef` classique |

## Exemples ciblés (API à vérifier sur la version installée)

```csharp
// Sur une classe représentant le joueur :
public class PlayerPawn : PlayerIdentity<PlayerPawn> { }

// Depuis la logique serveur, une fois le PlayerID connu :
if (PlayerPawn.TryGetPlayer(playerId, out var player))
{
    // Utiliser player dans une logique autorisée, pas sur le client par confiance.
}
```

```csharp
// Dans une NetworkBehaviour/NetworkIdentity :
private SyncLazyRef<NetworkIdentity> _target = new();

protected override void OnSpawned(bool asServer)
{
    _target.onChanged += OnTargetChanged;
    if (asServer) _target.value = targetIdentity; // Doit déjà être spawné.
}

protected override void OnDespawned(bool asServer)
{
    _target.onChanged -= OnTargetChanged;
}

private void OnTargetChanged(NetworkIdentity oldValue, NetworkIdentity newValue)
{
    // newValue == null : cible absente, scène non chargée ou cible despawned.
}
```

Ces snippets illustrent des signatures tirées des docs ; ils nécessitent des champs définis et un contrôle dans Unity. Pour `SyncLazyRef` la référence est portée par `GlobalNetworkID` (scène + NetworkID). Le **cible doit être spawné au moment de l'assignation**, même si le destinataire peut la résoudre plus tard. Au déspawn/unload la valeur résolue peut redevenir `null`, puis se résoudre après retour.

## Séquencement des événements

`onClientConnectionState=Connected` (transport) → authentification → `onPlayerJoined`/réception de `PlayerID` → présence dans la scène → `onPlayerLoadedScene` → observations par identité. Il ne s'agit pas d'un ordre global immuable de tous les callbacks, mais de **conditions distinctes** ; `onPlayerJoinedScene` signale l'appartenance, pas la fin du chargement. Les callbacks avec `asServer` peuvent apparaître deux fois en host. Un abonnement après l'arrivée des joueurs doit lire `networkManager.players` car les événements passés ne sont pas rejoués.

## Tests

Client rejoint en retard, premier join puis reconnexion via cookie, scène chargée après l'attribution `PlayerID`, cible dans une autre scène non chargée, déchargement/rechargement de cible, transfert d'owner, host sans double initialisation.

**Statut** : exemples illustratifs non compilés avec Unity ici.
