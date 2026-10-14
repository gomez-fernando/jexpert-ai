SELECT
  COUNT(*) AS total,
  COUNTIF(contacto_id IS NULL) AS anonimas,
  SAFE_DIVIDE(COUNTIF(contacto_id IS NULL), COUNT(*)) AS pct_anonimas,
  COUNTIF(is_test) AS ventas_test
FROM `jakamedy-data-ia.demo_modelado.ventas_offline`;
