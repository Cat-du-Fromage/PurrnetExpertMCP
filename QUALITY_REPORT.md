# Audit et rapport de livraison — PurrNet Expert v0.9.0

## Périmètre et sources (13 novembre 2026)

- Documentation officielle : https://purrnet.dev/docs, dépôt `PurrNet/PurrDocs` branche `main`, arbre Git consulté `5b146a3bd382ffda7d214af912b106d131301c0c` : **217 pages Markdown** répertoriées. Relecture ciblée des pages cruciales (Best Practices PurrDiction, Input, State, mirroring, visibilité, client spawning, DDOL, PlayerIdentity, SyncLazyRef, ColliderRollback, Network Rules, RPC, etc.). **Ce n'est pas une relecture humaine mot à mot des 217 pages.**
- Bonnes pratiques Anthropic de construction d'une skill : https://platform.claude.com/docs/fr/agents-and-tools/agent-skills/best-practices : description action + conditions à la troisième personne, frontmatter, moins de 500 lignes, références directes, divulgation progressive, workflows, feedback loops, vrais essais d'agent.
- Référence structurelle conservée : `edgegap-purrnet`, cf. `references/edgegap-comparison.md` ; ne pas copier ni installer des composants cloud sans demande.
- Priorité des sources **pour le code généré** : package effectivement installé dans Unity > sources officielles versionnées > docs officielles compatibles > exemples illustratifs > Discord historique.

## Faiblesses détectées et corrections appliquées

| Point | Défaut dans v0.8 | Correction v0.9 |
| --- | --- | --- |
| Spawning client | Validation surtout mentionnée | `core/spawn-security-and-persistence.md`, exemple **deny-by-default**, `onClientSpawnValidate`, `SpawnPacket.TryGetRawPrefab`, quotas et test de refus |
| Objets persistants | DDOL peu explicité | `alwaysIncludeDontDestroyOnLoadScene`, ordre d'initialisation, tests « Not Spawned » |
| Joueurs / références | `PlayerIdentity<T>` et `SyncLazyRef` sous-utilisés | Sélection des primitives, `GlobalNetworkID`, résolutions différées après chargement, événements de connexion distincts |
| Visibility | Rule-set OU connu, priorité précise absente | Ordre parent > whitelist > blacklist > no rules > owner > rules, overrides par composant et `EvaluateVisibility` |
| Combat classique | Risque de confondre rollback et prédiction | `ColliderRollback` classique versus `predictionManager.lagCompensation`, sécurité du tick de tir |
| Mirroring PurrDiction | Simple mention de la version | Contrat **PurrDiction <1.4 / >=1.4**, ownership, observers, vie du miroir, visibilité et coûts |
| Input réconcilié | Recommandations trop compactes | `UpdateInput`, `GetFinalInput`, `SanitizeInput`, `ModifyExtrapolatedInput`, replay, tests de fronts perdus |
| Interaction prédite inter-identités | Page source non routée obligatoirement | Route spécifique vers `multi-identity-interactions.md` |
| Activation négative | « pas PurrNet » pouvait déclencher la skill | Correctif dans `trigger_probe.py` et `cross_skill_selector.py`, test de régression |
| Conformité Anthropic | Pas de contrôle d'auteur dédié | `scripts/audit_skill_authoring.py` + `references/anthropic-skill-authoring.md` + références directes depuis le SKILL |
| Couverture critique | Inventaire sans seuil spécifique | `doc_coverage_matrix.py --fail-unrouted-critical` sur clone synchronisé, avec liste de pages à haut risque |
| Validation LLM | Uniquement proxies et JSON | Plan explicite `evals/V09_REAL_AGENT_PLAN.md` (à exécuter, pas de résultats inventés) |

## Mesures structurelles

- `SKILL.md` : **58 lignes hors frontmatter** ; `description` **887 caractères**, à la troisième personne et contenant des déclencheurs techniques/implicites et des exclusions.
- **16 liens directs** depuis `SKILL.md` vers les références fondamentales ; les autres guides sont sélectionnés par routes explicites et chemins complets. Pas de références Markdown de plus de 100 lignes nécessitant un sommaire parmi les fichiers livrés.
- `references/task-routes.json` : **70 routes**, **106 pages officielles distinctes explicitement référencées**, **71 guides locaux** couverts au moins par une route. Ces nombres mesurent l'index, **pas l'exhaustivité de la connaissance ou de la lecture par le LLM**.
- Synchronisation intégrale opt-in : `scripts/sync_sources.py` clone toutes les pages du dépôt sur le poste. Le ZIP n'embarque pas les docs PurrDocs sous licence de redistribution non confirmée, ni les 15 031 messages Discord revendiqués par l'archive Stray.
- 13 scénarios dans `evals/v0.9-hardcases.json`, chacun avec assertions à vérifier dans un vrai agent. Tests Python de routage ≠ exécution de ces assertions dans Unity.

## Validation réellement exécutée

| Contrôle | Résultat |
| --- | --- |
| Tests statiques historiques v0.2–v0.8 | **89/89 passent** |
| Tests statiques v0.9, y compris négatifs/Anthropic | **13/13 passent** |
| Ensemble Python | **102/102 réussis** (47 + 21 + 34) |
| Contrôle de la structure et de BP-01..BP-10 | Réussi |
| Audit Anthropic (frontmatter, 500 lignes, liens, routes) | **0 erreur** ; avertissement non testé |
| Vérification du ZIP après extraction | **Réussie : 161/161 empreintes SHA-256 conformes**, ZIP intégral et mêmes 102/102 tests Python depuis les fichiers extraits |

### Non exécuté — aucune inférence de réussite permise

- Compilation C# dans l'Unity Editor du projet réel : **non**.
- Test réseau host + client distant, serveur Linux headless + deux clients, late join, désync, performance : **non**.
- Déclenchement spontané réel de `purrnet-expert` par Claude Haiku/Sonnet/Opus ou Codex : **non**.
- Contrôle `doc_coverage_matrix.py` sur un clone Git réel PurrDocs complet **dans cet environnement** : **non** ; seul l'arbre GitHub a été inventorié et la logique de classement testée sur des fixtures.
- Compilation de Roslyn optionnel (outil de prédiagnostic) : **non**.
- Conformité d'API par version garantie pour les fragments C# : **non** ; exemples de la doc adaptés et non compilés.

## Commandes de reproduction

```bash
python scripts/audit_skill_authoring.py
python scripts/validate_skill.py
python -m unittest discover -s scripts -p 'test_*.py' -q

# Après installation : copie intégrale et audit sur le poste du développeur
python scripts/sync_sources.py
python scripts/doc_coverage_matrix.py --fail-missing-routed --fail-unrouted-critical
python scripts/route_docs.py "PurrDiction PredictedIdentitySpawner 1.4.0"
```

**Conclusion** : v0.9 réduit plusieurs zones où le LLM pourrait choisir l'ancienne API, contourner l'autorité, manquer une condition Inspector ou oublier une page utile. L'exhaustivité et la fiabilité en production requièrent toujours des tests réels d'agent et Unity. Les nouveaux scripts rendent l'écart vérifiable, non invisible.
