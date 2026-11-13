# Source map PurrNet

> Initial verification: November 12, 2026. Branches and pages evolve.

## 1. Official documentation

- Index humain : https://purrnet.dev/docs
- GitHub source index, navigable and versionable : https://github.com/PurrNet/PurrDocs/blob/main/SUMMARY.md
- Sources Markdown : https://github.com/PurrNet/PurrDocs
- Installation : https://purrnet.dev/docs/getting-started/installation-setup
- Minimal Setup : https://purrnet.dev/docs/getting-started/getting-started
- Network Manager : https://purrnet.dev/docs/systems-and-modules/network-manager
- Network Rules : https://github.com/PurrNet/PurrDocs/blob/main/systems-and-modules/network-manager/network-rules.md
- NetworkIdentity : https://purrnet.dev/docs/systems-and-modules/network-identity
- NetworkBehaviour : https://purrnet.dev/docs/systems-and-modules/network-identity/networkbehaviour
- RPC : https://purrnet.dev/docs/systems-and-modules/remote-procedure-call-rpc
- SyncVar : https://github.com/PurrNet/PurrDocs/blob/main/systems-and-modules/network-modules/sync-types/syncvar.md
- Spawning/Despawning : https://purrnet.dev/docs/systems-and-modules/network-identity/spawning-and-despawning
- Prediction : https://purrnet.dev/docs/client-side-prediction

The `SUMMARY.md` file is a **yearbook** of subjects, not proof that
each page corresponds to the installed version. The site has a selector
"Package versions": check versions in sensitive questions.

## 2. Repositories officiels

Organisation : https://github.com/orgs/PurrNet/repositories

- Core : https://github.com/PurrNet/PurrNet (branche `release` stable,
  `dev` more recent, but more changing)
- Docs source : https://github.com/PurrNet/PurrDocs
- Prediction : https://github.com/PurrNet/PurrDiction
- Lobby : https://github.com/PurrNet/PurrLobby
- Dissonance : https://github.com/PurrNet/PurrNet-Dissonance
- Sample : https://github.com/PurrNet/PurrNet-Incremental-Sample
- Example/template : https://github.com/PurrNet/game-jam-template

Core code in `Assets/PurrNet/Runtime/`; package UPM in
`Assets/PurrNet/package.json`. Examples can also be found in
`Assets/PurrNet/Examples/`. Check file existence and symbols
before quoting an implementation.

Example of a documented stable installation:
`https://github.com/PurrNet/PurrNet.git?path=/Assets/PurrNet#release`

## 3. Base historique Discord/Stray Help

- Index `llms.txt` **Added to commit provided**:
  https://github.com/nmban/Purrnet-Stray_Help/blob/e6140a571228044fe670b500e245f6bb370b2e06/llms.txt
- FAQ :
  https://github.com/nmban/Purrnet-Stray_Help/blob/e6140a571228044fe670b500e245f6bb370b2e06/docs/FAQ.md
- Quick Reference :
  https://github.com/nmban/Purrnet-Stray_Help/blob/e6140a571228044fe670b500e245f6bb370b2e06/docs/QUICK_REFERENCE.md
- History and developers: see the paths listed in `llms.txt`.

The index announces more than 15,000 Q/R and a history up to v1.20.0.
is **dated testimony**, not current official documentation.
Avoid importing the entire logs into context at each query.

## 4. Targeted search procedure

1. Read the class name/attribute in the application.
2. Open `SUMMARY.md` to discover the relevant page.
3. Search for the symbol in the exact code installed (or commit core repository).
4. Confirm with the corresponding documentation.
5. On known bug only, search the FAQ and then the historical answers.
6. For an addon function, check its **dependence and separate version**.

## New entry points in v0.3

- `references/documentation-map.md` to discover **all** documented categories, not a whitelist of nine files.
- `references/documentation-policy.md` and `scripts/sync_sources.py` to clone PurrDocs and keep SHA source (without redistributing doc to ZIP).
- `scripts/docs_catalog.py coverage`: checks critical paths and links SUMMARY, `search`: searches all over the clone, including pages not listed in SUMMARY.
- `references/purrdiction-best-practices.md` and `references/purrdiction-architecture.md`: mandatory prediction rules.
- `references/networking-best-practices.md`: module life cycle, authority, RPC and standard PurrNet limits.
- `scripts/inspect_project.py` covers `dev.purrnet.purrdiction` independently of the core.

## Update v0.7 — Stray Help pinned incidents

- Case verified at historical source `e6140a571228044fe670b500e245f6bb370b2e06`: `references/historical/incident-catalog.json` (35 **sorting scenarios**, not 35 current bugs).
- Synthetic sources: [`docs/QUICK_REFERENCE.md`](https://github.com/nmban/Purrnet-Stray_Help/blob/e6140a571228044fe670b500e245f6bb370b2e06/docs/QUICK_REFERENCE.md), [`docs/FAQ.md`](https://github.com/nmban/Purrnet-Stray_Help/blob/e6140a571228044fe670b500e245f6bb370b2e06/docs/FAQ.md), [`docs/changelogs/versions.md`](https://github.com/nmban/Purrnet-Stray_Help/blob/e6140a571228044fe670b500e245f6bb370b2e06/docs/changelogs/versions.md).
- `docs/dev-answers/*.md` files and raw Discord (total advertised: ~15k Q&A messages) are **not all analyzed**. Optional local search after `scripts/sync_stray_archive.py`, via `scripts/search_stray_archive.py`. Do not assume redistribution permission.
- Known contradictions with current PurrDocs: "last" version, old repo `BlenMiner`, integration Dissonance, serialization of references, membership vs loaded-scene events and old callback names. The exact source of the project takes precedence.
