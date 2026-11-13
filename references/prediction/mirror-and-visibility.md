# PurrDiction : identité réseau miroir et visibilité versionnée

**Sources officielles** : `client-side-prediction/built-in-components/predicted-identity-spawner.md`, `client-side-prediction/predicted-visibility.md`, `client-side-prediction/predicted-hierarchy.md`, `client-side-prediction/security.md`.

## Garde de version impérative

| Version **PurrDiction** | Contrat documenté |
| --- | --- |
| **>= 1.4.0** | `NetworkIdentity` dans un prefab prédit : mirroring **automatique**. `PredictedIdentitySpawner` obsolète, à retirer. |
| **< 1.4.0** | Si le prefab doit fournir une vraie `NetworkIdentity`, l'ancien pont `PredictedIdentitySpawner` peut être requis : vérifier la doc/version exacte. |
| Version absente / conflit d'assemblages | Ne générer aucun code d'API de mirroring avant l'inspection du package. |

La source de vérité sur la vie du miroir >=1.4.0 est le monde prédit :

- `NetworkIdentity` n'est créée côté client **qu'une fois la topologie vérifiée par le serveur**, pas au spawn spéculatif. Les IDs, owners, observers viennent du monde prédit.
- Spawn/despawn classiques **manuels** du miroir interdits ; il suit le `PredictedHierarchy` et son pooling. Un RPC bufferisé attend un observateur réellement prêt.
- `Network Rules` de spawning/visibility classiques **ne s'appliquent pas** aux identités miroir gérées manuellement. Utiliser la visibilité **prédite** sur la racine pour filtrer.
- RPC et Sync Types sur le miroir sont possibles pour données **hors gameplay rejoué** : pseudo, chat, interaction UI. Ne pas transformer le miroir en second écrivain de la simulation.
- Éviter le miroir sur chaque projectile/débris : le coût d'une `NetworkIdentity`, de ses observers, RPC et sync demeure.

## Visibilité prédite (à partir de la version prise en charge)

- `predictionManager.HideFrom/ShowTo`, etc. sont **serveur uniquement**, et visent les objets dynamiques créés via le système de hiérarchie. Les objets de scène prédits suivent leur propre contrat et ne sont pas cachés par cette API selon la doc actuelle.
- Cacher une racine retire son état et ses inputs au client ; la montrer de nouveau équivaut à une nouvelle apparition réseau, avec impacts sur la vue et les caches.
- L'ownership d'un descendant peut forcer la visibilité de l'instance et de ses ancêtres requis. Un parent attaché via `PredictedParent` peut entraîner la visibilité des descendants/ascendants ; tester l'assemblage complet.

## Recette de conception : avatar avec pseudo et déplacements prédits

1. `PredictedIdentity<INPUT, STATE>` gère mouvement, stamina et collisions ; `PredictedTransform` rend les corrections.
2. Ajouter `NetworkIdentity` pour le pseudo **uniquement si la version du mirroring le supporte**. Ne pas y mettre de `NetworkTransform` concurrent sur la même pose.
3. Écrire le pseudo par Sync Type autorisé (hors simulation) et laisser au monde prédit l'ownership/topologie.
4. Si l'avatar doit être caché à une équipe, le serveur applique HideFrom à la racine prédite; ne pas s'appuyer sur les Network Visibility Rules du miroir.
5. Tester spawn prédit finalement refusé, correction, owner transfer, changement d'équipe, late join, pool reuse et destruction.

**Statut** : contrat de conception basé sur les docs ; API à confirmer par version installée ; pas de prefab Unity compilé dans cette archive.
