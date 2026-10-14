"""Comprobaciones de las 11 copias de BBank, las mismas que la de prueba. Solo lecturas.

No imprime filas: profiledata y propensity llevan datos personales (ficticios).
"""
import json
import re
import sys
from pathlib import Path

from aep import aep_get, query_all

SANDBOX = 'dev'
SOURCE_NAMES = {
    'fdg_tfm_bbank_profiledata': 'BBANK_DemoCJA_BCR_ProfileData',
    'fdg_tfm_bbank_applications': 'BBANK_DemoCJA_BCR_Applications',
    'fdg_tfm_bbank_fulfillment': 'BBANK_DemoCJA_BCR_Fulfillment',
    'fdg_tfm_bbank_webinteractions': 'BBANK_DemoCJA_BCR_WebInteractions',
    'fdg_tfm_bbank_bankaccount': 'BBANK_BankAccount_Demo_BC',
    'fdg_tfm_bbank_loyalty': 'Training_BBank_Loyalty_ds_AbelPerez',
    'fdg_tfm_bbank_atmtransactions': 'Training_BBank_ATMTransactions_ds_AbelPerez',
    'fdg_tfm_bbank_productinteractions': 'Training_BBank_ProductInteractions_ds',
    'fdg_tfm_bbank_products': 'Training_BBank_Products_ds_AbelPerez',
    'fdg_tfm_bbank_atminfo': 'Training_BBank_ATMInfo_ds_AbelPerez',
    'fdg_tfm_bbank_propensity': 'BBANK_Propensity_ds',
}
PROPS = 'name,schemaRef,tags,classification,createdClient,created,observableSchema'

ids = json.loads(Path(__file__).with_name('ctas_ids.json').read_text(encoding='utf-8'))
only = set(sys.argv[1:])


def dataset(name):
    r = aep_get('/data/foundation/catalog/dataSets', params={'property': f'name=={name}', 'properties': PROPS},
                sandbox=SANDBOX)
    if len(r) != 1:
        return None, None, len(r)
    k, v = next(iter(r.items()))
    return k, v, 1


def obs_paths(d):
    out = []

    def walk(props, prefix):
        for k, v in (props or {}).items():
            p = f'{prefix}.{k}' if prefix else k
            if v.get('type') == 'object' and v.get('properties'):
                walk(v['properties'], p)
            else:
                out.append((p, v.get('type'), v.get('format')))
    walk((d.get('observableSchema') or {}).get('properties'), '')
    return sorted(out)


results = {}
for name, v in ids.items():
    if only and name not in only:
        continue
    m = re.match(r'CREATE TABLE (\S+) WITH .* AS \(SELECT (.+) FROM (\S+)\)$', v['sql'])
    dst_table, cols, src_table = m.group(1), m.group(2), m.group(3)
    r = {}
    src_id, src, n_src = dataset(SOURCE_NAMES[name])
    dst_id, dst, n_dst = dataset(name)
    if not dst:
        results[name] = {'error': f'copia no encontrada en Catalog ({n_dst} coincidencias)'}
        print(name, results[name], flush=True)
        continue
    r['dataset'] = dst_id
    r['mismo_schema'] = bool(src) and dst['schemaRef']['id'] == src['schemaRef']['id']
    if not src:
        r['aviso_origen'] = f'origen no localizado por nombre ({n_src} coincidencias)'
    tags = dst.get('tags') or {}
    r['perfil'] = tags.get('unifiedProfile')
    r['identidad'] = tags.get('unifiedIdentity')
    r['tabla_qs'] = tags.get('adobe/pqs/table')
    r['clase'] = dst.get('classification', {}).get('dataBehavior')
    r['createdClient'] = dst.get('createdClient')
    if src:
        so, do = obs_paths(src), obs_paths(dst)
        r['campos_iguales'] = so == do
        r['campos'] = (len(so), len(do))
        if so != do:
            r['solo_origen'] = sorted(set(so) - set(do))[:20]
            r['solo_copia'] = sorted(set(do) - set(so))[:20]
    b = aep_get('/data/foundation/catalog/batches', params={'dataSet': dst_id, 'properties': 'status,created'},
                sandbox=SANDBOX)
    r['lotes'] = sorted(x.get('status') for x in b.values())
    counts = query_all(f"select 'origen' as t, count(1) as n from {src_table} union all "
                       f"select 'copia' as t, count(1) as n from {dst_table}", sandbox=SANDBOX, retries=1,
                       query_timeout=900)
    r['filas'] = {c['t']: c['n'] for c in counts}
    for a, z, key in ((dst_table, src_table, 'copia_no_en_origen'), (src_table, dst_table, 'origen_no_en_copia')):
        r[key] = query_all(f'select count(1) as n from (select to_json(struct({cols})) as j from {a} '
                           f'except select to_json(struct({cols})) as j from {z})',
                           sandbox=SANDBOX, retries=1, query_timeout=900)[0]['n']
    results[name] = r
    print(name, json.dumps(r, ensure_ascii=False, default=str), flush=True)

Path(__file__).with_name('ctas_verify.json').write_text(json.dumps(results, indent=2, ensure_ascii=False, default=str),
                                                       encoding='utf-8')
