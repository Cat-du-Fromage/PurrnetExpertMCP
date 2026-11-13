# Implementation status of code recipes

**No Unity compilation has been executed for bundled `.cs` examples.** The inherited `ExampleNetworkCounter.cs` and `ExampleWorldSeed.cs` remain didactic samples. Do not label them verified/production-ready. The v0.5 improvement focuses on **version-indexed recipes and executable test plans** instead of false assurances.

For every delivered implementation require:
- Source PurrNet/PurrDiction package versions and Git commit, relevant docs commit.
- Explicit component/Inspector configuration and non-code dependencies.
- Compilation with Unity batchmode on a clean project, including IL2CPP if needed.
- Two remote builds, dedicated server where relevant, late join, ownership, permission tests, packet loss/jitter, host parity, PurrDiction rollback where relevant.
- `tested` / `not tested` / `unsupported by installed version` recorded per test.

Suggested fixture backlog: authoritative SyncVar health and validated inventory, NetworkAnimator trigger, owner and server NetworkTransform, predicted input/STATE controller, predicted projectile/physics, static and dynamic PredictedModule, predicted StateMachine, Addressable spawn with additive scenes, dedicated world seed with no host local client. No fixture is marked passed until a real Unity log and reproducible run exist.
