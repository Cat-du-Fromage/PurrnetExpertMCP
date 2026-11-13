# NetworkBones and NetworkOwnershipToggle — case of use and control

**Official sources**:
- [Network Bones](https://purrnet.dev/docs/plug-n-play-components/network-bones)
- [Network Ownership Toggle](https://purrnet.dev/docs/plug-n-play-components/network-ownership-toggle)
- [Network Animator](https://purrnet.dev/docs/plug-n-play-components/network-animator)

These components are **not** interchangeable with `NetworkTransform` / `NetworkAnimator` or with `PredictedTransform` simulation PurrDiction. Read the pages and inspect their properties in the installed version before producing code.

## NetworkBones

Synchronizing a bone structure or parts of a character can be useful for ragdoll, members pose and other articulated visual objects. Check hierarchy, bone references, frequency, authority, local/world space conversions, and interaction with Animator/physics. For an unpredicted player character, compare the cost of transmitting only animation parameters and reconstructing the pose locally; do not synchronize dozens of bones by default.

**Tests**: master character + 2 observers, change of pose, change of owner, output/input of visibility, interpolation and bandwidth. If an animated component controls the same pose in the observer, define who is the only writer.

## NetworkOwnershipToggle

Helps to activate/disable items according to ownership. Always separate ** local display** (camera, input) from **authoritative validation** (inventory, attack, damage). A GameObject or component disabled for a non-owner does not constitute a network security guarantee.

**Tests**: spawn without owner, local owner, remote owner, transfer, host (server/client), dedicated; ensure that the server continues the necessary processing when no local player exists.

## Deliverable expected

Precise component name in the package, Inspector settings, what to sync, which has the state, bandwidth estimate, two clients and late join. Do not invent fields/events not read in the source code.
