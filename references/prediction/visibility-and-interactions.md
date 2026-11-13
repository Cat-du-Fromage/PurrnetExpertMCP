# Visibilité prédite et interactions entre identités

**Sources** `client-side-prediction/predicted-visibility.md` (>=1.3.0), `multi-identity-interactions.md`, `predicted-state-machine/README.md`, `predicted-state-machine/predicted-state-node.md`, `built-in-components/predicted-parent.md`.

## Visibilité
- La visibilité prédite est **distincte de Network Visibility** classique. Les appels `predictionManager.HideFrom/ShowTo` concernent les objets **dynamiques créés via la hiérarchie** et sont appliqués **uniquement par le serveur**. Les objets de scène prédits peuvent être toujours visibles (voir version).
- La visibilité s'applique à des racines complètes, pas seulement une pièce; objets attachés peuvent entraîner visibilité d'ancêtres, et les owned objects peuvent bénéficier de règles spéciales. Cacher peut retirer entièrement un objet du monde client et interrompre état/input; ne pas simplement désactiver Renderer.
- Quand un NetworkIdentity est mirrored dans prefab prédit (>=1.4), sa visibilité et son owner suivent le monde prédit, pas l'asset Network Visibility normal.

## Plusieurs identités
- Stocker IDs stables dans STATE, lookup au moment de lecture, mutation uniquement pendant simulation; `[SimulationOnly]` possible selon source installée. Ne pas muter une identité depuis un callback de rendu ou un MonoBehaviour en ignorant timeline.
- `PredictedEvent` filtre présentation/one shots, **ne constitue ni RPC ni transcript réseau** ; tous les peers doivent pouvoir générer l'occurrence dans la simulation, et la mutation STATE doit rester rejouable.
- `PredictedStateNode`/state machine : états de mouvement/combat avec état prédit (vérifier les hooks/active node et transitions selon version). Ne pas mélanger state machine UI classique et timeline prédite.
- `PredictedPlayers` : vérifier les API et événements présents dans le package; lors d'initialisation déterministe utiliser événements appelés sur la timeline simulée.

## Tests
Deux équipes, fog of war, objet enfant attaché, owner, late join, collision entre identités, états dynamiques, et limites d'observation cross-client.
