# Transport, accommodation and network diagnosis

**Official sources**: `systems-and-modules/transports/README.md`, `udp-transport.md`, `web-transport.md`, `steam-transport.md`, `purr-transport.md`, `composite-transport.md`, `local-transport.md`, `eos-transport.md`, `simulating-latency.md`; `guides/test-with-friends/`.

- Distinguish selected transport (UDP, WS/WSS, Steam, relay, composite, local), platform and browser constraints. **WebGL cannot open UDP socket**; choose a compatible web transport and a valid TLS configuration.
- Do not assume that the transports have the same properties `address`/`serverPort`, the same cross NAT or the same security. PurrTransport relay and relay third parties have their limitations and costs; check the current doc.
- Inspect server listening address (often `0.0.0.0`), internal port, protocol, endpoint/port **external** returned by host; Firewall/NAT/IPv6 attention.
- A dedicated server is distinct from a host player: avoid initializations only on client, camera/audio/IU calls, and observe RPC whose body must also be executed on the server.
- Before recommending an infrastructure, clarify (if unknown) platform, topology, number of players, authority model and matchmaking; for Edgegap delegate to `edgegap-purrnet` if installed.

## Diagnostic minimal
Server started? port listen? authenticator accepted? `PlayerID` created? scene loaded? observe? state? Test loopback, LAN, different networks, simulated losses and headless; separate these phases in logs.
