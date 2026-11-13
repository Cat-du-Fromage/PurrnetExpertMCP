# PredictedHierarchy, pièces, spawn et PredictedParent

**Sources** `client-side-prediction/predicted-hierarchy.md`, `predicted-object-references.md`, `built-in-components/predicted-parent.md`, `built-in-components/predicted-identity-spawner.md`, `best-practices.md`.

- Le predicted world crée/détruit les pièces avec `predictionManager.hierarchy.Create/Delete`; `Instantiate`/`Destroy` classiques dans la simulation créent des objets non synchronisés avec rollback.
- Une **pièce** est un GameObject muni d'une `PredictedIdentity` au sein du prefab; un root peut contenir plusieurs pièces. Les IDs sont `PredictedObjectID` ou `PredictedComponentID`; stocker ces IDs en STATE, **pas** une référence GameObject/Transform entre ticks, puis résoudre au tick d'utilisation.
- La création client qui doit être immédiate doit être causée par INPUT dans `Simulate` pour être exécutée aussi sur le serveur; un simple clic UI qui appelle `hierarchy.Create` côté client peut disparaître à la prochaine vérification. Pour une action one-shot sensible aux paquets répétés, envisager compteur d'action, plutôt qu'un booléen constamment vrai.
- Alternative **acceptée** : le bouton UI demande via un ServerRpc sur une NetworkIdentity autorisée, le serveur crée l'objet prédit; pas de prédiction côté client, apparition après RTT. N'envoyer jamais ce RPC depuis chaque replay `Simulate`.
- `PredictedGameObject.SetActive` utile pour toggle réversible; `Delete` effectue une vraie suppression de pièce.
- Pour reparenting de gameplay, ajouter **`PredictedParent`** sur la pièce. L'attachement se produit pendant la simulation et est enregistré dans state, restauré lors du rollback et envoyé au late join. Sans composant, changer de parent est purement une décoration locale au mieux; parent sous Transform imbriqué non-pièce non répliqué identiquement.
- Préfabs prédits avec `NetworkIdentity` pour chat/UI: **>=1.4** mirror automatiquement, ne pas ajouter `PredictedIdentitySpawner` obsolète; **<1.4** bridge distinct. Mirror suit le verified world, pas le spawn spéculatif, et visibilité/ownership mirror dérivent de la prédiction, pas des Network Rules ordinaires.

## Tests
Spawn client puis rejet serveur, projectile pool rollback, parent détruit/recréé, reparent cross-prefab, owner transfer, scene reload, late join et visibility cachée.
