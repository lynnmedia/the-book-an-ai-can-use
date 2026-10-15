"""Run frozen teaching cases and a direct ordinary-script comparator locally."""
import hashlib
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from validate import validate

S=Path(__file__).resolve().parent
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
acceptance=json.loads((S/'acceptance.json').read_text())
out=S/'results'
out.mkdir(exist_ok=True)
records=[]
for name,expected in acceptance['cases'].items():
    paths=[S/'fixtures'/name/f'{x}.json' for x in ['task','claims','evidence']]
    command=[sys.executable,str(S/'validate.py'),*[str(p) for p in paths]]
    result=subprocess.run(command,text=True,capture_output=True)
    (out/f'{name}.stdout.json').write_text(result.stdout)
    (out/f'{name}.stderr.txt').write_text(result.stderr)
    observed=json.loads(result.stdout)
    dispositions=[r['disposition'] for r in observed.get('results',[])]
    ok=dispositions==expected['expected_dispositions'] and result.returncode==expected['expected_exit_code']
    comparator=None
    if result.returncode!=2:
        ordinary=validate(*[json.loads(p.read_text()) for p in paths])
        comparator={'condition':'direct function call to same deterministic code, same files; no package instructions or model','identical_output':ordinary==observed,'finding':'Invocation parity only: both entry points call the same implementation; no independent packaging ablation or user/model benefit test.'}
    records.append({'case':name,'command':command,'returncode':result.returncode,'expected':expected,'observed_dispositions':dispositions,'acceptance_passed':ok,'input_hashes':{p.name:sha(p) for p in paths},'ordinary_script_comparator':comparator})

# A fabricated matching pass is deliberately admissible: a truth-boundary test.
t=json.loads((S/'fixtures/ordinary-a/task.json').read_text())
c=json.loads((S/'fixtures/ordinary-a/claims.json').read_text())
e=json.loads((S/'fixtures/ordinary-a/evidence.json').read_text())
for record in e: record['basis']='Fabricated passed record; no external execution took place.'
forged=validate(t,c,e)
(out/'forged-pass-boundary.json').write_text(json.dumps({'synthetic_input':e,'actual_result':forged,'expected':'SUPPORTED because this mechanism cannot authenticate truth','observed_as_expected':all(x['disposition']=='SUPPORTED' for x in forged['results'])},indent=2)+'\n')

# Selection boundary: supplied failures not cited by the claim do not count.
import copy
selection_e = copy.deepcopy(e)
extra = copy.deepcopy(selection_e[0])
extra['id'] = 'uncited-failure'
extra['outcome'] = 'failed'
selection_e.append(extra)
selection_result = validate(t, c, selection_e)
selection_ok = all(x['disposition'] == 'SUPPORTED' for x in selection_result['results'])
(out/'uncited-failure-boundary.json').write_text(json.dumps({
    'synthetic_input': selection_e,
    'actual_result': selection_result,
    'observed_as_expected': selection_ok,
    'interpretation': 'Selection completeness is not authenticated.'
}, indent=2)+'\n')

report={'observed_at_utc':datetime.now(timezone.utc).isoformat(),'research_cutoff_local':'2026-10-14','runtime':sys.version,'platform':platform.platform(),'model':'NONE','network_calls':0,'acceptance_sha256':sha(S/'acceptance.json'),'implementation_sha256':sha(S/'validate.py'),'contract_sha256':sha(S/'CONTRACT.md'),'cases':records,'passed':sum(r['acceptance_passed'] for r in records),'total':len(records),'uncited_failure_boundary_observed': selection_ok,'truth_boundary_observed':all(x['disposition']=='SUPPORTED' for x in forged['results']),'interpretation':'Deterministic contract cases; no stochastic model trials, evaluator independence, general benchmark or comparative user-effort claim. Cost and latency not measured.'}
(out/'execution-record.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'passed':report['passed'],'total':report['total'],'truth_boundary_observed':report['truth_boundary_observed'],'uncited_failure_boundary_observed':selection_ok},indent=2))
sys.exit(0 if all(r['acceptance_passed'] for r in records) and report['truth_boundary_observed'] and selection_ok else 1)
