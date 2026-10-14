SELECT
  COUNTIF(v.contacto_id IS NOT NULL AND c.contacto_id IS NULL) AS ventas_contacto_huerfano,
  COUNTIF(a.campana_id IS NOT NULL AND cp.campana_id IS NULL) AS atribuciones_campana_huerfana
FROM `jakamedy-data-ia.demo_modelado.ventas_offline` v
LEFT JOIN `jakamedy-data-ia.demo_modelado.contactos` c USING (contacto_id)
LEFT JOIN `jakamedy-data-ia.demo_modelado.atribucion_venta_campana` a USING (ticket_id)
LEFT JOIN `jakamedy-data-ia.demo_modelado.campanas` cp USING (campana_id);
