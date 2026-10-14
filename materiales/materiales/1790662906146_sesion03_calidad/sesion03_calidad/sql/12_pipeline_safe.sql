CREATE OR REPLACE TABLE `jakamedy-data-ia.demo_calidad.stg_pedidos_routed` AS
WITH source AS (
  SELECT * FROM `jakamedy-data-ia.demo_calidad.raw_pedidos_quarantine`
), duplicate_profile AS (
  SELECT
    pedido_id,
    COUNT(*) AS rows_per_id,
    COUNT(DISTINCT TO_JSON_STRING(STRUCT(fecha_pedido, importe, categoria, cliente_id, unidades))) AS variants_per_id
  FROM `jakamedy-data-ia.demo_calidad.raw_pedidos_quarantine`
  GROUP BY pedido_id
), parsed AS (
  SELECT
    s.*,
    d.rows_per_id,
    d.variants_per_id,
    CASE
      WHEN importe IS NULL OR importe = '' THEN NULL
      WHEN ENDS_WITH(importe, CHR(8364)) THEN SAFE_CAST(REPLACE(REPLACE(REPLACE(importe, CHR(8364), ''), '.', ''), ',', '.') AS NUMERIC)
      ELSE SAFE_CAST(importe AS NUMERIC)
    END AS importe_num,
    SAFE.PARSE_DATE('%Y-%m-%d', fecha_pedido) AS fecha_pedido_date,
    m.categoria_canonica AS categoria_norm,
    SAFE_CAST(unidades AS INT64) AS unidades_num
  FROM source s
  JOIN duplicate_profile d USING (pedido_id)
  LEFT JOIN `jakamedy-data-ia.demo_calidad.category_mapping` m
    ON s.categoria = m.categoria_raw
), classified AS (
  SELECT *,
    (importe IS NULL OR importe = '') AS importe_vacio,
    (importe_num < 0) AS importe_negativo,
    (rows_per_id > 1 AND variants_per_id > 1) AS duplicado_conflictivo,
    (importe_num > 90000) AS importe_outlier,
    (categoria_norm IS NULL) AS categoria_desconocida,
    (unidades_num IS NULL OR unidades_num <= 0) AS unidades_invalidas
  FROM parsed
)
SELECT
  source_row_id,
  pedido_id,
  fecha_pedido AS fecha_pedido_raw,
  fecha_pedido_date AS fecha_pedido,
  importe AS importe_raw,
  importe_num AS importe,
  categoria AS categoria_raw,
  categoria_norm AS categoria,
  cliente_id,
  unidades_num AS unidades,
  CASE
    WHEN importe_negativo OR unidades_invalidas THEN 'reject'
    WHEN importe_vacio OR duplicado_conflictivo OR categoria_desconocida OR importe_outlier THEN 'review'
    ELSE 'clean'
  END AS route,
  ARRAY_TO_STRING(
    ARRAY(
      SELECT reason FROM UNNEST([
        IF(importe_vacio, 'importe vacío', NULL),
        IF(importe_negativo, 'importe negativo', NULL),
        IF(duplicado_conflictivo, 'pedido_id repetido con datos diferentes', NULL),
        IF(categoria_desconocida, 'categoría fuera del mapping aprobado', NULL),
        IF(importe_outlier, 'importe superior a 90000 EUR', NULL),
        IF(unidades_invalidas, 'unidades no positivas o inválidas', NULL)
      ]) AS reason
      WHERE reason IS NOT NULL
    ), '; '
  ) AS reason
FROM classified;

CREATE OR REPLACE VIEW `jakamedy-data-ia.demo_calidad.stg_pedidos_clean` AS
SELECT * EXCEPT(route, reason) FROM `jakamedy-data-ia.demo_calidad.stg_pedidos_routed` WHERE route = 'clean';

CREATE OR REPLACE VIEW `jakamedy-data-ia.demo_calidad.review_pedidos` AS
SELECT * FROM `jakamedy-data-ia.demo_calidad.stg_pedidos_routed` WHERE route = 'review';

CREATE OR REPLACE VIEW `jakamedy-data-ia.demo_calidad.reject_pedidos` AS
SELECT * FROM `jakamedy-data-ia.demo_calidad.stg_pedidos_routed` WHERE route = 'reject';
