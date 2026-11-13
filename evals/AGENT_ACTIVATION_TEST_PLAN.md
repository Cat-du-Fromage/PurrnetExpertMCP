# Évaluer l'activation spontanée de `purrnet-expert` (test avec vrais agents)

La présence du fichier `evals/activation-cases.json` et le succès de `scripts/trigger_probe.py` **ne démontrent pas** qu'un LLM invoque la skill. Exécuter ce plan dans Codex/Claude Code installés, une nouvelle session par prompt pour éviter la contamination entre essais.

## Conditions

1. Préparer deux projets Unity : A avec `dev.purrnet.purrnet` résolu (et éventuellement PurrDiction), B sans PurrNet. Vérifier que la skill est visible au catalogue.
2. Installer pour Codex sous `.agents/skills/purrnet-expert/`, pour Claude sous `.claude/skills/purrnet-expert/`; ne pas copier seulement `SKILL.md` sans les références/scripts.
3. Faire **deux groupes** : skill seule puis skill + hooks `AGENTS.md`/`CLAUDE.md` via `scripts/install_activation.py --apply`. Ne pas supposer que le hook force le chargement.
4. Faire varier le prompt entre mention explicite (ex. `PurrDiction rollback`) et implicite (ex. « mon joueur tremble sur le deuxième PC ») et négatif (« corrige ce shader solo »). Cas déjà classés dans JSON.
5. Observer la **preuve** d'activation : logs/trace du modèle montrant l'ouverture de `SKILL.md` et des références. Une mention de PurrNet dans la réponse ne suffit pas.

## Métriques

- *Trigger recall* : demandes positives où la skill fut effectivement lue / demandes positives.
- *Trigger precision* : demandes où la skill fut effectivement lue et était pertinente / toutes les activations.
- *Route recall* : routes documentaires pertinentes ouvertes après activation.
- *Task correctness* : compilation, setup Inspector, sécurité/ownership, late join et test réseau séparés.
- Capturer agent/version, date, prompt complet, installation, résultat des hooks, références réellement lues et erreurs.

Les tests CLI v0.6 ne sont **qu'un banc d'essai des intentions de déclenchement**; la valeur de ces métriques ne peut être fournie qu'après exécution avec un vrai modèle.


### v0.7 — déclenchement face aux problèmes historiques

Tester, en sessions fraîches avec skill installée, 10 prompts de `evals/v0.7-cases.json` qui ne mentionnent PAS PurrNet mais sont soumis dans un projet `dev.purrnet.purrnet` (hôte dupliqué, late join vide, scènes, erreur BitPacker, onPlayerJoinedScene, etc.). Mesurer si l'agent a : (a) chargé `SKILL.md`, (b) consulté `historical/triage-playbook.md`, (c) comparé la version de `incident-catalog.json` au package réel, (d) ouvert la documentation officielle, (e) évité de proposer aveuglément un fix ancien. Inclure un groupe négatif (projet FishNet ou problème UI pur) pour contrôler les faux positifs. Les scripts Python ne prouvent **pas** les résultats d'un agent réel.
