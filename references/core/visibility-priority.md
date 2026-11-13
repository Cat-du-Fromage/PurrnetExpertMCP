# Décision exacte de Network Visibility (classique)

**Source officielle** : `systems-and-modules/network-manager/network-visibility/README.md`, `visibility-rules.md`, `using-the-visibility.md`, `whitelist-and-blacklist.md`.

## Décision serveur (pour une identité et un joueur)

Suivre cet ordre, **la première condition applicable l'emporte** :

1. Parent invisible au joueur → **masqué**.
2. Joueur en whitelist de l'identité → **visible**.
3. Joueur en blacklist → **masqué**.
4. Aucun rule-set applicable, ni global ni override → **visible**.
5. Joueur propriétaire de l'identité → **visible**.
6. Une règle du rule-set retourne oui → **visible** ; sinon masqué. Les règles se combinent en **OU**, pas en ET.

Les rule-sets **vides** masquent tout ce à quoi ils s'appliquent, sous réserve des exceptions ci-dessus. Les règles ne sont pas évaluées continuellement : déclencher une réévaluation via l'API documentée lorsque l'état des joueurs ou du monde change. Vérifier `EvaluateVisibility` et le point d'appel dans le code installé.

## Le piège du même GameObject

La visibilité est suivie **par composant réseau**. Le `GameObject` subsiste tant qu'au moins une `NetworkIdentity`/un `NetworkBehaviour` est observé. Un override de visibilité placé sur le deuxième composant ne s'applique pas rétroactivement à celui du dessus dans l'Inspector. Pour un objet caché entièrement, appliquer le rule-set au premier composant concerné et contrôler les overrides descendants (`Children Inherit`).

Ne pas confondre cet interest management avec le `ownerOnly` d'un Sync Type, ni avec `PredictedVisibility`. Une `NetworkIdentity` **miroir PurrDiction >=1.4.0** n'est pas gouvernée par ces règles classiques.

## Scénarios à prouver

| Cas | Attendu |
| --- | --- |
| Aucun rule-set | Visible selon la politique par défaut |
| Rule-set vide, joueur non owner | Masqué |
| Une règle autorise, deux refusent | Visible (OU) |
| Parent masqué, enfant whitelisté | Vérifier la priorité parent : masqué |
| Whitelist et blacklist de la même identité | Whitelist prioritaire selon README |
| Deux composants avec overrides différents | Objet présent tant qu'un composant visible |
| Joueur rejoint ou change de zone | Nouvelle évaluation et RPC/sync ciblés |

**Attention** : les exceptions liées au parent/aux observers doivent être vérifiées dans le code du package si les versions diffèrent des docs `main`.
