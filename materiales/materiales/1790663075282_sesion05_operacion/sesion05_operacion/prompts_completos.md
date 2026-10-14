# Prompts completos — Sesión 5 (operación)

Los cuatro prompts de la sesión, literales y listos para usar con `repo_demo/`
como carpeta raíz de la sesión local de Claude Code. Las rutas que Claude cite
en sus respuestas deben empezar por `sesion05_operacion/`: `sql/...` y
`output/...` solos no se abren desde esa raíz. Los ensayos ejecutados están
en `sesion05_operacion/output/` (trazas, diffs y ejecuciones
reales del 28/09/2026). Stack del equipo: **Cloud Workflows + Scheduler +
BigQuery** (sin Airflow, sin Dataform: los modelos son SQL embebido en el
workflow).

## 1 · Demo A — encargo de generación (coding agent en el repo)

```text
Necesito un pipeline diario que cargue sesion05_operacion/data/ventas_offline.csv
(en GCS: gs://jakamedy-data-ia-demo/raw/ventas_offline.csv) a BigQuery,
lo normalice según nuestras convenciones y cree el modelo incremental
fct_ventas_diarias, con sus assertions.
```

El agente lee por sí solo la skill, los tres contextos firmados
(`contexto_equipo.md`, `contexto_kpis.md`, `contexto_calidad.md`) y las
plantillas. Escribe la propuesta en `output/workflows/` para revisión humana;
no despliega.

Secuencia de la demo: generar el workflow → revisar significado, operación y
calidad → ejecutar con aprobación humana. Resultado capturado en
`output/log_workflow_verde_ventas.txt`: SUCCEEDED, assertions sin violaciones.
Un fallo de un ensayo anterior sigue documentado en `output/`, pero no forma
parte del guion de esta demo.

## 2 · Demo B — diagnóstico (NO CAMBIES NADA)

```text
El paso `normalizar_importes` del workflow `ingesta_diaria` falla desde el
martes. Investiga la causa usando el error, INFORMATION_SCHEMA y el repo.

NO CAMBIES NADA.

Devuélveme:
- causa probable
- evidencia (mínimo 2 piezas, citables)
- plan de verificación en 3 pasos

Al citar ficheros en tu respuesta, usa rutas relativas a la raíz repo_demo:
`sesion05_operacion/sql/...` y `sesion05_operacion/output/...`.
No uses enlaces con rutas abreviadas `sql/...` ni `output/...`.
```

Material de entrada: `output/log_job_fallido.txt` (error real del job de
BigQuery), la ejecución fallida del workflow real
(`workflows/ingesta_diaria.yaml` desplegado en `jakamedy-data-ia`), o
re-ejecución en vivo: `bq query --use_legacy_sql=false < sql/normalizar_importes.sql`.
Ensayo capturado: `output/traza_demo_b.md` con las evidencias
(`evidencia_columns.txt`, `evidencia_bq_show_stg.txt`, `q00_jobs_historial.txt`).

## 3 · Demo B — propuesta de parche para revisión humana

```text
Revisa los resultados ya capturados en sesion05_operacion/output/q03_verificacion.txt.
Explica qué indican y qué no permiten concluir; señala qué debe confirmarse
con el equipo origen. Después propón el cambio mínimo como diff para revisión
humana. No ejecutes consultas ni apliques el parche.

Al citar ficheros en tu respuesta, usa rutas relativas a la raíz repo_demo,
siempre con el prefijo `sesion05_operacion/`; no enlaces `sql/...` ni
`output/...` sin ese prefijo.
```

Respuesta de referencia: `sql/normalizar_importes_parcheado.sql` (una línea:
`CAST(total_importe AS FLOAT64) AS importe`). La evidencia de verificación ya
está en `output/q03_verificacion.txt`; tras la revisión, solo una persona puede
aplicar el parche (resultado histórico en `output/q04_job_parcheado.txt`).

## 4 · Observabilidad — troubleshooting de degradación

```text
Tarea: este pipeline se ha degradado. Diagnostica.

Contexto:
  pipeline        : ingesta_ventas_offline (Cloud Workflow)
  tabla destino   : demo_ops.fct_ventas_diarias
  último cambio   : primer despliegue del workflow esta semana
  señales (3 sem.): duración 14 → 27 min · nulos 3,1 % → 5,2 %
                    tokens/run 41k → 94k · requiere_revision 5 % → 12 %

Entregable:
  1. UNA causa más probable
  2. máximo TRES hipótesis alternativas, y qué descartaría cada una
  3. comandos o queries concretos para verificar cada hipótesis

No propongas cambios de código todavía.
```

Nota de diseño: es el mismo patrón del prompt 2, segunda vez a propósito —
diagnosticar y reparar son dos fases separadas.
