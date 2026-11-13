# Workflow B — Réparer un bug sans attribuer une cause prématurément

## 0. Collecter des preuves

Demander/chercher, sans répétition : description exacte, rôle host/dedicated/client, version PurrNet/PurrDiction, OS/build vs Editor, transports, repro minimal, logs séparés `server.log` et `Player.log`, package lock. Capturer « attendu / observé » et nombre de joueurs.

## 1. Reproduction contrôlée

Établir la matrice : Editor host (serveur+client local), client distant, dedicated (sans client local), client tardif ; comparer les logs. Une correction plausible sans scénario reproduit doit être présentée comme hypothèse.

## 2. Arbre décisionnel des symptômes

| Symptôme | Première vérification, puis docs |
|---|---|
| RPC manquant | spawn, ownership, observateurs, connexions, canal, mode host/client ; `core/messaging-and-mtu.md` |
| RPC doublé | `OnSpawned(bool asServer)` host, subscriptions répétées, `runLocally`, appel serveur + client |
| World vide sur dedicated | `isHost`, client-only `ObserversRpc` qui initialise le serveur, spawn serveur, scenes in build |
| Connexion boucle instantanément | `StartClient` async ; état `Disconnected` transitoire, auto-start et port |
| Transform jitter | plus d'un writer, ownership, sync buffer, Rigidbody patch, transport, FPS/latency |
| Late join vide | `SyncVar/SyncList` état initial, observateurs, chargement de scène, pooling, abonnement tardif |
| Build IL2CPP | .asmdef, stripping, type packer/codegen, versions installées, log exact |
| Correction prédite | état non restauré, input externe en `Simulate`, effet non idempotent, policy, versions |

Voir `references/tools/troubleshooting-playbook.md`, `references/dedicated-server.md` et `references/historical/triage-playbook.md`.

## 3. Historique = piste, pas diagnostic

`python scripts/historical_issues.py "<SYMPTÔME>" --project <PROJECT> --json`. Comparer le fix historique avec la version installée et le code actuel. Un bug « corrigé en 1.2.1 » **n'explique pas** le même symptôme en 1.25.0 sans preuve de régression.

## 4. Isoler puis corriger

Produire une cause testable : `« aucune initialisation serveur avant diffusion RPC »`, pas `« problème de PurrNet »`. Changer la zone minimale. Ne pas mettre `runLocally: true` sur tous les RPC sans discernement ; préférer souvent un appel explicite de la logique serveur + RPC purement client. Éviter de remplacer le transport/dépendance si les logs pointent vers une double souscription.

## 5. Régression

Même reproducer AVANT/APRÈS, host+dédié si applicable, deux clients, late join, perte réseau et version. Si impossible, fournir script de reproduction et étapes de logging. Résultats observés et non observés selon `references/validation/acceptance.md`.
