#!/usr/bin/env python3
"""Static pack audit, Python/JSON checks and required PurrDiction coverage gates (not Unity)."""
from pathlib import Path
import ast
import argparse
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    'SKILL.md', 'README.md', '.gitignore', 'QUALITY_REPORT.md', 'references/cache.README.md',
    'references/source-map.md', 'references/version-policy.md',
    'references/api-map.md', 'references/recipes.md',
    'references/dedicated-server.md', 'references/verification.md',
    'references/edgegap-integration.md', 'references/troubleshooting.md',
    'references/test-matrix.md', 'references/networking-best-practices.md',
    'references/purrdiction-best-practices.md', 'references/purrdiction-architecture.md',
    'references/purrdiction-test-matrix.md', 'references/documentation-map.md',
    'references/documentation-policy.md',
    'assets/unity/README.md', 'assets/unity/ExampleNetworkCounter.cs',
    'assets/unity/ExampleWorldSeed.cs',
    'evals/tasks.json', 'evals/routing.json', 'evals/purrdiction.json',
    'scripts/inspect_project.py', 'scripts/find_api.py', 'scripts/sync_sources.py',
    'scripts/docs_catalog.py', 'scripts/guard_predicted_code.py', 'scripts/test_scripts.py',
    'scripts/route_docs.py', 'scripts/check_doc_versions.py', 'scripts/docs_drift.py',
    'scripts/audit_doc_links.py', 'scripts/audit_project_assets.py', 'scripts/test_v04.py',
    'references/task-routes.json', 'evals/v0.4-hardcases.json',
    'scripts/doc_coverage_matrix.py','scripts/test_v05.py','scripts/test_v06.py','scripts/trigger_probe.py','scripts/install_activation.py','scripts/install_project.py',
    'evals/activation-cases.json','evals/AGENT_ACTIVATION_TEST_PLAN.md',
    'references/activation/auto-trigger.md','references/coverage/feature-readiness.md',
    'references/core/sync-recipes.md','references/core/messaging-and-mtu.md','references/core/scene-playbook.md',
    'references/core/serialization-playbook.md','references/components/network-bones-ownership.md',
    'references/prediction/real-world-recipes.md','references/prediction/state-machine-playbook.md',
    'references/tools/troubleshooting-playbook.md','references/build/build-release-checklist.md',
    'assets/unity/ExampleNetworkAnimator.cs','assets/unity/ExamplePredictedData.cs',
    'references/components/component-selector.md', 'references/components/network-transform.md',
    'references/components/network-animator.md', 'references/components/network-rigidbody.md',
    'references/components/network-audio.md', 'references/components/network-reflection.md',
    'references/components/network-state-machine.md', 'references/core/serialization-advanced.md',
    'references/core/network-assets-addressables.md', 'references/core/sync-types-decision.md',
    'references/core/auth-permission-hardening.md', 'references/core/rpc-advanced.md',
    'references/build/production-and-stripping.md', 'references/tools/diagnostics.md',
    'references/prediction/advanced-state-and-tools.md', 'references/prediction/manager-inspector.md',
    'references/prediction/hierarchy-advanced.md', 'references/recipes/IMPLEMENTATION_STATUS.md',
    'scripts/roslyn/PurrNetReplayAudit.csproj','scripts/roslyn/Program.cs', 'scripts/roslyn/README.md',
    'evals/v0.5-hardcases.json','evals/UNITY_VALIDATION_PLAN.md',
    'references/addons/purrlobby-workflow.md','references/addons/purrvoice-workflow.md',
    'references/core/transports-platforms.md','references/core/visibility-advanced.md',
    'references/historical/README.md','references/historical/triage-playbook.md',
    'references/historical/case-studies.md','references/historical/legacy-version-map.md',
    'references/historical/incident-catalog.json',
    'scripts/historical_issues.py','scripts/sync_stray_archive.py','scripts/search_stray_archive.py',
    'scripts/test_v07.py','evals/v0.7-cases.json',
    'references/workflows/README.md','references/workflows/feature.md',
    'references/workflows/bug.md','references/workflows/dedicated.md',
    'references/workflows/prediction.md','references/workflows/edgegap-handoff.md',
    'references/validation/acceptance.md','references/edgegap-comparison.md',
    'assets/validation/evidence.example.json','scripts/audit_dedicated_readiness.py',
    'scripts/check_evidence.py','scripts/cross_skill_selector.py','scripts/unity_compile_check.py','scripts/test_v08.py',
    'evals/v0.8-routing.json','evals/v0.8-end-to-end.json','evals/V08_E2E_PLAN.md',
    'references/anthropic-skill-authoring.md', 'scripts/audit_skill_authoring.py',
    'references/core/spawn-security-and-persistence.md', 'references/core/player-identity-and-lazy-refs.md',
    'references/core/visibility-priority.md', 'references/core/collider-rollback-classic.md',
    'references/prediction/mirror-and-visibility.md', 'references/prediction/one-shot-input-and-events.md',
    'scripts/test_v09.py', 'evals/v0.9-hardcases.json', 'evals/V09_REAL_AGENT_PLAN.md',
    'evals/fixtures/v08/README.md','evals/fixtures/v08/HostOnlyWorld.cs.txt',
    'evals/fixtures/v08/ConnectLoop.cs.txt','evals/fixtures/v08/ServerBoot.cs.txt','evals/fixtures/v08/Scene.unity.txt',
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--release', action='store_true', help='Refuse a local docs cache in a distribution tree')
    args = parser.parse_args()
    errors = []
    for name in REQUIRED:
        if not (ROOT / name).is_file():
            errors.append(f'Missing: {name}')
    if (ROOT / 'SKILL.md').is_file():
        content = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
        if not re.search(r'\A---\s*\nname:\s*purrnet-expert\b', content):
            errors.append('Invalid SKILL frontmatter')
        if not re.search(r'\nmetadata:\s*\n\s+version:\s*[\'"]?0\.9\.', content):
            errors.append('Expected metadata.version v0.9')
        for item in sorted(set(re.findall(r'(?:references|assets|scripts|evals)/[A-Za-z0-9_./-]+', content))):
            if not (ROOT / item.rstrip('.,:;)')).exists() and '/cache/' not in item:
                errors.append(f'Broken internal reference {item}')
        for term in ['purrdiction-best-practices.md', 'docs_catalog.py', 'core/authentication.md',
                     'SanitizeInput', 'PredictedObjectID', 'IDuplicate<T>', 'ModifyExtrapolatedInput']:
            if term not in content:
                errors.append(f'Missing mandatory skill guardrail {term}')
    routes = ROOT / 'references/task-routes.json'
    if routes.is_file():
        try:
            routing = json.loads(routes.read_text(encoding='utf-8'))
            if not routing.get('rules'): errors.append('No routes')
            for route in routing.get('rules', []):
                for guide in route.get('guides', []):
                    if not (ROOT / 'references' / guide).is_file():
                        errors.append(f'Missing route guide: {guide}')
                for doc in route.get('docs', []):
                    if doc.startswith('/') or '..' in Path(doc).parts:
                        errors.append(f'Unsafe document route: {doc}')
        except (OSError, ValueError, TypeError) as e:
            errors.append(f'Bad task routes: {e}')
    # v0.8: every cross-skill routing fixture should have its expected label.
    try:
        labels = [x.get('expected_skill') for x in json.loads((ROOT/'evals/v0.8-routing.json').read_text())]
        if not labels or not set(labels).issubset({None, 'purrnet-expert', 'edgegap-purrnet'}):
            errors.append('Invalid cross-skill routing labels')
    except (OSError, ValueError, TypeError) as e:
        errors.append(f'Invalid v0.8 routing eval: {e}')
    try:
        e2e = json.loads((ROOT/'evals/v0.8-end-to-end.json').read_text())
        if len(e2e.get('scenarios', [])) < 8 or any(not s.get('assertions') for s in e2e['scenarios']):
            errors.append('Insufficient v0.8 E2E scenarios')
    except (OSError, ValueError, KeyError, TypeError) as e:
        errors.append(f'Invalid v0.8 end-to-end eval: {e}')
    bp = ROOT / 'references/purrdiction-best-practices.md'
    if bp.is_file():
        text = bp.read_text(encoding='utf-8')
        for i in range(1, 11):
            if f'BP-{i:02d}' not in text:
                errors.append(f'Missing official Best Practice domain BP-{i:02d}')
    for name in ['evals/tasks.json', 'evals/routing.json', 'evals/purrdiction.json', 'evals/v0.4-hardcases.json','evals/v0.5-hardcases.json']:
        path = ROOT / name
        if not path.is_file(): continue
        try:
            obj = json.loads(path.read_text(encoding='utf-8'))
            if not isinstance(obj, list) or not obj:
                errors.append(f'Empty or invalid eval {name}')
            elif name.endswith(('tasks.json', 'purrdiction.json', 'v0.4-hardcases.json', 'v0.5-hardcases.json')):
                if not all(isinstance(x.get('assertions'), list) and x['assertions'] for x in obj):
                    errors.append(f'Eval missing assertions {name}')
        except (OSError, ValueError) as e:
            errors.append(f'Invalid JSON {name}: {e}')
    try:
        from audit_skill_authoring import audit as audit_authoring
        for failure in audit_authoring(ROOT)['errors']:
            errors.append('Anthropic authoring: '+failure)
    except Exception as exc:
        errors.append(f'Anthropic authoring validation unavailable: {exc}')
    scripts = sorted((ROOT / 'scripts').glob('*.py'))
    for path in scripts:
        try:
            ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
        except (OSError, SyntaxError) as e:
            errors.append(f'Invalid Python {path.name}: {e}')
    cache = ROOT / 'references' / 'cache' / 'official-docs'
    if args.release and cache.exists():
        errors.append('Docs cache present: do not package original full documentation without explicit licence review')
    if errors:
        for error in errors: print('ERROR:', error, file=sys.stderr)
        return 1
    print(f'OK: {len(REQUIRED)} required files, {len(scripts)} parsable Python files, frontmatter, JSON evaluations and BP-01..BP-10.')
    print('DISCLAIMER: No Unity compilation, multiplayer E2E, or live documentation sync was executed.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
