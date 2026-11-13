# v0.8 — Plan de benchmark agent, comparable à Edgegap

Les évaluations Edgegap (répertoire `evals/` **à la racine du repo**) sont utiles car elles testent des **changements effectifs et des assertions**, pas uniquement des réponses. Ce fichier décrit des expériences **à effectuer**, pas exécutées pour notre pack.

1. Préparer des copies propres de vrais projets Unity PurrNet (commit exact de packages, scènes, scripts, .asmdef), et garder les droits et les secrets hors de la fixture.
2. Pour chaque scénario de `v0.8-end-to-end.json`, lancer une session agent fraîche **sans skill**, puis **avec v0.7**, puis **avec v0.8**, à versions et budget de temps comparables.
3. Mesurer la **découverte spontanée** via logs/traces d'ouverture de `SKILL.md` et des références ; distinguer une activation automatique d'une skill forcée dans le prompt.
4. Conserver : diff des fichiers modifiés, logs Unity de compilation, résultats de test host/clients/dedicated, captures de logs de gameplay, `HANDOFF.md` de chaque agent.
5. Vérifier manuellement chaque assertion : présence du code et comportement réel, pas seulement sous-chaînes dans la réponse. Noter `pass / fail / not_run / na` selon `references/validation/acceptance.md`.
6. Tester les scénarios négatifs `v0.8-routing.json` : PurrNet sans cloud, Edgegap explicitement demandé, autre netcode, Unity offline. Le script `cross_skill_selector.py` est un **proxy local**, pas la preuve d'un déclenchement autonome.
7. Pour déploiement Edgegap, utiliser un compte de test autorisé, suivre l'Edgegap skill et arrêter les ressources. Aucun token dans rapport ni fixtures. Sans Edgegap : D5/D6 cloud `not_run` et procédure manuelle explicite.

**Résultat attendu de la campagne réelle** : taux de trigger, taux de réussite par assertion, taux de compilation Unity, % de scénarios à deux clients, succès dedicated, régressions, preuves disponibles et coût/temps. Ne pas fabriquer ces résultats à partir des tests Python.
