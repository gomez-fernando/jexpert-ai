WITH golden AS (
  SELECT * FROM `jakamedy-data-ia.demo_calidad.pedidos_dorado`
), predictions AS (
  SELECT 'naive' AS pipeline, source_row_id, fecha_pedido, importe, categoria, cliente_id, unidades, route
  FROM `jakamedy-data-ia.demo_calidad.stg_pedidos_naive`
  UNION ALL
  SELECT 'safe' AS pipeline, source_row_id, fecha_pedido, importe, categoria, cliente_id, unidades, route
  FROM `jakamedy-data-ia.demo_calidad.stg_pedidos_routed`
), compared AS (
  SELECT
    p.pipeline,
    p.source_row_id,
    g.expected_route,
    p.route,
    p.fecha_pedido IS NOT DISTINCT FROM g.fecha_pedido
      AND p.importe IS NOT DISTINCT FROM g.importe
      AND p.categoria = g.categoria
      AND p.cliente_id = g.cliente_id
      AND p.unidades = g.unidades AS fields_match
  FROM predictions p
  JOIN golden g USING (source_row_id)
)
SELECT
  pipeline,
  COUNT(*) AS golden_rows,
  COUNTIF(fields_match AND route = expected_route) AS exact_match,
  COUNTIF(fields_match AND route = 'clean' AND expected_route = 'clean') AS clean_correct,
  COUNTIF(fields_match AND route = 'review' AND expected_route = 'review') AS review_correct,
  COUNTIF(route = 'clean' AND NOT fields_match) AS silent_field_error,
  COUNTIF(route = 'clean' AND expected_route = 'review') AS missed_review,
  COUNTIF(route = 'review' AND expected_route = 'clean') AS unnecessary_review,
  COUNTIF(route = expected_route) AS route_correct
FROM compared
GROUP BY pipeline
ORDER BY pipeline;
