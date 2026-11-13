# Choix RPC / Broadcast / événements et MTU — procédure

**Sources** : [Remote Procedure Calls](https://purrnet.dev/docs/systems-and-modules/remote-procedure-call-rpc), [Network Manager](https://purrnet.dev/docs/systems-and-modules/network-manager), [Broadcasts](https://purrnet.dev/docs/systems-and-modules/broadcast), [Bandwidth Profiler](https://purrnet.dev/docs/systems-and-modules/bandwidth-profiler).

## Direction et sécurité

| Besoin | Mécanisme | Contrôles |
|---|---|---|
| Client demande un achat | `[ServerRpc]` sur NetworkIdentity | Ownership/RequireOwnership selon règles, identité appelant, prix/stock côté serveur |
| Serveur notifie observers | `[ObserversRpc]` | Vérifier qui observe, `BufferLast` pour dernière occurrence seulement |
| Serveur répond à un joueur | `[TargetRpc]` avec `PlayerID` | PlayerID valide/authentifié; visibilité et timing |
| Information sans NetworkIdentity | `Broadcast` | Abonnement/désabonnement, connection vs player scope, validation |
| État durable côté late join | SyncVar/SyncList/State | Éviter de reconstruire un monde depuis une série d'RPC bufferisés |

**Extrait documentaire illustratif** :

```csharp
[ServerRpc(requireOwnership: false)]
private void RequestAction()
{
    // Valider ici l'appelant et les règles métier avant de muter l'état.
}

[ObserversRpc(bufferLast: true)]
private void AnnounceState(int value)
{
    // Ne remplace pas un snapshot complet.
}
```

Les noms exacts/paramètres d'attributs peuvent varier dans le codegen/entre docs ; vérifier la casse/surcharge de **la version installée**. `RunLocally` peut entraîner l'exécution locale ; sur serveur dédié, ne pas mettre tout le spawn ou la génération du monde dans un observer-only callback exécuté uniquement côté client.

## Livraison, fragmentation et volume

- `ReliableOrdered` pour les opérations qui ne doivent pas être perdues; `Unreliable` ou `UnreliableSequenced` pour les états fréquemment remplacés. La sémantique d'`UnreliableSequenced` dépend du transport et du réglage MTU : inspecter code et docs actuels.
- Un payload supérieur à la MTU peut être fragmenté, **promu en fiable** ou abandonné suivant `NetworkManager.mtuExceededBehaviour` ou l'override de RPC. Les fragments perdus peuvent invalider tout le message ; éviter d'utiliser la fragmentation comme protocole de fichier.
- `Immediate` réduit l'attente de flush mais la mise en lot est moins efficace. Mesurer avant d'augmenter son usage.
- Vérifier les pertes dans **Tools/PurrNet/Analysis/Bandwidth Profiler**. Les catégories `Expired`, `Evicted`, `BudgetExceeded`, `SequencedStale` guident le diagnostic.

## Test reproductible

1. Vérifier avec host, client distant, dédié (si pertinent), non-observateur et client non autorisé.
2. Capturer et rejouer un input susceptible d'être perdu; déterminer si un état durable doit être synchronisé.
3. Forcer payload volumineux, variation MTU, perte et latence; relever les messages tombés et bytes/sec.
4. Tester des RPC envoyés avant fin d'auth/scène/observation : ne pas supposer que le destinataire existe déjà.
5. Pour l'audio, l'Animator ou un Transform, évaluer d'abord les composants PurrNet (éviter RPC maison par tick).
