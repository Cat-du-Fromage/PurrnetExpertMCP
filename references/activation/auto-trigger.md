# Déclenchement automatique : contrat et limites

**Le modèle choisit une skill d'après son `name` et surtout son `description`** (frontmatter). Le routeur `scripts/route_docs.py` est exécuté **après** activation et n'influence pas directement cette décision. Aucun texte dans `SKILL.md` ne garantit que tous les modèles chargeront spontanément cette skill.

## Déclenchement souhaité

1. **Mention explicite** : PurrNet, PurrDiction, PurrLobby, PurrVoice, `NetworkTransform`, `NetworkBehaviour`, `SyncVar`, `ServerRpc`, `PredictionManager` et autres symboles officiels ; génération, correction, documentation, review, erreur de compilation.
2. **Contexte implicite dans un projet reconnu PurrNet** : jeu multijoueur, joueur distant qui jitter, balles non synchronisées, late join, owner vs server, scènes qui diffèrent, inventaire entre clients, serveur dédié, matchmaking, désync, lag, packet loss.
3. **Fichiers** : `Packages/manifest.json` déclare `dev.purrnet.purrnet` / `dev.purrnet.purrdiction`, code `using PurrNet;`, sous-classes `NetworkBehaviour` / `PredictedIdentity`; une tâche qui modifie ces fichiers et leurs données réseau.
4. **Coopération** : PurrNet gameplay + Edgegap déploiement -> utiliser les deux skills si installées ; ne pas remplacer `edgegap-purrnet` sur la gestion Edgegap.

## Anti-triggers (négatifs)

Ne pas activer juste parce que l'utilisateur dit Unity, C#, animation d'une cinématique locale, dessin de shader, UI non synchronisée, sauvegarde solo, caméra offline, ou jeu multijoueur **FishNet/Mirror/NGO** sans PurrNet.

## Déploiement dans les agents

- Codex : installer `purrnet-expert/` dans `.agents/skills/` (répertoire du projet) ; la description sert à l'activation implicite. `AGENTS.md` optionnel renforce les tâches sous-entendues.
- Claude Code : installer `purrnet-expert/` dans `.claude/skills/` ; conserver le déclenchement par le modèle activé (ne pas définir `disable-model-invocation: true`). `CLAUDE.md` optionnel donne le contexte du projet.
- Utiliser `scripts/install_activation.py <projet> --target both --apply` **uniquement** si les deux installations existent. Sans `--apply`, le script est en lecture seule. `--remove --apply` retire uniquement les blocs balisés. Les autres lignes des fichiers existants restent intactes.
- Ce hook est **une instruction textuelle** et **pas** un système déterministe d'événements. Les tests hors modèle ci-dessous valident les métadonnées, les chemins et des routes, pas la probabilité réelle de déclenchement chez Codex/Claude.

## Validation de l'activation sur vrais agents

Exécuter les prompts positifs et négatifs du fichier `evals/activation-cases.json` à partir de sessions fraîches de l'agent, skill visible dans son catalogue. Mesurer : `loaded` (le fichier SKILL.md a-t-il été ouvert ?), `references_read` (guides requis ?), `API_verified`, `no_wrong_activation`. Comparer avec/sans `AGENTS.md` / `CLAUDE.md`, versions de modèle, et noter les false negatives. Le script `test_v06.py` n'est qu'un **proxy déterministe** ; il ne teste pas l'activation réelle d'un LLM.

## Format de compte rendu d'un essai réel

| Champ | Valeur |
|---|---|
| Agent/version | ... |
| Projet détecté comme PurrNet | oui/non |
| Prompt | ... |
| Skill sélectionnée automatiquement | oui/non/non vérifiable |
| Routes choisies | ... |
| Guides effectivement lus | ... |
| Justification des erreurs | ... |

## v0.8 — Eviter la collision de skills entre PurrNet et Edgegap

- Si la demande parle **seulement** de PurrNet `SyncVar`, ownership, prediction ou code gameplay : `purrnet-expert`, pas Edgegap.
- Si la demande implique explicitement **Edgegap cloud** (déploiement, Docker, build app/version, matchmaker, port externe, self-stop) : `edgegap-purrnet` est l'implémenteur principal ; `purrnet-expert` reste un reviewer gameplay si nécessaire.
- Serveur dédié **sans Edgegap** : `purrnet-expert` (préparation générique) ; ne pas inventer des dépendances Edgegap.
- Projet uniquement Mirror/FishNet/NGO : ne pas sélectionner `purrnet-expert`, même sur Edgegap, sauf migration explicite.
- Le diagnostic `python scripts/cross_skill_selector.py "<demande>" [--purrnet-project]` et les cas `evals/v0.8-routing.json` restent des **proxies statiques**. Les vraies activations spontanées doivent être observées dans des sessions agent.
