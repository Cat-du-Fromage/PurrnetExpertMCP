# Patrons Unity C# — opt-in, not automatic installation

These files are ** autonomous examples written for this skill**. They are **not** Edgegap deployment templates and have **not been compiled with Unity** here. Before making them project scripts:

1. Check the `Assets/PurrNet/Runtime/` or `Packages/dev.purrnet.purrnet/` signature of the installed revision.
2. Copy only the useful file to `Assets/` from your Unity project; adjust the namespace / `.asmdef`.
3. Add the script to a GameObject with/configured with a `NetworkIdentity` according to documentation and Network Rules. Check for prefab and ownership in Unity.
4. Test in host then with two clients; never declare ready for a competitive game without explicit permission and splendour.

## Patron 1 : ExampleNetworkCounter.cs

Minimum example of a ** client intention** to the server via `[ServerRpc]` and then a durable `SyncVar<int>` state. The call should come from the right owner under Network Rules strict; this demo version is **not** spam resistant and **does not** replace gameplay validations.

## Patron 2 : ExampleWorldSeed.cs

Example of server initialization and seed diffusion with `[ObserversRpc(runLocally: true, bufferLast: true)]`. Demonstrate host / dedicated distinction and late arrival. For a real game, keep server-side determinant states and use the appropriate replication mechanism; a received seed does not automatically represent the state of the entire world.

Sources to be checked:
- https://github.com/PurrNet/PurrDocs/blob/main/systems-and-modules/remote-procedure-call-rpc/README.md
- https://github.com/PurrNet/PurrDocs/blob/main/systems-and-modules/network-modules/sync-types/syncvar.md
- https://github.com/PurrNet/PurrDocs/blob/main/systems-and-modules/network-identity/networkbehaviour.md

### PurrDiction v0.3

**No C# PurrDiction template is certified here.** Predictive signatures (including modules/policies) evolve; read `references/purrdiction-best-practices.md` and the source actually installed before building an example. It is preferable to derive a controller from the official sample of the corresponding commit rather than provide a false example "ready to compile".

## v0.6 additional examples (NOT Unity-compiled)

- `ExampleNetworkAnimator.cs` illustrates the official `NetworkAnimator.SetTrigger` call; the application must make sure the caller has authority. A pure `Animator.SetTrigger` is not automatically synchronized.
- `ExamplePredictedData.cs` provides `IPredictedData` input/state *shapes* only; it is not a controller and does not demonstrate complete IMath, rollback, Animator view or input sanitization. Use `references/prediction/real-world-recipes.md` and the installed PurrDiction source before building a controller.

**Provenance:** Adapted from official API documentation, not independently compiled or tested against Unity/PurrDiction packages in this archive. Treat as learning aids.
