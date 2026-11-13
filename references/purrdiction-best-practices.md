# PurrDiction : contrat exhaustif des Best Practices officielles

**Source primaire** : https://purrnet.dev/docs/client-side-prediction/best-practices — fichier https://github.com/PurrNet/PurrDocs/blob/main/client-side-prediction/best-practices.md (consulté le 12-11-2026). **Résumé original raisonné**, pas une copie de la page. Vérifier tout symbole contre la version installée. Lire la page intégrale synchronisée dans `references/cache/official-docs/client-side-prediction/best-practices.md` si disponible. Les 10 rubriques officielles sont toutes représentées ci-dessous.

## BP-01 — Tout ce qui influe sur une simulation ultérieure est du STATE

- `INPUT : struct, IPredictedData` et `STATE : struct, IPredictedData<STATE>` (le STATE participe également à l'interface math/packing de la version) ; déclarer `Dispose()`.
- Position, vitesse, rotation, cooldowns, ammo, mode/animation affectant des règles, compteur de combos, cible, RNG et IDs stables appartiennent à STATE. Un champ Inspector mutable à runtime influant sur les ticks n'est **pas** un substitut : capturer dans STATE ou passer par une opération prévue.
- `GetInitialState` définit le snapshot complet initial ; si Transform, Rigidbody ou d'autres composants Unity portent une partie du résultat de simulation, implémenter `GetUnityState(ref STATE)` et `SetUnityState(STATE)` pour rollback/restauration. Vérifier les composants intégrés qui le font déjà.
- Pour interpolation de STATE : `IMath<T>`/surcharge `Interpolate` pour quaternions et données non linéaires ; **ne pas** ajouter les champs purement UI dans STATE.
- **Contrôle** : énumérer tous les champs mutés pendant simulation et pour chacun indiquer sa présence dans STATE ou sa restitution par bridge explicite.

## BP-02 — Initialisation complète et état Unity restaurable

- Pas de réinitialisation furtive dans `Awake`, `Update` ou `OnEnable` modifiant la vérité prédite en dehors du timeline ; pour un `DeterministicIdentity`, utiliser la simulation (`SimulationStart`) plutôt que des callbacks de setup variables selon les peers.
- Les lectures/écritures de physique doivent être compatibles avec la restauration ; le moteur de physique Unity peut supporter rollback sans être strictement bit-déterministe multiplateforme.
- **Contrôle** : après correction, chaque composant impactant un futur tick revient à l'état attendu.

## BP-03 — Simulate/LateSimulate sont rejoués

- Effets irréversibles interdits dans une simulation non gardée : audio, particules, achievements, sauvegardes, analytics, HTTP, monnaie, notifications, ordinary RPC répétés, etc.
- `PredictedEvent`, vues (`UpdateView`/`LateUpdateView`) et `predictionManager.isVerifiedView` pour effets une seule fois, avec vérification de l'API exacte. Les récompenses serveur doivent être idempotentes.
- Ne pas utiliser `isCatchingUpFrames` pour sauter une mutation déterministe (cela change le résultat du replay).
- **Contrôle** : rejouer le même tick n'augmente pas les récompenses, coûts externes, RPC ni FX.

## BP-04 — Ne pas mélanger les deux modèles d'objets

| Simulation classique à éviter *dans un gameplay prédit* | Remplacer par |
| --- | --- |
| `[ServerRpc]`, `[ObserversRpc]`, `[TargetRpc]` pour changer le gameplay | Actions `INPUT` puis calcul et restauration `STATE` |
| `SyncVar`, `SyncList`, autres sync types | Champs dans le `STATE` prédit |
| `Instantiate`, `Destroy` pour le prédictible | `predictionManager.hierarchy.Create/Delete` avec IDs stables |
| `NetworkTransform` ou `NetworkRigidbody` classique sur la même simulation | `PredictedTransform` / `PredictedRigidbody` / `PredictedRigidbody2D` |
| `NetworkAnimator` pour la même simulation | `Animator` alimenté par `UpdateView` |
| `GameObject`, `Transform`, `PredictedIdentity` en INPUT/STATE | `PredictedObjectID` / `PredictedComponentID` puis résolution immédiate |

**Exception indispensable** : RPC/sync classiques pour systèmes hors gameplay prédit (chat, lobby, affichage de nom) sur `NetworkIdentity` distinct/mirrored. À partir de PurrDiction **1.4.0**, les `NetworkIdentity` présents dans prefabs prédits sont mirroirés automatiquement et gouvernés par topologie/visibilité prédite ; les `Network Rules` de spawning/visibility classiques ne gouvernent pas cette mirror. Avant 1.4.0 le mécanisme `PredictedIdentitySpawner` est différent. Ne jamais déduire que les deux mécanismes marchent ensemble.

## BP-05 — Temps et aléatoire de la simulation prédite

- Interdits dans le chemin des ticks : `Time.deltaTime`, `Time.time`, `Time.frameCount`, `DateTime.Now`, `Stopwatch` comme source de gameplay, `UnityEngine.Random`.
- Utiliser `delta` fourni au callback, `PredictedTime`, `PredictedRandom` dans un flux rejouable et stateful ; vérifier API de la version.
- Pour déterminisme fort : `DeterministicIdentity`, `sfloat`/fixe et math déterministe. Physics Unity classique **n'assure pas** le bit-à-bit entre machines.

## BP-06 — Validation des INPUT côté serveur

- `GetFinalInput(ref INPUT)` lit la commande par tick. `UpdateInput(ref INPUT)` capture `GetKeyDown` / `WasPressedThisFrame` pour ne pas rater un front entre deux ticks ; la simulation lit **uniquement** INPUT sauvegardé, pas un composant MonoBehaviour.
- `SanitizeInput(ref INPUT)` borne mouvement, aim, valeurs non finies et tailles. Cela ne suffit pas : le serveur simule **cooldown, portée, ammo, stamina, autorisation/ownership, limites de débit**, collisions/hits.
- `ModifyExtrapolatedInput(ref INPUT)` retire les one-shots (`jump`, `fire`, `interact`, `purchase`) avant répétition de paquet perdu. Configurer Repeat Input Factor selon le réseau réel ; trop faible fait arrêter les joueurs éloignés, trop fort entraîne overshoot et snaps.
- L'authority n'est pas modifiée par une prediction policy ; jamais croire une position/dégât envoyé par le client comme verdict.

## BP-07 — Choisir la policy la moins coûteuse et correcte

- `FullPrediction`: interactions critiques et rollback exact ; coût de replay élevé.
- `PredictedIfOwned`: full pour owner, relay pour remote ; bon défaut pour player/vehicle si interaction distante non critique.
- `ServerRelay`: observe l'état serveur avec latence ; pas de future speculation client.
- `SoftCorrection`: converge au lieu de restaurer/rejouer le vivant ; seulement si état non critique et composant officiellement supporté. Certains objets non compatibles basculent silencieusement en `ServerRelay` ; ne pas y cacher un bug.
- `PredictedIfOwnedWithSoftFallback`: exists dans la doc actuelle, à **vérifier dans la version installée**, fallback soft/relay pour non-owner.
- Scopes (`PredictionPolicyScope`), overrides, ownership change et pooling changent le résultat ; vérifier le comportement réel et la priorité de policy.

## BP-08 — Gestion du cycle de vie mémoire

- Collections `DisposableList<T>`, `DisposableDictionary<K,V>`, `DisposableArray<T>` via `Create`, puis `Dispose` en fin de vie / dans `STATE.Dispose`.
- Une copie struct superficielle d'une collection disposable ne possède pas un buffer indépendant : `Duplicate` requis. `IDuplicate<T>` dans les structs composites si buffers possédés ; `IEquatable<T>` utile quand égalité chère/ambiguë.
- Ne jamais conserver `CollisionContactList` ou autres contacts temporaires après callback ; vérifier docs versionnées de physique/pooling.
- **Contrôle** : snapshot, cleanup, resimulation et pooling sans fuite, double dispose ou mutation du snapshot passé.

## BP-09 — Identifiants prédits stables

- `PredictedObjectID` et `PredictedComponentID` plutôt que référence d'objet si création, deletion, pooling ou rollback possibles. Résoudre au moment de l'emploi ; échec de résolution doit être géré.
- `TryCreateAndGet` donne un objet valable dans **le tick courant**, pas une référence stable à garder après rewind.
- `PredictedHierarchy` gère pièces parentes/enfants, ownership et topologie ; éviter `Transform.SetParent` arbitraire pour une hiérarchie prédite sans protocole documenté.

## BP-10 — Tests des défaillances

- Toujours tester **client distant**, pas seulement host : ping, jitter, pertes, changement d'owner, reconnexion, téléports, gros écarts, late join, spawn/despawn au milieu de rollback, reuse du pool, frame rates/tick rates différents.
- Mesurer avec profilers bandwidth **et prediction** : nombre/longueur de snapshots, coût par tick, fréquence des corrections, input redundancy ; optimiser à partir des mesures et non d'impressions.
- Critères opérationnels dans `purrdiction-test-matrix.md`.

## Conditions pour affirmer « conforme Best Practices »

Produire un tableau BP-01..BP-10 indiquant **OK démontré / N/A motivé / non vérifié / défaut**, avec chemin de code et test/preuve. Une absence de doc locale, de source API, de build Unity ou de tests distants **interdit** de déclarer conformité exhaustive. Le scan C# `scripts/guard_predicted_code.py` est **heuristique**, ne remplace pas la revue.
