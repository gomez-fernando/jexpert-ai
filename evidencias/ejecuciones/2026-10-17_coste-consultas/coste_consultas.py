"""Coste de Data Distiller de las consultas del TFM en la sandbox dev, sacado del registro de consultas.

Solo lee el registro de consultas. No imprime ningún valor de la configuración ni de las credenciales,
ni los campos clientId o userId de las consultas.
"""
from collections import defaultdict
from datetime import datetime, timezone

from aep import aep_get

SANDBOX = 'dev'
DESDE = '2026-10-10T00:00:00Z'
PATRON = 'fdg_tfm_bbank'


def ahora() -> str:
    return datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')


def texto(q: dict) -> str:
    # El listado trae el SQL en effectiveSQL; sql puede venir vacío o no venir.
    return q.get('effectiveSQL') or q.get('sql') or ''


def tipo(sql: str) -> str:
    inicio = sql.lstrip().upper()
    if inicio.startswith(('CREATE TABLE', 'INSERT')):
        return 'batch'
    if inicio.startswith(('SELECT', 'WITH')):
        return 'lectura'
    return 'otra'


def horas(q: dict) -> float | None:
    metrics = q.get('computeMetrics') or {}
    return metrics.get('clusterVMHours')


print(f'Inicio: {ahora()}', flush=True)

consultas = {}
path = '/data/foundation/query/queries'
params = {'limit': 500, 'orderby': '+created', 'property': f'created>={DESDE}'}
pagina = 0
while path and pagina < 200:
    pagina += 1
    page = aep_get(path, params=params, sandbox=SANDBOX)
    nuevas = [q for q in page.get('queries', []) if q['id'] not in consultas]
    for q in nuevas:
        consultas[q['id']] = q
    ultima = nuevas[-1].get('created', '')[:19] if nuevas else '-'
    print(f'Página {pagina}: {len(nuevas)} nuevas, {len(consultas)} en total, última {ultima}', flush=True)
    if not nuevas:
        break
    path = ((page.get('_links') or {}).get('next') or {}).get('href')
    params = None
consultas = list(consultas.values())

tfm = [q for q in consultas if PATRON in texto(q).lower()]

for q in tfm:
    if tipo(texto(q)) == 'batch' and horas(q) is None:
        q.update(aep_get(f"/data/foundation/query/queries/{q['id']}", sandbox=SANDBOX))

print(f'\nConsultas en {SANDBOX} desde {DESDE}: {len(consultas)}. Del TFM ({PATRON}): {len(tfm)}\n')
for q in tfm:
    if tipo(texto(q)) == 'lectura':
        continue
    h = horas(q)
    sql = ' '.join(texto(q).split())[:60]
    print(f"{q.get('created', '')[:19]}  {q['id']}  {q.get('state', ''):<9} {q.get('client', ''):<18} "
          f"{'-' if h is None else f'{h:.4f}':>7}  {sql}")

resumen = defaultdict(lambda: {'n': 0, 'con_horas': 0, 'horas': 0.0})
for q in tfm:
    r = resumen[(tipo(texto(q)), q.get('state', ''))]
    r['n'] += 1
    h = horas(q)
    if h is not None:
        r['con_horas'] += 1
        r['horas'] += h

print('\nTipo     Estado     Consultas  Con horas  clusterVMHours')
for (t, estado), r in sorted(resumen.items()):
    print(f"{t:<8} {estado:<10} {r['n']:>9}  {r['con_horas']:>9}  {r['horas']:>14.4f}")
print(f"\nTotal clusterVMHours: {sum(r['horas'] for r in resumen.values()):.4f}")
print(f'Fin: {ahora()}')
