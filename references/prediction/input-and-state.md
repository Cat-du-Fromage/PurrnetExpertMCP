# INPUT, STATE, validation et répétition

**Sources** `client-side-prediction/input-handling.md`, `state-handling.md`, `security.md`, `flow.md`, `predicted-identities.md`.

- `PredictedIdentity<INPUT,STATE>` collecte l'intention locale via `GetFinalInput(ref INPUT)` **une fois par tick**; les fronts `GetKeyDown` doivent être accumulés en `UpdateInput(ref INPUT)` entre les ticks pour ne pas être perdus.
- INPUT est une struct `IPredictedData`, STATE une struct `IPredictedData<STATE>`; stocker dans STATE toutes les données qui changent les ticks futurs (position, vitesse, cooldown, ammo, mode, RNG, IDs). Inspector = paramètres *constants* ou transférés à l'état lorsqu'ils changent.
- `SanitizeInput(ref INPUT)` pour borner mouvement, nombres non finis, aim et tailles ; serveur valide EN PLUS cooldown, ressources, ownership, collision, vitesse et permissions. Un input « bien formé » n'est pas « légitime ».
- `ModifyExtrapolatedInput(ref INPUT)` neutralise les événements one-shot (fire, jump, interact, achats) si input répété faute de paquet. Le `Repeat Input Factor` trop petit stoppe remote actors; trop grand les fait overshoot. Choisir selon RTT et policy.
- Dans `Simulate(INPUT input, ref STATE state, float delta)`, ne jamais lire `Input`, `PlayerInput`, un `InputHandler` MonoBehaviour, les frames Unity ni un RPC. Simulation doit dépendre d'INPUT+STATE+sources prédictibles uniquement.
- `GetInitialState` snapshot complet; `GetUnityState/SetUnityState` pour Unity physics/transform/caches qui impactent le futur tick. `UpdateView` utilise viewState interpole mais ne doit pas modifier le verdict du gameplay.
- Les events du rendu utilisent `PredictedEvent`/verified view, pas mutation de state en callback audio.

## Tests
Press/release entre ticks, perte d'un paquet contenant un fire, input falsifié, cooldown, input stale, rollback, join tardif et changement de policy. Vérifier que state du serveur gagne toujours.
