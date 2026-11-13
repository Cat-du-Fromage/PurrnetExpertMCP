# Validation du premier jalon

Essais locaux sous Windows le 13 novembre 2026. L’installation verrouillée a résolu le SDK officiel MCP Python 2.3.0 et la grammaire Tree-sitter C#.

| Vérification | Résultat observé |
| --- | --- |
| Tests MCP | 14 réussis sur Python 3.11.14 et 3.12.12. Le client SDK découvre et appelle les quatre outils dans un processus stdio indépendant. |
| Régression de la skill | 102 tests réussis sur les deux versions Python, dont le clonage d’un dépôt synthétique et le routage d’activation heuristique. |
| Installation Codex et Claude Code | Les deux copies de la skill s’installent dans un projet synthétique, préservent les instructions préexistantes et réussissent l’audit de distribution. |
| PurrDocs officiel | 217 fichiers synchronisés au commit `5b146a3bd382ffda7d214af912b106d131301c0c`, dont 216 pages consultables et 767 passages. Empreintes confirmées, cibles du sommaire présentes. |
| Recherche en stdio sur le cache officiel | Requêtes mirroring, SyncVar, Network Rules, ObserversRpc et visibilité. Le résultat de mirroring pointe vers le bloc `>=1.4.0`. |
| Distribution Python | Installation depuis `uv.lock` et construction d’une wheel. Inspection du contenu de la wheel. |

Les tests MCP couvrent également les deux plages de mirroring sur une version PurrDiction synthétique 1.3.7, un verrou Git non résolu, un cache Git divergent, la provenance documentaire, la recherche hors ligne, les signatures locales et leurs surcharges, un symbole absent, un index absent et la préservation de l’index après un échec. Les cas d’activation de la skill sont des tests déterministes. La compilation Unity, les parties multijoueurs et l’activation spontanée dans Codex ou Claude Code restent à mesurer.

## Suite priorisée

1. Ajouter une résolution Roslyn à partir des assemblies, symboles et paramètres Unity. Vérifier les signatures héritées, les API générées et les surcharges liées dans des projets aux versions fixées.
2. Exécuter les [comparaisons avec de vrais agents](../evals/MCP_COMPARATIVE_PLAN.md) et compiler les scénarios Unity qui modifient du C#.
3. Récupérer explicitement les sources et exemples officiels au commit du package quand les sources locales manquent. Établir des preuves reproductibles pour les couples de versions PurrNet/PurrDiction.
4. Relier les [incidents historiques](../references/historical/triage-playbook.md) aux scénarios de régression avec leurs dates et versions d’origine.
