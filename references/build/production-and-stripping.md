# Production builds, code stripping, IL2CPP, dedicated servers

Official: `systems-and-modules/code-stripping.md`, `systems-and-modules/network-manager/README.md`, `guides/setting-up-a-server.md`.

- Project Settings → Multiplayer → PurrNet → **Strip Code Mode**. The `[ServerOnly]` attribute and documented `StripCodeModeOverride` options allow removing/replacing server-only methods from client builds; **verify actual emitted client assembly** rather than assuming secrecy. Strip mode differs between server/client build configurations.
- Shipping client code with server secrets, tokens, private keys or private business logic is unsafe; stripping cannot replace backend authorization, secret storage or input validation.
- Validate dedicated (no local client) and host mode separately. An Observer RPC body that changes server state may not run on a dedicated server unless local execution is intentionally configured; prefer explicit server logic for state decisions.
- IL2CPP/AOT: confirm serializers/codegen/asmdefs run in Player builds; compile target platforms, not just Editor. Ensure packages and defines are present.
- Sign-off: reproduce clean Windows/Linux client and Linux Dedicated Server builds if targeted; inspect logs, connections, active scene list, stripping result and version IDs. This skill contains no executable Unity build environment.
