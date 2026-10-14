# Inventario de la sandbox dev de Jakala

Extracción del 2026-10-10 sobre la sandbox `dev` de la organización de Jakala (tenant `valuelabemeaptrsd`), hecha con el paquete `aep/`. El inventario sale de las APIs de Catalog, Schema Registry, Segmentation, Identity y Profile, y los recuentos y el perfilado de campos, de Query Service.

Los datos extraídos están en `sandbox-dev/`: `datasets.json` con el resumen de los 733 datasets (schema, clase, identidades, lotes y familia), `counts.json` con las filas y la ventana de fechas de cada dataset con datos, y `profile/` con el perfilado por campo de los 64 datasets de BBank, Snowclub y Luma. El perfilado da cobertura, cardinalidad, mínimo y máximo, y la distribución de valores de los campos con 25 valores distintos o menos. De los campos con datos personales (nombre, email, teléfono, dirección, DNI, IBAN e identificadores) no se guardan valores.

## Contenido general

| Elemento | Cantidad |
| --- | --- |
| Datasets | 733, de los que 493 tienen datos |
| Schemas | 644, de los que 412 los usan datasets con datos |
| Field groups | 491 |
| Namespaces de identidad | 248, de los que 211 son propios |
| Políticas de fusión | 19. La de perfil por defecto es `Default Timebased` (`05e1420b-46e3-4cab-a5d4-32803f4ed8b4`) |
| Audiencias | 453, de ellas 327 batch, 60 streaming y 66 edge |
| Perfiles | 97.482 en `profile_snapshot_export_b985eb1c_4167_44f6_8b42_5c59e93c2ee7`, el snapshot de la política por defecto |

La sandbox se usa desde julio de 2024 para formación y pruebas. Mezcla demos con datos ficticios, POC de clientes, ejercicios de alumnos y datasets de sistema.

## Familias de datos

| Familia | Datasets | Con datos | Filas | Valoración |
| --- | --- | --- | --- | --- |
| BBank, banco ficticio | 78 | 66 | 682.462 | Candidata |
| Snowclub, estación de esquí ficticia | 26 | 24 | 10.590 | Descartada |
| Luma, tienda del tutorial de Adobe | 7 | 4 | 2.060 | Descartada |
| POC de clientes (Santander, LaLiga, Real Madrid, Repsol y otros) | 99 | 85 | 71.219.649 | Excluida |
| Ejercicios y pruebas de alumnos | 381 | 203 | 3.228.506 | Sin familia aprovechable |
| Sistema (snapshots de perfil, AJO, Audience Manager) | 142 | 111 | 603.531 | Solo el snapshot de perfil |

En Snowclub cada alumno montó su propio schema y sus propios identificadores, y ningún conjunto pasa de 133 perfiles. Luma tiene 1.003 perfiles con ciudad, género y datos de contacto, 1.000 registros de fidelización con nivel y puntos, 10 productos y 47 eventos web. Las POC de clientes se excluyen porque son datos de proyectos de Jakala, aunque sean de prueba. En los ejercicios de alumnos, las tres tablas grandes (`all_email_events_extended`, `all_interactions_and_feedback` y `combined_interactions_feedback`, con algo más de un millón de filas cada una) salen por Query Service de la POC de Santander, y el resto no pasa de 8.000 filas.

## BBank

Banco ficticio con web propia (`bbank.bmind.es`). Varios alumnos cargaron copias de los mismos datos. La más completa es la línea DemoCJA BCR, cargada el 2026-04-19, con eventos entre el 2025-10-01 y el 2026-07-01. Sus datasets se unen por el namespace `TRBbankProfileID`, que en el snapshot de perfil aparece en 23.396 perfiles. Son más que los 7.730 clientes de la línea BCR porque otras copias cargan identificadores del mismo namespace (sin confirmar).

### Datasets

| Dataset | Tabla | Clase | Filas | Contenido |
| --- | --- | --- | --- | --- |
| `BBANK_DemoCJA_BCR_ProfileData` | `bbank_democja_bcr_profiledata` | Perfil | 7.730 | Clientes con datos personales, ingresos, crédito preaprobado, sucursal, productos y consentimientos |
| `BBANK_DemoCJA_BCR_Applications` | `bbank_democja_bcr_applications` | Evento | 40.414 | Solicitudes de producto con estado y motivo de rechazo |
| `BBANK_DemoCJA_BCR_Fulfillment` | `bbank_democja_bcr_fulfillment` | Evento | 15.577 | Entregas de productos aceptados. No está habilitado para perfil |
| `BBANK_DemoCJA_BCR_WebInteractions` | `bbank_democja_bcr_webinteractions` | Evento | 260.627 | Navegación con UTM y paso del embudo, entre 22.000 y 37.000 eventos al mes |
| `BBANK_BankAccount_Demo_BC` | `bbank_bankaccount_demo_bc` | Perfil | 2.530 | Tipo, saldo y estado de cada cuenta |
| `Training_BBank_Loyalty_ds_AbelPerez` | `training_bbank_loyalty_ds_abelperez` | Perfil | 1.002 | Fecha de alta y puntos de fidelización |
| `Training_BBank_ATMTransactions_ds_AbelPerez` | `training_bbank_atmtransactions_ds_abelperez` | Evento | 1.000 | Operaciones en cajero entre 2006 y 2024 |
| `Training_BBank_ProductInteractions_ds` | `training_bbank_productinteractions_ds` | Evento | 315 | Compra, interés, consulta y renovación de productos |
| `Training_BBank_Products_ds_AbelPerez` | `training_bbank_products_ds_abelperez` | Producto | 44 | Catálogo de productos con nombre y categoría |
| `Training_BBank_Branch_ds_AbelPerez` | `training_bbank_branch_ds_abelperez` | Sucursal | 11 | Sucursales con dirección |
| `Training_BBank_ATMInfo_ds_AbelPerez` | `training_bbank_atminfo_ds_abelperez` | Cajero | 43 | Cajeros con ciudad y estado |
| `BBANK_Propensity_ds` | `bbank_propensity_ds` | Perfil | 100 | Puntuaciones de propensión por producto |

### Cruces entre datasets

| Cruce | Identificadores | Encontrados |
| --- | --- | --- |
| Solicitudes con cliente en `BBANK_DemoCJA_BCR_ProfileData` | 7.354 | 7.354 |
| Entregas con cliente | 7.640 | 7.640 |
| Interacciones web con cliente | 6.782 | 6.782 |
| Entregas con solicitud en `BBANK_DemoCJA_BCR_Applications` | 10.528 | 10.528 |
| Cuentas de `BBANK_BankAccount_Demo_BC` con cliente | 2.530 | 2.525 |
| Fidelización con cliente | 502 | 500 |
| Operaciones de cajero con cliente | 321 | 321 |
| Interacciones con producto con cliente | 55 | 55 |
| Propensión con cliente, por email | 100 | 0 |

En todos los cruces, el cliente es un `personID` de `BBANK_DemoCJA_BCR_ProfileData`. Las 10.528 entregas con solicitud coinciden con las 10.528 solicitudes aceptadas.

### Atributos de `BBANK_DemoCJA_BCR_ProfileData`

| Atributo | Ruta | Cobertura | Valores |
| --- | --- | --- | --- |
| Género | `person.gender` | 100 % | female 3.949, male 3.781 |
| Fecha de nacimiento | `person.birthDate` | 100 % | Del 1925-04-23 al 2005-09-22 |
| Ciudad | `homeAddress.city` | 100 % | 13 ciudades. Bilbao, Madrid, Sevilla, Barcelona y Valencia pasan de 1.000 clientes. "Valencia" (1.068) y "València" (254) son valores distintos |
| Ingresos anuales | `_valuelabemeaptrsd.financialDetail.annualIncome` | 100 % | De 11.110 a 79.991 |
| Crédito preaprobado | `_valuelabemeaptrsd.financialDetail.preapprovedCreditAmount` | 100 % | De 1.501 a 36.300 |
| Sucursal | `_valuelabemeaptrsd.financialDetail.branch_id` | 100 % | 13 códigos. ZAR01, VLC01, MAL01 y OPO01 (819 clientes) no existen en `Training_BBank_Branch_ds_AbelPerez` |
| Alta del primer producto | `_valuelabemeaptrsd.financialDetail.firstProductActivationDate` | 100 % | Del 2005-01-19 al 2026-06-28 |
| Productos | `_valuelabemeaptrsd.financialDetail.product_ids` | 100 % | La lista llega como texto dentro de un único elemento (`['597-824-395766967583']`), así que no se puede filtrar por producto sin tratarla antes |
| Canal preferido | `consents.marketing.preferred` | 100 % | email 6.237, sms 838, push 655 |
| Consentimiento de email | `consents.marketing.email.val` | 32,7 % | y 1.330, n 1.195 |
| Consentimiento de llamada | `consents.marketing.call.val` | 32,7 % | y 1.113, n 1.412 |

Lleva además nombre, apellidos, email, móvil, código postal, DNI e IBAN, todos ficticios, que no entran en el catálogo.

### Atributos de los eventos

| Dataset | Atributo | Ruta | Cobertura | Valores |
| --- | --- | --- | --- | --- |
| Solicitudes | Estado final | `_valuelabemeaptrsd.ApplicationDetails.Application.finalStatus` | 100 % | denied 29.886, accepted 10.528 |
| Solicitudes | Motivo de rechazo | `_valuelabemeaptrsd.ApplicationDetails.Application.rejectionReason` | 73,9 % | high_risk 10.015, fraud_suspected 9.973, incomplete_application 9.898 |
| Solicitudes | Producto | `_valuelabemeaptrsd.ApplicationDetails.productID` | 100 % | 5 productos: Premium Account y Standard Account (ahorro), Bbank Premium Card, Bbank Customized Cash Rewards y Bbank Green Card (tarjetas) |
| Solicitudes | Cliente | `_valuelabemeaptrsd.ApplicationDetails.profileID` | 26,1 % | El resto de solicitudes solo lleva el email y su hash |
| Entregas | Método | `_valuelabemeaptrsd.DetailsOfFulfillment.Fulfillment_.fulfillmentMethod` | 100 % | home 7.907, branch 7.670 |
| Entregas | Estado | `_valuelabemeaptrsd.DetailsOfFulfillment.Fulfillment_.deliveryStatus_` | 100 % | delivered 7.812, pending 7.765 |
| Entregas | Sucursal | `_valuelabemeaptrsd.DetailsOfFulfillment.Fulfillment_.branchID_` | 49,2 % | BAR01, BIL01, MAD01, SEV01 y VAL01 |
| Web | Paso | `eventType` | 100 % | Seis pasos del alta de cuenta (selectAccount, formAccount, conditionsaccountView, processingAccount, confirmAccount y deniedAccount) y siete de la tienda de tarjetas (productList, viewProduct, cartView, checkout, processingCards, purchase y deniedShop) |
| Web | Campaña | `_valuelabemeaptrsd.UTM.campaign` | 100 % | (none) 159.109, black_friday_exclusive, application_recovery_program, january_sales_finance y christmas_savings_plan, con unos 25.000 eventos cada una |
| Web | Medio | `_valuelabemeaptrsd.UTM.medium` | 100 % | cpc, organic, referral, (none), cpa, sms y email |
| Web | Fuente | `_valuelabemeaptrsd.UTM.source` | 100 % | google, facebook, partner, instagram, direct, affiliate y crm |
| Web | Producto | `_valuelabemeaptrsd.transaction_identifiers.product_id` | 32,6 % | Los mismos 5 productos |
| Web | Cliente | `_valuelabemeaptrsd.transaction_identifiers.profile_id` | 28,2 % | |
| Web | Dispositivo | `_valuelabemeaptrsd.Device.deviceType` | 100 % | Solo mobile |
| Cajero | Tipo de operación | `_valuelabemeaptrsd.transactionData.transactionType` | 100 % | cash_withdrawal 341, cash_deposit 243, money_transfer 218, bill_payment 198 |
| Cajero | Importe | `_valuelabemeaptrsd.transactionData.amount` | 100 % | De 52 a 3.000 |
| Producto | Tipo de interacción | `_valuelabemeaptrsd.transactionData.transactionType` | 98,4 % | purchase 88, interest 80, inquiries 70, renewal 68 |

### Atributos de las tablas de apoyo

| Dataset | Atributo | Ruta | Valores |
| --- | --- | --- | --- |
| Cuentas | Tipo | `_valuelabemeaptrsd.BankAccountDetails.accountType` | Checking 1.824, Savings 706 |
| Cuentas | Saldo | `_valuelabemeaptrsd.BankAccountDetails.accountBalance` | De -611,17 a 87.324 |
| Cuentas | Activa | `_valuelabemeaptrsd.BankAccountDetails.isActive` | true 2.521, false 9 |
| Fidelización | Puntos | `loyalty.points` | De 1 a 998 |
| Fidelización | Fecha de alta | `loyalty.joinDate` | Del 2005-05-30 al 2025-07-16 |
| Productos | Categoría | `productCategoryName` | Checking Account, Credit Card, Investment Account, Mortgage, Personal Loan y Savings Account |
| Propensión | Puntuaciones | `_valuelabemeaptrsd.propensity.cards_score`, `credit_score`, `investment_score` y `mortgages_score` | De 1 a 100 |

### Audiencias existentes

63 de las 453 audiencias usan datos de BBank, creadas entre octubre de 2024 y mayo de 2026. Algunos ejemplos son `Adrian_MujeresEntre30_40_Bbank`, `Berto - Nacionales con Cuentas Extranjeras`, `LMD_AbandonedCart`, `Abandoned cart in Bbank`, `Clientes_CampañaDigital_Tarjeta_Contratada` y `ControlGroup_BBank_Collab_true`. La mayoría se construyó sobre otras copias de BBank y falta revisar cuáles usan atributos de la línea DemoCJA BCR.

## Limitaciones

1. La sandbox es compartida y cualquier alumno puede modificar o borrar estos datasets antes de la entrega del TFM.
2. No hay movimientos de tarjeta, evolución del saldo ni importe de las solicitudes. La fidelización cubre 500 clientes, las operaciones de cajero 321 y las interacciones con producto 55.
3. El dataset de propensión no cruza con ningún cliente.
4. Las incoherencias de los datos (la lista de productos guardada como texto, las sucursales sin ficha, las dos grafías de Valencia y los consentimientos al 32,7 %) son reales y se pueden usar como casos límite de la skill.

## Acceso y particularidades de la API

Pasó aquí desde Datos clave de `status.md` el 2026-10-14.

- Host de Query Service `valuelabemeaptrsd.platform-query.adobe.io`, base `dev:all`. Comprobado el 2026-10-10: token IMS, lectura de Catalog y Schema Registry, `select 1` y 758 tablas visibles.
- Sandbox Management responde 403 `SMS-2010-403`: la credencial no puede listar sandboxes.
- El fichero de credenciales guarda `SCOPES` como lista JSON, y hay que enviarlos a IMS unidos por comas. Si se mandan como parámetro repetido, IMS concede solo el primero y toda la API responde 403 `403027` "User region is missing" (incidencia I01 de `evidencias/incidencias.md`).
- Las tablas de Query Service solo tienen los campos que han recibido datos, que son los del `observableSchema` de Catalog. Catalog solo devuelve el `observableSchema` de un dataset por llamada (incidencia I04).
- `/tenant/descriptors` corta en 300 y no pagina. Los descriptores de cada schema salen pidiéndolo con `Accept: application/vnd.adobe.xed-full-desc+json; version=1` (incidencia I02).
- `matched` no vale como alias en Query Service.
