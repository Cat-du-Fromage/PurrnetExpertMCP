# PurrNet diagnosis workflow and utilities

Official: `systems-and-modules/bandwidth-profiler.md`, `tools/type-hash-resolver.md`, `systems-and-modules/transports/simulating-latency.md`, `tools/conversion-tool/README.md`, `systems-and-modules/instance-handler.md`, `systems-and-modules/bots.md`.

1. **Collect evidence**: package hashes, Unity Editor.log/Player.log, exact failing role/server, scene, transport, connection state, tick and reproduction.
2. **Bandwidth Profiler**: Tools → PurrNet → Analysis → Bandwidth Profiler. Look at per-object, RPC, parameters, dropped fragmented unreliable messages; sample reasons include Expired, Evicted, BudgetExceeded, SequencedStale. Compare before/after bytes, not guesses.
3. **Type Hash Resolver**: Tools → PurrNet → Analysis → Type Hash Resolver. Accepts signed/unsigned decimal or `0x` hash and returns matching type/assembly and registration status; it does **not** register it.
4. **Simulated latency**: verify loss/jitter/RTT/different frame rates; note tool/provider and exact settings. Test host and actual remote build.
5. **InstanceHandler**: look up documented registry/manager access patterns instead of inventing arbitrary global singletons.
6. **Bots**: convenient repeatable load/logic tests; verify bots traverse correct network state/lifecycle and do not count as real clients without proof.
7. **Conversion Tool**: for Mirror/FishNet migration review official converter source and manual cleanup; don't assume full semantic equivalence.

Create a minimal repro with known versions before rewriting large networking subsystems.
