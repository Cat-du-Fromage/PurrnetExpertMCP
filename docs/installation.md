# Installation locale

Prérequis pour le serveur et la CI locale. Python 3.11 ou supérieur avec SQLite FTS5, Git et uv. Lancez `uv sync --locked` depuis le dépôt pour créer l’environnement à partir de `uv.lock`. Les configurations ci-dessous réutilisent cet environnement avec `--no-sync`.

## Synchronisation explicite

```sh
uv run --no-sync python scripts/sync_sources.py
uv run --no-sync purrnet-expert-cache index
uv run --no-sync purrnet-expert-cache status --verify
```

Pour mettre à jour PurrDocs, relancez le script avec `--refresh`, puis l’indexation. Pour reproduire un instantané, utilisez `--commit <SHA complet>` avant d’indexer. Le script conserve l’inventaire du commit précédent dans `docs-index.previous.json`. L’index existant reste lisible pendant une mise à jour et après un échec de reconstruction.

Le cache par défaut est `references/cache/official-docs` dans ce dépôt. Pour partager un autre emplacement avec la skill, définissez `PURRNET_DOCS_DIR` sur le chemin absolu du clone dans l’environnement du serveur et dans celui des scripts. Utilisez un répertoire parent dédié, car celui-ci contient aussi `docs-index.json` et `purrdocs.sqlite3`. Les scripts de la skill peuvent consulter ce clone sans installer le serveur. L’état `stale` indique un changement d’inventaire depuis l’indexation. `status --verify` vérifie également les empreintes sur disque.

## Installer la skill dans un projet Unity

```sh
uv run --no-sync python scripts/install_project.py "/absolute/path/to/UnityProject" --target both
uv run --no-sync python scripts/install_project.py "/absolute/path/to/UnityProject" --target both --apply
```

La première commande affiche les modifications prévues. La seconde publie la skill dans `.agents/skills/purrnet-expert` pour Codex et `.claude/skills/purrnet-expert` pour Claude Code. Elle ajoute un bloc délimité dans `AGENTS.md` et `CLAUDE.md`. `--skip-hooks` installe uniquement la skill et `--upgrade` sauvegarde l’installation précédente. Dans une session sans MCP, la skill utilise le routeur, le catalogue PurrDocs, la recherche C# et le vérificateur de versions existants.

## Codex

Ajoutez une entrée au fichier `~/.codex/config.toml`. Remplacez les deux chemins et utilisez le chemin absolu de `uv` si le client ne le trouve pas.

```toml
[mcp_servers.purrnet-expert]
command = "uv"
args = ["--directory", "/absolute/path/to/PurrnetExpertMCP", "run", "--no-sync", "purrnet-expert-mcp"]

[mcp_servers.purrnet-expert.env]
PURRNET_PROJECT_ROOTS = "/absolute/path/to/UnityProject"
```

Relancez la session et vérifiez l’entrée avec `codex mcp list`. [Documentation officielle Codex](https://developers.openai.com/codex/mcp).

## Claude Code

Ajoutez l’entrée de [claude.mcp.example.json](claude.mcp.example.json) sous `mcpServers` dans le fichier `.mcp.json` à la racine du projet Unity. Remplacez les chemins, ouvrez le projet dans Claude Code et vérifiez le serveur dans `/mcp`. Sous Windows, les chemins JSON acceptent les barres obliques ou des contre-obliques échappées. [Documentation officielle Claude Code](https://code.claude.com/docs/en/mcp).

`PURRNET_PROJECT_ROOTS` limite les projets consultables. Pour plusieurs racines, utilisez le séparateur de chemins du système, `;` sous Windows et `:` sous Linux/macOS. Les appels MCP prennent un chemin absolu du projet.

## Tests

```sh
uv run --no-sync python -X utf8 -m unittest discover -s tests -v
uv run --no-sync python -X utf8 -m unittest discover -s scripts -p "test*.py" -v
uv run --no-sync python -X utf8 scripts/validate_skill.py
```

Le contrôle `validate_skill.py --release` s’applique à un arbre destiné à être distribué. La CI l’exécute sur un checkout sans cache.
