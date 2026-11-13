# PurrnetExpertMCP

**purrnet-expert** is an Agent Skill for designing, debugging and testing Unity multiplayer with PurrNet and PurrDiction. **PurrNet Expert MCP** gives the skill installed package versions, local C# declarations and official PurrDocs passages with source references.

## Quick start

From this repository, with Git, uv and Python 3.11 or later:

```sh
uv sync --locked
uv run --no-sync python scripts/sync_sources.py
uv run --no-sync purrnet-expert-cache index
uv run --no-sync purrnet-expert-cache status --verify
uv run --no-sync purrnet-expert-mcp
```

The last command starts a stdio MCP server. See the [installation guide](docs/installation.md) for Codex, Claude Code, cache updates and standalone skill use.

| Tool | When to call it |
| --- | --- |
| `get_purrnet_project_context` | Identify the Unity version and installed packages before working on a networking task. |
| `search_purrnet_docs` | Find official passages about an API or behavior and its version conditions. |
| `get_purrnet_api` | Find local C# declarations and overloads before using an API. |
| `check_purrnet_compatibility` | Check version conditions for a `path.md:line` reference or inspect evidence for a symbol. |

The server searches its local SQLite FTS5 index offline. Tree-sitter checks the syntax of C# declarations. Full C# resolution, generated APIs, Unity settings and multiplayer behavior require further validation. See the [architecture](docs/architecture.md), [source policy](docs/source-policy.md) and [validation report](docs/validation.md).

The [skill](SKILL.md) loads focused guides on demand and includes scripts for working without the MCP server. See the [v0.9.0 quality report](QUALITY_REPORT.md) for the historical validation record.
