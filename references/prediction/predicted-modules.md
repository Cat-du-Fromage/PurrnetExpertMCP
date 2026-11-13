# PredictedModule et états dynamiques

**Source** `client-side-prediction/predicted-modules/README.md`, `predicted-modules/predicted-timer-module.md`, `flow.md`.

- `PredictedModule<TState>` intègre un sous-état et une simulation à l'identité : delta/history/reconciliation automatiques, mais coût de snapshot et simulation supplémentaire.
- Modules **statiques** créés avant premier tick (typiquement `LateAwake`) : la **même liste et le même ordre** doivent être créés sur TOUS les peers. Ne jamais conditionner le roster statique à owner/server, sinon `PredictedModuleRosterMismatchException` suspend la réplication pour cette identité.
- Modules **dynamiques** créés pendant simulation : l'existence est elle-même réconciliée. Le constructeur doit être public, premier paramètre `PredictedIdentity`, autres paramètres optionnels; paramètres de gameplay dynamiques dans STATE, pas seulement en args de ctor.
- `Dispose()` d'un module dynamique lors de simulation déclenche la suppression réconciliée; `Dispose` d'un statique est invalide/no-op + erreur. Callback `onDisposed` à utiliser pour nettoyer des références externes.
- Une référence dynamique mise en cache hors STATE peut pointer vers une ancienne instance après rollback. Préférer `TryGetModule<T>` / lookup actuel; vérifier signatures des méthodes dans package.
- À ne pas confondre avec les `NetworkModule` classiques : ces derniers ne sont jamais créés comme une liste à l'exécution et ne sont pas réconciliés via history.

## Tests
Roster mismatch simulé, dynamique créé puis supprimé pendant rollback, constructor avec config non persistée, pool, état dupliqué et deux clients à FPS différents.
