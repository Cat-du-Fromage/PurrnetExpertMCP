# Lag compensation et hit validation

**Sources** `client-side-prediction/lag-compensation.md` (frontmatter >=1.4.0), `systems-and-modules/collider-rollback.md`, `client-side-prediction/security.md`.

- Deux chemins différents : PurrNet classique peut utiliser `rollbackTick` du NetworkIdentity et un RPC + `RollbackModule`, tandis que PurrDiction >=1.4 fournit `lagCompensationTick` **dans `Simulate`** et `predictionManager.lagCompensation` (Raycast/CircleCast/etc.). Ne pas confondre les tick spaces.
- Les cibles intéressantes doivent disposer de `ColliderRollback`; le système enregistre leur historique. Le serveur utilise son propre history et borne l'offset demandé via `Max Lag Compensation Seconds` (défaut documenté 0.15s dans certaines versions).
- L'input d'attaque contient l'intention (`fire`), pas un « j'ai touché cet ennemi pour 80 dégâts » ; résultat issu du raycast prédictible + validation serveur dans STATE. L'input n'envoie pas de `rollbackTick` pour le chemin PurrDiction moderne.
- `Forward View Offsets` facilite les résultats correspondants sur clients remotes au coût de bande passante supplémentaire; choisir selon gameplay.
- Éviter que le raycast fasse un effet audio/analytics à chaque replay; utiliser events/views filtrés.

## Tests
Tir à haute latence sur cible en mouvement, faux offset, cible cachée, cible despawn avant impact, client modifié, hitscan 2D et 3D, late join.
