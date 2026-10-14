# Traza real — Demo A: el agente genera el primer pipeline del equipo

Ensayo ejecutado el 2026-09-28 con el coding agent trabajando sobre
`repo_demo/` como workspace. Es el camino B de la demo (si el directo divaga,
se proyecta esto). Stack del equipo: Cloud Workflows + Scheduler + BigQuery.

Narrativa de la sesión: llegamos con el proyecto vivo (S1–S4) y esta mañana
montamos **el primer pipeline asistido por el agente**.

## Encargo (literal)

```text
Necesito un pipeline diario que cargue ventas_offline.csv de Cloud Storage
(en GCS: gs://jakamedy-data-ia-demo/raw/ventas_offline.csv) a BigQuery,
lo normalice según nuestras convenciones y cree el modelo incremental
fct_ventas_diarias, con sus assertions.
```

## El bucle (lo que hizo el agente)

1. **Leyó `skills/generar-pipeline-workflows/SKILL.md`** → los pasos y las
   reglas (PR, assertions en el workflow, aviso de PII).
2. **Leyó los tres contextos firmados del equipo**:
   - `contexto_equipo.md` → canon operativo: stack, capas `raw_`/`stg_`/`fct_`,
     `_nk`, auditoría `_fuente` + `_cargado_en`, cron `17 3 * * *`, 2 retries /
     15 min / alerta al agotar, idempotencia (WRITE_TRUNCATE + guarda MAX).
   - `contexto_kpis.md` → grano y KPIs firmados: las ventas diarias son
     tienda × día; `campana_id` puede venir vacío y NO se imputa (las métricas
     de campaña van separadas).
   - `contexto_calidad.md` → política: toda fct lleva assertions `uniqueKey` +
     `nonNull` como pasos que deben devolver cero violaciones.
3. **Leyó `templates/workflow_ingesta_template.yaml` y
   `templates/modelo_incremental_template.sql`** → estructura a respetar.
   Nadie le pegó la plantilla: fue a buscarla él.
4. **Escribió la propuesta en `output/workflows/`** (nunca en producción):
   un solo fichero autocontenido, `ingesta_ventas_offline.yaml` — carga +
   modelo stg + modelo fct + pasos de assertion.
5. **Lo resolvió TODO desde los documentos firmados** (la prueba está en la
   cabecera que escribió): grano tienda × día, métricas y claves directos de
   `contexto_kpis.md`; assertions de `contexto_calidad.md`; defaults de
   `contexto_equipo.md`. **Cero decisiones abiertas: venía todo escrito.**
   Mensaje para la sala: cuanto mejor está escrito el contexto del equipo,
   menos hay que decidir sobre la marcha.

## La revisión (voz alta)

Como el pipeline es NUEVO, su diff es entero en sumas (+176 líneas desde
`/dev/null`): `output/pr_demo_a_nueva.txt`. Limpio de canon: cron
`17 3 * * *` en el bloque INFRA, retry/backoff del equipo, esquema declarado
(autodetect off), WRITE_TRUNCATE, `_nk`, `_fuente` + `_cargado_en`,
incremental con guarda `MAX(fecha)` y las dos assertions. Sin decisiones
abiertas pendientes: canon, catálogo y encargo lo cubrían todo.

*«El flujo de revisión es el mismo que con código humano.»* — y se firmó.

## La primera ejecución: FAILED (y eso es lo bueno)

Desplegado tras la PR aprobada → **primera ejecución FAILED**. No por la
lógica de negocio: la condición de validación leía `rows` en la respuesta de
BigQuery, y `rows` NO EXISTE cuando la query devuelve cero filas — que es
justo cuando las assertions pasan. El pipeline fallaba POR IR BIEN.

Diagnóstico en segundos (el error lo decía: KeyError rows), corrección a
`totalRows`, segunda ejecución: **SUCCEEDED**, 11 s, result "ok".

La lección, dicha sin adornos: el diff estaba limpio en la revisión y aun así
falló al correr. Por eso la PR incluye la prueba en seco, y por eso el primer
despliegue se hace con alguien delante.

## Estado final materializado

| Pieza | Resultado |
|---|---|
| Workflow `ingesta_ventas_offline` | revisión 000002-fa5, ACTIVE |
| Segunda ejecución | **SUCCEEDED** — `output/log_workflow_verde_ventas.txt` |
| raw / stg | 30.000 filas (staging con `_fuente` + `_cargado_en`) |
| `fct_ventas_diarias` | incremental con guarda: 0 filas nuevas al estar al día (idempotencia real) |
| assertions | 0 violaciones `uniqueKey(fecha, tienda_nk)`, 0 nulos |

Artefactos: `output/_primer_intento/` (la v0 con el bug), `diff_demo_a.patch`
(v0 → final: la corrección), `q01_carga_ventas_offline.txt`,
`q02_modelo_fct_ventas.txt` (17.030 filas, 533 días en la primera carga).

Pregunta de cierre a la sala: *"¿Cuánto habríais tardado en escribir esto
desde cero? ¿Cuánto hemos tardado? ¿Dónde se ha ido ese tiempo ahorrado?"* —
a revisar y decidir, no a teclear.
