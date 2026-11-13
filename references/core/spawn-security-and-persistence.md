# Spawning client, validation serveur et objets persistants

**Source officielle** : `systems-and-modules/network-identity/spawning-and-despawning/client-spawning-validation.md`, `systems-and-modules/network-identity/dont-destroy-on-load.md`, `systems-and-modules/network-manager/network-rules.md`.

## Quand l'utiliser et quand l'éviter

- Si les règles autorisent le spawn client, **enregistrer un validateur serveur** pour les prefabs, quotas et permissions. Ne pas considérer le fait qu'un objet soit observé comme une preuve d'autorisation.
- Si seuls les serveurs spawnenent, garder la validation d'intention côté serveur (RPC, commande, INPUT) ; ne pas ajouter un validateur de spawn client inutile.
- `SpawnPacket` peut représenter une **création partielle** d'identités : `TryGetRawPrefab` confirme la création simple avant de donner le prefab. Rejeter ou traiter explicitement les packets partiels selon la conception ; ne pas les interpréter comme un simple prefab garanti.
- Les `Network Rules` ont plusieurs presets : `Unsafe` est utile pour prototypes **non fiables**, `ServerStrict` pour serveur autoritaire, `ServerOwner` comme compromis. Les noms exacts doivent être vérifiés dans le package installé.

## Exemple officiel adapté — validateur minimal, PAS production

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

        // Démo : NE PAS retourner true sans vérifier la whitelist, le quota,
        // les droits de ce player, la scène et les règles du jeu.
        return false;
    }
}
```

**Important** : c'est un *squelette de signature*, pas une solution prêt-à-coller : aucun spawn client ne passe tant que la politique de permissions n'est pas implémentée. Il faut vérifier dans Unity que `onClientSpawnValidate` existe sur la version réellement installée. Les exemples de la documentation officielle autorisent tout prefab simple : cela n'est pas une politique de sécurité suffisante.

## `DontDestroyOnLoad` et « Not Spawned »

- Un `NetworkIdentity` déplacé dans la scène DDOL doit y être déplacé **avant le démarrage du réseau**, par exemple pendant `Awake` selon la doc.
- Si le `NetworkManager` ne réside pas lui-même dans la scène DDOL, activer `NetworkRules.alwaysIncludeDontDestroyOnLoadScene` dans les règles de scène. Sinon l'objet persistant peut afficher **Not Spawned**.
- Une suppression de scène additive et une reconnexion exigent des tests spécifiques : ne pas dupliquer un NetworkManager et ne pas persister deux copies d'une même identité.

## Validation observable

1. Client autorisé : prefab inscrit et quota valide ; les deux clients voient l'objet.
2. Client non autorisé : le serveur refuse le paquet, l'objet localement spéculatif disparaît, aucune donnée persistante ne fuit.
3. Spawn partiel : comportement explicitement conçu (refus ou traitement), sans crash.
4. Changement de scène : identité DDOL toujours `spawned`, pas de doublon ; test inverse avec la règle DDOL désactivée.
5. Reconnect/late join : état durable et observations corrects.

**Statut de compilation** : exemple adapté de la doc, non compilé avec Unity dans ce pack.
