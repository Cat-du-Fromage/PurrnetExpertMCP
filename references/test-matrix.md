# Matrice minimale de tests multijoueurs

| Test | À vérifier |
| --- | --- |
| Host seul | `OnSpawned` peut être invoqué pour les deux rôles : pas de double logique métier |
| Deux clients + serveur dédié | Client owner/non owner, RPC envoyés à la bonne cible |
| Client 2 rejoint tard | Spawning, état durable, visibilité et valeurs initiales corrects |
| Déconnexion / reconnexion | Clean-up, identités et éventuelles cookies de reconnexion |
| Client non autorisé | Impossible d'invoquer une action critique ou d'écrire un état non permis |
| Despawn / changement de scène | Aucun objet fantôme ni événement dupliqué |
| Build standalone | Même comportement hors Unity Editor, pas uniquement en host |
| Latence/perte simulées | Pas d'hypothèse implicite d'ordre ou de fiabilité pour des canaux non fiables |

Toujours mentionner ce qui a été réellement testé et ce qui reste seulement
proposé. Une compilation C# n'est pas une validation réseau.

## Tests PurrDiction supplémentaires v0.3

Pour tout `PredictedIdentity` / `PredictedModule` / rollback / prédiction, la matrice ci-dessus ne suffit pas : lire **`references/purrdiction-test-matrix.md`** (PD-01..PD-23). Rejouer les ticks, changer ownership, simuler pertes et RTT, pools et spawn/despawn, vérifier prédiction/reconciliation et mémoire, et contrôler les usages du site Web pour les versions installées.
