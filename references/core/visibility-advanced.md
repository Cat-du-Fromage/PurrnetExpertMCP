# Network Visibility: exact evaluation order and pitfalls

Official: `systems-and-modules/network-manager/network-visibility/{README.md,visibility-rules.md,whitelist-and-blacklist.md,distance-condition.md,using-the-visibility.md}`.

## Server evaluation order

For a player and a NetworkIdentity, the first matching condition wins according to current official docs:
1. Parent hidden → child hidden.
2. Player in the identity's **whitelist** → visible.
3. Player in the identity's **blacklist** → hidden.
4. No applicable rule-set → visible.
5. Player is owner → visible.
6. **At least one rule in rule-set returns true** → visible; otherwise hidden.

Therefore multiple rules are OR, not AND. A whitelist can override a blacklist where both are present per the documented evaluation order. A parent hidden condition still comes first.

## Component and hierarchy specificity

- Observers are tracked per network component, not only GameObject. A GameObject remains spawned while at least one component is visible. `OnObserverAdded/Removed` may fire per component.
- Per-identity override applies downwards with **Children Inherit**; placing override on a lower component in the same GameObject does not override components above it. Put override on the top relevant network component to avoid unintended visibility.
- Visibility is **not continuously recalculated**; ask for reevaluation when game state changes (see `using-the-visibility.md`). `CanSee` runs on server; prioritize cheap tests in custom rules.
- Visibility is about which data is replicated, not a trusted authorization check. Use separate server validation to guard attack/trade/chat actions. OwnerOnly scopes module data, not spawned identity.
- PurrDiction predicted visibility uses separate server controls (`PredictionManager.HideFrom/ShowTo`), not these ordinary Network Rules.

Tests: 3 players, mixed owners, whitelists and blacklists, nested children, per-component override, scene loads, late join and re-evaluation after team change; capture observers/server logs to prove no private data escaped.
