# Classic Network Visibility decision order

**Official sources** include `systems-and-modules/network-manager/network-visibility/README.md`, `visibility-rules.md`, `using-the-visibility.md` and `whitelist-and-blacklist.md`.

## Server decision for one identity and one player

The first matching condition wins.

1. A hidden parent hides the identity.
2. The identity's whitelist makes it visible to the player.
3. The blacklist hides it from the player.
4. With neither a global rule set nor an override, the identity is visible.
5. The owner sees the identity.
6. A rule set combines its rules with **OR**. The identity is visible if any rule allows it.

An empty rule set hides the identities it applies to, subject to the earlier conditions. When player or world state changes, trigger reevaluation through the documented API. Check `EvaluateVisibility` and where to call it in the installed source.

## Multiple identities on one GameObject

Visibility applies per network component. The GameObject remains while any `NetworkIdentity` or `NetworkBehaviour` is observed. A visibility override on the second component does not apply to the first one in Inspector order. To hide the entire object, apply the rule set to the first relevant component and check descendant overrides and `Children Inherit`.

Treat classic visibility, Sync Type `ownerOnly` and `PredictedVisibility` as separate mechanisms. For a mirrored `NetworkIdentity` in PurrDiction >=1.4.0, use the predicted visibility rules.

## Cases to verify

| Case | Expected behavior |
| --- | --- |
| No rule set | Visible under the default policy |
| Empty rule set and player is not the owner | Hidden |
| One rule allows and two deny | Visible (OR) |
| Hidden Parent and whitelisted child | Hidden by parent priority |
| Identity whitelist and blacklist both match | Whitelist wins according to the official README |
| Two components have different overrides | Object remains while one component is visible |
| Player joins or changes area | Reevaluation and targeted RPC or sync |

Check parent and observer exceptions in installed package source when it differs from the docs on `main`.
