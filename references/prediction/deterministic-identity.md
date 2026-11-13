# DeterministicIdentity, Math and Desynchronization

**Sources** `client-side-prediction/deterministic-identity.md`, `flow.md`, `best-practices.md`.

- `DeterministicIdentity<STATE>` / `<INPUT,STATE>` for strictly bit-stable simulation; callback `Simulate` with **`sfloat delta`**, deterministic math `sfloat` / `FP`, not non-deterministic Unity float for decisive calculations.
- `STATE` must be complete and math operations (`IMath<T>`) compatible with interpolation. No state mutations from Awake/LateAwake, but during simulated timeline (`SimulationStart`, `Simulate`, events from simulation).
- A deterministic model does not send a complete snapshot of each tick in the same direction as a predicted non-deterministic identity; hash checks allow for the detection of disagreements.
- **Desync Policy**: `Ignore` (no checks), `Report` (diagnostic events), `Resync` (full client database), `Correct` (identification corrects). Check API and version compatibility; set the CPU/bandwidth compromise and frequency (`Desync Check Interval`).
- A `SoftCorrection` policy is not supported by deterministic identities; the client effect falls to ServerRelay. Do not interpret this fallback as validating the desired behavior.
- Desynchronization is not corrected by adding `Time.deltaTime`, replayed RPC or arbitrary Unity physics; identify the first divergent tick.

## Tests
Windows/Linux buildings, static construction order, lost payload / full frame rebase, 0/1/5% losses, join, artificial divergence and effective reaction Report/Correct/Resync.
