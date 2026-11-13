# Local installation

Use Git, uv and Python 3.11 or later with SQLite FTS5. Run `uv sync --locked` in this repository to install from `uv.lock`. The configurations below reuse that environment with `--no-sync`.

## Synchronize documentation

```sh
uv run --no-sync python scripts/sync_sources.py
uv run --no-sync purrnet-expert-cache index
uv run --no-sync purrnet-expert-cache status --verify
```

To update PurrDocs, rerun the sync script with `--refresh`, then rebuild the index. To reproduce a snapshot, pass `--commit <FULL_SHA>` before indexing. The script retains the previous commit's inventory in `docs-index.previous.json`. The existing index stays readable during updates and after a failed rebuild.

The default checkout is `references/cache/official-docs` in this repository. To share another checkout between the skill and server, set `PURRNET_DOCS_DIR` to its absolute path in both environments. Use a dedicated parent directory for the checkout, `docs-index.json` and `purrdocs.sqlite3`. The skill scripts can read the checkout directly. A `stale` status indicates that the inventory has changed since indexing. `status --verify` also checks file hashes.

## Install the skill in a Unity project

```sh
uv run --no-sync python scripts/install_project.py "/absolute/path/to/UnityProject" --target both
uv run --no-sync python scripts/install_project.py "/absolute/path/to/UnityProject" --target both --apply
```

The first command previews changes. The second installs the skill in `.agents/skills/purrnet-expert` for Codex and `.claude/skills/purrnet-expert` for Claude Code. It adds a delimited activation block to `AGENTS.md` and `CLAUDE.md`. Use `--skip-hooks` to install only the skill and `--upgrade` to back up and replace the previous installation. Without the MCP server, the skill uses its router, PurrDocs catalog, C# search and version checker.

## Codex

Add this entry to `~/.codex/config.toml`. Replace the paths and use the absolute path to `uv` if Codex cannot locate it.

```toml
[mcp_servers.purrnet-expert]
command = "uv"
args = ["--directory", "/absolute/path/to/PurrnetExpertMCP", "run", "--no-sync", "purrnet-expert-mcp"]

[mcp_servers.purrnet-expert.env]
PURRNET_PROJECT_ROOTS = "/absolute/path/to/UnityProject"
```

Restart the session and verify the entry with `codex mcp list`. [Codex documentation](https://developers.openai.com/codex/mcp).

## Claude Code

Add the entry from [claude.mcp.example.json](claude.mcp.example.json) under `mcpServers` in the Unity project's `.mcp.json`. Replace the paths, open the project in Claude Code and check the server in `/mcp`. Windows JSON paths accept forward slashes or escaped backslashes. [Claude Code documentation](https://code.claude.com/docs/en/mcp).

`PURRNET_PROJECT_ROOTS` limits which projects the server can inspect. Separate multiple roots with the system's path separator, `;` on Windows and `:` on Linux/macOS. Pass absolute project paths to MCP tools.

## Tests

```sh
uv run --no-sync python -X utf8 -m unittest discover -s tests -v
uv run --no-sync python -X utf8 -m unittest discover -s scripts -p "test*.py" -v
uv run --no-sync python -X utf8 scripts/validate_skill.py
```

Use `validate_skill.py --release` to audit a distribution tree. CI runs it on a clean checkout without the documentation cache.
