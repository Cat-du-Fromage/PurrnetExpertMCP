# NetworkBones et NetworkOwnershipToggle — cas d'usage et contrôle

**Sources officielles** :
- [Network Bones](https://purrnet.dev/docs/plug-n-play-components/network-bones)
- [Network Ownership Toggle](https://purrnet.dev/docs/plug-n-play-components/network-ownership-toggle)
- [Network Animator](https://purrnet.dev/docs/plug-n-play-components/network-animator)

Ces composants ne sont **pas** interchangeables avec `NetworkTransform` / `NetworkAnimator` ni avec `PredictedTransform` en simulation PurrDiction. Lire les pages et inspecter leurs propriétés dans la version installée avant de produire du code.

## NetworkBones

Synchroniser une structure d'os ou de parties d'un personnage peut être utile pour le ragdoll, pose de membres et autres objets visuels articulés. Vérifier la hiérarchie, les références d'os, la fréquence, l'autorité, les conversions espace local/monde et l'interaction avec Animator/physics. Pour un personnage joueur non prédit, comparer au coût de transmettre uniquement les paramètres d'animation et reconstruire localement la pose ; ne pas synchroniser des dizaines d'os par défaut.

**Tests** : personnage maître + 2 observateurs, changement de pose, changement d'owner, sortie/entrée de visibilité, interpolation et bande passante. Si un composant animé pilote la même pose chez l'observateur, définir qui est le seul écrivain.

## NetworkOwnershipToggle

Aide à activer/désactiver des éléments selon ownership. Toujours séparer **affichage local** (caméra, input) de **validation autoritaire** (inventaire, attaque, dégâts). Un GameObject ou composant désactivé pour un non-owner ne constitue pas une garantie de sécurité réseau.

**Tests** : spawn sans owner, owner local, owner distant, transfert, host (server/client), dedicated; s'assurer que le serveur continue le traitement nécessaire quand aucun local player n'existe.

## Deliverable attendu

Nom exact du composant dans le package, réglages Inspector, quoi synchroniser, qui possède l'état, estimation bande passante, deux clients et late join. Ne pas inventer des champs/événements non lus dans le code source.
