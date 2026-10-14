"""Comprobaciones sobre el catálogo del 2026-10-14. Solo lecturas, sin imprimir datos personales."""
from aep import query_all

S = 'dev'
A = 'fdg_tfm_bbank_applications'
P = 'fdg_tfm_bbank_profiledata'
st = '`_valuelabemeaptrsd`.`ApplicationDetails`.`Application`.`finalStatus`'
pid = '`_valuelabemeaptrsd`.`ApplicationDetails`.`profileID`'
em = '`_valuelabemeaptrsd`.`ApplicationDetails`.`Email`'

checks = {
    'solicitudes por estado, con y sin cliente': f'select {st} as estado, count(1) as n, count({pid}) as con_cliente from {A} group by 1',
    'emails de solicitudes que están en la base, por estado':
        f'select a.estado, count(distinct a.e) as emails, count(distinct p.e) as en_base, count(distinct p.pid) as clientes '
        f'from (select {st} as estado, lower(trim({em})) as e from {A}) a '
        f'left join (select lower(trim(personalEmail.address)) as e, personID as pid from {P}) p on a.e = p.e group by 1',
    'productos': 'select productID, productName, productCategoryName from fdg_tfm_bbank_products where productID in '
                 "('597-824-395766967583','117-092-615581165598','590-882-735839612672','816-504-258387688508','102-349-853011058806')",
    'filas de fidelización por cliente': 'select n, count(1) as clientes from (select personID, count(1) as n from fdg_tfm_bbank_loyalty group by 1) x group by 1',
    'clientes de fidelización con puntos distintos': 'select count(1) as clientes from (select personID from fdg_tfm_bbank_loyalty group by 1 '
                                                     'having count(distinct loyalty.points) > 1) x',
    'emails web que están en la base': 'select count(distinct w.e) as emails, count(distinct p.pid) as clientes from '
        '(select lower(trim(_valuelabemeaptrsd.transaction_identifiers.emailAddress)) as e from fdg_tfm_bbank_webinteractions '
        'where _valuelabemeaptrsd.transaction_identifiers.profile_id is null and _valuelabemeaptrsd.transaction_identifiers.emailAddress is not null) w '
        f'join (select lower(trim(personalEmail.address)) as e, personID as pid from {P}) p on w.e = p.e',
}
for name, sql in checks.items():
    print(name, query_all(sql, sandbox=S, retries=1, query_timeout=900))
