---
name: generar-pipeline-workflows
description: Genera un pipeline completo del equipo (Cloud Workflow + modelos SQL versionados, staging e incremental con assertions como pasos) a partir de una descripción en lenguaje natural, respetando las plantillas y convenciones del equipo. Usar cuando se pida crear una ingesta nueva de fichero a BigQuery con su modelo gold.
---

# Generar pipeline orquestado con Workflows — Equipo Data

## Cuándo usar esta skill

Cuando se pida crear un pipeline nuevo de ingesta (fichero en Cloud Storage →
BigQuery → modelos SQL). No usar para pipelines de streaming ni CDC.

## Antes de escribir nada

Lee los tres contextos del equipo — son documentos firmados que se han ido
acordando a lo largo del proyecto:

1. `sesion05_operacion/contexto_equipo.md` — canon operativo: stack, naming,
   capas, defaults de workflow, reglas con agentes.
2. `sesion05_operacion/contexto_kpis.md` — KPIs y grano acordados; si tu tabla
   afecta a un KPI vigente, respétalo o abre decisión abierta.
3. `sesion05_operacion/contexto_calidad.md` — política de calidad: qué
   assertions lleva toda fct y cómo se comportan.

Después:

4. Lee `sesion05_operacion/templates/workflow_ingesta_template.yaml` y
   `sesion05_operacion/templates/modelo_incremental_template.sql`. No te
   desvíes de su estructura.
5. Si la descripción del encargo no especifica: frecuencia, nombre de tabla
   destino, columna de fecha para particionar o clave única → **pregunta antes
   de generar** o enuméralo como DECISIÓN ABIERTA.

## Qué generar

1. **Un solo artefacto:**
   `sesion05_operacion/output/workflows/ingesta_<fuente>.yaml` a partir de la
   plantilla — workflow autocontenido con carga, modelo staging, modelo fct
   incremental y los pasos de assertion.
   - Ajustar SOLO lo marcado como CONFIG.
   - NUNCA modificar los defaults del equipo (retry/backoff, alerta, guarda
     de idempotencia, comentario INFRA con el cron).
   - Staging siempre con `_fuente` y `_cargado_en`.
   - Todo `fct_` es incremental (guarda `MAX(fecha)`), y la tabla va
     particionada por fecha y cluster por la clave de negocio (DDL en
     `sql/` si no existe).
   - Pasos finales de **assertion** (`uniqueKey` y `nonNull`): queries que
     deben devolver cero violaciones o el workflow va a rojo. Sin excepción.
2. Un bloque final de texto con:
   - Lista de archivos creados/modificados.
   - DECISIONES ABIERTAS (todo lo asumido sin confirmar).
   - Qué debe revisar el ingeniero antes de aprobar el despliegue.

## Reglas

- El código generado pasa por revisión humana como cualquier código del
  equipo. Nunca desplegar el workflow ni ejecutar contra `fct_` sin aprobación.
- Ninguna tabla `fct_` nueva sin sus pasos de assertion en el workflow.
- Si la fuente tiene PII, avisar explícitamente: aplican las políticas de
  `contexto_equipo.md` (pseudonimización antes de salir del perímetro).
