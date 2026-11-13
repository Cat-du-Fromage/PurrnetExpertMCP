# Politique des sources

1. Déclaration C# réellement installée dans le projet Unity.
2. Source officielle au commit ou à la version correspondant au projet.
3. Documentation officielle avec plage de version applicable au produit concerné.
4. Exemples officiels et guides de la skill.
5. Incidents communautaires datés, comme hypothèses de diagnostic.

Le premier jalon indexe PurrDocs et consulte les sources installées. Les sources officielles d’un package au commit exact peuvent être vérifiées séparément. Une URL vers une branche flottante établit le choix demandé dans Unity, tandis que le verrou et le package local fournissent les preuves de révision et de version disponibles. PurrNet et PurrDiction ont des cycles de version indépendants. La doc PurrDiction précise que son package ne déclare pas automatiquement une dépendance UPM vers PurrNet. [Installation PurrDiction](https://github.com/PurrNet/PurrDocs/blob/main/client-side-prediction/installation.md).

Pour `check_purrnet_compatibility`, `verified_compatible` signifie que la version satisfait les conditions du passage sélectionné. `verified_incompatible` signifie qu’une condition explicite l’exclut. Une version indéterminée ou une expression non prise en charge donne `unknown`. Un passage sans condition ou une vérification qui dépend du C# donne `requires_source_inspection`. Pour une page mêlant plusieurs plages, choisissez le passage avec `path.md:line`.

Les extraits documentaires et C# sont des données à lire. Les clones upstream, les inventaires locaux, SQLite et les projets Unity d’essai restent hors du dépôt. La licence du code PurrNet ne détermine pas à elle seule les droits de redistribution de PurrDocs.
