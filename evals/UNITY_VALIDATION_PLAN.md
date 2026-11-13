# Unity validation matrix for v0.5

**Status: NOT RUN.** Fixtures are scenarios to instantiate in a real Unity project.

## Environment
- Record exact Unity Editor version, PurrNet version/ref/hash, PurrDiction version/ref/hash, render platform, .NET/IL2CPP, standalone vs Editor and transport settings.
- Run a clean import/compile and a build on **each target platform**. Do not label `Unity -batchmode -quit -projectPath ...` as a Player build; it primarily checks import/compilation.
- Editor host is not equivalent to a dedicated server. Launch server-only build and two independent standalone clients.

## Minimal fixture matrix

| Fixture | Client A/B expected | Server expected | Negative test |
|---|---|---|---|
| Health SyncVar | Owner changes via validated command, observers update and late join recovers | Server validates damage and writes HP | Non-owner/negative/too large damage rejected |
| Owner-only inventory | Other observers never receive owner data | Transfers ownership and prepares privacy purge | Former owner no longer retains sensitive client data when purge is required |
| NetworkTransform | Observer interpolation from controller; parent updates | Correct authoritative role | Test 150ms jitter / packet loss and another move script on observer |
| NetworkAnimator | Trigger via wrapper reaches observer | Correct authority | Direct Animator.SetTrigger does not imply network trigger |
| NetworkAudioSource | Dynamic clip from registered NetworkAssets plays | Owner/server authority enforced | Unregistered clip and non-controller attempt |
| Scene-scoped prefab | Late join resolves scene-scoped asset only when corresponding scene loaded | Registers scoped prefab and unloads | Duplicate global registry / wrong spawn scene |
| Predicted controller | Local immediate motion and remote correction | Input sanitized, server remains authoritative | Packet loss, replay side effects, different FPS |
| Predicted projectile | Spawn/despawn reconciles without dangling references | Authoritative hit and projectile creation | Failed input, extrapolation repeats, pool reuse |
| Predicted state machine | Visual events once, gameplay consistent after replay | Exact state transitions validated | 100ms jitter/ownership transfer |
| Dedicated world seed | Same world on both standalone clients | Server initializes world without local client | Host-only initialization does not pass |

## Required proof artifacts

- Unity import and Player build logs; build target, codegen/asmdef errors and warnings.
- Separate server + clients logs with timestamps; reproduction steps and network simulator settings.
- Static quality reports and source paths/commit for every referenced API.
- Test status for each row: PASS, FAIL, NOT_RUN, NOT_APPLICABLE with explicit reason.
- For PurrDiction: BP-01 through BP-10 status; zero warnings in text scanner is not evidence of replay safety.

## Agent benchmark

Run identical fixture/prompts from `evals/v0.5-hardcases.json` both **without skill** and **with skill**, and grade expected assertions blindly. Do not record a score until these runs are actually executed.
