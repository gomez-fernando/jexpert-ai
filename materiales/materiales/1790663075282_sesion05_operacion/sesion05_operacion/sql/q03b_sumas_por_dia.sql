-- q03b · Verificacion paso 2 (demo B): comparar volumenes y sumas por dia antes
-- y despues del rename. Descarta perdida de dato y CAMBIO DE SEMANTICA
-- (que el rename no venga con otra cosa debajo, p. ej. impuestos incluidos).
WITH dias AS (
  SELECT fecha, COUNT(*) AS filas, ROUND(SUM(importe), 2) AS suma, 'antes' AS tramo
  FROM `jakamedy-data-ia.demo_ops.fct_ingesta_diaria`
  GROUP BY fecha
  UNION ALL
  SELECT fecha, COUNT(*), ROUND(SUM(total_importe), 2), 'despues'
  FROM `jakamedy-data-ia.demo_ops.stg_ingesta_diaria`
  GROUP BY fecha
)
SELECT * FROM dias
ORDER BY fecha;
