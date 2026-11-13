# Automatic triggering: contract and limits

**The model chooses a skill based on its `name` and especially its `description`** (frontmatter). The `scripts/route_docs.py` router is executed **after** activation and does not directly influence this decision. No text in `SKILL.md` guarantees that all models will spontaneously load this skill.

## Desired trigger

1. **Explicit statement**: PurrNet, PurrDiction, PurrLobby, PurrVoice, `NetworkTransform`, `NetworkBehaviour`, `SyncVar`, `ServerRpc`, `PredictionManager` and other official symbols; generation, correction, documentation, review, compilation error.
2. **Implicit context in a recognized project PurrNet**: multiplayer game, remote player who jitters, unsynchronized balls, late join, owner vs server, different scenes, client inventory, dedicated server, matchmaking, desync, lag, packaget loss.
3. **Files**: `Packages/manifest.json` declares `dev.purrnet.purrnet` / `dev.purrnet.purrdiction`, code `using PurrNet;`, subclasses `NetworkBehaviour` / `PredictedIdentity`; a task that modifies these files and their network data.
4. **Cooperation**: PurrNet gameplay + Edgegap deployment -> use both skills if installed; do not replace `edgegap-purrnet` on Edgegap management.

## Anti-triggers (negative)

Do not activate just because the user says Unity, C#, animation of a local kinematic, shadow drawing, unsynchronized UI, solo backup, offline camera, or multiplayer game **FishNet/Mirror/NGO** without PurrNet.

## Deployment of staff

- Codex: Install `purrnet-expert/` in `.agents/skills/` (project directory); description is used for implicit activation. `AGENTS.md` optional strengthens the underlying tasks.
- Claude Code : install `purrnet-expert/` in `.claude/skills/` ; keep the trigger by the enabled model (do not set `disable-model-invocation: true`). `CLAUDE.md` optional gives the context of the project.
- Use `scripts/install_activation.py <PROJECT> --target both --apply` **only** if both installations exist. Without `--apply`, the script is read-only. `--remove --apply` removes only marked blocks. Other lines of existing files remain intact.
- This hook is **a textual instruction** and **not** a deterministic event system. The off-model tests below validate metadata, paths and routes, not the actual probability of triggering at Codex/Claude.

## Validation of activation on real agents

Execute the positive and negative prompts of the `evals/activation-cases.json` file from fresh sessions of the agent, visible in its catalog. Measure: `loaded` (file SKILL.md was opened?), `references_read` (guides required?), `API_verified`, `no_wrong_activation`. Compare with/without `AGENTS.md` / `CLAUDE.md`, model versions, and note negative false. The `test_v06.py` script is only a **terministic proxy**; it does not test the actual activation of a LLM.

## Reporting format of a real test

| Champ | Valeur |
|---|---|
| Agent/version | ... |
| Project detected as PurrNet | yes/no |
| Prompt | ... |
| Self-selected Skills | yes/no/not verifiable |
| Routes choisies | ... |
| Guides effectivement lus | ... |
| Justification of errors | ... |

## v0.8 — Avoiding skill collision between PurrNet and Edgegap

- If the application speaks **only** of PurrNet `SyncVar`, ownership, prediction or gameplay code: `purrnet-expert`, not Edgegap.
- If the request explicitly involves **Edgegap cloud** (deployment, Docker, build app/version, matchmaker, external port, self-stop): `edgegap-purrnet` is the main implementer; `purrnet-expert` remains a gameplay reviewer if necessary.
- Dedicated server **without Edgegap**: `purrnet-expert` (generic preparation); do not invent Edgegap dependencies.
- Project only Mirror/FishNet/NGO: do not select `purrnet-expert`, even on Edgegap, unless explicitly migrated.
- The `python scripts/cross_skill_selector.py "<demande>" [--purrnet-project]` diagnosis and the `evals/v0.8-routing.json` cases remain static **proxices**. True spontaneous activations should be observed in agent sessions.
