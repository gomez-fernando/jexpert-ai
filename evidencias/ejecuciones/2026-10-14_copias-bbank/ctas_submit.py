"""Lanza las 11 copias de BBank autorizadas por el usuario el 2026-10-14 en la sandbox dev.

Usa la API de Query Service (asíncrona) para que las 11 esperen en cola a la vez.
Antes de lanzar cada una comprueba que no existe ya un dataset con ese nombre.
"""
import json
import sys
from pathlib import Path

from aep import aep_get, aep_request, load_config

SANDBOX = 'dev'
OUT = Path(__file__).with_name('ctas_ids.json')

COPIES = [
    ('fdg_tfm_bbank_profiledata', 'Training_Bbank_ProfileData_sch_AbelPerez', 'bbank_democja_bcr_profiledata',
     '_valuelabemeaptrsd, consents, homeAddress, mobilePhone, person, personID, personalEmail'),
    ('fdg_tfm_bbank_applications', 'Training_Bbank_Application', 'bbank_democja_bcr_applications',
     '_id, _valuelabemeaptrsd, identityMap, timestamp'),
    ('fdg_tfm_bbank_fulfillment', 'Training_Bbank_Fulfillment_v2', 'bbank_democja_bcr_fulfillment',
     '_id, _valuelabemeaptrsd, eventMergeId, timestamp'),
    ('fdg_tfm_bbank_webinteractions', 'Training_BBank_WebInteractions6_sch_AbelPerez', 'bbank_democja_bcr_webinteractions',
     '_id, _valuelabemeaptrsd, eventType, identityMap, timestamp'),
    ('fdg_tfm_bbank_bankaccount', 'Training_BBank_BankAccount_sch_AbelPerez', 'bbank_bankaccount_demo_bc',
     '_valuelabemeaptrsd, personID'),
    ('fdg_tfm_bbank_loyalty', 'Training_BBank_Loyalty_sch_AbelPerez', 'training_bbank_loyalty_ds_abelperez',
     'loyalty, personID'),
    ('fdg_tfm_bbank_atmtransactions', 'Training_BBank_ATM_Transactions_sch_AbelPerez', 'training_bbank_atmtransactions_ds_abelperez',
     '_id, _valuelabemeaptrsd, timestamp'),
    ('fdg_tfm_bbank_productinteractions', 'Training_BBank_ProductsTransactions_sch_AbelPerez', 'training_bbank_productinteractions_ds',
     '_id, _valuelabemeaptrsd, eventType, timestamp'),
    ('fdg_tfm_bbank_products', 'Training_BBank_Products_sch_AbelPerez', 'training_bbank_products_ds_abelperez',
     'productCategoryName, productID, productName'),
    ('fdg_tfm_bbank_atminfo', 'Training_BBank_ATMInfo_sch_AbelPerez', 'training_bbank_atminfo_ds_abelperez',
     '_valuelabemeaptrsd, atmAddress, atmID, isAtmActive'),
    ('fdg_tfm_bbank_propensity', 'BBANK_Propensity', 'bbank_propensity_ds',
     '_valuelabemeaptrsd, person, personalEmail'),
]

cfg = load_config(sandbox=SANDBOX)
assert cfg.sandbox_name == 'dev' and cfg.db_name == 'dev:all', (cfg.sandbox_name, cfg.db_name)

submitted = json.loads(OUT.read_text(encoding='utf-8')) if OUT.exists() else {}
for name, schema, source, cols in COPIES:
    if name in submitted:
        print(name, 'ya lanzada antes:', submitted[name]['id'])
        continue
    existing = aep_get('/data/foundation/catalog/dataSets', params={'property': f'name=={name}', 'properties': 'name'},
                       sandbox=SANDBOX)
    if existing:
        print(name, 'YA EXISTE como dataset, no se lanza:', list(existing))
        continue
    sql = f"CREATE TABLE {name} WITH (schema='{schema}') AS (SELECT {cols} FROM {source})"
    r = aep_request('POST', '/data/foundation/query/queries', sandbox=SANDBOX, json_body={
        'dbName': cfg.db_name,
        'sql': sql,
        'name': name,
        'description': 'Copia de BBank para el TFM',
    }).json()
    submitted[name] = {'id': r.get('id'), 'state': r.get('state'), 'created': r.get('created'), 'sql': sql}
    OUT.write_text(json.dumps(submitted, indent=2, ensure_ascii=False), encoding='utf-8')
    print(name, '->', r.get('id'), r.get('state'))

print('Lanzadas:', len(submitted), 'en la sandbox', cfg.sandbox_name, file=sys.stderr)
