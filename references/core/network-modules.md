# Network Modules classiques

**Sources officielles** : `systems-and-modules/network-modules/README.md`, `common-pitfalls.md`, `owner-only.md`, `sync-types/README.md`.

- Les modules sont des **champs ou propriétés de NetworkIdentity** (ou d'un module imbriqué); pas de tableau/liste de modules, pas de création dynamique non déclarée.
- `OnInitializeModules()` pour initialisation/reconfiguration avant assignation IDs et premier envoi. Ne jamais réassigner un module après son spawn.
- Imbrication des modules autorisée en arbre, cycles interdits. `public`/`[SerializeField]` pour exposition Inspector selon type et version.
- Examiner les callbacks propres à `NetworkModule` (`OnSpawned`, `OnOwnerChanged`, `OnDespawned`) et assurer l'abonnement/désabonnement des événements; ne pas supposer la même signature que `NetworkBehaviour`.
- `ownerOnly` dans un custom module doit rester stable; changement à chaud n'efface pas l'état diffusé antérieurement.
- **Ne pas confondre** avec `PredictedModule`, qui dispose de modules *dynamiques* réconciliés pendant la simulation et de règles de roster statique.

## Tests
Module imbriqué, activation en host/dédié, sérialisation late join, ownership, pooling, tentative de réassignation après spawn et cas de structure interdite.
