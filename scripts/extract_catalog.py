"""Catálogo de atributos de una sandbox de AEP para la skill de viabilidad de audiencias.

Por defecto perfila los datasets cuyo nombre casa con --datasets y deja en --out-dir:

  catalogo.csv         un atributo por fila, con cobertura, valores, rangos y percentiles
  datasets.csv         un dataset por fila, con filas, clientes, ventana de datos y cargas
  relaciones.csv       cruces entre datasets y cuántos valores encuentran en el destino
  eventos_por_mes.csv  eventos y clientes por mes de cada dataset de eventos
  catalogo.md          el mismo catálogo en formato para leer
  extraccion.json      fecha, hora de inicio y fin en UTC, sandbox, base de clientes y errores.
                       Con la hora se localizan sus consultas en el registro de Query Service

Si existe notas.csv en la carpeta que contiene --out-dir, sus columnas significado_nulo y notas
pasan al catálogo. Las filas de notas.csv sin ruta son notas del dataset.

Con --full-inventory, en lugar del catálogo, hace el inventario de todos los datasets de la sandbox.

Solo hace lecturas: llamadas GET a las APIs de Platform y consultas SELECT en Query Service.
"""
import argparse
import csv
import json
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import quote

import psycopg2
from psycopg2.extras import RealDictCursor

from aep import AEPAPIError, aep_get, load_config
from aep.client import open_pg_connection
from aep.config import PROJECT_ROOT

DEFAULT_DATASETS = r'^fdg_tfm_bbank_'
PROFILE_CLASS = 'https://ns.adobe.com/xdm/context/profile'
EVENT_CLASS = 'https://ns.adobe.com/xdm/context/experienceevent'
SCHEMA_ACCEPT = {'Accept': 'application/vnd.adobe.xed-full-desc+json; version=1'}
CATEGORICAL_MAX = 30
PERCENTILES = (0.1, 0.25, 0.5, 0.75, 0.9)
CHUNK = 40
WORKERS = 4
QUERY_TIMEOUT = 900
TECHNICAL = re.compile(r'^(_id|identityMap|_repo\.|extSourceSystemAudit\.|producedBy)')
EMAIL = re.compile(r'email', re.I)
PERSONAL = re.compile(r'firstName|lastName|fullName|email|phone|mobile|street|postal|iban|identityNumber|dni|nif|passport'
                      r'|hash|gaid|ecid', re.I)

ROLE_CUSTOMER_ID = 'identificador de cliente'
ROLE_ID = 'identificador'
ROLE_EVENT_DATE = 'fecha del evento'
ROLE_PERSONAL = 'dato personal'
ROLE_ATTRIBUTE = 'atributo'

_local = threading.local()
_errors = []
_errors_lock = threading.Lock()


def log(*parts):
    print(time.strftime('%H:%M:%S'), *parts, flush=True)


def record_error(where, exc):
    with _errors_lock:
        _errors.append({'donde': where, 'error': str(exc).strip()[:500]})
    log('ERROR', where, str(exc).strip()[:200])


def run_sql(sql):
    """SELECT en Query Service con una conexión por hilo y un reintento si se cae."""
    for attempt in range(2):
        try:
            conn = getattr(_local, 'conn', None)
            if conn is None or conn.closed:
                conn = _local.conn = open_pg_connection(query_timeout=QUERY_TIMEOUT)
                conn.autocommit = True
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql)
                return [dict(r) for r in cur.fetchall()]
        except psycopg2.Error:
            try:
                _local.conn.close()
            except Exception:  # noqa: BLE001
                pass
            _local.conn = None
            if attempt == 1:
                raise
    return []


def col(path):
    return '.'.join(f'`{p}`' for p in path.replace('[]', '').split('.'))


def iso_day(ms):
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).strftime('%Y-%m-%d') if ms else None


def shown(path):
    """Ruta relativa a la raíz del repositorio, para no mostrar la ruta local en los logs."""
    try:
        return path.relative_to(PROJECT_ROOT)
    except ValueError:
        return path


def chunks(items, size):
    return [items[i:i + size] for i in range(0, len(items), size)]


# Catalog y Schema Registry

def list_datasets(properties):
    out, start = {}, 0
    while True:
        page = aep_get('/data/foundation/catalog/dataSets', params={'limit': 100, 'start': start, 'properties': properties})
        out.update(page)
        start += 100
        if len(page) < 100:
            return out


def fetch_schema(schema_id):
    last = None
    for container in ('tenant', 'global'):
        try:
            return aep_get(f'/data/foundation/schemaregistry/{container}/schemas/{quote(schema_id, safe="")}',
                           headers=SCHEMA_ACCEPT, timeout=120)
        except AEPAPIError as exc:
            last = exc
    raise last


def schema_titles(props, prefix='', out=None):
    out = {} if out is None else out
    for name, spec in (props or {}).items():
        path = f'{prefix}.{name}' if prefix else name
        items = spec.get('items') or {}
        if spec.get('type') == 'object' and spec.get('properties'):
            schema_titles(spec['properties'], path, out)
        elif spec.get('type') == 'array' and items.get('properties'):
            schema_titles(items['properties'], path + '[]', out)
        else:
            key = path + '[]' if spec.get('type') == 'array' else path
            out[key] = {'title': spec.get('title'), 'description': spec.get('description')}
    return out


def observed_fields(props, prefix=''):
    for name, spec in (props or {}).items():
        path = f'{prefix}.{name}' if prefix else name
        kind = spec.get('type')
        items = spec.get('items') or {}
        if kind == 'object' and spec.get('properties'):
            yield from observed_fields(spec['properties'], path)
        elif kind == 'object':
            continue
        elif kind == 'array':
            yield {'path': path + '[]', 'type': 'array<object>' if items.get('properties') else f"array<{items.get('type')}>"}
        else:
            yield {'path': path, 'type': kind + (f":{spec['format']}" if spec.get('format') else '')}


def schema_descriptors(doc):
    schema_id = doc.get('$id')
    identities, relations = [], []
    for d in doc.get('meta:descriptors') or []:
        if d.get('xdm:sourceSchema') not in (None, schema_id):
            continue
        path = (d.get('xdm:sourceProperty') or '').strip('/').replace('/', '.')
        if d.get('@type') == 'xdm:descriptorIdentity':
            identities.append({'path': path, 'ns': d.get('xdm:namespace'), 'primary': bool(d.get('xdm:isPrimary'))})
        elif d.get('@type') == 'xdm:descriptorOneToOne':
            dest = (d.get('xdm:destinationProperty') or '').strip('/').replace('/', '.') or None
            relations.append({'path': path, 'dest_schema': d.get('xdm:destinationSchema'), 'dest_path': dest})
    identities.sort(key=lambda x: not x['primary'])
    return identities, relations


def batch_info(dataset_id):
    page = aep_get('/data/foundation/catalog/batches',
                   params={'dataSet': dataset_id, 'limit': 100, 'orderBy': 'desc:created', 'properties': 'status,created'})
    created = sorted(b.get('created') or 0 for b in page.values() if b.get('status') == 'success')
    return {'loads': f'{len(created)}+' if len(page) == 100 else str(len(created)),
            'first_load': iso_day(created[0]) if created and len(page) < 100 else None,
            'last_load': iso_day(created[-1]) if created else None}


def kind_of(schema_class):
    return {PROFILE_CLASS: 'perfil', EVENT_CLASS: 'evento'}.get(schema_class, 'tabla de apoyo')


# Catálogo

def load_datasets(pattern):
    names = list_datasets('name,dataIngested,tags')
    selected = sorted((i for i, d in names.items() if pattern.search(d.get('name') or '')), key=lambda i: names[i]['name'])
    schemas, datasets = {}, []
    for dataset_id in selected:
        d = aep_get(f'/data/foundation/catalog/dataSets/{dataset_id}',
                    params={'properties': 'name,schemaRef,tags,classification,observableSchema,dataIngested'})[dataset_id]
        table = ((d.get('tags') or {}).get('adobe/pqs/table') or [None])[0]
        if not table:
            log('Sin tabla en Query Service, se omite:', d.get('name'))
            continue
        schema_id = (d.get('schemaRef') or {}).get('id')
        if schema_id not in schemas:
            schemas[schema_id] = fetch_schema(schema_id)
        doc = schemas[schema_id]
        identities, relations = schema_descriptors(doc)
        datasets.append({
            'id': dataset_id,
            'name': d['name'],
            'table': table,
            'schema_id': schema_id,
            'schema_title': doc.get('title'),
            'class': doc.get('meta:class'),
            'kind': kind_of(doc.get('meta:class')),
            'profile_enabled': any(str(t) == 'enabled:true' for t in (d.get('tags') or {}).get('unifiedProfile') or []),
            'fields': list(observed_fields((d.get('observableSchema') or {}).get('properties'))),
            'titles': schema_titles(doc.get('properties')),
            'identities': identities,
            'relations': relations,
            **batch_info(dataset_id),
        })
        log('Metadatos:', d['name'])
    return datasets


def count_rows(ds):
    window = ', cast(min(timestamp) as string) as desde, cast(max(timestamp) as string) as hasta' if ds['kind'] == 'evento' else ''
    try:
        row = run_sql(f'select count(1) as n{window} from {ds["table"]}')[0]
    except Exception as exc:  # noqa: BLE001
        record_error(f'{ds["name"]} filas', exc)
        row = {'n': 0}
    ds['rows'] = int(row['n'])
    ds['window_from'] = (row.get('desde') or '')[:10] or None
    ds['window_to'] = (row.get('hasta') or '')[:10] or None
    return ds


def choose_customer_base(datasets):
    candidates = [d for d in datasets if d['kind'] == 'perfil' and any(i['primary'] for i in d['identities'])]
    if not candidates:
        return None, None
    base = max(candidates, key=lambda d: d['rows'])
    return base, next(i for i in base['identities'] if i['primary'])['ns']


def assign_roles(ds, customer_ns):
    identity_paths = {i['path']: i['ns'] for i in ds['identities']}
    ds['key'] = next((i['path'] for i in ds['identities'] if i['ns'] == customer_ns and customer_ns), None)
    fields = []
    for f in ds['fields']:
        path = f['path']
        if TECHNICAL.search(path) or f['type'] == 'array<object>':
            continue
        if path in identity_paths:
            role = ROLE_CUSTOMER_ID if identity_paths[path] == customer_ns else ROLE_ID
        elif ds['kind'] == 'evento' and path == 'timestamp':
            role = ROLE_EVENT_DATE
        elif ds['kind'] != 'tabla de apoyo' and PERSONAL.search(path) and not path.startswith('consents.'):
            role = ROLE_PERSONAL
        elif path == 'eventMergeId':
            continue
        else:
            role = ROLE_ATTRIBUTE
        title = (ds['titles'].get(path) or {}).get('title')
        fields.append({**f, 'role': role, 'title': title})
    ds['fields'] = fields


def scalar_exprs(f, k, key):
    c = col(f['path'])
    base_type = f['type'].split(':')[0]
    exprs = [f'count({c}) as n{k}', f'count(distinct {c}) as d{k}']
    if key:
        exprs.append(f'count(distinct case when {c} is not null then {col(key)} end) as c{k}')
    if f['role'] in (ROLE_ATTRIBUTE, ROLE_EVENT_DATE) and (base_type in ('integer', 'number') or f['type'] in ('string:date', 'string:date-time')):
        exprs += [f'cast(min({c}) as string) as mn{k}', f'cast(max({c}) as string) as mx{k}']
    if f['role'] == ROLE_ATTRIBUTE and base_type in ('integer', 'number'):
        exprs.append(f'percentile_approx({c}, array({", ".join(str(p) for p in PERCENTILES)})) as p{k}')
    return exprs


def store_scalar(f, row, k):
    f['non_null'] = int(row.get(f'n{k}') or 0)
    f['distinct'] = int(row.get(f'd{k}') or 0)
    f['customers'] = int(row[f'c{k}']) if row.get(f'c{k}') is not None else None
    f['min'] = row.get(f'mn{k}')
    f['max'] = row.get(f'mx{k}')
    f['percentiles'] = row.get(f'p{k}')


def profile_scalars(ds, fields):
    for part in chunks(fields, CHUNK):
        exprs = [e for k, f in enumerate(part) for e in scalar_exprs(f, k, ds['key'])]
        try:
            row = run_sql(f'select {", ".join(exprs)} from {ds["table"]}')[0]
            for k, f in enumerate(part):
                store_scalar(f, row, k)
        except Exception:  # noqa: BLE001
            for f in part:
                try:
                    store_scalar(f, run_sql(f'select {", ".join(scalar_exprs(f, 0, ds["key"]))} from {ds["table"]}')[0], 0)
                except Exception as exc:  # noqa: BLE001
                    record_error(f'{ds["name"]} {f["path"]}', exc)


def profile_arrays(ds, fields):
    key = ds['key']
    for f in fields:
        c = col(f['path'])
        customers = f', count(distinct case when size({c}) > 0 then {col(key)} end) as c' if key else ''
        try:
            row = run_sql(f'select count(case when size({c}) > 0 then 1 end) as n{customers} from {ds["table"]}')[0]
            f['non_null'] = int(row['n'] or 0)
            f['customers'] = int(row['c']) if row.get('c') is not None else None
            f['distinct'] = int(run_sql(f'select count(distinct v) as d from (select explode({c}) as v from {ds["table"]}) x')[0]['d'] or 0)
        except Exception as exc:  # noqa: BLE001
            record_error(f'{ds["name"]} {f["path"]}', exc)


def profile_values(ds, fields):
    key = ds['key']
    customers = f'count(distinct {col(key)})' if key else 'cast(null as bigint)'
    for part in chunks(fields, 15):
        parts = []
        for f in part:
            c = col(f['path'])
            if f['path'].endswith('[]'):
                k = f', {col(key)} as k' if key else ''
                cust = 'count(distinct k)' if key else 'cast(null as bigint)'
                parts.append(f"select '{f['path']}' as f, cast(v as string) as v, count(1) as n, {cust} as c "
                             f"from (select explode({c}) as v{k} from {ds['table']}) x group by 2")
            else:
                parts.append(f"select '{f['path']}' as f, cast({c} as string) as v, count(1) as n, {customers} as c "
                             f"from {ds['table']} where {c} is not null group by 2")
        try:
            rows = run_sql(' union all '.join(parts))
        except Exception as exc:  # noqa: BLE001
            record_error(f'{ds["name"]} valores', exc)
            continue
        by_path = {f['path']: f for f in part}
        for r in rows:
            values = by_path[r['f']].setdefault('values', {})
            values[r['v']] = {'filas': int(r['n']), 'clientes': int(r['c']) if r['c'] is not None else None}


def profile_months(ds):
    key = ds['key']
    customers = f', count(distinct {col(key)}) as c' if key else ''
    rows = run_sql(f"select date_format(timestamp, 'yyyy-MM') as m, count(1) as n{customers} from {ds['table']} "
                   f"where timestamp is not null group by 1 order by 1")
    ds['months'] = [{'mes': r['m'], 'eventos': int(r['n']), 'clientes': int(r['c']) if r.get('c') is not None else None} for r in rows]


def profile_dataset(ds):
    try:
        if ds['key']:
            row = run_sql(f'select count(distinct {col(ds["key"])}) as c, count({col(ds["key"])}) as n from {ds["table"]}')[0]
            ds['customers'], ds['rows_with_customer'] = int(row['c']), int(row['n'])
        else:
            ds['customers'] = ds['rows_with_customer'] = None
        profile_scalars(ds, [f for f in ds['fields'] if not f['path'].endswith('[]')])
        profile_arrays(ds, [f for f in ds['fields'] if f['path'].endswith('[]')])
        categorical = [f for f in ds['fields'] if f['role'] == ROLE_ATTRIBUTE and 0 < (f.get('distinct') or 0) <= CATEGORICAL_MAX
                       and f['type'].split(':')[0] in ('string', 'boolean', 'integer', 'array<string>', 'array<integer>')]
        profile_values(ds, categorical)
        if ds['kind'] == 'evento':
            profile_months(ds)
    except Exception as exc:  # noqa: BLE001
        record_error(ds['name'], exc)
    log('Perfilado:', ds['name'], f'({len(ds["fields"])} campos)')
    return ds


def overlap(src_table, src_path, dst_table, dst_path, lower=False):
    def norm(path):
        expr = f'trim(cast({col(path)} as string))'
        return f'lower({expr})' if lower else expr
    sql = (f'select count(distinct s.id) as ids, count(distinct r.id) as found '
           f'from (select {norm(src_path)} as id from {src_table} where {col(src_path)} is not null) s '
           f'left join (select distinct {norm(dst_path)} as id from {dst_table} where {col(dst_path)} is not null) r '
           f'on s.id = r.id')
    row = run_sql(sql)[0]
    return int(row['ids'] or 0), int(row['found'] or 0)


def build_relations(datasets, base):
    by_schema = {}
    for d in datasets:
        by_schema.setdefault(d['schema_id'], []).append(d)
    observed = {d['name']: {f['path'] for f in d['fields']} for d in datasets}
    todo = []
    if base:
        base_ns = {i['ns']: i['path'] for i in base['identities']}
        for d in datasets:
            if d is base:
                continue
            if d['key']:
                todo.append((d, d['key'], base, base['key'], 'cliente'))
            else:
                for i in d['identities']:
                    if i['ns'] in base_ns and i['path'] in observed[d['name']]:
                        todo.append((d, i['path'], base, base_ns[i['ns']], f'identidad compartida ({i["ns"]})'))
        base_email = next((i['path'] for i in base['identities'] if (i['ns'] or '').lower() == 'email'), None)
        if base_email:
            for d in datasets:
                taken = {t[1] for t in todo if t[0] is d}
                for f in d['fields']:
                    if (d is not base and EMAIL.search(f['path']) and 'hash' not in f['path'].lower()
                            and f['type'].startswith('string') and f['path'] not in taken):
                        todo.append((d, f['path'], base, base_email, 'email'))
    for d in datasets:
        for rel in d['relations']:
            if rel['path'] not in observed[d['name']]:
                continue
            for target in by_schema.get(rel['dest_schema'], []):
                dest = rel['dest_path'] or next((i['path'] for i in target['identities'] if i['primary']), None)
                if dest and dest in observed[target['name']] and target is not d:
                    todo.append((d, rel['path'], target, dest, 'relación del schema'))

    def run(item):
        src, src_path, dst, dst_path, kind = item
        try:
            ids, found = overlap(src['table'], src_path, dst['table'], dst_path, lower=kind == 'email')
        except Exception as exc:  # noqa: BLE001
            record_error(f'cruce {src["name"]}.{src_path} -> {dst["name"]}.{dst_path}', exc)
            ids = found = None
        return {'origen': src['name'], 'campo_origen': src_path, 'destino': dst['name'], 'campo_destino': dst_path,
                'tipo': kind, 'valores_distintos': ids, 'encontrados': found,
                'pct_encontrados': round(100 * found / ids, 1) if ids else None}

    with ThreadPoolExecutor(WORKERS) as pool:
        return list(pool.map(run, todo))


def load_notes(path):
    notes = {}
    if path.exists():
        with path.open(encoding='utf-8', newline='') as fh:
            for r in csv.DictReader(fh):
                notes[(r.get('dataset') or '', r.get('ruta') or '')] = r
    return notes


def pct(part, total):
    return round(100 * part / total, 1) if part is not None and total else None


def values_text(values, field):
    if not values:
        return ''
    ordered = sorted(values.items(), key=lambda kv: -(kv[1][field] or 0))
    return '; '.join(f'{str(v).replace(";", ",")}={n[field]}' for v, n in ordered if n[field] is not None)


def write_csv(path, rows, header):
    with path.open('w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=header)
        w.writeheader()
        w.writerows(rows)


def fmt_int(n):
    return '' if n is None else f'{n:,}'.replace(',', '.')


def fmt_pct(p):
    return '' if p is None else f'{p:.1f} %'.replace('.', ',')


def fmt_num(x):
    if x is None:
        return ''
    x = float(x)
    if not x.is_integer():
        return f'{x:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    return fmt_int(int(x))


def describe_values(f):
    if f['role'] in (ROLE_CUSTOMER_ID, ROLE_ID, ROLE_PERSONAL):
        return f'{fmt_int(f.get("distinct"))} valores distintos, que no se muestran'
    if f.get('values'):
        top = sorted(f['values'].items(), key=lambda kv: -kv[1]['filas'])
        return ', '.join(f'{v} {fmt_int(n["filas"])}' for v, n in top[:12]) + (', …' if len(top) > 12 else '')
    if f.get('min') is not None:
        text = f'De {f["min"][:10] if f["type"].startswith("string") else fmt_num(float(f["min"]))} ' \
               f'a {f["max"][:10] if f["type"].startswith("string") else fmt_num(float(f["max"]))}'
        if f.get('percentiles'):
            text += f', mediana {fmt_num(f["percentiles"][PERCENTILES.index(0.5)])}'
        return text
    return f'{fmt_int(f.get("distinct"))} valores distintos'


def write_catalog(out_dir, datasets, base, customer_ns, relations, notes, meta):
    base_customers = base['customers'] if base else None
    attr_rows, ds_rows, month_rows = [], [], []
    for d in datasets:
        dn = notes.get((d['name'], ''), {})
        ds_rows.append({
            'dataset': d['name'], 'tabla': d['table'], 'clase': d['kind'], 'schema': d['schema_title'],
            'filas': d['rows'], 'clientes': d.get('customers'), 'filas_con_cliente': d.get('rows_with_customer'),
            'campo_cliente': d['key'] or '',
            'identidades': '; '.join(f'{i["path"]}={i["ns"]}{" (primaria)" if i["primary"] else ""}' for i in d['identities']),
            'perfil_habilitado': str(d['profile_enabled']).lower(), 'cargas': d['loads'], 'primera_carga': d['first_load'] or '',
            'ultima_carga': d['last_load'] or '', 'ventana_desde': d['window_from'] or '', 'ventana_hasta': d['window_to'] or '',
            'notas': dn.get('notas', ''),
        })
        for m in d.get('months') or []:
            month_rows.append({'dataset': d['name'], **m})
        for f in d['fields']:
            n = notes.get((d['name'], f['path']), {})
            p = f.get('percentiles')
            attr_rows.append({
                'dataset': d['name'], 'tabla': d['table'], 'clase': d['kind'], 'ruta': f['path'], 'titulo': f['title'] or '',
                'tipo': f['type'], 'rol': f['role'], 'filas': d['rows'], 'filas_con_valor': f.get('non_null'),
                'cobertura_filas_pct': pct(f.get('non_null'), d['rows']), 'clientes_con_valor': f.get('customers'),
                'cobertura_clientes_pct': pct(f.get('customers'), base_customers), 'distintos': f.get('distinct'),
                'minimo': f.get('min') or '', 'maximo': f.get('max') or '',
                'percentiles': '; '.join(f'p{int(q * 100)}={v}' for q, v in zip(PERCENTILES, p)) if p else '',
                'valores_filas': values_text(f.get('values'), 'filas'),
                'valores_clientes': values_text(f.get('values'), 'clientes'),
                'ventana_desde': d['window_from'] or '', 'ventana_hasta': d['window_to'] or '',
                'ultima_carga': d['last_load'] or '',
                'significado_nulo': n.get('significado_nulo', ''), 'notas': n.get('notas', ''),
            })

    write_csv(out_dir / 'catalogo.csv', attr_rows, list(attr_rows[0]) if attr_rows else ['dataset'])
    write_csv(out_dir / 'datasets.csv', ds_rows, list(ds_rows[0]) if ds_rows else ['dataset'])
    write_csv(out_dir / 'relaciones.csv', relations, ['origen', 'campo_origen', 'destino', 'campo_destino', 'tipo',
                                                      'valores_distintos', 'encontrados', 'pct_encontrados'])
    write_csv(out_dir / 'eventos_por_mes.csv', month_rows, ['dataset', 'mes', 'eventos', 'clientes'])

    md = ['# Catálogo de atributos', '',
          f'Extraído el {meta["fecha"]} de la sandbox `{meta["sandbox"]}` con `scripts/extract_catalog.py`, '
          f'sobre los datasets cuyo nombre casa con `{meta["datasets"]}`.', '']
    if base:
        md += [f'La base de clientes es `{base["name"]}`, con {fmt_int(base_customers)} clientes identificados por '
               f'`{base["key"]}` en el namespace `{customer_ns}`. La cobertura por clientes se calcula sobre esa base.', '']
    md += ['## Datasets', '', '| Dataset | Clase | Filas | Clientes | Ventana de datos | Última carga | Notas |', '| --- | --- | --- | --- | --- | --- | --- |']
    for r in ds_rows:
        window = f'{r["ventana_desde"]} a {r["ventana_hasta"]}' if r['ventana_desde'] else ''
        md.append(f'| `{r["dataset"]}` | {r["clase"]} | {fmt_int(r["filas"])} | {fmt_int(r["clientes"])} | {window} | '
                  f'{r["ultima_carga"]} | {r["notas"]} |')
    md += ['', '## Cruces entre datasets', '', '| Origen | Campo | Destino | Campo de destino | Valores | Encontrados |', '| --- | --- | --- | --- | --- | --- |']
    for r in relations:
        md.append(f'| `{r["origen"]}` | `{r["campo_origen"]}` | `{r["destino"]}` | `{r["campo_destino"]}` | '
                  f'{fmt_int(r["valores_distintos"])} | {fmt_int(r["encontrados"])} ({fmt_pct(r["pct_encontrados"])}) |')
    for d in datasets:
        md += ['', f'## Atributos de `{d["name"]}`', '',
               '| Atributo | Ruta | Rol | Cobertura en filas | Cobertura en clientes | Valores | Notas |', '| --- | --- | --- | --- | --- | --- | --- |']
        for f in d['fields']:
            n = notes.get((d['name'], f['path']), {})
            note = ' '.join(x for x in (n.get('significado_nulo'), n.get('notas')) if x)
            md.append(f'| {f["title"] or ""} | `{f["path"]}` | {f["role"]} | {fmt_pct(pct(f.get("non_null"), d["rows"]))} | '
                      f'{fmt_pct(pct(f.get("customers"), base_customers))} | {describe_values(f)} | {note} |')
    (out_dir / 'catalogo.md').write_text('\n'.join(md) + '\n', encoding='utf-8')


def utc_now():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def build_catalog(pattern_text, out_dir, sandbox):
    started, started_utc = time.time(), utc_now()
    datasets = load_datasets(re.compile(pattern_text))
    if not datasets:
        sys.exit(f'Ningún dataset con tabla en Query Service casa con {pattern_text}')
    with ThreadPoolExecutor(WORKERS) as pool:
        datasets = list(pool.map(count_rows, datasets))
    for d in [d for d in datasets if not d['rows']]:
        log('Sin filas, se omite:', d['name'])
    datasets = [d for d in datasets if d['rows']]
    if not datasets:
        sys.exit(f'Ningún dataset con filas casa con {pattern_text}')
    base, customer_ns = choose_customer_base(datasets)
    log('Base de clientes:', base['name'] if base else 'ninguna', customer_ns or '')
    for d in datasets:
        assign_roles(d, customer_ns)
    with ThreadPoolExecutor(WORKERS) as pool:
        datasets = list(pool.map(profile_dataset, datasets))
    relations = build_relations(datasets, base)
    notes = load_notes(out_dir.parent / 'notas.csv')
    meta = {'fecha': date.today().isoformat(), 'sandbox': sandbox, 'datasets': pattern_text,
            'base_clientes': base['name'] if base else None, 'campo_cliente': base['key'] if base else None,
            'namespace_cliente': customer_ns, 'datasets_perfilados': [d['name'] for d in datasets],
            'inicio_utc': started_utc, 'fin_utc': utc_now(), 'segundos': round(time.time() - started), 'errores': _errors}
    write_catalog(out_dir, datasets, base, customer_ns, relations, notes, meta)
    (out_dir / 'extraccion.json').write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding='utf-8')
    log('Catálogo en', shown(out_dir), '| datasets:', len(datasets), '| errores:', len(_errors))


# Inventario completo

def count_objects():
    counts = {}
    try:
        n, params = 0, {'limit': 300}
        while True:
            page = aep_get('/data/foundation/schemaregistry/tenant/schemas', params=params,
                           headers={'Accept': 'application/vnd.adobe.xed-id+json'})
            n += len(page.get('results') or [])
            nxt = (page.get('_page') or {}).get('next')
            if not nxt:
                break
            params['start'] = nxt
        counts['schemas_propios'] = n
    except Exception as exc:  # noqa: BLE001
        record_error('schemas', exc)
    for key, path, params, size in [
        ('namespaces', '/data/core/idnamespace/identities', None, len),
        ('politicas_de_fusion', '/data/core/ups/config/mergePolicies', {'limit': 100}, lambda r: len(r.get('children') or [])),
        ('audiencias', '/data/core/ups/segment/definitions', {'limit': 1}, lambda r: (r.get('page') or {}).get('totalCount')),
    ]:
        try:
            counts[key] = size(aep_get(path, params=params))
        except Exception as exc:  # noqa: BLE001
            record_error(key, exc)
    return counts


def build_inventory(out_dir, sandbox):
    started, started_utc = time.time(), utc_now()
    datasets = list_datasets('name,schemaRef,tags,classification,created,createdClient,dataIngested')
    log('Datasets en la sandbox:', len(datasets))

    def count(item):
        dataset_id, d = item
        table = ((d.get('tags') or {}).get('adobe/pqs/table') or [None])[0]
        res = {}
        if table and d.get('dataIngested'):
            events = (d.get('classification') or {}).get('dataBehavior') == 'time-series'
            window = ', cast(min(timestamp) as string) as desde, cast(max(timestamp) as string) as hasta' if events else ''
            try:
                res = run_sql(f'select count(1) as n{window} from {table}')[0]
            except Exception:  # noqa: BLE001
                try:
                    res = run_sql(f'select count(1) as n from {table}')[0]
                except Exception as exc:  # noqa: BLE001
                    res = {'error': str(exc).strip()[:300]}
        return {
            'dataset': d.get('name'), 'tabla': table or '', 'id': dataset_id,
            'comportamiento': (d.get('classification') or {}).get('dataBehavior') or '',
            'creado': iso_day(d.get('created')) or '', 'cliente_creador': d.get('createdClient') or '',
            'perfil_habilitado': str(any(str(t) == 'enabled:true' for t in (d.get('tags') or {}).get('unifiedProfile') or [])).lower(),
            'con_datos': str(bool(d.get('dataIngested'))).lower(), 'filas': res.get('n', ''),
            'ventana_desde': (res.get('desde') or '')[:10], 'ventana_hasta': (res.get('hasta') or '')[:10],
            'schema': (d.get('schemaRef') or {}).get('id') or '', 'error': res.get('error', ''),
        }

    rows = []
    with ThreadPoolExecutor(WORKERS) as pool:
        for i, r in enumerate(pool.map(count, datasets.items()), 1):
            rows.append(r)
            if i % 50 == 0:
                log('Contados', i, 'de', len(datasets))
    rows.sort(key=lambda r: (r['dataset'] or '').lower())
    write_csv(out_dir / 'inventario.csv', rows, list(rows[0]) if rows else ['dataset'])
    summary = {'fecha': date.today().isoformat(), 'sandbox': sandbox, 'datasets': len(rows),
               'datasets_con_datos': sum(1 for r in rows if r['con_datos'] == 'true'),
               'datasets_con_perfil': sum(1 for r in rows if r['perfil_habilitado'] == 'true'),
               'filas': sum(int(r['filas']) for r in rows if str(r['filas']).isdigit()),
               **count_objects(), 'inicio_utc': started_utc, 'fin_utc': utc_now(),
               'segundos': round(time.time() - started), 'errores': _errors}
    (out_dir / 'inventario.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding='utf-8')
    log('Inventario en', shown(out_dir), '| datasets:', len(rows), '| errores:', len(_errors))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--datasets', help=f'Expresión regular sobre el nombre de los datasets en Catalog. Opcional. '
                                           f'Por defecto, {DEFAULT_DATASETS}. No se combina con --full-inventory.')
    parser.add_argument('--out-dir', help='Carpeta de salida, absoluta o relativa a la raíz del repositorio. Opcional. '
                                          'Por defecto, catalogo/AAAA-MM-DD/ con la fecha del día, o inventario/AAAA-MM-DD/ '
                                          'con --full-inventory.')
    parser.add_argument('--full-inventory', action='store_true',
                        help='Alternativa al comportamiento por defecto: en lugar del catálogo, hace el inventario de todos '
                             'los datasets de la sandbox (filas, ventana de fechas y metadatos) y cuenta schemas, '
                             'namespaces, políticas de fusión y audiencias. Su salida lleva los nombres de todos los '
                             'datasets de la sandbox, por eso su carpeta por defecto está fuera de git.')
    args = parser.parse_args()
    if args.full_inventory and args.datasets:
        parser.error('--datasets y --full-inventory son alternativas: usa solo una.')

    today = date.today().isoformat()
    default_dir = Path('inventario' if args.full_inventory else 'catalogo') / today
    out_dir = Path(args.out_dir) if args.out_dir else default_dir
    out_dir = out_dir if out_dir.is_absolute() else PROJECT_ROOT / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    sandbox = load_config().sandbox_name
    log('Sandbox:', sandbox, '| salida:', shown(out_dir))

    if args.full_inventory:
        build_inventory(out_dir, sandbox)
    else:
        build_catalog(args.datasets or DEFAULT_DATASETS, out_dir, sandbox)


if __name__ == '__main__':
    main()
