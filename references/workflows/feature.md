# Workflow A — Implémenter une fonctionnalité PurrNet

## 0. Définition de fini

Écrire une phrase observable : *« Dans un serveur + 2 clients, l'action X déclenchée par A modifie Y seulement si l'autorité l'autorise, B reçoit l'état, un client arrivé tard récupère Y. »* Les exceptions (objet ownerOnly, visibilité, ServerRelay) doivent être explicites.

## 1. Inspecter AVANT de générer

- Unity exact, `dev.purrnet.purrnet`, versions Addons, transports, `.asmdef`, NetworkManager/Rules, scènes et prefabs installés.
- Trouver une implémentation existante pour ne pas créer un second écrivain (`NetworkTransform` + script de transform, deux spawners, plusieurs subscriptions).
- Identifier si l'objet est purement classique PurrNet, prédit, ou contient un `NetworkIdentity` miroir pour des données hors prédiction.

## 2. Choisir l'API (exemple)

| Besoin | Envisager d'abord | Vérification |
|---|---|---|
| Score ou santé persistante | `SyncVar`, serveur autoritaire | propriétaire, état initial, late join |
| Liste d'inventaire | `SyncList`, `ownerOnly` si privée | ownership transfer, ancienne copie |
| Input vers serveur | `SyncInput<T>` / PurrDiction `INPUT` | input validé côté serveur |
| Impact fugitif | RPC / `SyncEvent` (hors prédiction) | observers, canal, buffer et taille |
| Avatar mobile | `NetworkTransform` / `PredictedTransform` | NE PAS utiliser les deux pour le même état |
| Audio | `NetworkAudioSource` / effet en vue prédite | ressources enregistrées, rollback |
| Référence différée | `SyncLazyRef`, `GlobalNetworkID` | scène du référent absente puis chargée |

Consulter `references/components/component-selector.md`, `references/core/sync-types-decision.md`, `references/core/messaging-and-mtu.md` et les docs officielles routées ; ne pas inventer la signature d'une API.

## 3. Contrat autorité / timeline

Qui demande ? Qui possède ? Qui valide ? Qui écrit l'état autoritaire ? Qui reçoit ? À quelle phase/lifecycle ? Comment late join, reconnect, spawn/despawn, scene load et pooling se déroulent-ils ? Pour PurrDiction, passer au [workflow de prédiction](prediction.md) et respecter toutes les BP.

## 4. Changement minimal

Modifier les composants existants avant d'ajouter une nouvelle architecture. Éviter de toucher aux scènes, prefabs, registries et flags de lancement si une adaptation de code suffit. Lorsqu'un changement de scène ou d'Inspector est nécessaire, fournir les chemins, champs et valeurs exacts, sans fabriquer d'asset Unity en dehors de l'Editor si cela compromet les GUID/meta.

## 5. Tests à niveaux

- **G0** API trouvée dans package installé ; résumer version/source et exigences .asmdef.
- **G1** Unity compile après modifications ; recueillir log et résultat de commande.
- **G2** Host et client : action autorisée, acteur non autorisé, RPC/sync sans double callback.
- **G3** Serveur dédié seul + deux clients : système complet, pas uniquement « connected ».
- **G4** Late join, reconnexion, transfert owner, scène/visibility, packet loss pertinent.

## 6. Hand-off

`Fichiers modifiés`, `Composants/Inspector`, `Autorité`, `Gates observées/non observées`, `Cas limites`, `Limites de la preuve`. Tout non exécuté est `non vérifié`.
