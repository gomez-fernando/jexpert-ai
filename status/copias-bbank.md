# Copias de los datasets de BBank

Propuesta del 2026-10-11. Sandbox `dev` de Jakala. El usuario autoriza solo la copia de prueba, `fdg_tfm_bbank_branch`, y decide no copiar los schemas. El resto espera a la vista de la prueba. El 2026-10-14 autoriza las 11 restantes.

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

## Copias del 2026-10-14

Lanzadas a la vez por la API de Query Service a las 14:53 UTC del 2026-10-14. Las 11 terminaron en `SUCCESS` a las 15:07 UTC. Lanzadas en paralelo, todo el lote tardó 14 minutos, lo mismo que una sola copia. El consumo total fue de 1,87 `clusterVMHours`.

| Copia | Dataset | Consulta | Segundos | `clusterVMHours` |
| --- | --- | --- | --- | --- |
| `fdg_tfm_bbank_profiledata` | `6acf9882c45f8bce17046ded` | `ae1047ee-f1ee-4ce5-9a74-3afd9f637492` | 425 | 0,13 |
| `fdg_tfm_bbank_applications` | `6acf98a434e4d258bab246a0` | `63482ac0-ad37-4181-86e7-79e3f75101c3` | 484 | 0,15 |
| `fdg_tfm_bbank_fulfillment` | `6acf989d35953e0d1775cf3c` | `f2e6fe1e-b8d3-4c73-a1c3-55f703c67c03` | 482 | 0,14 |
| `fdg_tfm_bbank_webinteractions` | `6acf98961e695f5e51febdbd` | `fe9d509f-82ac-464f-bc24-6c2268be7241` | 480 | 0,14 |
| `fdg_tfm_bbank_bankaccount` | `6acf99c5f07a3d91b7634513` | `46fa32cb-2933-46dd-9b5f-2614325f9d47` | 779 | 0,31 |
| `fdg_tfm_bbank_loyalty` | `6acf9884230d559194bd933d` | `97a4d673-091b-4d6c-93b7-c5fe982010f3` | 416 | 0,13 |
| `fdg_tfm_bbank_atmtransactions` | `6acf988834e4d258bab2469f` | `fffcbc5c-c392-4046-b781-93644efa82fe` | 414 | 0,13 |
| `fdg_tfm_bbank_productinteractions` | `6acf989a93227ab0b0fe4bc5` | `6d4dc879-1c86-4feb-b9be-191378c1fe3c` | 473 | 0,14 |
| `fdg_tfm_bbank_products` | `6acf9a0393227ab0b0fe4da4` | `5946add6-b266-4c87-89c1-6fb9041d907b` | 832 | 0,34 |
| `fdg_tfm_bbank_atminfo` | `6acf9881c45f8bce17046dec` | `a6188177-01a0-4565-9881-bf802fd768b6` | 409 | 0,13 |
| `fdg_tfm_bbank_propensity` | `6acf9882f2ff6682a927e6fe` | `27a1b6e6-2405-4634-a406-7d383709b445` | 407 | 0,13 |

El consumo no depende del tamaño: `fdg_tfm_bbank_webinteractions` (260.627 filas) gastó 0,14 horas y `fdg_tfm_bbank_products` (44 filas) gastó 0,34.

Las 11 pasan las mismas comprobaciones que la de prueba: el mismo schema que el origen, sin habilitar para perfil ni para identidad, un lote en `success`, las mismas filas y 0 diferencias de contenido en los dos sentidos comparando cada fila como JSON. Esta vez la comprobación cubre también la clase de evento (`time-series`), `identityMap` y los arrays. Los campos observados coinciden en todas salvo en `fdg_tfm_bbank_atmtransactions` y `fdg_tfm_bbank_productinteractions`, donde Catalog registra `_id` con el formato `uri-reference` del schema en la copia y sin formato en el origen. Los valores de `_id` son idénticos. Lo más probable es que los orígenes se cargaran por otra vía de ingesta (sin confirmar).

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
