# Recettes PurrDiction — contrôleur, tir, rollback, spawn et view

**Sources** : [Best Practices](https://purrnet.dev/docs/client-side-prediction/best-practices), [Input](https://purrnet.dev/docs/client-side-prediction/input-handling), [State](https://purrnet.dev/docs/client-side-prediction/state-handling), [Hierarchy](https://purrnet.dev/docs/client-side-prediction/predicted-hierarchy), [Lag Compensation](https://purrnet.dev/docs/client-side-prediction/lag-compensation), [View](https://purrnet.dev/docs/client-side-prediction/views-and-interpolation). Le code ici est **illustratif et non compilé** dans Unity ; vérifier package et version (notamment `>=1.4.0`).

## 1. Controller INPUT vs STATE

```csharp
using PurrNet.Prediction;
using UnityEngine;

public struct MoveInput : IPredictedData
{
    public Vector2 move;
    public bool jump;
    public void Dispose() { }
}

public struct MoveState : IPredictedData<MoveState>
{
    public Vector3 position;
    public Vector3 velocity;
    public float cooldown;
    public void Dispose() { }
}
```

`INPUT` est une intention collectée sur le contrôleur. `STATE` est tout ce qui influence un résultat futur, même lorsque la donnée est également présente sur un Transform ou un Rigidbody. Les champs Inspector doivent être des réglages immuables ou copiés dans STATE avant d'influer sur une simulation.

**Squelette des responsabilités** (non compilable tel quel) :

```text
UpdateInput: accumulate frame-level edge (jump |= WasPressedThisFrame).
GetFinalInput: collect continuous axes once per simulation tick.
SanitizeInput: clamp [-1,1], reject NaN/Inf; enforce server-side move limits.
ModifyExtrapolatedInput: jump=false, fire=false when repeating missing remote input.
GetInitialState: complete snapshot, incl. cooldown and random state.
Simulate(INPUT, ref STATE, delta): deterministic tick state mutation; NEVER Input.GetKeyDown.
GetUnityState/SetUnityState: bridge Rigidbody/Transform not already covered by built-ins.
UpdateView(viewState, verified): render pose/Animator/FX; do not change gameplay.
```

La simulation peut être appelée plusieurs fois pour le même tick. `Time.deltaTime`, `Time.time`, `UnityEngine.Random` et effets irréversibles sont interdits dans le chemin rejouable. Audio/particles/achievements: view callbacks, `PredictedEvent`, verified view. Éviter les effets dans `LateSimulate` également.

## 2. Projectile / hit-scan

**Spawning réactif** : la demande de tir doit être dans INPUT, vérifiée par STATE (munitions, cooldown, owner) ; créer par `predictionManager.hierarchy.Create` **pendant** `Simulate`. Pour un événement de création, un compteur monotone dans l'input peut mieux résister aux répétitions qu'un booléen. Un appel `Create` depuis un bouton UI du client en dehors de la simulation ne rend pas la création autoritaire : elle peut disparaître à la correction.

**Spawning non prédit** : un bouton UI peut déclencher un `ServerRpc` sur une identité réseau classique, et le serveur crée l'objet prédit; le client le voit lors du retour de l'état vérifié. Ne pas envoyer de RPC ordinaire *depuis le replay*.

**Hitscan (API moderne)** : `predictionManager.lagCompensation.Raycast(lagCompensationTick, ray, out hit, range, mask)` pendant `Simulate`, cible avec `ColliderRollback` configuré, délai de vue borné par serveur. Le `lagCompensationTick` prédit n'est pas le `NetworkIdentity.rollbackTick` classique. Le succès du hit doit modifier STATE ; le son de tir reste en view.

## 3. Interaction avec un objet

- Dans STATE, une cible persistante est `PredictedObjectID` ou `PredictedComponentID`, **pas** `GameObject`/`Transform` susceptible d'être détruit ou recyclé au rollback.
- Résoudre le handle dans le monde courant juste avant l'interaction (`TryGetGameObject`, `TryGetIdentity` selon la version). Un lookup manquant est normal si le partenaire n'existe plus.
- `PredictedParent` rend les changements de parent rejouables; reparent depuis la simulation, utiliser des pieces reconnues.
- `PredictedGameObject.SetActive` peut être préférable pour masquer provisoirement un objet, sans coût de destruction/recréation.

## 4. Prediction policies : exemple de décision

| Rôle | Policy indicative | Pourquoi |
|---|---|---|
| Joueur local | `PredictedIfOwned` | local prédictif, copies distantes vérifiées |
| Combat interactif | `FullPrediction` | cohérence historique des collisions |
| Décor cosmétique / ragdoll | `SoftCorrection` si supportée | convergence visuelle, pas de garantie de collision historique |
| Ennemis contrôlés serveur | `ServerRelay` si latence acceptable | pas de replay client inutile |
| Voiture locale + remote douce | `PredictedIfOwnedWithSoftFallback` si supportée | fallback de soft selon composant |

Testez `NetworkIdentity` mirroring selon la version : avant PurrDiction 1.4 `PredictedIdentitySpawner` peut être requis; à partir de 1.4 le mirror est automatique et l'ancien composant obsolète.

## 5. Test de réception / replay

- Deux builds clients, host vs dedicated, 0/100/250ms RTT, jitter 30ms, pertes simulées.
- Répéter les inputs fire/jump sous perte, vérifier ni double tir ni son multiplié après correction.
- Rejouer spawn/delete/reparent, pool reuse, ownership transfer, reconnect, teleport (ResetInterpolation si nécessaire).
- Comparer `currentState`, `verifiedState`, `viewState` à une même époque; mesurer correction et coût history.
