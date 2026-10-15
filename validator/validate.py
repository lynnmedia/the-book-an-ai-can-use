#!/usr/bin/env python3
"""Original educational specimen v1.0.0. Validates supplied records, not truth."""
import argparse
import json
import sys
from collections import Counter
from pathlib import Path

VERSION = '1.0.0'

def require(ok, message):
    if not ok:
        raise ValueError(message)

def string(value):
    return isinstance(value, str) and bool(value.strip())

def validate(task, claims, evidence):
    require(isinstance(task, dict), 'task must be an object')
    require(string(task.get('task_id')), 'task_id is required')
    artifact = task.get('artifact')
    require(isinstance(artifact, dict) and all(string(artifact.get(k)) for k in ['id', 'version']), 'artifact id/version are required')
    checks = task.get('checks')
    require(isinstance(checks, list) and bool(checks), 'task checks must be nonempty')
    ids = []
    for check in checks:
        require(isinstance(check, dict) and string(check.get('id')), 'check id is required')
        require(type(check.get('applicable')) is bool, 'applicable must be a declared boolean')
        require(check['applicable'] or string(check.get('reason')), 'inapplicable check needs a declared reason')
        ids.append(check['id'])
    require(len(ids) == len(set(ids)), 'duplicate task check')
    require(isinstance(claims, list) and isinstance(evidence, list), 'claims/evidence must be arrays')
    claim_map = {}
    for claim in claims:
        require(isinstance(claim, dict) and claim.get('check_id') in ids, 'unknown claimed check')
        require(claim['check_id'] not in claim_map, 'duplicate claimed check')
        refs = claim.get('evidence_ids')
        require(isinstance(refs, list) and all(string(x) for x in refs) and len(refs) == len(set(refs)), 'evidence_ids must be unique strings')
        claim_map[claim['check_id']] = refs
    records = {}
    for record in evidence:
        require(isinstance(record, dict) and all(string(record.get(k)) for k in ['id', 'task_id', 'check_id']), 'evidence identity fields are required')
        require(record['id'] not in records, 'duplicate evidence id; cannot resolve conflicting identities')
        require(isinstance(record.get('artifact'), dict) and all(string(record['artifact'].get(k)) for k in ['id', 'version']), 'evidence artifact id/version are required')
        require(record.get('outcome') in ['passed', 'failed', 'unknown'], 'inadmissible evidence outcome')
        records[record['id']] = record
    results = []
    for check in checks:
        cid = check['id']
        refs = claim_map.get(cid, [])
        base = {'check_id': cid, 'evidence_ids': refs}
        if not check['applicable']:
            disposition, reason = 'NOT_APPLICABLE', check['reason']
        elif not refs or any(ref not in records for ref in refs):
            disposition, reason = 'MISSING', 'required evidence reference is absent'
        else:
            selected = [records[ref] for ref in refs]
            if any(r['task_id'] != task['task_id'] or r['check_id'] != cid or r['artifact']['id'] != artifact['id'] or r['artifact']['version'] != artifact['version'] for r in selected):
                disposition, reason = 'STALE_MISMATCHED', 'evidence task, check, artifact identity or version differs'
            elif any(r['outcome'] == 'failed' for r in selected):
                disposition, reason = 'FAILED', 'at least one supplied matching record reports failure; a pass cannot erase it'
            elif any(r['outcome'] == 'unknown' for r in selected):
                disposition, reason = 'MISSING', 'matching record does not establish a passed outcome'
            else:
                disposition, reason = 'SUPPORTED', 'all cited matching records report passed'
        results.append({**base, 'disposition': disposition, 'reason': reason})
    return {'specimen': 'original-educational-evidence-reference-validator', 'version': VERSION,
            'task_id': task['task_id'], 'artifact': artifact, 'results': results,
            'counts': dict(Counter(r['disposition'] for r in results)),
            'limitation': 'Supplied-record consistency only; no proof of record truth, external execution or release authorization.'}

def read(path):
    with Path(path).open(encoding='utf-8') as f:
        return json.load(f, parse_constant=lambda s: (_ for _ in ()).throw(ValueError('invalid JSON constant')))

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('task'); p.add_argument('claims'); p.add_argument('evidence')
    args = p.parse_args()
    try:
        result = validate(read(args.task), read(args.claims), read(args.evidence))
    except (ValueError, OSError, TypeError) as e:
        print(json.dumps({'error': 'INVALID_INPUT', 'message': str(e), 'version': VERSION}, indent=2))
        return 2
    print(json.dumps(result, indent=2))
    return 0 if all(r['disposition'] in ['SUPPORTED', 'NOT_APPLICABLE'] for r in result['results']) else 1

if __name__ == '__main__':
    sys.exit(main())
