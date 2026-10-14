WITH labelled AS (
  SELECT
    source_row_id,
    pedido_id,
    fecha_pedido_raw,
    importe_raw,
    categoria_raw,
    reason,
    CASE
      WHEN CONTAINS_SUBSTR(reason, 'importe vacío') THEN 'importe_vacio'
      WHEN CONTAINS_SUBSTR(reason, 'datos diferentes') THEN 'duplicado_conflictivo'
      WHEN CONTAINS_SUBSTR(reason, '90000') THEN 'outlier'
      ELSE 'otro'
    END AS case_type
  FROM `jakamedy-data-ia.demo_calidad.review_pedidos`
)
SELECT *
FROM labelled
QUALIFY ROW_NUMBER() OVER (PARTITION BY case_type ORDER BY source_row_id) = 1
ORDER BY case_type;
