-- q01 · Demo A: modelo staging ejecutado (el mismo SQL que lleva el paso
-- modelo_stg del workflow generado por el agente).
CREATE OR REPLACE TABLE `jakamedy-data-ia.demo_ops.stg_ventas_offline` AS
SELECT
  CAST(ticket_id AS STRING)      AS ticket_nk,
  CAST(tienda_id AS STRING)      AS tienda_nk,
  fecha,
  CAST(importe_total AS FLOAT64) AS importe,
  unidades,
  campana_id,
  "gs://jakamedy-data-ia-demo/raw/ventas_offline.csv" AS _fuente,
  CURRENT_TIMESTAMP()            AS _cargado_en
FROM `jakamedy-data-ia.demo_ops.raw_ventas_offline`;
