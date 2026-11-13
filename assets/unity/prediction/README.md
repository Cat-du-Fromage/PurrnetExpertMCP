# PurrDiction recipes without fake template compiled

Do not deliver a single "universal" predicted controller copied from `PurrDocs/main`: its signatures and dependencies depend on the installed version. Read in this order:
1. `references/prediction/best-practices.md` and `references/prediction/input-and-state.md`.
2. `references/cache/official-docs/client-side-prediction/predicted-identities.md` and `input-handling.md`.
3. The `PredictedIdentity<INPUT,STATE>` and `IPredictedData<T>` actually installed (source / compile).
4. `references/prediction/hierarchy-and-parenting.md`, `physics-and-collisions.md`, then policy/lag compensation according to gameplay.
5. Test host + two clients, rollback, late join, pool and jitter.

This v0.4 **does not claim any compiled PurrDiction template**: providing an unverified source file allegedly compatible would be less secure than the documented recipe.
