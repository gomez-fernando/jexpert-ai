# Equipo Data — Contexto operativo

Canon operativo del equipo para pipelines del dataset `demo_ops` (proyecto
`jakamedy-data-ia`, región EU). Si un workflow viejo o un documento discrepan
de este fichero, **este fichero manda**.

Este es el canon de operación. Antes de generar o tocar pipelines hay que leer
además:

- `contexto_kpis.md` — definiciones acordadas: grano, métricas y KPIs.
- `contexto_calidad.md` — política de calidad: assertions y umbrales.

(Documentos que el equipo ha ido firmando a lo largo del proyecto; los
mantienen humanos.)

## Stack de orquestación

- **Cloud Workflows + Cloud Scheduler + BigQuery.** Un workflow = un fichero
  `.yaml` autocontenido por ingesta: carga, modelos y assertions viven como
  pasos, versionados juntos en `workflows/`.
- No usamos Airflow ni Dataform: los modelos son SQL embebido en el workflow.
- El tiempo de cómputo vive en BigQuery (`jobs.insert` / `jobs.query`); el
  workflow solo orquesta pasos, reintentos y alertas.

## Convenciones de naming

- Capas: `raw_<fuente>` (llegada en crudo: espejo exacto del fichero),
  `stg_<fuente>` (normalizada con auditoría) y `fct_<nombre>` (hechos gold,
  siempre incremental). Nada de `silver_` ni `bronze_` en código nuevo.
- Claves naturales: sufijo `_nk`, siempre `STRING` (castea en el modelo).
- Columnas snake_case; fechas `DATE` ISO (YYYY-MM-DD); importes `FLOAT64` o
  `NUMERIC`, nunca strings con formato local.
- Toda tabla de staging lleva auditoría: `_fuente STRING` (fichero origen) y
  `_cargado_en TIMESTAMP`.

## Defaults de workflow (no se negocian)

- **Cron: `17 3 * * *`** (Cloud Scheduler, Europe/Madrid) — 03:17, NUNCA en
  punto. Esquivamos el pico de la plataforma en el que arrancan todos los
  jobs programados en punto.
- Reintentos: `max_attempts: 3` (1 + 2) con `backoff` de **15 min** y, tras
  agotarlos, alerta al canal del equipo. Un fallo transitorio no despierta
  a nadie.
- Idempotencia: carga `WRITE_TRUNCATE`, modelos incrementales con guarda
  `MAX(fecha)`, y el scheduler dispara una ejecución cada vez.

## Fuentes de otros equipos

- `demo_ops.stg_ingesta_diaria` la publica el equipo origen (espejo de su
  fichero diario). **No sigue este canon**: puede cambiar de esquema sin
  avisar. Precedente: el 21/09/2026 renombró `importe_total` →
  `total_importe` y el workflow `ingesta_diaria` empezó a fallar la misma
  noche.
- Nuestro contrato aguas abajo es `fct_ingesta_diaria` (`registro_nk`,
  `fecha`, `importe`, `tienda_nk`, particionada por `fecha`).

## Al trabajar con asistentes / coding agents

- El agente escribe propuestas en `output/` de la sesión y presenta el diff.
  **Nunca despliega workflows ni toca tablas `fct_` directamente.**
- Nada llega a producción sin PR revisada por un humano. El parche rápido
  (alias de columna) es válido para volver a verde, pero se etiqueta como
  parche: la solución es actualizar el contrato de esquema con el origen.
- Diagnóstico y reparación son dos fases separadas: primero causa + evidencia
  + plan de verificación, luego (con aprobación) el cambio.
- Si falta información para decidir, enumérala como DECISIÓN ABIERTA; no la
  inventes.
