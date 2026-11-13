# Audit structurel : PurrNet Expert v0.7 -> v0.8 contre edgegap-purrnet

Reference examined: https://github.com/edgegap/llm-agent-skills/tree/main/skills/edgegap-purrnet — tree `main` **fd510ba826ea29ab359e70e185d2e650ef6827de**. Comparison made on `SKILL.md`, four references, assets Unity/Docker/matchmaker, assessments under **`evals/purrnet-evals.json`** and **`evals/purrnet-routing-eval.json`** at the root of the repository (not in the skill file).

## Audited results

| Dimension | Edgegap PurrNet | PurrNet Expert v0.7 | Correction v0.8 |
|---|---|---|---|
| Perimeter | Very targeted: dedicated and matchmaking Edgegap | Large: API, prediction, sync, bugs, components | Keep perimeter, clarify handoffs |
| Frontmatter | Symptoms + addictions and negative cases | Good FR/EN but too much overlap with hosting | Short description and explicit border |
| SKILL Entry | ~12.5 KB, numbered phases and checks | ~19 KB, many priority rules | ~10.5 KB, short run to load as needed |
| Workflows | Local -> Docker -> direct deploy -> matchmaker -> 2 clients -> stop | General single phase, few observable checks | Workflows feature/bug/dedicated/prediction/Edgegap |
| Modifications | Bootstrap runtime without touching the scenes | Recommends minimum changes but without method | Rule "Preserve Editor host + clones" and flag inspection |
| Assets | Config, C#, .meta, link.xml, matchmaker and Docker scripts, tested on a sample | Some educational snippets NOT compiled Unity | Keep explicit marking + verification tools and integration steps |
| Evidence | Sample Unity PurrNet Incremental, two built clients and server on Edgegap announced | Python static, no Unity compilation | D0-D6 Evidence Contract, Screened and Manifest Evidence Test |
| Evaluations | 3 rich scenarios with environmental assertions and limits, positive/negative routing | Lots of JSON evaluations, but no E2E harness | New scenarios requiring file and log change; evidence harness |
| Security | API secret and register, stop of allowances invoiced | Generic warning | Cloud checklist in handoff workflow, never copy tokens |

## Observed risks and arbitrations

1. **Don't turn the pack into Edgegap**: SDK, 7777, Dockerfile, tickets and self-stops of the specialized skill have no meaning for a local server or other platform. Adapt PurrNet gameplay architecture, not cloud templates.
2. **Do not confuse documented test and compilation in our environment**: Edgegap reports a sample tested with Unity 6000.3.11f1, PurrNet `dev` and SDK 3.5.5 (its instructions now require 3.5.6+ for some cases). Our pack does not have this proof.
3. **Fresh vs hardcode reference**: Edgegap formulates certain choices like "use the latest SDK version"; in our skill, prefer to inspect and lock a version tested in a reproducible project rather than update without verification.
4. **Host-specific bug**: the documented example `ResourceSpawner.InitSeed` is based on `ObserversRpc` not running on dedicated without `runLocally:true`. Include it as a generic symptom and pre-dedicated test, without imposing this patch on all RPC.
5. **Asynchronicity of `StartClient`**: a `Disconnected` state just after the call does not mean failure; the static test must report the retry loops too immediate, not modify the transports automatically.
6. **Inter-skill** negative routing: `SyncVar` without hosting should not activate Edgegap, Edgegap explicit hosting should choose `edgegap-purrnet`, NGO/FishNet should not activate PurrNet Expert. Cases are formalized in `evals/v0.8-routing.json` and in local proxy tests.

## Distinction de validations

The Python v0.8 suite checks scanners, data, demonstrations and contract rules. **It does not measure a model benchmark, does not compile Unity, does not validate a Docker image and does not trigger a Codex/Claude skill.** For a test comparable to the Edgegap test, take a known Unity project and run `evals/V08_E2E_PLAN.md` on a real agent session by recording traces, diffs, logs, two clients and dedicated.
