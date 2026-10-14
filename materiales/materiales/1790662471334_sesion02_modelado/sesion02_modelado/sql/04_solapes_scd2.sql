SELECT
  a.contacto_id,
  a.fecha_desde AS a_desde,
  a.fecha_hasta AS a_hasta,
  b.fecha_desde AS b_desde,
  b.fecha_hasta AS b_hasta
FROM `jakamedy-data-ia.demo_modelado.segmentos_contacto_hist` a
JOIN `jakamedy-data-ia.demo_modelado.segmentos_contacto_hist` b
  ON a.contacto_id = b.contacto_id
 AND a.fecha_desde < b.fecha_desde
 AND COALESCE(a.fecha_hasta, DATE '9999-12-31') > b.fecha_desde;
