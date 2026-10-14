# Crítica de la propuesta v1 (ensayo real)

Checkpoint aplicado sobre `output/modelo_v1.md` + `output/modelo_v1_erd.mmd` con la
tabla de la sesión. Regla: cada defecto cita evidencia; no se critican convenciones
que el contexto acotado no entrega.

## Lo que está bien (no va al diff)

- Grano declarado y compatible con la fuente en los cuatro hechos (incluida la nota
  «no existe fuente de líneas de producto»).
- `campana_id` fuera de la venta; la relación vive en la tabla de atribución.
- Anónimas conservadas con miembro desconocido (coherente con el 40 % medido).
- Crosswalk preservado como puente de trazabilidad (`bridge_contacto_origen`).
- Sin producto, sin particionado, sin ROI inventado: «falta definición de ROI»
  aparece como riesgo explícito en lugar de fórmula.
- El propio modelo anticipa sus dos puntos débiles: dim_tienda sin atributos y la
  unicidad del grano de atribución.

## Defectos con evidencia (entran en el diff v1 → v2)

| Área | Defecto | Evidencia (ejecutada / firmada) | Corrección v2 |
|---|---|---|---|
| Semántica | `fct_atribucion_venta_campana` lleva FK a dim_fecha por `fecha_atribucion` | Firma: ventana = *mes de la venta atribuida*. En la fixture, fecha_atribucion = venta + 1 día: un ticket a fin de mes caería al mes siguiente en el ROI | El bridge hereda la fecha de `fct_venta`; la fecha de la métrica sale del hecho, no del puente |
| Naming | Claves naturales sin sufijo `_nk` (`contacto_id`, `campana_id`, `ticket_id`, …) | Contexto acotado: «Claves naturales: *_nk» | Sufijo `_nk` en todas las claves de negocio |
| SCD | Historia como dimensión hija (`dim_segmento_contacto_hist`) separada de `dim_contacto` | Arquitectura aprobada §9: `dim_contacto_scd` (la firma exige "vigente en la fecha de venta"; ambas cumplen, pero la casa ya tenía dueño) | Plegada en `dim_contacto_scd` (sk_contacto por intervalo), o justificar la mini-dimensión si convence a Data Governance |
| Entidades | `dim_tienda` sin un solo atributo propio | La fuente solo aporta `tienda_id`; ninguna pregunta de negocio la usa | Atributo degenerado en `fct_venta` (además ya riesgo señalado) |
| Naming | `fct_atribucion_*` y `bridge_contacto_origen` bajo prefijos de lo que no son | Contexto acotado: puentes = `bridge_*` solo para N:M con peso; el crosswalk es artefacto de integración | `bridge_venta_campana`; el crosswalk se llama `identity_crosswalk` |

## Respuestas que la v2 debe dar con las firmas ya existentes

- is_test: excluido en las métricas (firma Data Governance) — fue decisión abierta en v1.
- Grano de atribución: un modelo por ticket (la fixture: los pesos suman 1 por ticket en modelo y ventana únicos).
- Moneda: EUR única en la fixture; el contrato lo marca.

## Nota de proceso

El rendimiento del checklist no presuponía ningún fallo concreto: salieron cinco.
La tabla de decisiones firmadas entra íntegra en el prompt de iteración.
