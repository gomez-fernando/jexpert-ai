# Copias de los datasets de BBank

Propuesta del 2026-10-11. Sandbox `dev` de Jakala. El usuario autoriza solo la copia de prueba, `fdg_tfm_bbank_branch`, y decide no copiar los schemas. El resto espera a la vista de la prueba.

## Resultado de la prueba

`fdg_tfm_bbank_branch` (`6acac72535953e0d1770b5d7`) se creó el 2026-10-11 con la consulta `2c4be3db-706b-4318-9d73-017867e9b705`. Estuvo unos 13 minutos en cola (`SUBMITTED`) y tardó 878 segundos en total.

| Comprobación | Resultado |
| --- | --- |
| Schema | El mismo que el origen, `Training_BBank_Branch_sch_AbelPerez` |
| Perfil e identidades | Sin habilitar |
| Clase y origen | `record`, creado por `acp_foundation_queryService_write` |
| Campos observados | Los mismos 5 que el origen |
| Lotes | Uno, en estado `success` |
| Filas | 11 en el origen y 11 en la copia |
| Contenido | 0 diferencias en las dos direcciones, comparando cada fila como JSON |
| Consumo | 0,37 `clusterVMHours` según `computeMetrics` del registro de consultas |

Las consultas batch de otros alumnos en `dev` gastaron entre 0,10 y 0,34 `clusterVMHours` cada una, aunque escribieran una sola fila, y las fallidas también consumen. El coste lo marca el arranque del clúster, no el volumen. Que `clusterVMHours` sea exactamente lo que descuenta la licencia de Data Distiller está sin confirmar.

La prueba no cubre la clase de evento (`_id` y `timestamp`), `identityMap` ni los arrays, porque el schema de sucursales no los tiene. Cada copia nueva se comprueba con lo mismo que esta.

Cada copia se crea con un CTAS de Query Service sobre el mismo schema XDM que el dataset de origen, con las columnas de primer nivel que tienen datos según el `observableSchema` de Catalog. Así la copia conserva la clase, los títulos de los campos y las identidades del schema. No se habilita para perfil: compartiría valores de `TRBbankProfileID` con las copias de otros alumnos y se fusionaría con ellas en el perfil. El tamaño de una audiencia se calcula con Query Service sobre las copias.

En esta sandbox ya hay datasets creados con CTAS sobre un schema XDM, como `rankingtestadrian_2` (2024-11-18), así que la vía funciona aquí.

## Orden

1. Crear `fdg_tfm_bbank_branch`, la más pequeña (11 filas) y con una columna struct.
2. Comprobar que su contenido coincide con el origen.
3. Crear las otras 11.
4. Contar las filas de cada copia y compararlas con las del origen.

## Sentencias

| Copia | Origen | Schema | Filas |
| --- | --- | --- | --- |
| `fdg_tfm_bbank_branch` | `training_bbank_branch_ds_abelperez` | `Training_BBank_Branch_sch_AbelPerez` | 11 |
| `fdg_tfm_bbank_profiledata` | `bbank_democja_bcr_profiledata` | `Training_Bbank_ProfileData_sch_AbelPerez` | 7.730 |
| `fdg_tfm_bbank_applications` | `bbank_democja_bcr_applications` | `Training_Bbank_Application` | 40.414 |
| `fdg_tfm_bbank_fulfillment` | `bbank_democja_bcr_fulfillment` | `Training_Bbank_Fulfillment_v2` | 15.577 |
| `fdg_tfm_bbank_webinteractions` | `bbank_democja_bcr_webinteractions` | `Training_BBank_WebInteractions6_sch_AbelPerez` | 260.627 |
| `fdg_tfm_bbank_bankaccount` | `bbank_bankaccount_demo_bc` | `Training_BBank_BankAccount_sch_AbelPerez` | 2.530 |
| `fdg_tfm_bbank_loyalty` | `training_bbank_loyalty_ds_abelperez` | `Training_BBank_Loyalty_sch_AbelPerez` | 1.002 |
| `fdg_tfm_bbank_atmtransactions` | `training_bbank_atmtransactions_ds_abelperez` | `Training_BBank_ATM_Transactions_sch_AbelPerez` | 1.000 |
| `fdg_tfm_bbank_productinteractions` | `training_bbank_productinteractions_ds` | `Training_BBank_ProductsTransactions_sch_AbelPerez` | 315 |
| `fdg_tfm_bbank_products` | `training_bbank_products_ds_abelperez` | `Training_BBank_Products_sch_AbelPerez` | 44 |
| `fdg_tfm_bbank_atminfo` | `training_bbank_atminfo_ds_abelperez` | `Training_BBank_ATMInfo_sch_AbelPerez` | 43 |
| `fdg_tfm_bbank_propensity` | `bbank_propensity_ds` | `BBANK_Propensity` | 100 |

```sql
CREATE TABLE fdg_tfm_bbank_branch WITH (schema='Training_BBank_Branch_sch_AbelPerez') AS (
  SELECT branchAddress, branchID FROM training_bbank_branch_ds_abelperez
)

CREATE TABLE fdg_tfm_bbank_profiledata WITH (schema='Training_Bbank_ProfileData_sch_AbelPerez') AS (
  SELECT _valuelabemeaptrsd, consents, homeAddress, mobilePhone, person, personID, personalEmail FROM bbank_democja_bcr_profiledata
)

CREATE TABLE fdg_tfm_bbank_applications WITH (schema='Training_Bbank_Application') AS (
  SELECT _id, _valuelabemeaptrsd, identityMap, timestamp FROM bbank_democja_bcr_applications
)

CREATE TABLE fdg_tfm_bbank_fulfillment WITH (schema='Training_Bbank_Fulfillment_v2') AS (
  SELECT _id, _valuelabemeaptrsd, eventMergeId, timestamp FROM bbank_democja_bcr_fulfillment
)

CREATE TABLE fdg_tfm_bbank_webinteractions WITH (schema='Training_BBank_WebInteractions6_sch_AbelPerez') AS (
  SELECT _id, _valuelabemeaptrsd, eventType, identityMap, timestamp FROM bbank_democja_bcr_webinteractions
)

CREATE TABLE fdg_tfm_bbank_bankaccount WITH (schema='Training_BBank_BankAccount_sch_AbelPerez') AS (
  SELECT _valuelabemeaptrsd, personID FROM bbank_bankaccount_demo_bc
)

CREATE TABLE fdg_tfm_bbank_loyalty WITH (schema='Training_BBank_Loyalty_sch_AbelPerez') AS (
  SELECT loyalty, personID FROM training_bbank_loyalty_ds_abelperez
)

CREATE TABLE fdg_tfm_bbank_atmtransactions WITH (schema='Training_BBank_ATM_Transactions_sch_AbelPerez') AS (
  SELECT _id, _valuelabemeaptrsd, timestamp FROM training_bbank_atmtransactions_ds_abelperez
)

CREATE TABLE fdg_tfm_bbank_productinteractions WITH (schema='Training_BBank_ProductsTransactions_sch_AbelPerez') AS (
  SELECT _id, _valuelabemeaptrsd, eventType, timestamp FROM training_bbank_productinteractions_ds
)

CREATE TABLE fdg_tfm_bbank_products WITH (schema='Training_BBank_Products_sch_AbelPerez') AS (
  SELECT productCategoryName, productID, productName FROM training_bbank_products_ds_abelperez
)

CREATE TABLE fdg_tfm_bbank_atminfo WITH (schema='Training_BBank_ATMInfo_sch_AbelPerez') AS (
  SELECT _valuelabemeaptrsd, atmAddress, atmID, isAtmActive FROM training_bbank_atminfo_ds_abelperez
)

CREATE TABLE fdg_tfm_bbank_propensity WITH (schema='BBANK_Propensity') AS (
  SELECT _valuelabemeaptrsd, person, personalEmail FROM bbank_propensity_ds
)
```

## Comprobación de la primera copia

Las dos consultas tienen que devolver 0. Comparan como JSON para que una desalineación de campos dentro del struct salga como diferencia.

```sql
SELECT count(1) FROM (
  SELECT to_json(struct(branchAddress, branchID)) AS j FROM fdg_tfm_bbank_branch
  EXCEPT
  SELECT to_json(struct(branchAddress, branchID)) AS j FROM training_bbank_branch_ds_abelperez
)

SELECT count(1) FROM (
  SELECT to_json(struct(branchAddress, branchID)) AS j FROM training_bbank_branch_ds_abelperez
  EXCEPT
  SELECT to_json(struct(branchAddress, branchID)) AS j FROM fdg_tfm_bbank_branch
)
```

Si la copia trae campos nulos que el origen no tenía, el JSON puede diferir sin que haya error en los datos. En ese caso se compara campo a campo.
