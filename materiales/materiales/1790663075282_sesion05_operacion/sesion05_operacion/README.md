# Sesión 5 — Automatización de pipelines y operación

Repo autocontenido de la sesión. Todo lo que se ve en clase existe de verdad
en el proyecto `jakamedy-data-ia`: dataset `demo_ops`, bucket
`gs://jakamedy-data-ia-demo/`, **dos Cloud Workflows desplegados**
(europe-west1) y el historial de jobs.

Stack del equipo (canon): **Cloud Workflows + Cloud Scheduler + BigQuery**.
Sin Airflow, sin Composer, sin Dataform: un pipeline es un `.yaml`
autocontenido (carga → modelos SQL → assertions como pasos) versionado en
`workflows/`.

El conocimiento del equipo vive en TRES contextos firmados
(`contexto_equipo.md` operativo, `contexto_kpis.md` de grano y KPIs,
`contexto_calidad.md` de assertions) que son el acervo del proyecto: la skill
es el router que dice al agente qué leer antes de escribir nada.

```text
sesion05_operacion/
  contexto_equipo.md   Canon operativo (stack, naming, defaults, reglas con agentes)
  contexto_kpis.md     Grano y KPIs firmados (las definiciones acordadas del proyecto)
  contexto_calidad.md  Política de calidad (assertions y umbrales)
  skills/              generar-pipeline-workflows/SKILL.md — el router: dice qué leer y cuándo
  templates/           workflow_ingesta_template.yaml · modelo_incremental_template.sql
  workflows/           ingesta_diaria.yaml — el pipeline viejo de producción (roto)
  data/                fixtures (seed 20260928, self-check antes de escribir)
  scripts/             generar_datos_s5.py
  sql/                 DDL + job del pipeline (roto y parcheado) + queries de evidencia
  prompts_completos.md Los cuatro prompts literales
  output/              ensayos ejecutados: trazas, diff, errores y ejecuciones reales
  _archivo_airflow_dataform/  primera versión del material (DAG Airflow + Dataform),
                              archivada tras el cambio de stack
```

## Estado vivo en GCP (28/09/2026)

| Pieza | Dónde | Estado |
|---|---|---|
| Workflow heredado (demo B) | `workflows/ingesta_diaria` (europe-west1) | desplegado; ejecución real FAILED (reintentos del canon viejo) |
| Workflow nuevo (demo A) | `workflows/ingesta_ventas_offline` | desplegado (rev 000002) y **SUCCEEDED**: 30.000 filas, assertions 0 |
| Fuente renombrada | `demo_ops.stg_ingesta_diaria` | 5.000 filas (16–30 sep), esquema NUEVO (`total_importe`) |
| Destino del pipeline, ya parcheado | `demo_ops.fct_ingesta_diaria` | 9.500 = 4.500 pre-rename + 5.000 post |
| Crudo del fichero de ventas | `demo_ops.raw_ventas_offline` | 30.000 |
| Staging con auditoría (demo A) | `demo_ops.stg_ventas_offline` | 30.000 |
| Modelo incremental (demo A) | `demo_ops.fct_ventas_diarias` | 17.030 (grano tienda × día) |
| Fichero origen | `gs://jakamedy-data-ia-demo/raw/ventas_offline.csv` | — |

Historial de jobs real en `INFORMATION_SCHEMA.JOBS`: `s5_normalizar_verde_01`
(verde), rojos `s5_normalizar_rojo_01..03` (`Unrecognized name: importe_total`),
el merge `s5_normalizar_verde_02_parcheado` y los jobs lanzados por los dos
workflows. Consulta: `sql/q00_jobs_historial.sql`.

## Cómo re-ejecutar la sesión desde cero

```powershell
# 0. Fixture reproducible
python repo_demo\sesion05_operacion\scripts\generar_datos_s5.py

# 1. Histórico en verde (la fuente con el esquema VIEJO)
bq load --replace --source_format=CSV --skip_leading_rows=1 `
  demo_ops.stg_ingesta_diaria data\stg_ingesta_diaria_prev.csv `
  registro_id:STRING,fecha:DATE,importe_total:FLOAT64,tienda_id:STRING
bq query --use_legacy_sql=false < sql\normalizar_importes.sql      # VERDE (4.500)

# 2. El rename del origen (esquema NUEVO) y el fallo
bq load --replace --source_format=CSV --skip_leading_rows=1 `
  demo_ops.stg_ingesta_diaria data\stg_ingesta_diaria.csv `
  registro_id:STRING,fecha:DATE,total_importe:FLOAT64,tienda_id:STRING
gcloud workflows deploy ingesta_diaria --location=europe-west1 `
  --source=repo_demo\sesion05_operacion\workflows\ingesta_diaria.yaml
gcloud workflows run ingesta_diaria --location=europe-west1         # ROJO: 400

# 3. Verificación y parche (tras aprobación humana)
bq query --use_legacy_sql=false < sql\q03a_rango_importes.sql
bq query --use_legacy_sql=false < sql\q03b_sumas_por_dia.sql
bq query --use_legacy_sql=false < sql\normalizar_importes_parcheado.sql   # VERDE
```

En Windows usa `cmd /c "bq query --use_legacy_sql=false < fichero.sql"` y
evita `>` de PowerShell para SQL/salidas binarias.

## Camino B (sin directo)

Para la demo A actual, abre el YAML de `output/workflows/` y muestra el estado
SUCCEEDED y las assertions en `output/log_workflow_verde_ventas.txt`. La traza
y el diff de una preparación anterior se conservan por transparencia, pero
**no forman parte de la secuencia de clase**. La demo B usa el fallo y sus
consultas de evidencia capturadas en `output/`.

| Fichero | Qué es |
|---|---|
| `log_job_fallido.txt` | Error 400 real del job roto |
| `log_workflow_rojo.txt` | El workflow heredado ejecutado en ROJO de verdad (46 s, 4 intentos a 5 s) |
| `q00_jobs_historial.txt` | Tira de jobs: verde → 3 rojos consecutivos |
| `evidencia_columns.txt` | INFORMATION_SCHEMA.COLUMNS de ambas tablas |
| `evidencia_bq_show_stg.txt` | `bq show`: lastModifiedTime justo antes del 1er rojo |
| `output/workflows/ingesta_ventas_offline.yaml` | Código generado para revisar antes de la ejecución de prueba |
| `log_workflow_verde_ventas.txt` | Ejecución observada SUCCEEDED, con assertions sin violaciones; al final conserva una nota histórica de preparación |
| `traza_demo_a.md`, `pr_demo_a_nueva.txt`, `diff_demo_a.patch` | Historial de una preparación anterior; no proyectar como flujo de la demo actual |
| `traza_demo_b.md` | Investigación completa con evidencias citables |
| `q01`/`q02` | Jobs verdes de la demo A (30.000 filas, assertions OK) |
| `q03_verificacion.txt` | Rangos + sumas por día antes/después del rename |
| `q04_job_parcheado.txt` | El merge corre en verde: 9.500 filas, 30 días |

## Regla de oro de la sesión

El agente propone diagnósticos y parches; **el humano aprueba y aplica**. En
este entorno al agente le basta `bigquery.dataViewer` + `bigquery.jobUser`:
puede leer esquemas y historial, no puede escribir — y el
`repo_demo/.claude/settings.json` le deniega además el DML y tocar
`workflows/`, `templates/`, `skills/` y `sql/normalizar_importes.sql`.

## Impartición con Claude Code (app de escritorio, sesión LOCAL)

El agente de las demos es Claude Code en la app de Claude (Enterprise),
sesión **local** sobre `repo_demo/` (verificado 28/09: `bq` autenticado y
`demo_ops` visible). NO usar sesiones web/cloud: no hay `bq` allí y el repo
viajaría a infra de Anthropic.

- **La política viaja con el repo**: `repo_demo/.claude/settings.json`
  (escritura solo en `output/`, `bq query/show/ls` permitido, DML/DDL y
  archivos de referencia denegados). El deny por patrón es cinturón de
  seguridad, no IAM: el nivel definitivo es una service account read-only.
- **Demo B en modo plan** (selector de modo del turno): "NO CAMBIES NADA"
  forzado por herramienta, no solo por prompt.
- Sonido de prueba antes de clase: pedirle un fichero en `output/` (debe
  poder) y un arreglo de `workflows/ingesta_diaria.yaml` (debe salir el deny).
