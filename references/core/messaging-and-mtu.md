# Choice RPC / Broadcast / Events and MTU — Procedure

**Sources** : [Remote Procedure Calls](https://purrnet.dev/docs/systems-and-modules/remote-procedure-call-rpc), [Network Manager](https://purrnet.dev/docs/systems-and-modules/network-manager), [Broadcasts](https://purrnet.dev/docs/systems-and-modules/broadcast), [Bandwidth Profiler](https://purrnet.dev/docs/systems-and-modules/bandwidth-profiler).

## Directorate and security

| Need | Mechanism | Controls |
|---|---|---|
| Client demande un achat | `[ServerRpc]` on NetworkIdentity | Ownership/RequireOwnership according to rules, calling identity, server-side price/stock |
| Server notifies observers | `[ObserversRpc]` | Check who observes, `BufferLast` for last occurrence only |
| Server responds to a player | `[TargetRpc]` with `PlayerID` | Valid/authenticated PlayerID; visibility and timing |
| Information without NetworkIdentity | `Broadcast` | Subscription/unsubscribe, connection vs player scope, validation |
| Durable state on the late join side | SyncVar/SyncList/State | Avoid rebuilding a world from a series of buffered RPC |

**Extrait documentaire illustratif** :

```csharp
[ServerRpc(requireOwnership: false)]
private void RequestAction()
{
    // Validate the caller and gameplay rules before changing state.
}

[ObserversRpc(bufferLast: true)]
private void AnnounceState(int value)
{
    // Ne remplace pas un snapshot complet.
}
```

The exact names/attribute parameters may vary in the codegen/between docs; check the case/overload of **the installed version**. `RunLocally` can result in local execution; on dedicated server, do not put the entire spawn or generation of the world into an observation-only callback executed only on the client side.

## Delivery, fragmentation and volume

- `ReliableOrdered` for operations that must not be lost; `Unreliable` or `UnreliableSequenced` for frequently replaced states. The semantics of `UnreliableSequenced` depend on the transport and setting MTU: inspect current code and docs.
- A payload higher than the MTU can be fragmented, **promoted as reliable** or abandoned following `NetworkManager.mtuExceededBehaviour` or the RPC override. Lost fragments can invalidate the entire message; avoid using fragmentation as a file protocol.
- `Immediate` reduces flush wait but batching is less effective. Measure before increasing its use.
- Check losses in **Tools/PurrNet/Analysis/Bandwidth Profiler**. The categories `Expired`, `Evicted`, `BudgetExceeded`, `SequencedStale` guide the diagnosis.

## Test reproductible

1. Check with host, remote client, dedicated (if relevant), non-observer and unauthorized client.
2. Capture and replay an input likely to be lost; determine whether a lasting state should be synchronized.
3. Force large payload, MTU variation, loss and latency; record fallen and bytes/sec messages.
4. Test RPC sent before the end of auth/scene/observation: do not assume that the recipient already exists.
5. For audio, Animator or Transform, first evaluate PurrNet components (avoid RPC home by tick).
