# Recettes PurrDiction sans faux template compilé

Ne pas livrer un unique contrôleur prédit "universel" copié depuis `PurrDocs/main` : ses signatures et dépendances dépendent de la version installée. Lire dans cet ordre :
1. `references/prediction/best-practices.md` et `references/prediction/input-and-state.md`.
2. `references/cache/official-docs/client-side-prediction/predicted-identities.md` et `input-handling.md`.
3. Le `PredictedIdentity<INPUT,STATE>` et `IPredictedData<T>` réellement installés (source / compile).
4. `references/prediction/hierarchy-and-parenting.md`, `physics-and-collisions.md`, puis policy/lag compensation selon gameplay.
5. Test host + deux clients, rollback, late join, pool et jitter.

Cette v0.4 **ne revendique aucun template PurrDiction compilé** : fournir un fichier source non vérifié prétendument compatible serait moins sûr que la recette documentée.
