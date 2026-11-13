# Audit de profondeur fonctionnelle v0.6 et lacunes résiduelles

**Ce n'est pas la documentation officielle.** Sources des pages : https://purrnet.dev/docs et https://github.com/PurrNet/PurrDocs. Documenter la différence entre (a) une page présente dans le clone, (b) une route qui oblige à l'ouvrir, (c) un exemple illustratif, (d) un exemple réellement compilé/testé.

| Famille PurrDocs | Statut dans v0.6 | Modules de lecture | Limites de preuve |
|---|---|---|---|
| NetworkManager, auth et sessions | guides fonctionnels | `core/network-manager`, `authentication`, `connection-lifecycle` | tests auth en Unity non exécutés |
| Ownership, Network Rules, Visibility | guides + scénarios | `core/ownership-and-rules`, `network-visibility`, `visibility-advanced` | pas de fixtures multi-observers vérifiées |
| RPC, Broadcast et channels | guide + recette | `core/rpc-advanced`, `messaging-and-mtu` | codegen/MTU à mesurer par package |
| Sync Types / Modules | guide + snippets | `core/sync-types`, `sync-recipes` | seulement exemples pédagogiques |
| Transports / platforms | guides | `core/transports*` | Steam/EOS/WebGL non connectés ici |
| Spawning, scenes, registries, Addressables | guide + procédures | `core/spawning-and-scenes`, `scene-playbook` | aucune scène Unity de validation |
| Plug n Play components | 7 guides + selector | `components/` | quelques composants rares (NetworkBones) surtout indexés; pas de bench |
| Serialization / profiling | guides + playbook | `core/serialization*`, `tools/diagnostics` | pas de validation IL2CPP/BitPacker |
| PurrDiction INPUT/STATE, rollback, view | contrat BP + guide + recette | `prediction/*` | pas de compilation de contrôleur complet |
| Prediction physics, hierarchy, modules, policies | guides et recettes ciblées | `prediction/*` | pas de simulation à jitter/latence |
| Tools et addons | guides synthétiques | `addons/`, `tools/`, `build/` | limitations produit/tiers et dépendances évolutives |
| Guides d'exemples, community guides, Made-with | clonés recherchables | `references/cache/official-docs` | non transformés en règles, ce ne sont pas des specs API |

## Priorité en cas de nouvelle tâche

1. Identifier l'élément de l'inventaire officiel correspondant à la demande, **ne pas choisir une recette par habitude**.
2. Lire le guide du pack **et** les pages officielles routées/versionnées, puis les dépendances proches.
3. Si une fonctionnalité est uniquement « recherchable », consulter la page officielle et noter l'ajout à faire à la route, au lieu de l'ignorer.
4. Vérifier la vraie signature dans le package Unity installé ; ne pas présenter le snippet de ce pack comme compilé.
5. Pour une couverture plus approfondie, exécuter `doc_coverage_matrix.py` sur le clone réel et prioriser les `technical-searchable-not-mandatory` qui concernent les tâches du projet.

## Limitations structurantes

Le déclenchement automatique dépend de l'agent et de son catalogue de skills. Le `description` frontmatter, les hooks de projet et `trigger_probe.py` fournissent des déclencheurs **meilleurs et testables localement**, mais aucune garantie absolue d'invocation. Les tests d'activation en situation avec agent restent à exécuter (voir `evals/AGENT_ACTIVATION_TEST_PLAN.md`).
