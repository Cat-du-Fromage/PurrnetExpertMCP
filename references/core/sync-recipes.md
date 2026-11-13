# Recettes Sync Types : choisir, implémenter, valider

**Sources** : [SyncVar](https://purrnet.dev/docs/systems-and-modules/network-modules/sync-types/syncvar), [ValidatedSyncVar](https://purrnet.dev/docs/systems-and-modules/network-modules/sync-types/validated-syncvar), [Owner Only](https://purrnet.dev/docs/systems-and-modules/network-modules/owner-only), [SyncInput](https://purrnet.dev/docs/systems-and-modules/network-modules/sync-types/syncinput), [SyncEvent](https://purrnet.dev/docs/systems-and-modules/network-modules/sync-types/syncevent), [Common Pitfalls](https://purrnet.dev/docs/systems-and-modules/network-modules/common-pitfalls). Voir aussi `core/sync-types.md` et `core/serialization-advanced.md`. **Extraits pédagogiques non compilés dans Unity** ; vérifier les signatures dans le package du projet.

## 1. Décider de l'objet à répliquer

| Nature de l'information | Premier choix | Rejet/contrôle |
|---|---|---|
| Santé, score, état persistant | `SyncVar<T>` | Mise à jour par l'autorité, snapshot pour late join |
| Tableau d'objets/inventaire | `SyncList<T>` ou autres collections sync | Éléments sérialisables; jamais une liste **de modules** `List<SyncVar<...>>` |
| Modification locale immédiate avec validation serveur | `ValidatedSyncVar<T>` | Callback de rejet; autorité réelle du serveur |
| Événement ponctuel sans état à conserver | `SyncEvent<T>` | Ne remplace pas le dernier état pour late join |
| Inputs continus vers logique serveur | `SyncInput<T>` | Accepte le délai réseau sans client-side prediction |
| Compte à rebours | `SyncTimer` | Tick/intervalle de réconciliation et autorité |
| Valeur privée du propriétaire | `ownerOnly: true` sur un module | Ne fait pas oublier une valeur déjà divulguée |
| Input et état à prédire/rollback | PurrDiction `INPUT/STATE` | Ne pas mettre `SyncVar` dans la simulation prédite |

## 2. Santé synchronisée : exemple minimal tiré des API documentées

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

Ne pas copier ce snippet tel quel dans un vrai système : prévoir unsubscribe selon le callback disponible, un accès public limité, une demande de dégâts authentifiée, les conditions de respawn et le test de host (double callback `OnSpawned(bool)`). Les dégâts ne doivent **jamais** être acceptés comme une nouvelle valeur décrétée par un client. Ne pas réinitialiser santé à 100 si un objet poolé ou reconnecté doit garder son état : choisir explicitement une politique d'initialisation.

## 3. `ownerOnly` : exemple et piège de confidentialité

```csharp
private SyncList<int> _inventory = new(ownerOnly: true);
private SyncVar<int> _gold = new(0, ownerOnly: true);
```

Le module est invisible pour les non-owners, même si l'objet est observé. **Lors d'un transfert de propriété**, le précédent propriétaire conserve sa copie locale du dernier état. Ne transférez pas l'ownership en supposant que la mémoire du client est effacée ; purgez d'abord les données sensibles ou refondez le modèle de propriété (une identité privée par joueur), avec test réel de transfert. Une valeur envoyée au client peut être copiée même après nettoyage ; ne transmettez jamais un secret qui ne doit pas être découvert.

## 4. ValidatedSyncVar : workflow à tester

- Le client propriétaire écrit de manière optimiste ; l'autorité serveur vérifie avec `serverValidation` et confirme ou rejette ; `onValidationFail` est côté propriétaire.
- Une validation de plage n'est pas la validation métier : les achats vérifient argent, stock, cooldown, transaction et propriétaire dans l'état du serveur.
- Tester owner absent, transfert owner, changements rapides/ACK anciens, latence et client falsifié.

## 5. Conditions de validité pour chaque recette

1. Module déclaré **dans un champ/propriété de l'identité**, initialisé avant connexion/spawn (`OnInitializeModules()` possible). Il ne peut pas être remplacé après spawn, ni placé dans une collection de modules.
2. Comparer `ownerAuth` (pouvoir d'écrire) et `ownerOnly` (destinataires), et Network Rules/Network Visibility.
3. Pour un événement, préciser si un late join doit voir un état antérieur, sinon utiliser un Sync Type durable en plus.
4. Vérifier sérialiseur, observer, permissions, état initial, server-only, host, deux clients, late join et reconnexion.
