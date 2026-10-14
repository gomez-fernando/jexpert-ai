-- q04 · Post-check tras el merge del parche: fct_ingesta_diaria completa.
SELECT
  MIN(fecha) AS fecha_min,
  MAX(fecha) AS fecha_max,
  COUNT(*) AS filas,
  COUNT(DISTINCT fecha) AS dias,
  COUNTIF(importe IS NULL) AS nulos
FROM `jakamedy-data-ia.demo_ops.fct_ingesta_diaria`;
