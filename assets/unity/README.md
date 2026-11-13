# Patrons Unity C# — opt-in, pas une installation automatique

Ces fichiers sont **des exemples autonomes écrits pour cette skill**. Ils ne sont **pas** des templates de déploiement Edgegap et n'ont **pas été compilés avec Unity** ici. Avant d'en faire des scripts du projet :

1. Vérifier la signature dans `Assets/PurrNet/Runtime/` ou `Packages/dev.purrnet.purrnet/` de la révision installée.
2. Copier uniquement le fichier utile dans `Assets/` de ton projet Unity ; ajuster le namespace / `.asmdef`.
3. Ajouter le script à un GameObject possédant/configuré avec une `NetworkIdentity` selon la documentation et les Network Rules. Vérifier le prefab et l'ownership dans Unity.
4. Tester en host puis avec deux clients ; jamais déclarer prêt pour un jeu compétitif sans autorisation et rate-limit explicites.

## Patron 1 : ExampleNetworkCounter.cs

Exemple minimal d'une **intention client** vers le serveur via `[ServerRpc]` puis d'un état durable `SyncVar<int>`. L'appel devrait provenir du bon propriétaire sous Network Rules strictes ; cette version démo n'est **pas** résistante au spam et **ne doit pas** remplacer les validations de gameplay.

## Patron 2 : ExampleWorldSeed.cs

Exemple d'initialisation du serveur et diffusion d'une graine avec `[ObserversRpc(runLocally: true, bufferLast: true)]`. Démontre la distinction host / dedicated et l'arrivée tardive. Pour un jeu réel, conserver les états déterminants côté serveur et utiliser le mécanisme de réplication approprié ; un seed reçu ne représente pas automatiquement l'état du monde complet.

Sources à contrôler :
- https://github.com/PurrNet/PurrDocs/blob/main/systems-and-modules/remote-procedure-call-rpc/README.md
- https://github.com/PurrNet/PurrDocs/blob/main/systems-and-modules/network-modules/sync-types/syncvar.md
- https://github.com/PurrNet/PurrDocs/blob/main/systems-and-modules/network-identity/networkbehaviour.md

### PurrDiction v0.3

**Aucun template C# PurrDiction n'est certifié ici.** Les signatures de prédiction (notamment modules/policies) évoluent ; lire `references/purrdiction-best-practices.md` et la source réellement installée avant de construire un exemple. Il est préférable de dériver un contrôleur du sample officiel du commit correspondant plutôt que fournir un faux exemple « prêt à compiler ».

## v0.6 additional examples (NOT Unity-compiled)

- `ExampleNetworkAnimator.cs` illustrates the official `NetworkAnimator.SetTrigger` call; the application must make sure the caller has authority. A pure `Animator.SetTrigger` is not automatically synchronized.
- `ExamplePredictedData.cs` provides `IPredictedData` input/state *shapes* only; it is not a controller and does not demonstrate complete IMath, rollback, Animator view or input sanitization. Use `references/prediction/real-world-recipes.md` and the installed PurrDiction source before building a controller.

**Provenance:** Adapted from official API documentation, not independently compiled or tested against Unity/PurrDiction packages in this archive. Treat as learning aids.
