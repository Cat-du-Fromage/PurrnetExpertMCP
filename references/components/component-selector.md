# Choose existing PurrNet components before hand-writing network replication

Official docs in `plug-n-play-components/` (11 Markdown pages plus child adaptive-sync page).

| Need | Classic PurrNet | PurrDiction alternative |
| --- | --- | --- |
| Pose | NetworkTransform (+ Adaptive Sync) | PredictedTransform |
| Rigidbody / Rigidbody2D | NetworkRigidbody / NetworkRigidbody2D | PredictedRigidbody 3D/2D |
| Animator parameters + triggers | NetworkAnimator (triggers through wrapper) | UpdateView from predicted view state |
| Skeletal/bone pose | NetworkBones | verify suitability of predicted view renderer |
| Audio playback | NetworkAudioSource | view-only/PredictedEvent for replay safety |
| Generic component property mirror | NetworkReflection | predicted STATE if gameplay-critical |
| Runtime state machine | NetworkStateMachine | PredictedStateMachine/PredictedStateNode |
| Enable local-only scripts by owner | NetworkOwnershipToggle | predicted owner/controller view gating |

**Ask before custom netcode:** Can a built-in component do this? Will its authority model, bandwidth and late-join semantics fit? Are we writing on the same field/Transform twice? Does the installed branch match the docs? Test with two remote clients, not only host.
