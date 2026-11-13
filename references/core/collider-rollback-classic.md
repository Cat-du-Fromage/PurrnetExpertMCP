# Collider Rollback classique versus Lag Compensation de PurrDiction

**Sources** : `systems-and-modules/collider-rollback.md` et `client-side-prediction/lag-compensation.md`, `client-side-prediction/security.md`.

## Choisir sans mélanger les timelines

| Architecture de gameplay | Mécanisme | Où résoudre l'impact ? |
| --- | --- | --- |
| `NetworkIdentity` classique + déplacement autoritaire serveur | `ColliderRollback` et contrôle serveur du tick/latence | Sur le serveur, après vérification de la demande |
| `PredictedIdentity` sous PurrDiction | `predictionManager.lagCompensation`, `lagCompensationTick` durant `Simulate` | Timeline prédite, résultat serveur autoritaire |
| Mouvement entièrement owner-auth et non validé | Aucun ne garantit l'anti-cheat à lui seul | Revoir l'autorité avant de traiter le hit |

## Workflow classique de tir à hit validation

1. Activer le composant `ColliderRollback` sur les colliders concernés et paramétrer l'historique selon les docs et le package.
2. Le client transmet une **intention de tir** (direction et tick/latence), jamais une décision « j'ai touché X » acceptée directement.
3. Le serveur vérifie `RPCInfo.sender`/owner, munitions, cooldown, tick ancien borné et origine plausible.
4. Le serveur effectue le test via `ColliderRollback` de sa version. Ne pas importer une signature ancienne copiée d'un message Discord.
5. Les dégâts sont calculés et appliqués côté serveur. L'impact visuel se diffuse sans confondre feedback et décision.

## Anti-patterns

- Comparer deux positions rendues localement et annoncer un hit validé.
- Faire deux rollback simultanés (ColliderRollback classique et lagCompensation PurrDiction) pour un même acteur sans plan de conversion.
- Faire confiance à un tick arbitrairement ancien transmis par client : fenêtre de compensation bornée.
- Appliquer les dégâts dans un RPC d'observateurs pour que « tous voient pareil ».

## Scénarios

Un tir valide à 100 ms, un tir au-delà de la fenêtre permise, un joueur caché, un joueur changeant de scène, un propriétaire malicieux et un hit en présence de perte de paquets. Mesurer l'écart entre rendu client et verdict serveur.

**Statut** : guide de décision ; aucun code de raycast complet n'est garanti compilable sans vérifier la version installée.
