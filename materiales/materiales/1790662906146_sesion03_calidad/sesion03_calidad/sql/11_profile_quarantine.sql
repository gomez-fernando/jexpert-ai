WITH parsed AS (
  SELECT *,
    CASE
      WHEN ENDS_WITH(importe, CHR(8364)) THEN SAFE_CAST(REPLACE(REPLACE(REPLACE(importe, CHR(8364), ''), '.', ''), ',', '.') AS NUMERIC)
      ELSE SAFE_CAST(importe AS NUMERIC)
    END AS importe_num
  FROM `jakamedy-data-ia.demo_calidad.raw_pedidos_quarantine`
)
SELECT
  COUNT(*) AS filas,
  COUNT(*) - COUNT(DISTINCT pedido_id) AS filas_id_repetido,
  COUNTIF(importe IS NULL OR importe = '') AS importe_vacio,
  COUNTIF(ENDS_WITH(importe, CHR(8364))) AS importe_europeo,
  COUNTIF(REGEXP_CONTAINS(fecha_pedido, r'^\d{4}-\d{2}-\d{2}$')) AS fecha_iso,
  COUNTIF(categoria IN ('Electronics','Home','Fashion','Sports','Beauty','Grocery')) AS categoria_ingles,
  COUNTIF(importe_num > 90000) AS outliers_mayor_90000
FROM parsed;
