"""Espera a que terminen las copias lanzadas con ctas_submit.py. Solo lecturas."""
import json
import time
from pathlib import Path

from aep import aep_get

SANDBOX = 'dev'
FINAL = {'SUCCESS', 'FAILED', 'KILLED', 'CANCELLED'}
ids = json.loads(Path(__file__).with_name('ctas_ids.json').read_text(encoding='utf-8'))

deadline = time.time() + 75 * 60
while True:
    states = {}
    for name, v in ids.items():
        try:
            states[name] = aep_get(f"/data/foundation/query/queries/{v['id']}", sandbox=SANDBOX)
        except Exception as exc:
            states[name] = {'state': f'ERROR_LECTURA {exc}'[:120]}
    summary = {}
    for q in states.values():
        summary[q.get('state')] = summary.get(q.get('state'), 0) + 1
    print(time.strftime('%H:%M:%S'), summary, flush=True)
    if all(q.get('state') in FINAL for q in states.values()) or time.time() > deadline:
        break
    time.sleep(60)

for name, q in states.items():
    errors = [e.get('message', '')[:300] for e in (q.get('errors') or [])]
    print(f"{name:36} {q.get('state'):10} {round((q.get('elapsedTime') or 0) / 1000):>5} s",
          json.dumps(q.get('computeMetrics')) if q.get('computeMetrics') else '', errors or '')
