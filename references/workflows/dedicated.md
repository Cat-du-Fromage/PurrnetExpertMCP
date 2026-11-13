# Workflow C — Host/client vers dedicated server (hébergeur neutre)

## Livrable cible

Un **processus serveur sans client local** démarre, génère son monde et possède les systèmes autoritaires. Deux clients DISTANTS chargent la scène, jouent et récupèrent les mutations d'état. Le test n'est pas validé par un simple événement `Connected`.

## Phase D0 — Audit du projet existant

`python scripts/audit_dedicated_readiness.py <PROJECT> --json` ; puis vérifier manuellement les trouvailles. Inspecter toutes les scènes et NetworkManager, Start Server/Client Flags, transports (UDP/WebTransport/Composite), port et `Application.targetFrameRate` ; chercher `isHost`, `StartHost`, `[ObserversRpc]`, `[TargetRpc]`, `runLocally`, `StartClient`, `clientState`, `OnSpawned(bool asServer)`, `Camera.main`, audio, `Input.*`, composants client-only. Chercher scripts qui déclenchent `StartServer()` ou `StartClient()` deux fois. Aucun résultat statique ne suffit à conclure.

## Phase D1 — Adapter SANS réécrire les scènes

- **Préserver le cycle Editor/host+clone** tant que l'utilisateur ne souhaite pas le remplacer ; éviter de changer toutes les start flags d'une scène pour un test dedicated.
- Un unique responsable déclenche le serveur ; ne pas démarrer un host/client local dans le process dedicated.
- Toute logique de score, seed, spawn ou round conditionnée par `isHost` doit fonctionner sur `isServer` sans client local.
- Un `[ObserversRpc]` ordinaire peut ne pas exécuter son propre corps sur dedicated. S'il initialise le serveur, séparer l'initialisation serveur et la diffusion, OU examiner `runLocally: true` après vérification de la signature et de la sémantique.
- Désactiver/éviter les dépendances à caméra/UI/audio/Unity Input côté serveur ; ne pas supprimer la logique de collision/physics utile sur dedicated.
- Paramètres réseau : binding du serveur sur son interface, port **interne** ; client vers adresse externe et port externe, protocoles compatibles. **Ne pas copier les ports par défaut du template Edgegap** dans un projet générique.
- `StartClient()` est asynchrone : ne pas interpréter son état initial `Disconnected` comme échec immédiat.

## Phase D2 — Validation locale

1. Unity compile un Linux Dedicated Server build (ou cible dedicated adaptée), toutes les scènes nécessaires dans Build Settings.
2. Le serveur démarre SEUL, charge le monde et logge son port, un timer/score/ressource autoritaire existe avant la première connexion.
3. Deux clients (builds distincts, pas uniquement clones Editor) rejoignent par une adresse/port configurable ; initialisation world, score, interaction contrôlée.
4. Un client est refusé pour une mutation non autorisée ; late join récupère état/synchronisation.
5. Déconnexion et arrêt propre, timeout et logs ; si hôte cloud, vérifier lifecycle correspondant.

## Phase D3 — Handoff cloud

Si la cible est Edgegap, **basculer sur `edgegap-purrnet`** pour Docker/SDK/plugin/credentials/port cloud/matchmaker et exécuter les étapes dans `edgegap-handoff.md`. N'assume pas que son sample testé prouve la compilation du projet utilisateur. WebGL impose un transport navigateur, à vérifier et tester directement.
