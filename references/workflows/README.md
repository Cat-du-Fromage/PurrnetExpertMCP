# Workflows, dans l'ordre minimal

Un agent ne doit pas lire le pack entier à chaque demande. Choisir **un parcours**, puis ouvrir seulement les références que son besoin déclenche. Les pages officielles restent prioritaires pour les signatures et les branches.

| Intention du joueur/développeur | Parcours | Critère qui prouve une fin utile |
|---|---|---|
| « Ajoute une fonctionnalité réseau » | [feature.md](feature.md) | Deux peers observent le même résultat, avec permissions et late join |
| « Mon RPC ne marche pas / jitter / bug » | [bug.md](bug.md) | Cause localisée, reproduction avant / après et contre-test |
| « Fonctionne en host, pas en serveur dédié » | [dedicated.md](dedicated.md) | Le serveur sans client local possède le monde et deux clients jouent |
| « Je veux rollback / prédiction » | [prediction.md](prediction.md) | Simulation réconciliée, effets non rejoués et test réseau dégradé |
| « Déployer sur Edgegap / matchmaking » | [edgegap-handoff.md](edgegap-handoff.md) | Délégation à `edgegap-purrnet`, vérification des interfaces entre skills |

Pour chaque parcours : inspecter d'abord, préserver l'existant, vérifier les API sur le package local, documenter les étapes Unity, **ne pas déclarer d'étape validée sans artefact de preuve**. Voir [acceptance.md](../validation/acceptance.md).

Points de preuve : D0 hypothèse, D1 doc, D2 signatures, D3 build, D4 deux clients, D5 dédié, D6 stress/sécurité. Un contrôle regex est un signal, jamais un résultat D3+.
