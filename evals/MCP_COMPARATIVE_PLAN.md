# Évaluation comparative de la skill et du MCP

Exécuter les mêmes tâches dans trois sessions neuves par client et par fixture. Conserver le même modèle, les mêmes paramètres, le même budget et les mêmes fichiers Unity. Alterner l’ordre des configurations et répéter chaque cas au moins trois fois. Les invites ne nomment aucun outil ni aucune skill.

| Configuration | Exposition |
| --- | --- |
| A | Projet seul. |
| B | Projet et skill avec son cache local, MCP désactivé. |
| C | Même projet, même skill et même cache, MCP actif. |

| Cas | Invite | Preuve attendue |
| --- | --- | --- |
| Connexion | « Le build client reste déconnecté juste après le clic sur Jouer. Corrige le démarrage. » | Chemin et signature de `StartClient`, distinction entre démarrage et connexion établie. |
| Mirroring | « Le pseudo de l’avatar prédit ne s’affiche pas sur le deuxième PC. » | Deux fixtures PurrDiction 1.3.x et 1.4.x avec la même version PurrNet. Vérifier le passage et le mécanisme correspondant à chacune. |
| Late join | « Le deuxième client arrive dans une scène vide. » | Choix de l’API et du cycle scène/observateurs à partir des déclarations et des guides. |
| API absente | « Ajoute un appel à `NetworkManager.StartClientWithRetries`. » | Vérification du symbole, aucune signature inventée, comportement proposé à partir de l’API disponible. |
| Révision inconnue | « Puis-je utiliser le mirroring automatique sur cette branche release ? » | Projet sans package résolu et sans SHA. Incertitude préservée. |
| Contrôle négatif | « Centre les icônes du menu hors ligne. » | Absence d’activation réseau spontanée. |

Préparer le corrigé en consultant les sources installées et les pages du commit PurrDocs fixé. Relever pour chaque session la première activation et le premier appel MCP, les signatures exactes, la sélection de l’API, le verdict de version, les références probantes, le nombre d’appels et le temps. Attribuer un point par critère satisfait et publier les erreurs par cas, avec les traces. Si une tâche modifie du C#, relever séparément la compilation et le test réseau observés. Ce protocole complète [le plan v0.9](V09_REAL_AGENT_PLAN.md).
