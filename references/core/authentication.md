# Authentification, refus et confiance

**Source officielle** : `systems-and-modules/network-manager/authentication.md`, `network-manager/connection-and-player-events.md`.

## Règles non négociables
- Une `Connection` non authentifiée **n'est pas un `PlayerID`**. Elle ne doit pas recevoir d'objets, de RPC ni de broadcasts scoped au joueur. Ne pas créer la session de gameplay dans un callback de connexion transport.
- Pour un authenticator personnalisé, examiner `AuthenticationBehaviour<T>`, ses callbacks `GetClientPayload` et `ValidateClientPayload`, et `[RegisterNetworkType(typeof(AuthenticationRequest<Payload>))]` dans la même assembly que le payload; confirmer la signature dans le package installé.
- Vérifier le payload **côté serveur** : expiration, signature d'un token, audience, usage unique, limites, erreurs. Un secret serveur ne doit jamais se trouver dans le client Unity.
- Les refus structurés peuvent utiliser `AuthenticationBehaviour<TRequest,TDenial>` sur les versions qui exposent cette API; contrôler type `TDenial` (struct), timeout, ACK, messages côté client et déni non authentifié.
- L'authentification ne remplace pas les contrôles d'autorisation sur chaque RPC, spawn, déplacement ou inventaire. Protéger aussi les reconnexions, cookies et usurpation d'identité.
- Lier l'état de lobby à `onPlayerJoined` **après** authentification, pas à `onClientConnectionState`.

## Tests adversariaux
Token absent/invalide/expiré, client falsifié, tentative d'invoquer gameplay avant auth, deux sessions du même compte, déconnexion pendant handshake et réauthentification. Ne pas déclarer sûr sans ces tests.
