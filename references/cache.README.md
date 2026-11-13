# Documentation officielle PurrDocs (cache optionnel)

Ce dossier de cache **n'est pas inclus dans l'archive**. Pour une copie Markdown complète utilisable hors ligne, exécuter :

```bash
python scripts/sync_sources.py
python scripts/docs_catalog.py coverage
```

Le script clone **tout** le dépôt `PurrNet/PurrDocs` sous `references/cache/official-docs/` et crée un `docs-index.json` indiquant le commit exact. Les synthèses originales dans `references/*.md` restent disponibles même sans synchronisation. Ne pas republier ce cache sans vérifier les droits.


## Archive Stray Help (opt-in, distincte de PurrDocs)

```bash
python scripts/sync_stray_archive.py
python scripts/search_stray_archive.py 'NetworkTransform' --limit 8
```

Ce script télécharge localement **le commit historique exact** de `nmban/Purrnet-Stray_Help`, sans écraser les fichiers et sans le republier. Les réponses Discord sont historiques, non normatives et potentiellement sensibles ; consulter uniquement quelques extraits utiles au diagnostic. Le dossier `references/cache/` est ignoré par Git et **exclu de tous les ZIP** de la skill.
