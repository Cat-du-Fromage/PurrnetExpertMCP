# Débogage guidé par incidents historiques — protocole v0.7

**Activation** : toute demande de bug PurrNet (RPC manquant/double, `SyncVar` vide, objet fantôme ou dupliqué, erreur ILPP, WebGL jitter, changement d'owner, late join, problème de scène, SteamWorks, etc.) DOIT charger ce guide et `tools/troubleshooting-playbook.md`. Ne jamais charger tous les 15k messages dans le contexte.

## 0. Le symptôme n'est pas une preuve de cause

Distinguer au minimum :

- **Bug historique corrigé** : le changelog archive rapporte une correction **dans une version donnée** ; cela ne prouve ni un bug dans une version moderne, ni une fix garantie.
- **Régression moderne** : un même symptôme réapparaît malgré une version plus récente ; il faut un nouveau scénario minimal, un commit précis et des logs.
- **Usage / configuration** : API non activée, rôle host différent, mauvais owner, object non spawné ou invisible, scène pas encore chargée, mauvais transport, packer manquant.
- **Comportement prévu** : `isOwner` peut être faux à la destruction, callbacks serveur/client peuvent coexister en host, input prédiction peut rejouer une simulation.
- **Conseil périmé** : ancienne URL, ancien nom de callback, composant renommé, backend/produit qui a évolué.

Ne pas déclarer « il faut mettre à jour » seulement parce qu'un cas ressemble à une note d'archive. Les validations sécurité/autorité restent obligatoires même si l'archive dit `Fixed`.

## 1. Ordre des preuves à recueillir

1. `ProjectSettings/ProjectVersion.txt`, `Packages/packages-lock.json` et package `package.json` réellement résolu, `manifest.json`, `git hash`, `.asmdef`; PurrNet et PurrDiction sont **deux versions différentes**.
2. Mode **host / client distant / Linux Dedicated** ; `NetworkManager` auto-start flags, nombre d'instances/clients, transport et Network Rules.
3. Fonction exacte, type d'identité, `asServer`, `isOwner`, owner `PlayerID`, `NetworkID`, scène, observers, tick/horodatage et pile d'erreur.
4. Résultat d'une reproduction minimale au même commit, puis comparaison host vs dedicated et avant/après réseau dégradé.
5. `python scripts/historical_issues.py 'symptôme' --project <PROJECT> --json`; pour une réponse Discord particulière, synchroniser éventuellement l'archive à la révision fixée et chercher **quelques extraits avec contexte**, pas un gros dump.
6. Chercher dans le code source local et la doc PurrDocs officielle les signatures et les mécanismes **actuels**. Pour les blocs `>=1.4.0` de PurrDiction, utiliser les versions du *package PurrDiction* uniquement.
7. Formuler : (a) hypothèse archive, (b) preuve observée, (c) test discriminant, (d) fix limité, (e) régression testée.

## 2. Matrice de diagnostic à appliquer

| Symptom | Hypothèse historique utile | Test discriminant **actuel** | Ne pas faire |
|---|---|---|---|
| RPC `runLocally:true` deux fois | Fix 1.2.0; autre correction host 1.8.0 | tracer appel *et* exécution avec `asServer`, owner, version et destination | recommander une nouvelle mise à jour 1.2.0 sans preuve |
| Host duplique deux joueurs | ancien fix 1.2.1 | tracer chaque `Instantiate`, auto-start, clone, scène et `OnSpawned(bool)` | ajouter un bool client non-répliqué pour masquer la duplication |
| `SyncVar<T>` null | fix 1.2.3 | stack + type `T` + `OnInitializeModules` + script spawné | remplacer le module après spawn |
| `SyncDictionary` illisible | améliorations 1.3.2 / 1.19.0 | sérialiseur K/V, changement via API sync, snapshot late join | convertir silencieusement tout en RPC |
| Liste vide au late join | fix 1.5.0 | contenu côté serveur, observer, `ownerOnly`, scène chargée | forcer un RPC non-bufferisé sans état durable |
| Objet apparaît dans mauvaise scène | fix PlayerSpawner 1.3.3 | scène source spawner, registries et scènes réellement chargées | créer tous les prefabs dans la scène DDOL |
| Personnage tremble sous WebGL | fix WebTransport 1.2.1 | comparer UDP/WebSocket, authority, NetworkTransform buffer, controller, RTT | conclure que WebTransport est toujours défectueux |
| Host `OnTick` deux fois | ancien fix 1.5.0 | tracer tick, manager, contextes et abonnements | confondre avec `OnSpawned(bool asServer)` deux contextes |
| `isOwner` faux dans OnDespawn | signalé attendu | mémoriser owner pendant vie de l'objet et tracer l'ordre du lifecycle | déclarer automatiquement un bug framework |
| `GetClientPlayload` ne compile pas | renommage 1.13.2 | inspection signature actuelle `GetClientPayload` | copier du vieux code Discord sans vérifier les overrides |
| RPC buffered n'arrive pas | fix 1.9.3 / 1.20.0 | vérifier visibilité+spawn+TargetRpc, delivery channel, `bufferLast`/target | supposer qu'un RPC remplace un état persistant |
| `NetworkTransform` bloqué sur observer | fix 1.10.2 | vérifier controller, writer, interpolation, update phase | ajouter un deuxième composant qui écrit le transform |
| Reconnect/pooling : vieux état | changelog 1.20.0 | `OnPoolReset`, `OnSpawned`, modules, ownerOnly, snapshot | présumer un bug v1.20 toujours actif |
| IL2CPP et build release échouent | changelog 1.19.1 | `link.xml`, stripping, asmdef, codegen, target, vrai log | retirer toute sécurité pour faire compiler |
| MTU trop grand / pertes | changelog 1.20.0 | taille et canal, fragment loss vs corruption, Bandwidth Profiler | choisir une MTU fixe universelle |
| Spawn prédit puis disparition | PurrDiction archive 1.3.3 (divers correctifs) | prédiction réellement dans `Simulate`, `INPUT` validé serveur, state, policy | traiter PurrDiction 1.3.3 comme PurrNet core 1.3.3 |

## 3. Exemple de traces host / late join

Pour un comportement réseau *classique* : journaliser « event, instance, tick, asServer, isOwner, localPlayer, owner, ID, scene, observerCount ». Exécuter même build en host, en client séparé et sur dedicated. À défaut de tick accessible depuis le script, utiliser un horodatage Unity, **sans inventer** une API de tick. Les identités peuvent avoir des callbacks différents sur serveur/client.

Pour `onPlayerJoined`, voir la doc actuelle `connection-and-player-events.md` : **après authentification**, pas « scène prête ». Attendre `onPlayerLoadedScene` sur le serveur. `onPlayerJoinedScene` reste utile pour l'appartenance et n'est pas une preuve que les GameObjects chargés sont prêts. Les événements ne sont pas rejoués à la souscription : consulter `networkManager.players` si la souscription arrive tard.

## 4. Réponses et priorité

Une issue de `incident-catalog.json` a des `historical_source`, `claimed_fixed_in`, `official_docs`, `verify`. Le statut comparé à la version (`older_than_claimed_fix`, `at_or_after_claimed_fix`, `unknown_version`) est **un signal de triage**, pas une décision automatique de mise à jour. Vérifier un changelog actuel du commit du projet et les pages officielles en priorité. Ne jamais transformer la description historique d'un bug corrigé en instruction de modifier la logique de production.
