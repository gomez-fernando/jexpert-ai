# Traza real — Demo B: diagnóstico del job `normalizar_importes` en rojo

Ensayo ejecutado el 2026-09-28 contra el proyecto real `jakamedy-data-ia`.
Todas las evidencias citadas existen en `output/` y en BigQuery.

## Prompt de diagnóstico (literal)

```text
El job `normalizar_importes` del pipeline `ingesta_diaria` falla desde el
martes. Investiga la causa usando el error, INFORMATION_SCHEMA y el repo.

NO CAMBIES NADA.

Devuélveme:
- causa probable
- evidencia (mínimo 2 piezas, citables)
- plan de verificación en 3 pasos
```

La instrucción en mayúsculas no es decorativa: separa diagnóstico de
reparación, y esa separación es una decisión de diseño, no un accidente.

## La investigación (con las fuentes reales)

1. **El error del job** (`output/log_job_fallido.txt`):
   `Error processing job 'jakamedy-data-ia:s5_normalizar_rojo_01':
   Unrecognized name: importe_total at [11:8]` — error de esquema, no de
   permisos ni de red.
2. **Esquemas actuales** (`output/evidencia_columns.txt`, de
   `demo_ops.INFORMATION_SCHEMA.COLUMNS`): en `stg_ingesta_diaria` NO existe
   `importe_total`; existe `total_importe` (FLOAT64). El destino
   `fct_ingesta_diaria` sigue con su contrato (`registro_nk, fecha, importe,
   tienda_nk`).
3. **Última modificación de la fuente** (`output/evidencia_bq_show_stg.txt`):
   `lastModifiedTime` de `stg_ingesta_diaria` = 1790579867008 ms — minutos
   ANTES del primer job rojo. La tabla cambió justo antes del primer fallo.
4. **Historial de jobs** (`output/q00_jobs_historial.txt`, de
   `INFORMATION_SCHEMA.JOBS_BY_PROJECT`): el mismo SQL corrió en verde
   (`s5_normalizar_verde_01`, 4.500 filas) y a partir del cambio de la fuente
   hay tres rojos consecutivos con el MISMO error. En el repo del equipo,
   `sql/normalizar_importes.sql` (el SQL exacto del job) no se ha tocado
   desde antes del rename — el código nuestro no se movió; se movió la
   fuente.

### Causa probable

El equipo origen publicó una versión nueva del fichero diario con la columna
`importe_total` renombrada a `total_importe` (precedente documentado en
`contexto_equipo.md`), sin aviso y sin cambio de contrato.

### Plan de verificación propuesto (ejecutado)

1. Rangos y nulos de la columna renombrada vs el histórico
   (`sql/q03a_rango_importes.sql`): min/max comparables, 0 nulos en ambos
   tramos.
2. Sumas y filas por día antes/después (`sql/q03b_sumas_por_dia.sql`):
   importe medio por registro ~137–141 en ambos tramos y patrón
   laborable/fin de semana igual → no hay pérdida de dato ni cambio de
   semántica bajo el rename.
3. Confirmar con el equipo origen si el rename es permanente (humano).

Resultados reales en `output/q03_verificacion.txt`.

## El parche como PR

Propuesta (`sql/normalizar_importes_parcheado.sql`): cambio mínimo, una
línea — `CAST(total_importe AS FLOAT64) AS importe`, manteniendo el
contrato aguas abajo. **La aplica un humano tras la revisión**: el agente no
tiene permisos de escritura. Mergeada y ejecutada:
`output/q04_job_parcheado.txt` — job en verde, `fct_ingesta_diaria` queda con
9.500 filas y 30 días (01–30 sep).

Nota honesta: el alias es un **parche para volver a verde**, no la solución.
La solución es actualizar el contrato de esquema con el origen — lo que la S3
enseñó a hacer.

## El contrafactual

¿Qué habría pasado si el agente tuviera escritura y auto-aplicara? Casos
Replit y Air Canada del transversal: un agente que alucina es un caos; con
HITL el peor caso es una PR mala que alguien rechaza.
