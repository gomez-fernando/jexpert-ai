-- informe_roi_campana_mes.sql · SQL heredado de Vivento · CONGELADO 23/09/2026
-- Versión exacta ejecutada con el prompt P2 (lineage). No editar sin abrir decisión.
CREATE OR REPLACE TABLE gold.informe_roi_campana_mes AS
SELECT
  FORMAT_DATE('%Y-%m', df.fecha)              AS mes,
  c.nombre                                     AS campana,
  SUM(f.importe_neto * a.peso_atribucion)      AS venta_atribuida,
  MAX(s.presupuesto) / DATE_DIFF(c.fecha_fin, c.fecha_inicio, DAY) * 30
                                               AS coste_imputado_mes,
  SUM(f.importe_neto * a.peso_atribucion)
    / (MAX(s.presupuesto) / DATE_DIFF(c.fecha_fin, c.fecha_inicio, DAY) * 30)
                                               AS roi
FROM gold.fct_venta f
JOIN gold.fct_atribucion_venta_campana a ON a.ticket_id = f.ticket_id
JOIN gold.dim_fecha df               ON df.sk_fecha = a.sk_fecha
LEFT JOIN gold.dim_contacto d        ON d.sk_contacto = f.sk_contacto
JOIN gold.dim_segmento_contacto_hist h
  ON h.contacto_id = d.contacto_id AND h.flag_vigente
JOIN gold.dim_campana c              ON c.sk_campana = a.sk_campana
JOIN gold.fct_spend_campana_diario s ON s.sk_campana = c.sk_campana
WHERE a.modelo_atribucion = 'lineal'
GROUP BY mes, campana
