# Authentication, refusal and trust

**Official source**: `systems-and-modules/network-manager/authentication.md`, `network-manager/connection-and-player-events.md`.

## Non-marketable rules
- An unauthenticated `Connection` **is not a `PlayerID`**. It must not receive any objects, RPC or broadcasts that are scoped to the player. Do not create the gameplay session in a transport connection callback.
- For a custom authenticator, review `AuthenticationBehaviour<T>`, its `GetClientPayload` and `ValidateClientPayload` callbacks, and `[RegisterNetworkType(typeof(AuthenticationRequest<Payload>))]` in the same assembly as payload; confirm the signature in the installed package.
- Check the payload **on the server side**: expiration, signature of a token, audience, single use, limits, errors. A server secret must never be in the Unity client.
- Structured refusals can use `AuthenticationBehaviour<TRequest,TDenial>` on versions that expose this API; control type `TDenial` (struct), timeout, ACK, client-side messages and unauthenticated denial.
- Authentication does not replace authorization controls on each RPC, spawn, displacement or inventory. Also protect reconnections, cookies and identity usurpation.
- Link the lobby status to `onPlayerJoined` **after** authentication, not to `onClientConnectionState`.

## Tests adversariaux
Token absent/invalid/expired, falsified client, attempt to invoke gameplay before auth, two sessions of the same account, disconnection during handshake and reauthentication. Do not declare safe without these tests.
