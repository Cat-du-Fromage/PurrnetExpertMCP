# Network Visibility and interest management

**Official source**: `systems-and-modules/network-manager/network-visibility/README.md`, `visibility-rules.md`, `whitelist-and-blacklist.md`, `distance-condition.md`, `using-the-visibility.md`.

- The server determines **by player and by NetworkIdentity** who watches the object. No observer = object absent from this player, therefore no RPC/state of this object.
- The rules of a rule-set are combined in **OR**: only one authorization is sufficient; the object is masked without a rule (except for exceptions). Never interpret multiple rules as an implied ET.
- White/black lists are evaluated before the rules; the owner retains visibility according to the documented contract. Check the exact order on the `README.md` page.
- Visibility may differ between several network components on the same GameObject. It remains present as long as at least one component is visible. Observation callbacks may be specific to the component or object.
- `CanSee` and the evaluation are **server only**; shared rules should not maintain an object-specific state. Promote low `complexity` on inexpensive rules.
- Do not confuse visibility filtering (optimization/confidentiality of objects) with `ownerOnly` (confidentiality of a module) or visibility **PurrDiction** (`references/prediction/visibility-and-interactions.md`).

## Tests
Two teams and three players at different distances, white/black list, transfer of owner, addition/deletion of observer, late join. Check data/RPC absence for the unauthorized player, not only made hidden.
