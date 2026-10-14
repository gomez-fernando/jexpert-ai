SELECT
  COUNT(*) AS total_filas,
  COUNT(DISTINCT cliente_id) AS clientes_distintos,
  ROUND(COUNT(DISTINCT cliente_id) * 100.0 / COUNT(*), 4) AS pct_valores_distintos
FROM `jakamedy-data-ia.demo_calidad.raw_pedidos_quarantine`;
