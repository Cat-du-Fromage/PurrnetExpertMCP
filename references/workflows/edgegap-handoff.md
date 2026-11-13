# Workflow E — Collaboration avec edgegap-purrnet, pas duplication

L'étude de `edgegap/llm-agent-skills` montre que son projet testé sur Edgegap valide une chaîne concrète `local dedicated -> Docker -> deploy direct -> matchmaker -> 2 clients -> arrêt`, avec assets Unity, logs et assertions. Notre skill est **généraliste** : conserver son rôle d'analyse du gameplay et laisser `edgegap-purrnet` gérer le produit Edgegap. Lire `references/edgegap-comparison.md`.

## Interface de transfert

**purrnet-expert transmet à edgegap-purrnet** : Unity exact, version PurrNet/package lock, nom de scène/NetworkManager, flags auto start existants, transport et port présents, `isHost`/`ObserversRpc` suspects, scénario de validation du monde autoritaire, limites de permissions. Produire un petit `HANDOFF.md` ou résumé avec chemins et lignes de code, sans secrets.

**edgegap-purrnet produit** : configuration de plugin/SDK, startup dédié, port interne vs externe, build Linux, Dockerfile/.dockerignore, registry et allocation, client connector, matchmaker, auto-stop, résultat des logs et tests. **Ne pas supposer** que l'accès Edgegap, Docker ou Unity existe ; séparer modifications locales et étapes manuelles. Ne pas envoyer tokens Edgegap au client, projet, logs ou fichiers versionnés.

**purrnet-expert vérifie ensuite** que les modifications serveur ne cassent pas l'ownership, le host local, le gameplay autoritaire, le late join et les RPCs ; reprendre les critères D2-D5. Ne pas réintroduire de logique `isHost` juste pour satisfaire un prefab Editor.

## Routage de choix (exemples)

- « Mon `SyncVar` ne se synchronise pas » → purrnet-expert uniquement.
- « Le monde est vide sur dedicated sans aucune mention Edgegap » → purrnet-expert, avec audit dedicated générique.
- « Je veux Find Match sur Edgegap avec PurrNet » → edgegap-purrnet propriétaire du déploiement ; purrnet-expert consultée pour changements de gameplay si besoin.
- « J'ai besoin d'un serveur Linux auto-hébergé PurrNet » → purrnet-expert (et workflows généralistes), pas Edgegap imposé.
- « Mirror ou FishNet sur Edgegap » → skills correspondantes, **pas** purrnet-expert.

## Définition de fini

Le projet Edgegap doit **vraiment être testé** par un serveur headless, deux clients, cloud/assignation externe, matchmaker et arrêt. Un échec de cloud access ne doit pas être déguisé : livrer modifications prêtes à tester et `HANDOFF.md` avec étapes restantes, pas un « déploiement réussi ».
