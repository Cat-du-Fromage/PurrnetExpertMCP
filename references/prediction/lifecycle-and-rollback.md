# Timeline, hooks, replay, présentations

**Sources** `client-side-prediction/flow.md`, `state-handling.md`, `views-and-interpolation.md`, `predicted-identities.md`, `best-practices.md`.

## Chronologie
Setup / `LateAwake` (initialisation view, pas mutations déterministes untracked) → préparation INPUT → snapshot pré-tick → `Simulate` → physique prédite → `LateSimulate` → snapshot/frames réseau → éventuellement rollback/verified tick/replay → interpolation `UpdateView` puis `LateUpdateView`.

- `Simulate` et `LateSimulate` peuvent être appelés PLUSIEURS fois pour le même tick lors de la réconciliation. Les invocations doivent être rejouables; ne pas y exécuter `AudioSource.Play`, particules, `PlayerPrefs`, analytics, requête HTTP, fichiers, ordinary RPC.
- Pour effets ponctuels : utiliser `PredictedEvent`, `predictionManager.isVerifiedView` ou les callbacks view adaptés; la simulation de state ne doit pas être ignorée pendant `isCatchingUpFrames`.
- Les objets Unity mutés pendant simulation doivent être capturés via `GetUnityState` et restaurés via `SetUnityState`; sinon rollback ne restaure qu'un morceau de la vérité. Les built-ins physics/transform ont leur propre bridge.
- La présentation `UpdateView(STATE viewState, STATE? verified)` peut être lissée; caméras/IK inter-identités dans `LateUpdateView` si disponible dans version. `ResetInterpolation()` pour téléport.
- `StatelessPredictedIdentity` a des signatures de view différentes selon PurrDiction <1.4 et >=1.4; vérifier le code source de la version.
- Profiling : taux de correction, longueur history, position avant/après replay, fuites mémoire et snap thresholds.

## Anti-pattern
`if (!isCatchingUpFrames) state.ammo--;` = divergence. À la place, muter ammo toujours, filtrer uniquement l'effet visuel de tir.

## Tests
Identité client sans authority, 150ms + jitter, resimulation multi-ticks, perte de frame, teleport et reparenting; comparer états vérifiés et rendus.
