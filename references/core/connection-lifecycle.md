# Life cycle connection/player/observation

**Official source**: `systems-and-modules/network-manager/connection-and-player-events.md`, `network-manager/authentication.md`, `network-identity/networkbehaviour.md`.

## Sequence and callbacks
1. Transport condition : `onServerConnectionState` / `onClientConnectionState` (`Connecting`, `Connected`, `Disconnecting`, `Disconnected`). No `PlayerID` guaranteed yet.
2. Accepted authentication: `onPlayerJoined(PlayerID, bool isReconnect, bool asServer)`. `isReconnect` indicates that an identifier already seen in the session returns, not that its world is automatically restored.
3. Scenes: `onPlayerLoadedScene` / `onPlayerUnloadedScene`; wait for relevant loading before assuming a ready stage object. Listen to the documented client/server side.
4. Observation: callbacks `OnObserverAdded` / `OnObserverRemoved`, server side; replication status per player. Useful for late join and targeted initial payload.
5. `onPlayerLeft`: Clean the state according to reconnection/persistence strategy, without deleting a session that can be recovered by mistake.

**Host lifecycle**: `asServer` can cause two distinct paths, one for server and one for client; explicitly check the role. Subscribe at the documented lifecycle point, such as `OnSpawned`, and unsubscribe symmetrically. Keep delegate references so handlers can be removed.

## Validation
Cookie reconnection, late join, scene change, win/lose visibility, host/dedicated, disconnection while loading. Measure the actual order of events in logs and keep consistent identifiers.
