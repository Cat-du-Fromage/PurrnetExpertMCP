# Network Visibility et interest management

**Source officielle** : `systems-and-modules/network-manager/network-visibility/README.md`, `visibility-rules.md`, `whitelist-and-blacklist.md`, `distance-condition.md`, `using-the-visibility.md`.

- Le serveur détermine **par joueur et par NetworkIdentity** qui observe l'objet. Pas observateur = objet absent chez ce joueur, donc pas de RPC/state de cet objet.
- Les règles d'un rule-set sont combinées en **OU** : une seule autorisation suffit; sans règle l'objet est masqué (sauf exceptions). Ne jamais interpréter plusieurs règles comme un ET implicite.
- Les listes blanches/noires sont évaluées avant les règles; l'owner conserve la visibilité selon le contrat documenté. Vérifier l'ordre exact dans la page `README.md`.
- La visibilité peut différer entre plusieurs composants réseau sur un même GameObject. Celui-ci reste présent tant qu'au moins un composant est visible. Les callbacks d'observation peuvent être propres au composant ou à l'objet.
- `CanSee` et l'évaluation sont **serveur uniquement**; les rules assets partagés ne doivent pas conserver d'état propre à un objet. Favoriser `complexity` faible sur les règles peu coûteuses.
- Ne pas confondre filtrage de visibilité (optimisation/confidentialité des objets) avec `ownerOnly` (confidentialité d'un module) ni avec la visibilité **PurrDiction** (`references/prediction/visibility-and-interactions.md`).

## Tests
Deux équipes et trois joueurs à distances différentes, liste blanche/noire, transfert d'owner, ajout/retrait d'observateur, late join. Contrôler absence de data/RPC pour le joueur non autorisé, pas seulement rendu caché.
