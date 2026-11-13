# Official documentation PurrDocs (optional cache)

This cache folder ** is not included in the archive**. For a complete Markdown copy that can be used offline, run:

```bash
python scripts/sync_sources.py
python scripts/docs_catalog.py coverage
```

The script clones **all** the `PurrNet/PurrDocs` repository on `references/cache/official-docs/` and creates a `docs-index.json` indicating the exact commit. The original syntheses in `references/*.md` remain available even without syncing. Do not republish this cache without checking the rights.

Set `PURRNET_DOCS_DIR` on the absolute path of the clone allows you to share the same cache between the installed copies of the skill and the MCP. The server builds its SQLite database next to the inventory with `uv run purrnet-expert-cache index` from the repository. The skills scripts read the Markdown directly.


## Archive Stray Help (opt-in, distincte de PurrDocs)

```bash
python scripts/sync_stray_archive.py
python scripts/search_stray_archive.py 'NetworkTransform' --limit 8
```

This script downloads locally **the exact historical commit** from `nmban/Purrnet-Stray_Help`, without overwriting the files and without republishing it. Discord responses are historical, non-normative and potentially sensitive; see only a few extracts useful for diagnosis. The `references/cache/` folder is ignored by Git and **excludes all ZIP** from the skill.
