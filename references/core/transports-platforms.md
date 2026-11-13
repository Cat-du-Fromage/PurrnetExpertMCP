# Transports: how to choose across platforms

Official: `systems-and-modules/transports/{README.md,udp-transport.md,web-transport.md,composite-transport.md,steam-transport.md,eos-transport.md,local-transport.md,purr-transport.md,simulating-latency.md}`.

| Requirement | First option to investigate | Important constraints |
|---|---|---|
| Local LAN/desktop | UDPTransport | Match IP, port, binding, firewall, NAT and protocol; dedicated server not same as host |
| Browser/WebGL | WebTransport (WebSocket) | Browsers do not offer raw UDP; check WS/WSS, TLS and CORS/deployment |
| Steam ecosystem | SteamTransport | Requires Steamworks.NET; a Steam lobby is metadata/discovery, not transport itself |
| Epic Online Services | EOSTransport | Official addon with PlayEveryWare plugin, EOS configuration and socketName agreement; check versionDefines |
| Cross platform multiple transports | CompositeTransport | Chooses first supported transport from list, server starts supported layers; port mapping for each |
| In-process tests | LocalTransport | Does not prove WAN NAT, jitter or production relay behavior |
| Relay/developer testing | PurrTransport | Check self-host/managed service policies and budget; don't silently assume hosted production SLA |

Before building: inspect installed transport components and their inspector fields; client/server transport match, protocol, port, SSL, startup flags, platform defines. For EOS require remote Product User ID and consistent socketName in current docs; no raw credentials in client code. For WebGL ensure WebTransport rather than UDP. For Edgegap deployment specifics route to `edgegap-purrnet`.

Test multi-build connection matrix (Win/Linux/macOS/WebGL/mobile as targeted), firewalls, strict NAT, reconnect, transport fallback order, loss/jitter and server restart. Record actual external vs internal port for hosting providers.
