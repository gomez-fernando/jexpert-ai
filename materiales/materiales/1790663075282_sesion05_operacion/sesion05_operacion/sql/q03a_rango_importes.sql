-- q03a · Verificacion paso 1 (demo B): rango y nulos de la columna RENOMBRADA
-- frente al historico ya cargado antes del rename.
SELECT
  'historico fct (pre-rename)' AS tramo,
  MIN(importe) AS min_importe,
  MAX(importe) AS max_importe,
  COUNT(*) AS filas,
  COUNTIF(importe IS NULL) AS nulos
FROM `jakamedy-data-ia.demo_ops.fct_ingesta_diaria`
UNION ALL
SELECT
  'fuente nueva (post-rename)' AS tramo,
  MIN(total_importe),
  MAX(total_importe),
  COUNT(*),
  COUNTIF(total_importe IS NULL)
FROM `jakamedy-data-ia.demo_ops.stg_ingesta_diaria`;
