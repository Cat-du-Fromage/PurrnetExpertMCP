# Chronologie indicative du dépôt Stray — NE PAS utiliser comme guide « latest »

Source **archive uniquement** : `docs/changelogs/versions.md` à `e6140a571228044fe670b500e245f6bb370b2e06`. Les dates et versions ci-dessous sont des **repères pour enquêter**, pas une preuve que la correction existe ou fonctionne dans le package actuel.

| Version PurrNet core mentionnée | Incident/fonctionnalité de l'époque | Question de diagnostic actuel |
|---|---|---|
| 1.2.0 | RPC `runLocally` en host, SteamWorks | Est-ce un callback double-context plutôt qu'un double RPC ? |
| 1.2.1 | spawns dupliqués, ownership host, WebTransport/transform | Spawn script exécuté deux fois ? autre writer ? |
| 1.2.3 | `SyncVar<T>` nullable, NetworkReflection host | Quand les modules s'initialisent-ils ? quelle sérialisation ? |
| 1.3.2 | BitPacker arrays / SyncDictionary | Le serializer actuel est-il configuré correctement ? |
| 1.3.3 | scènes, PlayerSpawner, callback owner durant despawn, NetworkAnimator exclude hashes | Scène chargée vs membre ? valeur `isOwner` attendue ? |
| 1.5.0 | late join listes, tick double, événements | Server state, observer, abonnement et host ? |
| 1.8.0/1.8.2 | RPC host, Collider Rollback, EvaluateVisibility | Contrats des canaux, réévaluation des rules ? |
| 1.9.3 | buffered RPC prématurés | Le destinataire observe-t-il déjà le NetworkIdentity ? |
| 1.10.2 | NetworkTransform non-controller | Qui écrit le transform ? |
| 1.13.2 | `GetClientPlayload` renommé `GetClientPayload`, types & ILPP | L'override existe-t-il dans la version installée ? |
| 1.17.0/1.18.0 | ValidatedSyncVar, SyncBigData, TargetRpc serveur | Que supporte le code résolu, quelle direction RPC ? |
| 1.19.1 | IL2CPP/build/stripping | Compiler avec le bon backend et le bon target. |
| 1.20.0 | RPC, transform/rigidbody, paquets, scènes, assets, ownership, reconnect | Plusieurs correctifs historiques ne démontrent pas un bug actuel. |

**PurrDiction : versionnage indépendant**. L'archive mentionne des milestones 1.2.3 et 1.3.3 en 2026 (input disposal, replay, hierarchy, policies, visibility). Les fonctionnalités `>=1.4.0` documentées sur PurrDocs **ne doivent pas être attribuées** à PurrDiction 1.3.3 sous prétexte que PurrNet core 1.20 existe.

Les URL anciennes `BlenMiner/PurrNet`, la négation d'une intégration Dissonance, et les « dernières versions » datées de l'archive ne sont pas normatives. En cas d'exception, prendre le `package.json` réellement installé et les release notes officielles de son commit.
