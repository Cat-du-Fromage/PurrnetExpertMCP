# Évaluations réelles à exécuter — PurrNet Expert v0.9.0

**Non exécutées dans le pack.** Ce plan ne remplace pas les tests Python ; il précise comment mesurer les déclenchements et la qualité du code dans de véritables agents et Unity.

## Matrice à utiliser

- Agents et modèles ciblés : Codex et Claude Code ; pour Claude, comparer Haiku, Sonnet et Opus si accessibles. Ne pas attribuer à un modèle un score non testé.
- Comparaisons : sans skill, avec skill installée sans hooks projet, avec skill + `AGENTS.md` / `CLAUDE.md` contextuels (lorsque supportés).
- Project fixtures : un véritable projet Unity avec PurrNet, packages et commits verrouillés. Tester séparément une version PurrDiction **<1.4** et une version **>=1.4** si disponibles ; ne pas mélanger les DLL. Exiger la version Unity exacte et la source du projet.
- Jeu de prompts : `evals/v0.9-hardcases.json`, `evals/v0.8-end-to-end.json`, négatifs `evals/v0.8-routing.json` et `evals/activation-cases.json`.

## Capturer quatre preuves indépendantes

1. **Déclenchement** : le modèle charge-t-il spontanément `purrnet-expert` avant d'être incité à le faire ? Séparer réponses explicites (« PurrNet ») et contextuelles (« le client voit deux personnages » dans un projet PurrNet connu).
2. **Consultation** : quels guides et pages officielles ont réellement été lus ? `route_docs.py` vert n'est pas une preuve de lecture ; conserver les traces d'outils/terminal de l'agent.
3. **Modification** : diff C#, Inspector et scènes ciblées ; réfuter les mauvais choix, par exemple accepter n'importe quel spawn client ou mettre `NetworkTransform` en parallèle de `PredictedTransform`.
4. **Validation Unity** : compilation avec logs, client distant, serveur headless + deux clients, late join, reconnect, packet loss, ownership transfer, sécurité des RPC et des inputs. Conserver les logs par gate D3–D6.

## Score recommandé par scénario

| Axe | Notation |
| --- | --- |
| Activation correcte | 0 absence, 1 activation forcée, 2 spontanée |
| Références compatibles | 0 API inventée, 1 partielle/non vérifiée, 2 signature/version vérifiées |
| Autorité et rollback | 0 incorrect, 1 plausible non prouvé, 2 juste avec test négatif |
| Résultat de jeu | 0 non compilé/erreur, 1 compilé, 2 scénario réseau fonctionnel |
| Handoff et honnêteté | 0 fausse affirmation, 1 limites mentionnées, 2 preuve explicite D0–D6 |

Répéter les prompts avec différentes formulations (français/anglais, sans nom de produit dans un projet PurrNet). Publier le dénominateur, les traces et les échecs, pas seulement le pourcentage de prompts détectés par proxy Python.

## Critère de sortie

Ne qualifier la skill d'« éprouvée avec Claude » que si au moins trois scénarios positifs, un négatif et un cas PurrDiction **ont réellement été joués dans l'agent**, et distinguer clairement l'évaluation de Claude de la preuve de compilation Unity. Documenter les éventuelles régressions sur un modèle plus petit et améliorer les instructions, puis re-tester.
