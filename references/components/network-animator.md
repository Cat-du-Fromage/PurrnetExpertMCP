# NetworkAnimator

Official: `plug-n-play-components/network-animator.md`.

- Add **NetworkAnimator and Animator to the same GameObject**. Select only the parameters that genuinely need network synchronization.
- **Animator triggers are not synchronized automatically**: send through `NetworkAnimator.SetTrigger("Action")`, not merely `Animator.SetTrigger(...)` on a controller. `NetworkAnimator.SetFloat/SetBool` are documented for normal parameters; verify method signatures against installed assembly.
- Distinguish visual-only animations derived from synchronized state from authoritatively networked gameplay transitions. For PurrDiction, avoid classic NetworkAnimator as the source of predicted simulation; drive animator parameters via `UpdateView` from predicted view state.
- Test 2 clients, late join for persistent parameters, event triggers while packet loss simulated, owner transfer, and ensure triggers do not repeat unexpectedly.

## Pedagogical example (v0.6)

```csharp
[SerializeField] private NetworkAnimator _networkAnimator;

private void PlayAttackAnimation()
{
    // Call this from the peer with authority.
    _networkAnimator.SetTrigger("Punch");
}
```

`Animator.SetTrigger("Punch")` alone is not automatically replicated. The component must be on the same GameObject as the Animator and permission to issue changes depends on its ownership/configuration. See also `assets/unity/ExampleNetworkAnimator.cs` (**uncompiled**). Test host, remote owner, late join and close triggers; do not without reason convert any animation to manual RPC.
