# Network Rigidbody 3D/2D

Official: `plug-n-play-components/network-rigidbody.md`, `network-rigidbody-2d.md`, `guides/physics-in-multiplayer.md`.

- Choose for **classic** synchronized Rigidbody physics, not as a replacement for PurrDiction `PredictedRigidbody` (rollback/replay). Use correct 2D component for Rigidbody2D.
- Inspector **Owner Auth** chooses simulation truth (owner or server). For important collisions and competitive games prefer server auth with validation; never assume owner auth prevents cheating.
- Read actual settings in version-installed docs before tuning: Interpolation Delay, Prediction Factor, Position/Rotation Strength, Correction Range, Hard Snap Distance. They interact; no universal values.
- Parent-relative correction settings matter for translating/rotating platforms; origin-shifted large worlds have dedicated documented strategies. For teleports use API documented under *Teleporting*, not blind direct transform writes on every peer.
- Do not run competing movement scripts on observers or combine pose writers without checking component interaction.

Tests: collisions at differing latency and frame rates, parent moving/rotating, teleport, hard correction, 2 clients and dedicated server, late join. Profile bandwidth and compare authoritative physics state.
