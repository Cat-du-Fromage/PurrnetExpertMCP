# Carte des sources PurrNet

> Vérification initiale : 12 novembre 2026. Les branches et pages évoluent.

## 1. Documentation officielle

- Index humain : https://purrnet.dev/docs
- Index source GitHub, navigable et versionnable : https://github.com/PurrNet/PurrDocs/blob/main/SUMMARY.md
- Sources Markdown : https://github.com/PurrNet/PurrDocs
- Installation : https://purrnet.dev/docs/getting-started/installation-setup
- Minimal Setup : https://purrnet.dev/docs/getting-started/getting-started
- Network Manager : https://purrnet.dev/docs/systems-and-modules/network-manager
- Network Rules : https://github.com/PurrNet/PurrDocs/blob/main/systems-and-modules/network-manager/network-rules.md
- NetworkIdentity : https://purrnet.dev/docs/systems-and-modules/network-identity
- NetworkBehaviour : https://purrnet.dev/docs/systems-and-modules/network-identity/networkbehaviour
- RPC : https://purrnet.dev/docs/systems-and-modules/remote-procedure-call-rpc
- SyncVar : https://github.com/PurrNet/PurrDocs/blob/main/systems-and-modules/network-modules/sync-types/syncvar.md
- Spawning/Despawning : https://purrnet.dev/docs/systems-and-modules/network-identity/spawning-and-despawning
- Prediction : https://purrnet.dev/docs/client-side-prediction

Le fichier `SUMMARY.md` est un **annuaire** de sujets, pas une preuve que
chaque page correspond à la version installée. Le site dispose d'un sélecteur
« Package versions » : vérifier les versions dans les questions sensibles.

## 2. Repositories officiels

Organisation : https://github.com/orgs/PurrNet/repositories

- Core : https://github.com/PurrNet/PurrNet (branche `release` stable,
  `dev` plus récente, mais plus changeante)
- Docs source : https://github.com/PurrNet/PurrDocs
- Prediction : https://github.com/PurrNet/PurrDiction
- Lobby : https://github.com/PurrNet/PurrLobby
- Dissonance : https://github.com/PurrNet/PurrNet-Dissonance
- Sample : https://github.com/PurrNet/PurrNet-Incremental-Sample
- Example/template : https://github.com/PurrNet/game-jam-template

Code du core dans `Assets/PurrNet/Runtime/` ; package UPM dans
`Assets/PurrNet/package.json`. Les exemples se trouvent aussi dans
`Assets/PurrNet/Examples/`. Vérifier l'existence des fichiers et les symboles
avant de citer une implémentation.

Exemple d'installation stable documentée :
`https://github.com/PurrNet/PurrNet.git?path=/Assets/PurrNet#release`

## 3. Base historique Discord/Stray Help

- Index `llms.txt` **épinglé au commit fourni** :
  https://github.com/nmban/Purrnet-Stray_Help/blob/e6140a571228044fe670b500e245f6bb370b2e06/llms.txt
- FAQ :
  https://github.com/nmban/Purrnet-Stray_Help/blob/e6140a571228044fe670b500e245f6bb370b2e06/docs/FAQ.md
- Quick Reference :
  https://github.com/nmban/Purrnet-Stray_Help/blob/e6140a571228044fe670b500e245f6bb370b2e06/docs/QUICK_REFERENCE.md
- Historique et développeurs : consulter les chemins répertoriés dans `llms.txt`.

L'index annonce plus de 15 000 Q/R et un historique jusqu'à v1.20.0. Il
s'agit de **témoignages datés**, non d'une documentation officielle actuelle.
Éviter d'importer l'intégralité des logs en contexte à chaque requête.

## 4. Procédure de recherche ciblée

1. Lire le nom de classe/attribut dans la demande.
2. Ouvrir `SUMMARY.md` pour découvrir la page pertinente.
3. Chercher le symbole dans le code exact installé (ou dépôt core au commit).
4. Confirmer avec la documentation correspondante.
5. Sur bug connu seulement, chercher la FAQ puis les réponses historiques.
6. Pour une fonction d'addon, vérifier sa **dépendance et version séparées**.

## Nouveaux points d'entrée en v0.3

- `references/documentation-map.md` pour découvrir **toutes** les catégories documentées, pas une whitelist de neuf fichiers.
- `references/documentation-policy.md` et `scripts/sync_sources.py` pour cloner PurrDocs et conserver SHA source (sans redistribution du dépôt doc dans le ZIP).
- `scripts/docs_catalog.py coverage` : vérifie chemins critiques et liens SUMMARY, `search` : recherche dans tout le clone, y compris pages non listées dans SUMMARY.
- `references/purrdiction-best-practices.md` et `references/purrdiction-architecture.md` : règles de prédiction obligatoires.
- `references/networking-best-practices.md` : cycle de vie des modules, authority, RPC et limites en PurrNet classique.
- `scripts/inspect_project.py` couvre `dev.purrnet.purrdiction` indépendamment du core.

## Mise à jour v0.7 — incidents Stray Help épinglés

- Cas vérifiés à la source historique `e6140a571228044fe670b500e245f6bb370b2e06` : `references/historical/incident-catalog.json` (35 scénarios **de triage**, pas 35 bugs actuels).
- Sources synthétiques : [`docs/QUICK_REFERENCE.md`](https://github.com/nmban/Purrnet-Stray_Help/blob/e6140a571228044fe670b500e245f6bb370b2e06/docs/QUICK_REFERENCE.md), [`docs/FAQ.md`](https://github.com/nmban/Purrnet-Stray_Help/blob/e6140a571228044fe670b500e245f6bb370b2e06/docs/FAQ.md), [`docs/changelogs/versions.md`](https://github.com/nmban/Purrnet-Stray_Help/blob/e6140a571228044fe670b500e245f6bb370b2e06/docs/changelogs/versions.md).
- Les fichiers `docs/dev-answers/*.md` et les raw Discord (total annoncé : ~15k messages Q&A) ne sont **pas tous analysés**. Recherche locale optionnelle après `scripts/sync_stray_archive.py`, via `scripts/search_stray_archive.py`. Ne pas supposer une autorisation de redistribution.
- Contradictions connues avec PurrDocs actuelle : version « latest », ancien repo `BlenMiner`, intégration Dissonance, sérialisation de références, membership vs loaded-scene events et vieux noms de callbacks. La source exacte du projet a priorité.
