# Politique de version et résolution des conflits

La doc en ligne et le code `dev` peuvent documenter une API absente de la
branche `release` ou de la version Unity installée.

## Détection de version dans le projet

Exécuter : `python scripts/inspect_project.py /chemin/vers/UnityProject`

Dans l'ordre, comparer :

- `Packages/manifest.json` > `dependencies["dev.purrnet.purrnet"]` :
  référence directe (URL git, registry, package local, etc.).
- `Packages/packages-lock.json` > `dependencies["dev.purrnet.purrnet"]` :
  version et, si disponible, hash/révision verrouillée.
- `Packages/dev.purrnet.purrnet/package.json` ou
  `Library/PackageCache/dev.purrnet.purrnet@*/package.json` ;
  en projet Unity embarqué, `Assets/PurrNet/package.json`.
- `ProjectSettings/ProjectVersion.txt` pour la version exacte d'Unity.

Si seul `#release` ou `#dev` est disponible dans le manifest, la référence
est **mobile**. Rechercher le commit résolu dans le lockfile ; sinon éviter
d'annoncer une révision précise.

## Cas concret de source périmée

Vérifié le 2026-11-12 : `PurrNet/PurrNet` branche `release`, fichier
`Assets/PurrNet/package.json`, annonce `1.25.0`. L'index Discord épinglé par
l'utilisateur annonce un historique allant jusqu'à `v1.20.0` et certaines FAQ
emploient l'ancien propriétaire `BlenMiner/PurrNet`.

Autre contradiction : la FAQ Stray peut dire « pas d'intégration Dissonance »,
mais l'organisation maintient `PurrNet/PurrNet-Dissonance`, et `PurrDocs` contient
une page `integrations/dissonance.md`. Une réponse Discord a un contexte de date.
Ne **jamais** reprendre aveuglément un diagnostic ancien.

## Ce qu'il faut rendre visible à l'utilisateur

- API confirmée dans le projet : **Vérifié (package local)**.
- Confirmée seulement dans un commit officiel : **Vérifié (commit/branche)**.
- Mentionnée seulement dans les docs : **Documenté, non compilé ici**.
- Tirée d'une FAQ ou d'un message : **Historique / à confirmer**.
- Sans source : **Hypothèse**, ne pas inventer d'API.

Conserver la provenance : fichier/repo, URL, commit ou version quand possible,
date de consultation, et restriction de branche. En cas de conflit,
faire primer le code **exact** utilisé par Unity.

## Mise à jour v0.3 — addons indépendants et changements PurrDiction

La résolution **doit être faite par package** : `dev.purrnet.purrnet` (core), `dev.purrnet.purrdiction` (prédiction), et tout autre `dev.purrnet.*` détecté. `scripts/inspect_project.py` renvoie désormais `packages[]` avec `manifest_spec`, `lock_hash` et `local_packages` pour chacun. Un projet avec core récent peut installer un addon plus ancien ; les docs de la branche `PurrDocs/main` ne doivent pas remplacer la source C# installée.

Cas versionnés identifiés dans les docs officielles :
- **PurrDiction < 1.4.0** : ancienne architecture pour intégration de `NetworkIdentity` dans les prefabs prédits et diagnostics d'input ; suivre la doc/version exacte.
- **PurrDiction >= 1.4.0** : mirroring automatique des `NetworkIdentity` dans les prefabs prédits, `PredictedIdentitySpawner` obsolète ; certaines pages de lag compensation marquées >=1.4.0 ; `PredictedIfOwnedWithSoftFallback` apparaît dans la doc récente. Ne pas inférer la présence de n'importe quelle API sans `find_api.py` et package installé.
- Les docs officielles sont un dépôt mobile (capturer SHA Git) ; les anciens messages Stray Help ne sont **pas normatifs** et peuvent contredire la doc actuelle.

## Mise à jour v0.4.0 — gate check explicite

Lancer `scripts/check_doc_versions.py <page relative> --project <UnityProject> --strict` pour obtenir, par section `{% version range="..." %}` et frontmatter `version`, le statut applicable / exclu / inconnu selon la **version PurrDiction ou core installée**. Ce script ne filtre pas automatiquement la doc et ne remplace pas le contrôle des méthodes et attributs dans le code C# réellement compilé.

Lors d'un refresh Git des docs, `scripts/sync_sources.py` préserve `references/cache/docs-index.previous.json`. `scripts/docs_drift.py` liste les changements et les guides à vérifier via les routes. Une page non mappée n'est jamais considérée comme automatiquement couverte ; elle nécessite classification. Les anciens guides restent à revoir jusqu'à examen humain/agent des changements.

## v0.7 — version des bugs historiques ≠ version de compatibilité d'API

`python scripts/historical_issues.py "double RPC" --project <UnityProject>` compare la version résolue au jalon de **fix historique rapporté**. Les statuts `older_than_claimed_fix` et `at_or_after_claimed_fix` ne prouvent **ni** la cause actuelle ni sa disparition. `PREDICTION_*` lit la version PurrDiction, les autres lisent la version PurrNet core. Les incohérences entre `packages-lock.json` et package installé renvoient `CONFLICTING` et désactivent la comparaison.

Ne jamais utiliser le jalon historique `1.20.0` comme la « version actuelle » automatiquement. Toujours lire le package Unity résolu ; le core `release` observé le 13 novembre 2026 annonçait `1.25.0`, mais ceci est seulement une observation datée.
