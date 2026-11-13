# Recettes opérationnelles — PurrNet Expert

But de chaque recette : **définition du résultat → inspection → implémentation → vérification**. Les chemins source sont listés dans `source-map.md`.

## A. Implémenter une feature multijoueur (inventaire, santé, loot, portes)

**Définition du résultat :** deux clients voient le même état autorisé ; les entrées client invalides ne modifient pas le serveur ; late join conforme au besoin.

1. Inspecter le composant Unity existant, owner / `NetworkIdentity`, network rules, transport et version de package.
2. Distinguer **intention** client → RPC vers serveur, **validation/état** côté serveur, **réplication durable** par `SyncVar` ou collection adaptée, et **cosmétique** via vues/RPC.
3. Vérifier dans le code local le `SyncVar<T>`, son initialisation, les `RPC` et leurs permissions ; vérifier la sérialisation des payloads.
4. Implémenter en isolant la logique gameplay : la validation de distance, cooldown, inventaire et paramètres se fait sur le serveur.
5. Tester owner / non-owner, host, deux clients, rejoin et RPC mal formé. Un client non autorisé doit être rejeté.

**Échec classique :** copier un pattern Mirror qui compile partiellement mais contourne les Network Rules, ou envoyer des `GameObject` arbitraires en RPC.

## B. Déboguer un RPC ou une SyncVar qui « ne marche pas »

**Résultat :** cause reproduite, correction localisée, même scénario passé en test.

1. Relever la version précise, log côté appelant et côté récepteur, objet spawné, owner, transport, et règles.
2. Chercher dans `references/troubleshooting.md` ; si issue historique, vérifier le contexte/version du correctif.
3. Pour RPC : vérifier sens client/serveur, permissions, attribut, payload sérialisable, object spawned, observateurs, et host/dedicated.
4. Pour SyncVar : vérifier autorité d'écriture, module initialisé, observation, lecture vs modification et late join.
5. Ne changer qu'une cause à la fois ; tester avant/après avec journal/compteur visuel.

## C. Convertir un code solo en multijoueur

**Résultat :** gameplay séparé en intention, logique autoritaire, état observable et rendu.

1. Identifier ce qui doit être partagé et ce qui reste local (input, caméra, UI, VFX non critiques).
2. Préserver les API gameplay existantes quand possible ; isoler les points d'entrée réseau.
3. Éviter de synchroniser l'état à chaque frame si un événement ou un SyncType suffit.
4. Tester clients non-owners, désynchronisation, changement de scène et reconnexion.

## D. Passer d'un host à un serveur dédié

**Résultat :** un processus headless crée le monde sans client local ; deux clients jouent ; serveur proprement arrêté.

1. Inspecter start flags, transport, port, `isHost`, scripts client-only, `[ObserversRpc]` de création de monde.
2. Corriger les dépendances au host (`isServer`, `OnSpawned(asServer)`, `runLocally` ciblé) en respectant la version PurrNet.
3. Tester **local d'abord**, serveur headless + 2 clients ; puis transport/infra ; puis matchmaking, séparément.
4. Ne pas confondre port interne d'écoute et port externe d'un hébergeur.

Lire `dedicated-server.md`. Pour Edgegap, charger `edgegap-purrnet` lorsqu'elle est installée.

## E. PurrDiction et mouvement

**Résultat :** commandes locales réactives, état serveur cohérent, visuels interpolés, rollback sans effets secondaires.

1. Confirmer que **PurrDiction est installé** et relever sa version ; c'est un addon, pas forcément inclus avec le cœur PurrNet.
2. Lire `PurrDocs/client-side-prediction/overview.md`, `input-handling.md`, `state-handling.md`, `flow.md` et les signatures locales.
3. Séparer input/simulate/state/views. Les effets non déterministes et audio/particles ne doivent pas se déclencher de façon incontrôlée dans une simulation rejouée.
4. Tester en latence simulée, client distant, rejoin ; comparer la position server et render.

## F. Migrer depuis Mirror, NGO ou FishNet

**Résultat :** feature migrée avec *mêmes règles fonctionnelles*, et pas une traduction mécanique des noms.

1. Recenser commandes/RPC/variables réseau/lifecycle/ownership/spawning de l'ancien netcode.
2. Mapper vers les mécanismes PurrNet **en recherchant les signatures locales**, page `getting-started/converting-to-purrnet/` de la documentation officielle.
3. Convertir une vertical slice puis compiler ; retirer anciens packages seulement une fois leur usage éliminé.
4. Tester autorité, réseau, sérialisation et late join ; vérifier que les usages spécifiques de transport restent compatibles.

## Modèle de hand-off

- Environnement exact et niveau de preuve.
- Fichiers modifiés et raisons.
- Scène/prefab/NetworkManager/Network Rules à configurer.
- Tests faits : commande et résultat. Tests restant à effectuer : étape précise + réussite attendue.
- Source URL/révision, zones non vérifiées et choix de sécurité.

## Recette impérative : gameplay PurrDiction (v0.3)

1. Détecter PurrDiction exact via `inspect_project.py` ; si absent, ne pas inventer des types comme s'ils étaient installés.
2. Lire les 10 BP (`purrdiction-best-practices.md`) et la documentation `best-practices.md`, `input-handling.md`, `state-handling.md`, `flow.md`, `security.md` et la page de la fonctionnalité.
3. Écrire une table INPUT (intentions), STATE (tout ce qui influe sur ticks futurs), simulation déterministe, bridges Unity, view, événements one-shot, ownership et policy.
4. Vérifier `PredictedModule` vs `NetworkModule`, hiérarchie prédite et IDs ; si `NetworkIdentity` coexiste, utiliser la règle versionnée >=1.4.0 ou l'alternative historique.
5. Mettre en place tests `purrdiction-test-matrix.md`, linter advisory et compilation/réseau si possible. Livrer grille BP-01..BP-10 avec OK/N/A/Non vérifié.
