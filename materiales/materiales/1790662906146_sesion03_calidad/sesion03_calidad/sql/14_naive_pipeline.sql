CREATE OR REPLACE TABLE `jakamedy-data-ia.demo_calidad.stg_pedidos_naive` AS
WITH parsed AS (
  SELECT
    source_row_id,
    pedido_id,
    SAFE.PARSE_DATE('%Y-%m-%d', fecha_pedido) AS fecha_pedido,
    -- "el hábito": quita el símbolo y las comas como si fueran separadores de miles
    SAFE_CAST(REPLACE(REPLACE(importe, CHR(8364), ''), ',', '') AS NUMERIC) AS importe,
    m.categoria_canonica AS categoria,
    cliente_id,
    SAFE_CAST(unidades AS INT64) AS unidades
  FROM `jakamedy-data-ia.demo_calidad.raw_pedidos_quarantine` q
  LEFT JOIN `jakamedy-data-ia.demo_calidad.category_mapping` m
    ON q.categoria = m.categoria_raw
)
SELECT
  *,
  IF(importe IS NULL, 'review', 'clean') AS route
FROM parsed;
