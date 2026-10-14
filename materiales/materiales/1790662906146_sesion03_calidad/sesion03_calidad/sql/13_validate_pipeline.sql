WITH routed AS (
  SELECT * FROM `jakamedy-data-ia.demo_calidad.stg_pedidos_routed`
), metrics AS (
  SELECT 'input_rows' AS metric, (SELECT COUNT(*) FROM `jakamedy-data-ia.demo_calidad.raw_pedidos_quarantine`) AS value
  UNION ALL SELECT 'routed_rows', COUNT(*) FROM routed
  UNION ALL SELECT 'clean_rows', COUNTIF(route = 'clean') FROM routed
  UNION ALL SELECT 'review_rows', COUNTIF(route = 'review') FROM routed
  UNION ALL SELECT 'reject_rows', COUNTIF(route = 'reject') FROM routed
  UNION ALL SELECT 'clean_null_importe', COUNTIF(route = 'clean' AND importe IS NULL) FROM routed
  UNION ALL SELECT 'clean_null_fecha', COUNTIF(route = 'clean' AND fecha_pedido IS NULL) FROM routed
  UNION ALL SELECT 'clean_bad_categoria', COUNTIF(route = 'clean' AND categoria IS NULL) FROM routed
  UNION ALL SELECT 'clean_duplicate_id', COUNT(*) FROM (
    SELECT pedido_id FROM routed WHERE route = 'clean' GROUP BY pedido_id HAVING COUNT(*) > 1
  )
  UNION ALL SELECT 'review_importe_vacio', COUNTIF(route = 'review' AND CONTAINS_SUBSTR(reason, 'importe vacío')) FROM routed
  UNION ALL SELECT 'review_duplicado_conflictivo', COUNTIF(route = 'review' AND CONTAINS_SUBSTR(reason, 'datos diferentes')) FROM routed
  UNION ALL SELECT 'review_outlier', COUNTIF(route = 'review' AND CONTAINS_SUBSTR(reason, '90000')) FROM routed
)
SELECT * FROM metrics ORDER BY metric;
