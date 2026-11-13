# PredictedStateMachine / PredictedStateNode — procédure

**Sources** : [State Machine](https://purrnet.dev/docs/client-side-prediction/predicted-state-machine), [Predicted State Node](https://purrnet.dev/docs/client-side-prediction/predicted-state-machine/predicted-state-node), [Flow](https://purrnet.dev/docs/client-side-prediction/flow), [Best Practices](https://purrnet.dev/docs/client-side-prediction/best-practices).

## Ne pas confondre

- `NetworkStateMachine` (PurrNet classique) réplique l'état; `StateNode` est un `NetworkBehaviour` dont les méthodes peuvent différencier `asServer`.
- La machine **prédite** évolue dans la timeline PurrDiction avec simulation/réconciliation. Les transitions qui influencent le gameplay doivent se produire dans un état que l'historique peut rétablir.
- `Enter`/`Exit` de simulation ne doivent pas envoyer de RPC, démarrer un audio irréversible ou écrire une sauvegarde à chaque replay. Les fonctions `ViewEnter`/`ViewExit` (selon version) sont liées à la présentation; vérifier leur signature avant implémentation.

## Exemple de responsabilité (pseudo-code)

```text
State: Idle -> Move -> Jump -> Land
Input: move axis + jump edge collected by UpdateInput
STATE: activeMode, jumpTicks, velocity, lastInteraction
On StateSimulate: update STATE deterministically, ask transitions only on simulated timeline
On UpdateView / ViewEnter: change Animator pose / VFX as needed
On rollback: restore previous state + replay transitions, no duplicate score/SFX.
```

- Les versions génériques de `PredictedStateNode<INPUT,STATE>` et `PredictedStateNode<STATE>` ne possèdent pas nécessairement les mêmes callbacks; lire l'implémentation locale.
- Si la machine contient des sous-modules dynamiques, leur création/destruction appartient à la simulation et suit le roster de predicted modules.
- Une animation locale ne doit pas déterminer seule une collision ou un cooldown serveur.

## Tests

Attaques enchaînées, transition rapide Idle→Jump→Land, correction pendant Enter/Exit, plus faible frame rate que tick rate, same tick multiple passes, late join au milieu d'état, pool reset et authority invalidée.
