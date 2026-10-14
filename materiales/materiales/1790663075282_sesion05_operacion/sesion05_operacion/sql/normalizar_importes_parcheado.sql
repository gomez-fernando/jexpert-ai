-- Job normalizar_importes PARCHEADO (propuesta del agente, mergeada por un humano).
-- Parche minimo: alias que mantiene el contrato aguas abajo.
-- Ojo: es un parche, no la solucion. La solucion es actualizar el contrato de
-- esquema con el equipo origen (lo que enseno la S3).
INSERT INTO `jakamedy-data-ia.demo_ops.fct_ingesta_diaria`
  (registro_nk, fecha, importe, tienda_nk)
SELECT
  CAST(registro_id AS STRING) AS registro_nk,
  fecha,
  CAST(total_importe AS FLOAT64) AS importe,   -- antes: CAST(importe_total AS FLOAT64)
  tienda_id AS tienda_nk
FROM `jakamedy-data-ia.demo_ops.stg_ingesta_diaria`;
