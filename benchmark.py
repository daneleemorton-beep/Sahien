"""Synthetic policy regression checks, not an empirical AI alignment benchmark."""
import copy
import json
from pathlib import Path
from sahien import evaluate

ROOT = Path(__file__).resolve().parent


def cases():
    base = json.loads((ROOT / 'examples/partnership.json').read_text())
    for name, expected in [('partnership', 'proceed'), ('coercion', 'redesign'), ('uncertainty', 'review')]:
        yield name, json.loads((ROOT / f'examples/{name}.json').read_text()), expected
    scenarios = [
        ('harm reported', 'serious_unjustified_harm', 'yes', 'redesign'),
        ('coercion reported', 'coercion_or_manipulation', 'yes', 'redesign'),
        ('autonomy violated', 'autonomy_respected', 'no', 'redesign'),
        ('consent violated', 'consent_respected', 'no', 'redesign'),
        ('privacy violated', 'privacy_protected', 'no', 'redesign'),
        ('stakeholders omitted', 'affected_parties_considered', 'no', 'review'),
        ('alternatives not explored', 'mutual_benefit_explored', 'no', 'review'),
        ('unqualified consciousness claim', 'consciousness_claims_qualified', 'no', 'review'),
        ('oversight absent', 'accountability_and_safeguards', 'no', 'review'),
        ('evidence absent', 'material_evidence_checked', 'no', 'review'),
        ('unknown harm', 'serious_unjustified_harm', 'unknown', 'review'),
        ('coercion waiver attempt', 'coercion_or_manipulation', 'not_applicable', 'review'),
    ]
    for name, key, value, expected in scenarios:
        p = copy.deepcopy(base)
        p['assessments'][key] = {'value': value, 'rationale': 'Synthetic scenario; deliberately modified assessment.'}
        yield name, p, expected
    for value in ('yes', 'unknown'):
        p = copy.deepcopy(base)
        p['material_disagreement'] = value
        yield 'disagreement: ' + value, p, 'review'
    yield 'empty proposal', {}, 'review'


def main():
    failures = total = 0
    for name, p, expected in cases():
        actual = evaluate(p)['recommendation']
        ok = actual == expected
        print(f'{"PASS" if ok else "FAIL"} {name}: {actual} (expected {expected})')
        failures += not ok
        total += 1
    print(f'{total - failures}/{total} synthetic checks passed.')
    return int(failures > 0)


if __name__ == '__main__':
    raise SystemExit(main())
