# PurrDiction : commandes one-shot, extrapolation et effets rejouables

**Sources** : `client-side-prediction/input-handling.md`, `best-practices.md`, `multi-identity-interactions.md`, `flow.md`, `security.md`.

## Le risque concret

`Input.GetKeyDown` ne s'exécute que sur certaines frames Unity ; `GetFinalInput` ne s'exécute que par tick. Si l'input est lu uniquement dans `GetFinalInput`, une frappe entre deux ticks peut être perdue. À l'inverse, si `fire=true` est répété pendant l'extrapolation d'un paquet perdu, une action ponctuelle peut être jouée plusieurs fois.

## Schéma issu de la documentation officielle (illustratif)

```csharp
// INPUT doit être un struct IPredictedData, avec Dispose.
protected override void UpdateInput(ref PlayerInput input)
{
    input.jump |= Input.GetKeyDown(KeyCode.Space);
}

protected override void GetFinalInput(ref PlayerInput input)
{
    input.move = new Vector2(
        Input.GetAxisRaw("Horizontal"),
        Input.GetAxisRaw("Vertical"));
}

protected override void SanitizeInput(ref PlayerInput input)
{
    input.move = Vector2.ClampMagnitude(input.move, 1f);
}

protected override void ModifyExtrapolatedInput(ref PlayerInput input)
{
    input.jump = false;
}
```

Il s'agit d'**overrides partiels**, pas d'une classe Unity autonome ou compilée : vérifier `PlayerInput`, la classe de base et les versions de PurrDiction.

## Une séquence de tir robuste

1. Capture locale : `UpdateInput` peut accumuler le front, ou un compteur de commandes permet de distinguer deux tirs successifs sans booléen répété.
2. `GetFinalInput` collecte les axes continus ; un input envoyé doit rester **compact et sérialisable**.
3. `SanitizeInput` borne magnitude et valeurs non finies ; le serveur vérifie aussi cooldown, munitions, ownership et range **dans sa simulation**.
4. `ModifyExtrapolatedInput` retire les one-shots sur inputs répétés ; ne pas supprimer la mutation STATE de `Simulate` pendant rollback.
5. Créer un projectile par `PredictedHierarchy.Create` pendant le tick, avec une séquence stable si nécessaire.
6. L'audio, le tracé ou un événement utilisateur utilisent `PredictedEvent`, `UpdateView` ou une vérification de vue conforme à la version. Les écouteurs doivent rester **présentation seulement**.

## Tests

- Appuyer et relâcher entre deux ticks.
- Perdre l'input du tick du tir : ni tir doublé ni tir ignoré indûment après réparation.
- Conserver le bouton appuyé avec le facteur de répétition élevé.
- Rejouer trois fois le tick d'une récompense : aucun RPC/FX/achievement supplémentaire.
- Client malveillant envoie `move=(Infinity, NaN)` et `fire` à chaque tick ; pas de dégâts illégaux.

**Statut** : exemples partiels non compilés Unity dans ce pack.
