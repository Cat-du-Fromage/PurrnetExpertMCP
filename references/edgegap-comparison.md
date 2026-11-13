# Audit structurel : PurrNet Expert v0.7 -> v0.8 contre edgegap-purrnet

Référence examinée : https://github.com/edgegap/llm-agent-skills/tree/main/skills/edgegap-purrnet — arbre `main` **fd510ba826ea29ab359e70e185d2e650ef6827de**. Comparaison effectuée sur `SKILL.md`, quatre références, les assets Unity/Docker/matchmaker, les évaluations sous **`evals/purrnet-evals.json`** et **`evals/purrnet-routing-eval.json`** à la racine du dépôt (non dans le dossier de la skill).

## Résultats vérifiés

| Dimension | Edgegap PurrNet | PurrNet Expert v0.7 | Correction v0.8 |
|---|---|---|---|
| Périmètre | Très ciblé : dedicated et matchmaking Edgegap | Large : API, prédiction, sync, bugs, composants | Conserver le périmètre, clarifier les handoffs |
| Frontmatter | Symptômes + dépendances et cas négatifs | Bon FR/EN mais trop de chevauchement avec hosting | Description raccourcie et frontière explicite |
| Entrée SKILL | ~12,5 Ko, phases numérotées et checks | ~19 Ko, nombreuses règles toutes prioritaires | ~10,5 Ko, parcours courts à charger au besoin |
| Workflows | Local -> Docker -> direct deploy -> matchmaker -> 2 clients -> stop | Phase unique générale, peu de checks observables | Workflows feature/bug/dedicated/prediction/Edgegap |
| Modifications | Bootstrap runtime sans toucher aux scènes | Recommande changements minimaux mais sans méthode | Règle « préserver Editor host + clones » et inspection des flags |
| Assets | Config, scripts C#, .meta, link.xml, matchmaker et Docker, testés sur un sample | Quelques snippets pédagogiques NON compilés Unity | Garder marquage explicite + outillage de vérification et étapes d'intégration |
| Preuve | Sample Unity PurrNet Incremental, deux builds clients et server sur Edgegap annoncés | Python static, pas de compilation Unity | Contrat de preuves D0-D6, test scénarisé et manifeste de preuves |
| Évaluations | 3 scénarios riches avec assertions et limites environnementales, routing positif/négatif | Beaucoup d'évaluations JSON, mais pas de harness E2E | Nouveaux scénarios exigeant changement de fichiers et logs ; harness de preuves |
| Sécurité | Secret d'API et registre, arrêt d'allocations facturées | Avertissement générique | Checklist cloud dans workflow de handoff, jamais copier les tokens |

## Risques observés et arbitrages

1. **Ne pas transformer le pack en Edgegap** : le SDK, la convention 7777, le Dockerfile, les tickets et self-stop de la skill spécialisée n'ont pas de sens pour un serveur local ou une autre plateforme. Adapter une architecture de gameplay PurrNet, pas les templates cloud.
2. **Ne pas confondre test documenté et compilation dans notre environnement** : Edgegap rapporte un sample testé avec Unity 6000.3.11f1, PurrNet `dev` et SDK 3.5.5 (ses instructions demandent désormais 3.5.6+ pour certains cas). Notre pack n'a pas cette preuve.
3. **Référence fraîche vs hardcode** : Edgegap formule certains choix comme « utiliser la dernière version SDK » ; dans notre skill, préférer inspecter et verrouiller une version testée en projet reproductible plutôt que mettre à jour sans vérification.
4. **Host-specific bug** : l'exemple documenté `ResourceSpawner.InitSeed` se base sur `ObserversRpc` ne s'exécutant pas sur dedicated sans `runLocally:true`. L'intégrer comme symptôme générique et test de préparation dedicated, sans imposer ce correctif à tous les RPC.
5. **Asynchronicité de `StartClient`** : un état `Disconnected` juste après l'appel ne signifie pas échec ; le test static doit signaler les boucles de retry trop immédiates, pas modifier les transports automatiquement.
6. **Routing négatif inter-skill** : `SyncVar` sans hosting ne doit pas activer Edgegap, Edgegap hosting explicite doit choisir `edgegap-purrnet`, NGO/FishNet ne doivent pas activer PurrNet Expert. Les cas sont formalisés dans `evals/v0.8-routing.json` et dans les tests de proxy locaux.

## Distinction de validations

La suite Python v0.8 vérifie les scanners, données, manifests et règles de contrat. **Elle ne mesure pas un benchmark modèle, ne compile pas Unity, ne valide pas une image Docker et ne déclenche pas une skill Codex/Claude.** Pour un test comparable au test Edgegap, prendre un projet Unity connu et exécuter `evals/V08_E2E_PLAN.md` sur une vraie session d'agent en enregistrant traces, diffs, logs, deux clients et dedicated.
