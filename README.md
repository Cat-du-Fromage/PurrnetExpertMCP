# PurrnetExpertMCP

**purrnet-expert** est une Agent Skill pour concevoir, diagnostiquer et tester le multijoueur Unity avec PurrNet et PurrDiction. **PurrNet Expert MCP** lui fournit les versions du projet, les déclarations C# locales et les passages officiels PurrDocs avec leur provenance.

## Démarrage

Depuis ce dépôt, avec Git, uv et Python 3.11+ :

```sh
uv sync --locked
uv run --no-sync python scripts/sync_sources.py
uv run --no-sync purrnet-expert-cache index
uv run --no-sync purrnet-expert-cache status --verify
uv run --no-sync purrnet-expert-mcp
```

La dernière commande attend un client MCP sur stdin. Le [guide d’installation](docs/installation.md) couvre Codex, Claude Code, la mise à jour du cache et le mode autonome de la skill.

| Outil | Quand l’appeler |
| --- | --- |
| `get_purrnet_project_context` | Identifier Unity et les packages réellement disponibles avant de traiter un problème réseau. |
| `search_purrnet_docs` | Retrouver des passages officiels sur un symbole ou un comportement et leurs éventuelles conditions de version. |
| `get_purrnet_api` | Retrouver les déclarations locales et leurs surcharges avant d’utiliser une API C#. |
| `check_purrnet_compatibility` | Vérifier une condition de version sur un passage `path.md:line` ou examiner les preuves disponibles pour un symbole. |

Le serveur consulte le cache hors ligne. Tree-sitter vérifie la syntaxe des déclarations retrouvées. La résolution C# complète, les API générées, la configuration Unity et les tests réseau relèvent de validations supplémentaires. Voir [l’architecture](docs/architecture.md), la [politique des sources](docs/source-policy.md) et le [rapport du premier jalon](docs/validation.md).

La skill v0.9.0 et ses [rapports existants](QUALITY_REPORT.md) restent à la racine. Son [point d’entrée](SKILL.md) charge les guides à la demande et fournit les scripts de repli.

