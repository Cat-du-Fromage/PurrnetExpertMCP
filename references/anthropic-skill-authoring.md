# Quality contract Agent Skills — Anthropic

**Primary source**: https://platform.claude.com/docs/fr/agents-and-tools/agent-skills/best-practices (accessed for v0.9.0). Do not confuse skill writing criteria with Best Practices **PurrDiction**.

## Concrete checklist and reason

| Aspect | Criterion v0.9 | Pourquoi |
| --- | --- | --- |
| Discovery | `description` to the 3rd person, action **and** triggers, <=1024 characters | This is the metadata read to select the skill |
| Metadata | `name` tiny / tores <=64 characters, YAML readable frontmatter | Compatibility Agent Skills |
| Contexte | `SKILL.md` <=500 lines, only critical safeguards + workflow choices | Do not saturate context with each activation |
| References | Direct paths from `SKILL.md` for frequent guides; avoid guide chain -> guide -> details | The model can interrupt deep navigation |
| Documentation longue | Table of contents if >100 lines | The agent can read only one extract |
| Workflows | Enter, choose, sequence, validation gate, correction after failure | Reduces audit omissions |
| Exemples | Distinguish explanatory fragment, recipe to complete, Unity code actually compiled | Avoid false confidence |
| Scripts | Python 3 stdlib whenever possible, explicit prerequisites, useful errors, safe and dry-run commands | Multi-environment reproducibility |
| Evaluation | Positive/negative cases, concrete context, comparison with/without, real model tests | Local proxies do not prove spontaneous activation |
| Composability | Handoff to `edgegap-purrnet` only if Edgegap tasks; do not divert FishNet/Mirror | Compatible with other skills |
| Versions | No immutable "last" or APIs guaranteed without installed package | Avoid outdated instructions |

## Validation cycle for an update

1. Audit the discovery and frontmatter: `python scripts/audit_skill_authoring.py`.
2. Check guides, links and routes: `python scripts/validate_skill.py` and `python scripts/route_docs.py "..."`.
3. Check the API **in** Unity installed, then compile and test the games if the Editor is available.
4. Perform agent evaluations **real**: triggered/untriggered recordings, actually open references, final modification and tests. Compare multiple models if it is the target audience.
5. Correct detected errors, then repeat. Do not mark "E2E successful" because the Python test tool is green.

## Levels of evidence

- Structure/frontmatter and scripts: Provable locally by Python.
- Coverage: estimated by index and route; no guarantee of LLM comprehension.
- Competency/autonomous activation: **requires real agent runs** (Haiku/Sonnet/Opus if targeted).
- Network behavior and compilation: **Requires Unity**; no Python output can replace it.
