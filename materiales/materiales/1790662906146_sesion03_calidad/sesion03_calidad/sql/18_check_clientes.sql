SELECT
  COUNT(*) AS filas,
  COUNT(DISTINCT cliente_id) AS clientes_distintos,
  COUNTIF(cliente_id = 'CT000001') AS filas_ct000001
FROM `jakamedy-data-ia.demo_calidad.raw_pedidos_quarantine`;
