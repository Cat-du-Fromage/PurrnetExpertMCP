# Functional depth audit v0.6 and residual deficiencies

**This is not official documentation.** Page Sources: https://purrnet.dev/docs and https://github.com/PurrNet/PurrDocs. Document the difference between (a) a page in the clone, (b) a route that requires it to be opened, (c) an illustrative example, (d) a truly compiled/tested example.

| Famille PurrDocs | Status in v0.6 | Modules de lecture | Limitations of evidence |
|---|---|---|---|
| NetworkManager, auth and sessions | guides fonctionnels | `core/network-manager`, `authentication`, `connection-lifecycle` | auth tests in Unity not performed |
| Ownership, Network Rules, Visibility | guides + scenarios | `core/ownership-and-rules`, `network-visibility`, `visibility-advanced` | no multi-observation fixtures verified |
| RPC, Broadcast and Channels | guide + recette | `core/rpc-advanced`, `messaging-and-mtu` | codegen/MTU to be measured by package |
| Sync Types / Modules | guide + snippets | `core/sync-types`, `sync-recipes` | only educational examples |
| Transports / platforms | guides | `core/transports*` | Steam/EOS/WebGL not connected here |
| Spawning, scenes, registries, Addressables | guide + procedures | `core/spawning-and-scenes`, `scene-playbook` | no Unity validation scene |
| Plug n Play components | 7 guides + selector | `components/` | some rare components (NetworkBones) mainly indexed; no Bench |
| Serialization / profiling | guides + playbook | `core/serialization*`, `tools/diagnostics` | no IL2CPP/BitPacker validation |
| PurrDiction INPUT/STATE, rollback, view | Best Practices, guides and recipes | `prediction/*` | no full controller compilation |
| Prediction physics, hierarchy, modules, policies | Targeted guides and income | `prediction/*` | no jitter/latency simulation |
| Tools and addons | synthetic guides | `addons/`, `tools/`, `build/` | product/third limitations and evolutionary dependencies |
| Guides d'exemples, community guides, Made-with | Researchable clones | `references/cache/official-docs` | Untransformed into rules, these are not API specs |

## Priority in case of new task

1. Identify the item in the official inventory corresponding to the request, **do not choose a recipe by habit**.
2. Read the guide to the package **and** the official pages routed/versioned, then the close dependencies.
3. If a feature is only "searchable", see the official page and note the addition to the road, instead of ignoring it.
4. Check the true signature in the installed Unity package; do not present the snippet of this pack as compiled.
5. For further coverage, execute `doc_coverage_matrix.py` on the actual clone and prioritize the `technical-searchable-not-mandatory` that relate to the project tasks.

## Limitations structurantes

The automatic triggering depends on the agent and its skill catalog. The `description` frontmatter, project hooks and `trigger_probe.py` provide ** best and locally testable triggers**, but no absolute guarantee of invocation. Activation tests with agent remain to be performed (see `evals/AGENT_ACTIVATION_TEST_PLAN.md`).
