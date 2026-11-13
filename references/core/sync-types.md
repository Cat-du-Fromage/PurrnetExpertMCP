# Sync Types et choix du mécanisme

**Sources officielles** : `systems-and-modules/network-modules/sync-types/README.md` et ses pages (`syncvar.md`, `validated-syncvar.md`, `synclist.md`, `syncdictionary.md`, `synclazyref.md`, `syncevent.md`, `synctimer.md`, `syncinput.md`, `synclist-1.md`, `synclist-1-1.md`, `synchashset.md`), `network-modules/owner-only.md`.

## Choisir
- `SyncVar<T>` : état durable répliqué, événements onChanged, autorité serveur par défaut ou `ownerAuth` explicite.
- `ValidatedSyncVar<T>` : modification réactive par owner avec validation serveur et retour d'échec; examiner `serverValidation`, `onValidationFail`, la version et les cas d'ACK obsolètes.
- `SyncList`, `SyncDictionary`, `SyncArray`, `SyncQueue`, `SyncHashset` : collections synchronisées; vérifier sérialisation des éléments, mise à jour des observers et late join, coût mémoire/bandwidth.
- `SyncLazyRef` : référence synchronisée (vérifier résolution, disparition et load); GameObject dans SyncList n'est pas équivalent à un identifiant réseau sérialisé.
- `SyncEvent` : occurrence; ne remplace pas un `SyncVar` pour l'état durable.
- `SyncTimer` : timer synchronisé et réconcilié; distinguer autorité et intervalles de resynchronisation.
- `SyncInput<T>` : input envoyé owner→serveur pour gameplay serveur, alternative **plus simple mais plus sensible à la latence** que client-side prediction; à préférer à un RPC par frame si le design accepte le délai.

## ownerOnly et ownership
`ownerOnly: true` filtre réellement l'envoi d'un module vers le propriétaire, pas seulement son rendu; l'ancien owner **conserve sa dernière valeur locale après transfert**. Si sensible, purger/transformer l'état *avant* changement d'owner et contrôler la stratégie de confidentialité. Nouveau owner reçoit l'état courant, non-owners ne reçoivent pas les updates. `ownerOnly` fixe pendant la vie du module; `ownerAuth` autorise l'écriture owner mais ne constitue pas une validation métier.

**Contraintes modules** : champs/propriétés déclarés au compile time; pas `List<SyncVar<...>>`, ne pas remplacer après spawn, initialiser dans `OnInitializeModules`. Voir `network-modules.md`.

## Tests
Late join, ownership transfer, observation, client malveillant, spam, packet loss, changements de valeur rapides, payload volumineux.
