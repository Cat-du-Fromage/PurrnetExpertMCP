# Débogage par symptôme — chemins de diagnostic

**Pour tout symptôme de bug PurrNet** : ouvrir aussi `references/historical/triage-playbook.md` et utiliser `scripts/historical_issues.py` pour vérifier si un incident ancien a déjà été signalé et dans quelle version. Les anciennes corrections sont des indices, pas des patchs applicables tels quels. Voir `references/historical/case-studies.md` pour six scénarios complets.

**Sources** : [Bandwidth Profiler](https://purrnet.dev/docs/systems-and-modules/bandwidth-profiler), [Type Hash Resolver](https://purrnet.dev/docs/tools/type-hash-resolver), [Connection Events](https://purrnet.dev/docs/systems-and-modules/network-manager/connection-and-player-events), [Best Practices PurrDiction](https://purrnet.dev/docs/client-side-prediction/best-practices).

| Symptom | Procédure dans l'ordre | Ne pas faire |
|---|---|---|
| `ServerRpc` non reçu | spawned identity → owner/rules → auth/playerID → transport/observer → signature/ILPP | désactiver toute restriction `RequireOwnership` sans validation |
| Duplications host | OnSpawned `asServer` deux contextes, auto-start, instantiate path, observers RPC `RunLocally` | ajouter bool local non répliqué au hasard |
| Écran vide sur serveur dédié | spawn exécuté en `ObserversRpc` uniquement client; asServer, headless scripts | croire qu'un host local équivaut à un dedicated |
| Transform jitter | autorité writer, interpolation buffer, `NetworkTransform` vs `PredictedTransform`, physics writer, RTT, controller patch | mettre deux composants qui écrivent le même Transform |
| Animator trigger ne réplique pas | `NetworkAnimator.SetTrigger` plutôt que `Animator.SetTrigger` seul, component setup | RPC maison avant examiner NetworkAnimator |
| Player connected but sees no object | authorization, loaded scene, visibility rules/whitelist/owner, registry | supposer qu'un NetworkIdentity spawn sur serveur est toujours visible |
| Hash inconnu dans sérialisation | Type Hash Resolver et registration assembly/codegen | inventer la signature de Packer |
| Message perdu / packet > MTU | profiler drops, fractionner fonctionnellement, choisir channel ou SyncBigData | envoyer un gros fichier chaque frame par RPC |
| Son/VFX joué plusieurs fois en prediction | audio/particles in Simulate/helper, PredictedEvent/isVerifiedView, view callback | ignorer replay et remettre effets dans LateSimulate |
| Projectile prédit disparaît après frame | Create client hors Simulate, input non relayé au serveur, cooldown validation | transformer client en autorité |
| SoftCorrection oscillations | supported component, correction rate, policy scope, verified vs view, state replay | choisir SoftCorrection juste pour masquer logique non déterministe |

## Trace de preuve minimale

1. Version exacte Unity, PurrNet, PurrDiction et addons, branch/commit; 2. logs serveur ET client avec horodatage/ticks; 3. type/ID/owner/observer et scène; 4. reproduction host vs client distant, puis dedicated; 5. conditions réseau; 6. patch minimal et scénarios de non-régression.
