# Lineage — gold.informe_roi_campana_mes

Análisis del SQL `informe_roi_campana_mes.sql` (versión de trabajo heredada). No se ha reescrito el SQL ni se han propuesto mejoras; el alcance es únicamente identificar lineage y riesgos.

## Deliverable (JSON)

```json
{
  "tablas_origen": [
    "gold.fct_venta",
    "gold.fct_atribucion_venta_campana",
    "gold.dim_fecha",
    "gold.dim_contacto",
    "gold.dim_segmento_contacto_hist",
    "gold.dim_campana",
    "gold.fct_spend_campana_diario"
  ],
  "tabla_destino": "gold.informe_roi_campana_mes",
  "transformaciones": [
    {
      "destino": "mes",
      "origenes": ["gold.dim_fecha.fecha"],
      "logica": "FORMAT_DATE('%Y-%m', df.fecha) sobre la fecha asociada al registro de atribución (df se une por a.sk_fecha, no por la fecha de venta)."
    },
    {
      "destino": "campana",
      "origenes": ["gold.dim_campana.nombre"],
      "logica": "Se propaga directamente el nombre de campaña, sin transformación."
    },
    {
      "destino": "venta_atribuida",
      "origenes": ["gold.fct_venta.importe_neto", "gold.fct_atribucion_venta_campana.peso_atribucion"],
      "logica": "SUM(importe_neto * peso_atribucion) agrupado por mes y campaña, filtrando solo filas con modelo_atribucion = 'lineal'."
    },
    {
      "destino": "coste_imputado_mes",
      "origenes": ["gold.fct_spend_campana_diario.presupuesto", "gold.dim_campana.fecha_inicio", "gold.dim_campana.fecha_fin"],
      "logica": "MAX(presupuesto) del spend diario de la campaña, dividido entre la duración total de la campaña en días y multiplicado por 30 (prorrateo mensual de un presupuesto asumido constante)."
    },
    {
      "destino": "roi",
      "origenes": ["venta_atribuida (calculado)", "coste_imputado_mes (calculado)"],
      "logica": "venta_atribuida / coste_imputado_mes; hereda todos los orígenes de ambas columnas derivadas."
    }
  ],
  "riesgos": [
    "fct_spend_campana_diario tiene grano diario (campaña x día) y se une por sk_campana sin agregar antes del join principal ni filtrar por rango de fechas: si el número de filas de spend por campaña cambia (más o menos días con registro), se duplican las filas de f y a antes del SUM, inflando o desinflando venta_atribuida y, en cascada, roi — un cambio silencioso en la cardinalidad de esta fuente rompe el cálculo sin que salte ningún error.",
    "dim_contacto se une con LEFT JOIN, pero dim_segmento_contacto_hist se une inmediatamente después con INNER JOIN sobre d.contacto_id: cualquier venta sin contacto resuelto (d NULL) queda excluida igualmente, anulando en la práctica el LEFT JOIN. Si crece la proporción de ventas sin contacto identificado, el informe subestima venta_atribuida sin aviso.",
    "dim_segmento_contacto_hist filtra por h.flag_vigente: si un contacto no tiene fila vigente en el momento de la carga (gap de vigencia), sus ventas caen del resultado por el INNER JOIN, igual que arriba.",
    "El catálogo marca sk_fecha en fct_atribucion_venta_campana como PENDIENTE de confirmar (fecha del touchpoint vs. fecha de venta vs. otra). La columna 'mes' del informe depende de esa semántica; si se aclara y no coincide con lo asumido hoy, el mes de todo el informe queda mal definido retroactivamente.",
    "coste_imputado_mes usa DATE_DIFF(c.fecha_fin, c.fecha_inicio, DAY) en el denominador: una campaña con fecha_fin nula (campaña abierta/en curso) o con fecha_fin = fecha_inicio produce NULL o división por cero, propagando NULL a coste_imputado_mes y roi para esa campaña.",
    "El filtro WHERE a.modelo_atribucion = 'lineal' está hardcodeado: si el owner de fct_atribucion_venta_campana renombra o retira ese valor del modelo de atribución (por ejemplo, versiona 'lineal' como 'lineal_v2'), la query no falla — simplemente deja de devolver filas, y el informe se vacía silenciosamente.",
    "MAX(s.presupuesto) asume que presupuesto es un valor constante repetido por día dentro de fct_spend_campana_diario (es decir, el presupuesto total de la campaña, no el gasto diario real). Si esa fuente pasa a registrar gasto diario variable en vez de presupuesto fijo, MAX ya no representa el presupuesto total y coste_imputado_mes queda mal calculado sin ningún error visible."
  ]
}
```

## Nota de fuente

El campo `sk_fecha` de `gold.fct_atribucion_venta_campana` está marcado como pendiente de confirmar en el catálogo interno (touchpoint vs. venta vs. otra fecha de referencia), lo cual sustenta el riesgo señalado arriba sobre la columna `mes`.
