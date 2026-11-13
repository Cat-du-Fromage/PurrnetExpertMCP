# Contrat d'acceptation par preuves — PurrNet Expert

**Une validation doit être un résultat observé.** Les scripts Python, logs d'analyse et signatures ne remplacent ni la compilation, ni un test multijoueur. Respecter les dépendances : ne jamais déclarer D4 « clients jouent » sans log/observation D3 « build compilé » sur la même révision.

## Niveaux de preuve

| Gate | Ce qui doit être prouvé | Preuve admissible | Piège à éviter |
|---|---|---|---|
| D0 | Hypothèse et plan | Fichiers/symptômes, reproduction projet | « probablement corrigé » présenté comme résultat |
| D1 | Documentation officielle consultée | URL+section+révision/branche, version gate | Archive Discord historique prise pour API courante |
| D2 | API exacte présente | Chemin package source/commit, signature, paramètres, namespaces | grep sur un commentaire uniquement |
| D3 | Compilation Unity | commande Editor/Unity, exit code, log + plateforme/Unity version | Python `py_compile` présenté comme build C# |
| D4 | Jeu sur 2 clients | 2 processus/builds, logs serveur et client, action gameplay observée | « connected » sans monde/autorité |
| D5 | Serveur dédié réel | build server sans client local, 2 clients, logs world init + interaction | réussite en host seulement |
| D6 | Résilience et sécurité | perte/jitter, late join, reconnect, owner transfer, tests d'inputs malveillants | aucune preuve, labels « production ready » |

## Mini-contrat de tâche avant modification

```
FONCTION       : exemple « deux clients tirent et voient l'impact »
PROJECT        : chemin/version Unity, commit packages, scène
AUTHORITY      : owner input -> server valide -> état -> observers
CHANGEMENTS    : fichiers touchés et justification
RISQUES        : RPC/host/dedicated/late join/prediction/MTU
GATES CIBLÉES  : D1,D2,D3,D4,D5,D6 (selon intention)
```

## Sortie à remettre

- Modifications par chemin ; scripts/Inspector/assemblies nécessaires ; comportement ancien préservé.
- Version PurrNet et addons, références officielles précises, API réellement vérifiées.
- Tableau des gates **réussies / échouées / non exécutées / non applicables** + preuve (commandes, logs, procédure manuelle).
- Cas testés : host, deux clients distants, dédié, late join, permissions, transport, prédiction selon portée.
- Problèmes ouverts avec diagnostic reproductible ; ne jamais masquer l'absence de Unity/cloud.

## Manifeste machine-readable (optionnel)

Pour enregistrer les résultats **observés**, utiliser `assets/validation/evidence.example.json` et lancer :

```bash
python scripts/check_evidence.py evidence.json --project <PROJECT>
```

Le contrôle rejette les statuts « pass » sans chemins de preuve lisibles, et les gates de haut niveau sans gates inférieures ; il ne juge ni la vérité des logs, ni la sémantique Unity. Ne pas le présenter comme un test E2E. Remplir les valeurs uniquement après avoir exécuté les étapes.

Pour lancer une compilation/import Unity en batch de façon **explicite** : `python scripts/unity_compile_check.py <PROJECT> --unity-exe <UNITY_EXE> --log-file <LOG> --run`. Sans `--run`, la commande ne fait qu’afficher son plan. Un retour `0` sans erreurs de compilateur valide l’import des scripts, **pas** la construction d’un client ou serveur dédié.

## Edgegap

La skill Edgegap dispose d'exemples et d'une validation annoncée sur son Incremental sample. Sa preuve porte sur **son projet test**, pas sur ce projet utilisateur et pas sur `assets/unity` du présent pack. Ne pas utiliser ses identifiants/tokens dans ce manifeste. En cloud, consigner identifiant d'allocation non sensible, version de build, résultats direct/matchmaker/autostop, coûts/ressources arrêtés.
