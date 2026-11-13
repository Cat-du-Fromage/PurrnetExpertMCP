# Coopération avec la skill edgegap-purrnet

Source : https://github.com/edgegap/llm-agent-skills/tree/main/skills/edgegap-purrnet

`purrnet-expert` intervient sur gameplay C#, RPC, modules de synchronisation, autorité, bugs host/dedicated, serialization, addon PurrDiction, version et débogage.

`edgegap-purrnet` (si installée) prend le relais pour : dedicated Linux, bootstrap autonome, plugin/build Docker, déploiements sur Edgegap, matchmaking, panel de connexion, ports cloud, lifecycle et destruction des serveurs. Ne pas la forcer pour un serveur auto-hébergé ou un projet host/relay.

## Flux de collaboration

1. `purrnet-expert` inspecte la version Unity/PurrNet et la logique du jeu ; note les changements host-only nécessaires.
2. `edgegap-purrnet` configure son bootstrap, ses templates de serveur/client et ses étapes local → Docker → cloud → matchmaking.
3. `purrnet-expert` relit les changements de logique jeu et les risques d'autorité, et vérifie que l'état monde existe sans client local.
4. Les deux passent la matrice de tests ; ne pas présenter le sample Edgegap comme une preuve du projet utilisateur.

Ne jamais intégrer de secret Edgegap dans le client ni dans les fichiers du projet. Pour toute action sur un compte réel ou un service facturé, respecter la confirmation attendue par l'outil concerné.

## v0.8 — Contrat opérationnel de transfert

Pour une demande Edgegap, charger `references/workflows/edgegap-handoff.md` puis, si la skill Edgegap est disponible, la laisser prendre le rôle principal dans le déploiement. Transmettre `Unity version`, `PurrNet version/commit`, `NetworkManager/scene`, `start flags`, `transport/port`, `callbacks host-only`, `build evidence` et `risks`. Retour attendu : logs d'un serveur **sans client local**, deux vrais clients, déploiement direct avant matchmaker, auto-stop et arrêt des ressources facturées. Ne jamais transformer une validation rapportée sur le sample Edgegap en preuve sur le projet utilisateur.

Comparaison détaillée et emplacement des évaluations Edgegap : `references/edgegap-comparison.md`.
