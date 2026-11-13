# Architecture du premier jalon

La racine reste la source canonique de la skill v0.9.0. Garder ses chemins préserve les appels directs à `scripts/`, les liens des guides et les scénarios existants. L’installateur publie ce même contenu pour les deux agents. Le paquet Python installable vit dans `src/purrnet_expert_mcp`. La wheel embarque le module commun qui définit les chemins du cache et les comparaisons de versions.

- **Contexte Unity** lit le manifeste, le verrou et les métadonnées des packages locaux. Il expose les candidats et les conflits, privilégie les packages embarqués et utilise les preuves du verrou pour départager les entrées du cache. Chaque produit a sa version et sa provenance.
- **Ingestion** utilise l’inventaire SHA-256 généré par le script de synchronisation de la skill. Elle découpe le Markdown par section et par plage de version, puis remplace la base par renommage après validation. Elle ignore le sommaire comme document de recherche. Les outils de consultation ouvrent SQLite en lecture seule.
- **Recherche** favorise la phrase exacte, puis les mots utiles classés par BM25. Chaque résultat indique son produit, le commit, l’empreinte, les lignes et le lien officiel correspondant. Un appel de compatibilité avec `path.md:line` restitue le passage ciblé.
- **API** utilise Tree-sitter C# pour reconnaître les types, méthodes, propriétés, événements et surcharges déclarés. Le statut `syntax_verified` porte sur une déclaration syntaxique dans le fichier identifié. Le statut `signature_unverified` accompagne les fragments incertains, notamment sous compilation conditionnelle.
- **Transport** expose quatre outils en stdio avec le SDK MCP Python officiel 2.3.0 verrouillé. Les appels lisent le disque local. Git intervient uniquement dans la synchronisation explicite.

Le découplage entre indexation et recherche, le stockage FTS5 et les cas comparatifs reprennent les principes du projet de référence. PurrDocs fournit des passages Markdown et des plages de version, tandis que les API PurrNet sont relevées dans les sources Unity. [unity-api-mcp](https://github.com/Codeturion/unity-api-mcp).

## Limites

La recherche lexicale s’appuie sur les termes présents dans les pages. Une question en français gagne en précision avec les noms techniques anglais. La fraîcheur en ligne dépend de la dernière synchronisation explicite.

L’inventaire Unity couvre les packages UPM sous `Packages` et `Library/PackageCache`, ainsi que les métadonnées sous `Assets` à profondeur bornée et les dossiers historiques connus. Les références `file:` hors de ces emplacements, les assemblies binaires, les actifs générés et les importations dont le dossier est inconnu nécessitent une vérification dans Unity. Les scans bornent la profondeur, le nombre d’entrées et le volume lu. Les liens et jonctions internes sont ignorés.

Une déclaration locale ne résout pas les symboles de compilation, les imports, l’héritage, les membres générés, les dépendances ni le choix d’une surcharge à l’appel. La recherche sans projet donne seulement des mentions officielles et ne télécharge aucune source C#.
