# DeterministicIdentity, math et désynchronisation

**Sources** `client-side-prediction/deterministic-identity.md`, `flow.md`, `best-practices.md`.

- `DeterministicIdentity<STATE>` / `<INPUT,STATE>` pour simulation strictement bit-stable; callback `Simulate` avec **`sfloat delta`**, math déterministe `sfloat` / `FP`, pas du float Unity non déterministe pour les calculs décisifs.
- `STATE` doit être complet et les opérations math (`IMath<T>`) compatibles avec interpolation. Pas de mutations d'état depuis Awake/LateAwake, mais pendant timeline simulée (`SimulationStart`, `Simulate`, events qui proviennent de simulation).
- Un modèle déterministe n'envoie pas de snapshot complet chaque tick dans le même sens qu'une identité prédite non déterministe; des checks de hash permettent de détecter les désaccords.
- **Desync Policy** : `Ignore` (pas de checks), `Report` (événements de diagnostic), `Resync` (rebase complet client), `Correct` (corrige l'identité). Vérifier API et compatibilité version; définir le compromis CPU/bande passante et fréquence (`Desync Check Interval`).
- Une policy `SoftCorrection` n'est pas supportée par deterministic identities; l'effet client retombe à ServerRelay. Ne pas interpréter ce fallback comme validant le comportement voulu.
- Désynchronisation ne se corrige pas en ajoutant de `Time.deltaTime`, du RPC replayé ou de physics Unity arbitraire; identifier le premier tick divergent.

## Tests
Windows/Linux builds, ordre de construction statique, payload perdu / full frame rebase, 0/1/5% pertes, rejoin, divergence artificielle et réaction effective Report/Correct/Resync.
