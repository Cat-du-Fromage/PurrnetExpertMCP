# Matrice de tests PurrDiction (hors tests Unity tant que non exécutés)

| ID | Scénario reproductible | Critère observable / défaut recherché |
| --- | --- | --- |
| PD-01 | Deux clients distants + serveur (pas uniquement host) | INPUT owner→serveur, STATE vérifié cohérent, actions invalides refusées |
| PD-02 | `UpdateInput` front jump/fire entre deux ticks | Action captée une fois, pas perdue ni dupliquée |
| PD-03 | Perte de paquets sur action one-shot | `ModifyExtrapolatedInput` supprime répétition du front |
| PD-04 | Input modifié: NaN / vitesse > autorisée / achat spam | `SanitizeInput` + règles métier serveur bloquent |
| PD-05 | Rollback/replay répété des mêmes ticks | Pas de double audio, analytics, RPC, récompense, sauvegarde |
| PD-06 | Mutation Transform/rigidbody pendant simulation puis correction | `GetUnityState`/`SetUnityState` ou composant intégré restaurent réellement état |
| PD-07 | Téléport et grande correction | `ResetInterpolation` si pertinent ; pas de dérive permanente |
| PD-08 | Pool réutilise objet durant rollback | ID stable résolu vers bon objet ; pas de référence morte |
| PD-09 | `PredictedHierarchy.Create/Delete` et reparenting durant replay | Topologie identique serveur/client, late join reconstruit |
| PD-10 | `PredictedModule` statiques tous peers | Ordre identique ; aucun `PredictedModuleRosterMismatchException` |
| PD-11 | `PredictedModule` dynamique créé/détruit dans `Simulate` | État recréable après correction ; pas de pointeur cached périmé |
| PD-12 | DATA avec `DisposableList`/buffers | deep copy indépendante, bon `Dispose`, pas de double free/leak sous stress |
| PD-13 | Ownership switch et reconnexion | Policy résolue et input contrôleur transféré, pas de double sim |
| PD-14 | FullPrediction vs PredictedIfOwned vs ServerRelay | Timelines et coût/corrections correspondent au besoin gameplay |
| PD-15 | SoftCorrection et fallback sur composant non supporté | Comportement relay identifié, pas de hit validation non exacte |
| PD-16 | 30/60/120 Hz de rendu et tick rates variables | Gameplay stable ; aucune dépendance `Time.deltaTime` en sim |
| PD-17 | Ping 0/100/250ms + jitter/perte | Input extrapolation réglée, overshoot/correction mesurés |
| PD-18 | Client arrive en retard, puis perd une connexion | Préfab prédit et données durables reconstructibles |
| PD-19 | PurrDiction >=1.4 avec `NetworkIdentity` mirror | UI RPC OK, gameplay prédit isolé, visibilité/ownership mirrored corrects |
| PD-20 | PurrDiction <1.4 en fixture séparée | Ne copie pas automatiquement mirroring nouveau ni lag-compensation récent |
| PD-21 | Lag compensation hitscan (version compatible) | Serveur vérifie ray sur historique, offset borné, pas de confiance sur hit client |
| PD-22 | Mesure bandwidth/prediction profiler | Coût par tick/snapshots, corrections et transmissions observés |
| PD-23 | 2 machines architectures différentes, strict determinism | `DeterministicIdentity` et sfloat/fixed; pas de float brut affectant tick |

## Gates de livraison

- Statique : `scripts/guard_predicted_code.py <projet>` ne signale pas d'interdit évident (outil heuristique) **ET** revue manuelle BP-01..BP-10.
- Compilation Unity réelle : package exact + addons, asmdef, codegen et builds cibles.
- Test d'exécution : PD-01, PD-02, PD-03, PD-04, PD-05, PD-07, PD-08, PD-13, PD-17, PD-18 selon feature. Ajouter toutes lignes relatives aux composants employés. Déclarer précisément toute ligne N/A.
- « Production ready » : impossible à confirmer par une skill seule ; profiler, tests automatisés, charge, sécurité et validation sur plateformes cibles requis.
