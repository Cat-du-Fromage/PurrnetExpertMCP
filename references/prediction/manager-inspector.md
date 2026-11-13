# PredictionManager setup and project checklist

Official: `client-side-prediction/{installation.md,overview.md,flow.md,predicted-identities.md,built-in-components/README.md,views-and-interpolation.md,security.md}`.

- Confirm **both packages** PurrNet and PurrDiction, their exact versions and compatibility, asmdef references, included scenes and platform.
- Inspect `PredictionManager` in each gameplay scene: physics providers (2D/3D), built-in systems (PredictedHierarchy, predicted players, physics where needed), tick rate, view-update phase, policies/scopes and predicted prefab registry. Do not assume auto registration and scene setup when code is generated.
- Choose `PredictedIdentity<STATE>`, `PredictedIdentity<INPUT,STATE>` or `StatelessPredictedIdentity` based on whether external input/state is needed. Inspect callback signatures in the installed PurrDiction package.
- For predicted physics: ensure Unity Physics 2D/3D script-mode integration and relevant predicted components; avoid direct FixedUpdate-based gameplay authoritative mutation that cannot be rewound.
- Decide object policy per role (owner, remote, server AI), stable IDs, input/cooldown state, state initialization and Unity state bridge; verify `PredictedHierarchy` prefab registration and any mirrored NetworkIdentity behavior by version (notably 1.4.0 boundary).
- Separate view/Animator/audio/camera from simulation. Test 30/60/144 FPS, 30/60 tick, 0/100/250 ms RTT, jitter/loss, late join, reconnect, ownership changes and pool reuse.

**Output checklist**: exact Inspector components and settings, required packages, input/state contract, authority, resimulation effects, debug traces and measured corrections. If no Unity Editor was available, mark Inspector verification NOT RUN.
