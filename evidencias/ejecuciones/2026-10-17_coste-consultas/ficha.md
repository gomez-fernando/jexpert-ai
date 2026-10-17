# Coste de las consultas del TFM

Fecha: 2026-10-17, de 20:53:47 a 20:53:59 UTC.

Lanzado por Claude Code desde el equipo del usuario, con `coste_consultas.py`, sobre la sandbox `dev` de Jakala. Solo lee el registro de consultas (`GET /data/foundation/query/queries`). El script no imprime la configuración de `aep/` ni los campos `clientId` y `userId` de las consultas. El último commit es `bbe0039`, y este script entra en el commit del 2026-10-17.

## Qué se ejecutó

`coste_consultas.py` lista todas las consultas de la sandbox creadas desde el 2026-10-10 a las 00:00 UTC, se queda con las que mencionan `fdg_tfm_bbank` en su SQL y suma `computeMetrics.clusterVMHours` por tipo (batch o lectura) y por estado. La salida está en `salida.log`, con las horas en UTC.

## Resultado

En la sandbox hay 4.211 consultas desde el 2026-10-10, de todos los usuarios. 207 son del TFM.

Las 12 CTAS que crearon las copias terminaron en `SUCCESS` y suman 2,2383 `clusterVMHours`. La copia de prueba gastó 0,3678 y las otras 11, 1,8705, lo mismo que recogen `../2026-10-10_copia-prueba/ficha.md` y `../2026-10-14_copias-bbank/ficha.md`.

| Consulta | Creada (UTC) | Cliente | Copia | `clusterVMHours` |
| --- | --- | --- | --- | --- |
| `2c4be3db-706b-4318-9d73-017867e9b705` | 2026-10-10 23:03:49 | Generic PostgreSQL | `fdg_tfm_bbank_branch` | 0,3678 |
| `ae1047ee-f1ee-4ce5-9a74-3afd9f637492` | 2026-10-14 14:53:31 | API | `fdg_tfm_bbank_profiledata` | 0,1300 |
| `63482ac0-ad37-4181-86e7-79e3f75101c3` | 2026-10-14 14:53:33 | API | `fdg_tfm_bbank_applications` | 0,1478 |
| `f2e6fe1e-b8d3-4c73-a1c3-55f703c67c03` | 2026-10-14 14:53:34 | API | `fdg_tfm_bbank_fulfillment` | 0,1444 |
| `fe9d509f-82ac-464f-bc24-6c2268be7241` | 2026-10-14 14:53:36 | API | `fdg_tfm_bbank_webinteractions` | 0,1417 |
| `46fa32cb-2933-46dd-9b5f-2614325f9d47` | 2026-10-14 14:53:38 | API | `fdg_tfm_bbank_bankaccount` | 0,3067 |
| `97a4d673-091b-4d6c-93b7-c5fe982010f3` | 2026-10-14 14:53:40 | API | `fdg_tfm_bbank_loyalty` | 0,1306 |
| `fffcbc5c-c392-4046-b781-93644efa82fe` | 2026-10-14 14:53:42 | API | `fdg_tfm_bbank_atmtransactions` | 0,1306 |
| `6d4dc879-1c86-4feb-b9be-191378c1fe3c` | 2026-10-14 14:53:44 | API | `fdg_tfm_bbank_productinteractions` | 0,1411 |
| `5946add6-b266-4c87-89c1-6fb9041d907b` | 2026-10-14 14:53:45 | API | `fdg_tfm_bbank_products` | 0,3417 |
| `a6188177-01a0-4565-9881-bf802fd768b6` | 2026-10-14 14:53:47 | API | `fdg_tfm_bbank_atminfo` | 0,1267 |
| `27a1b6e6-2405-4634-a406-7d383709b445` | 2026-10-14 14:53:49 | API | `fdg_tfm_bbank_propensity` | 0,1294 |

Las otras 195 consultas del TFM son lecturas interactivas, 194 correctas y una fallida. Ninguna tiene `computeMetrics`, así que en el registro de consultas no consta que gasten horas de clúster.

Hasta el 2026-10-17, el TFM ha consumido 2,24 horas de clúster de las 2.000 que tiene contratadas la organización, un 0,11 %.

## Fechado

Las 207 consultas están en el registro de Query Service con su ID y su hora de creación, que pone Adobe. La ejecución de este script solo hace lecturas de la API, que no dejan consulta en el registro. Su fecha se apoya en la hora que imprime la propia salida, en el push a GitHub del día y en el registro de la sesión de Claude Code.

## Incidencias

La primera versión del script no encontraba ninguna consulta del TFM: incidencia I07 de `../../incidencias.md`.
