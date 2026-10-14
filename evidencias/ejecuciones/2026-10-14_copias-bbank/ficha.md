# Copias de BBank

Fecha: 2026-10-14, de 14:53 a 15:07 UTC.

El script lo preparó Claude Code y lo lanzó el usuario desde PowerShell en su equipo, porque el control de permisos de Claude Code lo bloqueó (incidencia I03 de `../../incidencias.md`). Sandbox `dev` de Jakala.

## Qué se ejecutó

1. `ctas_submit.py` lanza las 11 copias a la vez por la API de Query Service. Antes de cada una comprueba que no existe un dataset con ese nombre, y guarda los IDs de las consultas en `ctas_ids.json`, con la sentencia de cada una.
2. `ctas_wait.py` consulta cada minuto el estado de las 11 hasta que terminan. Su salida es `espera_consultas.log`, con la hora local del equipo (UTC+2).
3. `ctas_verify.py` comprueba cada copia contra su origen. Su salida es `comprobaciones.log` y `ctas_verify.json`.

## Resultado

Las 11 consultas terminaron en `SUCCESS`. Como esperaron en la cola a la vez, el lote tardó 14 minutos, lo mismo que una sola copia, y consumió 1,87 `clusterVMHours` en total.

Las 11 copias tienen el mismo schema que su origen, no están habilitadas para perfil, tienen un lote en `success`, las mismas filas y 0 diferencias de contenido en los dos sentidos. En `fdg_tfm_bbank_atmtransactions` y `fdg_tfm_bbank_productinteractions`, Catalog registra el campo `_id` de la copia con el formato `uri-reference` del schema y el del origen sin formato. Los valores son idénticos.

| Copia | Dataset | Consulta | Filas | `clusterVMHours` |
| --- | --- | --- | --- | --- |
| `fdg_tfm_bbank_profiledata` | `6acf9882c45f8bce17046ded` | `ae1047ee-f1ee-4ce5-9a74-3afd9f637492` | 7.730 | 0,13 |
| `fdg_tfm_bbank_applications` | `6acf98a434e4d258bab246a0` | `63482ac0-ad37-4181-86e7-79e3f75101c3` | 40.414 | 0,15 |
| `fdg_tfm_bbank_fulfillment` | `6acf989d35953e0d1775cf3c` | `f2e6fe1e-b8d3-4c73-a1c3-55f703c67c03` | 15.577 | 0,14 |
| `fdg_tfm_bbank_webinteractions` | `6acf98961e695f5e51febdbd` | `fe9d509f-82ac-464f-bc24-6c2268be7241` | 260.627 | 0,14 |
| `fdg_tfm_bbank_bankaccount` | `6acf99c5f07a3d91b7634513` | `46fa32cb-2933-46dd-9b5f-2614325f9d47` | 2.530 | 0,31 |
| `fdg_tfm_bbank_loyalty` | `6acf9884230d559194bd933d` | `97a4d673-091b-4d6c-93b7-c5fe982010f3` | 1.002 | 0,13 |
| `fdg_tfm_bbank_atmtransactions` | `6acf988834e4d258bab2469f` | `fffcbc5c-c392-4046-b781-93644efa82fe` | 1.000 | 0,13 |
| `fdg_tfm_bbank_productinteractions` | `6acf989a93227ab0b0fe4bc5` | `6d4dc879-1c86-4feb-b9be-191378c1fe3c` | 315 | 0,14 |
| `fdg_tfm_bbank_products` | `6acf9a0393227ab0b0fe4da4` | `5946add6-b266-4c87-89c1-6fb9041d907b` | 44 | 0,34 |
| `fdg_tfm_bbank_atminfo` | `6acf9881c45f8bce17046dec` | `a6188177-01a0-4565-9881-bf802fd768b6` | 43 | 0,13 |
| `fdg_tfm_bbank_propensity` | `6acf9882f2ff6682a927e6fe` | `27a1b6e6-2405-4634-a406-7d383709b445` | 100 | 0,13 |

## Fechado

Las 11 consultas están en el registro de Query Service con su hora de creación (14:53:31 a 14:53:49 UTC) y de fin. Los 11 datasets tienen fecha de creación del 2026-10-14 en Catalog.
