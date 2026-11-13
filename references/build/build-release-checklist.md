# Multiplayer build and release: proof checklist

**Sources** : [Code Stripping](https://purrnet.dev/docs/systems-and-modules/code-stripping), [Network Manager](https://purrnet.dev/docs/systems-and-modules/network-manager), [Transport](https://purrnet.dev/docs/systems-and-modules/transports), [Bandwidth Profiler](https://purrnet.dev/docs/systems-and-modules/bandwidth-profiler).

## Before compilation

- Fix actual versions and revisions: `Packages/manifest.json`, `packages-lock.json`, packages embedded/PackageCache, `.asmdef` and define symbols.
- List client/server scenes, prefabs, NetworkAssets, Addressables catalog, external provider versions.
- Set configuration `StartServer` / `StartClient` flags for Editor, Clone, ClientBuild and ServerBuild; avoid double boot.
- Choose Network Rules (ServerStrict and custom rules if anti-triche), auth, handshake version, cookies/reconnect, visibility.
- Set `Strip Code Mode` in Project Settings → Multiplayer → PurrNet; `[ServerOnly]` can remove sensitive client build logic by mode, but **is not proof of server security**. Physically check the build/assembly result.

## Validation de compilation

1. Editor compiles without warning blocking or IL postprocessor error.
2. Build **client** target (Windows/Linux/Mac/WebGL depending on platforms) with IL2CPP if actual target.
3. Build **Linux Dedicated Server** if applicable (Linux Dedicated Server)
4. Analysis of assembly references, stripping, `link.xml`, serializers, AOT, Addressables and mono/IL2CPP.
5. Startup logs: network listening on the planned transport/port, no unexpected self-connection.

## Tests E2E

- 2 real clients + dedicated server, auth/refusal, late connection, scene transitions, disconnected/reconnected with cookie, ownership/visibility, synctypes late join.
- Latency/packet loss/MTU, load CPU/band pass, profile, load in number of players targeted.
- Inspect the supplied build: no server token, backend secret or unnecessary client-side data.
- No "compiled/tested" without logs/artifacts Unity and method of reproduction.
