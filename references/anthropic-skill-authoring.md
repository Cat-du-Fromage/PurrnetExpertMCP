# Contrat de qualité Agent Skill — Anthropic

**Source primaire** : https://platform.claude.com/docs/fr/agents-and-tools/agent-skills/best-practices (consultée pour la v0.9.0). Ne pas confondre critères de rédaction d'une skill et Best Practices **PurrDiction**.

## Checklist concrète et raison

| Aspect | Critère v0.9 | Pourquoi |
| --- | --- | --- |
| Découverte | `description` à la 3e personne, action **et** déclencheurs, <=1024 caractères | C'est la métadonnée lue pour sélectionner la skill |
| Métadonnées | `name` minuscule/tirets <=64 caractères, frontmatter YAML lisible | Compatibilité Agent Skills |
| Contexte | `SKILL.md` <=500 lignes, seulement les garde-fous critiques + choix des workflows | Ne pas saturer le contexte à chaque activation |
| Références | Chemins directs depuis `SKILL.md` pour les guides fréquents ; éviter chaîne guide -> guide -> details | Le modèle peut interrompre une navigation profonde |
| Documentation longue | Table des matières si >100 lignes | L'agent peut lire seulement un extrait |
| Workflows | Entrée, choix, séquence, gate de validation, correction après échec | Réduit les omissions de vérification |
| Exemples | Distinguer fragment explicatif, recette à compléter, code Unity réellement compilé | Évite la fausse confiance |
| Scripts | Python 3 stdlib lorsque possible, prérequis explicites, erreurs utiles, commandes safe et dry-run | Reproductibilité multi-environnements |
| Évaluation | Cas positifs/négatifs, contexte concret, comparaison avec/sans, tests modèles réels | Les proxies locaux ne prouvent pas l'activation spontanée |
| Composabilité | Handoff vers `edgegap-purrnet` seulement si tâches Edgegap ; ne pas détourner FishNet/Mirror | Compatible avec d'autres skills |
| Versions | Pas de « latest » immuable ni d'API garanties hors package installé | Évite les instructions périmées |

## Cycle de validation pour une mise à jour

1. Auditer la découverte et le frontmatter : `python scripts/audit_skill_authoring.py`.
2. Vérifier les guides, liens et routes : `python scripts/validate_skill.py` et `python scripts/route_docs.py "..."`.
3. Vérifier les API **dans** Unity installé, puis compiler et tester les jeux si l'Editor est disponible.
4. Exécuter des évaluations d'agent **réelles** : enregistrements déclenché / non déclenché, références effectivement ouvertes, modification finale et tests. Comparer plusieurs modèles si c'est le public visé.
5. Corriger les erreurs détectées, puis répéter. Ne pas marquer « E2E réussi » parce que l'outil de tests Python est vert.

## Niveaux de preuve

- Structure/frontmatter et scripts : prouvables localement par Python.
- Couverture : estimée par index et routes; aucune garantie de compréhension LLM.
- Compétence/activation autonome : **nécessite des runs réels d'agent** (Haiku/Sonnet/Opus si ciblés).
- Comportement réseau et compilation : **nécessite Unity** ; aucune sortie de Python ne peut s'y substituer.
