-- q02 · Demo A: modelo fct_ventas_diarias ejecutado (run inicial del incre-
-- mental sobre el historico completo). El mismo SQL que lleva el paso
-- modelo_fct del workflow generado por el agente.
CREATE TABLE IF NOT EXISTS `jakamedy-data-ia.demo_ops.fct_ventas_diarias` (
  fecha           DATE    NOT NULL,
  tienda_nk       STRING  NOT NULL,
  tickets         INT64,
  unidades        INT64,
  importe_total   FLOAT64,
  tickets_campana INT64
)
PARTITION BY fecha
CLUSTER BY tienda_nk
OPTIONS (
  description = 'Ventas agregadas por tienda y dia. Grano: tienda x dia. Fuente: demo_ops.stg_ventas_offline.'
);

INSERT INTO `jakamedy-data-ia.demo_ops.fct_ventas_diarias`
  (fecha, tienda_nk, tickets, unidades, importe_total, tickets_campana)
SELECT
  fecha,
  tienda_nk,
  COUNT(DISTINCT ticket_nk) AS tickets,
  SUM(unidades)             AS unidades,
  ROUND(SUM(importe), 2)    AS importe_total,
  COUNTIF(campana_id IS NOT NULL AND campana_id != "") AS tickets_campana
FROM `jakamedy-data-ia.demo_ops.stg_ventas_offline`
WHERE fecha > COALESCE(
  (SELECT MAX(fecha) FROM `jakamedy-data-ia.demo_ops.fct_ventas_diarias`),
  DATE '1900-01-01'
)
GROUP BY fecha, tienda_nk;
