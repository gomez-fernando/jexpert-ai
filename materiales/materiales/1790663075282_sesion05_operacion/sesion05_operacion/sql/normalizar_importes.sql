-- Job nocturno del pipeline ingesta_diaria: stg_ingesta_diaria -> fct_ingesta_diaria.
-- ES LA VERSION ROTA A PROPOSITO: la fuente renombro importe_total -> total_importe
-- el 21/09/2026 sin aviso ni cambio de contrato. Este SQL no se ha tocado desde
-- antes del rename, por eso revienta con Unrecognized name: importe_total.
-- NO corregir este fichero: el fallo ES la demo B.
INSERT INTO `jakamedy-data-ia.demo_ops.fct_ingesta_diaria`
  (registro_nk, fecha, importe, tienda_nk)
SELECT
  CAST(registro_id AS STRING) AS registro_nk,
  fecha,
  CAST(importe_total AS FLOAT64) AS importe,
  tienda_id AS tienda_nk
FROM `jakamedy-data-ia.demo_ops.stg_ingesta_diaria`;
