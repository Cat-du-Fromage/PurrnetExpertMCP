# Build et release multijoueur : checklist de preuve

**Sources** : [Code Stripping](https://purrnet.dev/docs/systems-and-modules/code-stripping), [Network Manager](https://purrnet.dev/docs/systems-and-modules/network-manager), [Transport](https://purrnet.dev/docs/systems-and-modules/transports), [Bandwidth Profiler](https://purrnet.dev/docs/systems-and-modules/bandwidth-profiler).

## Avant compilation

- Fixer versions et révisions effectives : `Packages/manifest.json`, `packages-lock.json`, packages embedded/PackageCache, `.asmdef` et define symbols.
- Lister scènes client/serveur, prefabs, NetworkAssets, Addressables catalog, versions de providers externes.
- Définir la configuration `StartServer` / `StartClient` flags pour Editor, Clone, ClientBuild et ServerBuild; éviter un double démarrage.
- Choisir Network Rules (ServerStrict et règles custom si anti-triche), auth, version handshake, cookies/reconnect, visibilité.
- Définir `Strip Code Mode` dans Project Settings → Multiplayer → PurrNet; `[ServerOnly]` peut retirer la logique sensible des builds clients selon le mode, mais **n'est pas une preuve de sécurité serveur**. Vérifier physiquement le résultat build/assembly.

## Validation de compilation

1. Editor compile sans warning bloquant ni IL postprocessor error.
2. Build **client** target (Windows/Linux/Mac/WebGL selon plateformes) avec IL2CPP si cible réelle.
3. Build **Linux Dedicated Server** si applicable (Linux Dedicated Server support installé).
4. Analyse des assembly références, stripping, `link.xml`, serializers, AOT, Addressables et mono/IL2CPP.
5. Startup logs : réseau en écoute sur le transport/port prévus, aucune auto-connexion inattendue.

## Tests E2E

- 2 vrais clients + serveur dédié, auth/refus, connexion tardive, scene transitions, disconnected/reconnected avec cookie, ownership/visibility, synctypes late join.
- Latence/packet loss/MTU, charge CPU/bande passante, profiler, charge en nombre de joueurs visé.
- Inspecter le build livré : pas de token serveur, secret backend ni données non nécessaires côté client.
- Aucun « compilé/testé » sans logs/artifacts Unity et méthode de reproduction.
