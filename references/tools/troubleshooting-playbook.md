# Debogage by symptom — diagnostic pathways

**For any PurrNet** bug symptoms: Open also `references/historical/triage-playbook.md` and use `scripts/historical_issues.py` to check if an old incident has already been reported and in which version. Old fixes are clues, not applicable patches as they are. See `references/historical/case-studies.md` for six full scenarios.

**Sources** : [Bandwidth Profiler](https://purrnet.dev/docs/systems-and-modules/bandwidth-profiler), [Type Hash Resolver](https://purrnet.dev/docs/tools/type-hash-resolver), [Connection Events](https://purrnet.dev/docs/systems-and-modules/network-manager/connection-and-player-events), [Best Practices PurrDiction](https://purrnet.dev/docs/client-side-prediction/best-practices).

| Symptom | Procedure in order | Do not do |
|---|---|---|
| `ServerRpc` not received | spawned identity → owner/rules → auth/playerID → transport/observer → signature/ILPP | disable any `RequireOwnership` restrictions without validation |
| Duplications host | OnSpawned `asServer` deux contextes, auto-start, instantiate path, observers RPC `RunLocally` | add local bool not replicated at random |
| Empty screen on dedicated server | spawn run in `ObserversRpc` only client; asServer, headless scripts | believe that a local host is equivalent to a dedicated |
| Transform jitter | writing authority, buffer interpolation, `NetworkTransform` vs `PredictedTransform`, physics writer, RTT, patch controller | put two components that write the same Transform |
| Animator trigger does not reply | `NetworkAnimator.SetTrigger` instead of `Animator.SetTrigger` alone, component setup | RPC house before examining NetworkAnimator |
| Player connected but sees no object | authorization, loaded scene, visibility rules/whitelist/owner, registry | assuming that a NetworkIdentity spawn on server is still visible |
| Hash unknown in serialization | Type Hash Resolver and registration assembly/codegen | Invent Packer's signature |
| Message perdu / packet > MTU | profile drops, split functionally, choose channel or SyncBigData | send a large file each frame by RPC |
| Sound/VFX played several times in foresight | audio/particles in Simulate/helper, PredictedEvent/isVerifiedView, view callback | ignore replay and restore effects in LateSimulate |
| Projectile predicted disappears after frame | Create client out of Simulate, input not relayed to server, cooldown validation | Transforming client into authority |
| SoftCorrection oscillations | supported component, correction rate, policy scope, verified vs view, state replay | choose SoftCorrection just to mask non-deterministic logic |

## Minimum evidence trace

1. Exact version Unity, PurrNet, PurrDiction and addons, branch/commit; 2. server logs AND client with time stamping/ticks; 3. type/ID/owner/observer and scene; 4. reproduction host vs remote client, then dedicated; 5. network conditions; 6. minimum patch and non-regression scenarios.
