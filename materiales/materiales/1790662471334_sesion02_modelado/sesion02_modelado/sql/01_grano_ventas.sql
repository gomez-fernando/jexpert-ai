SELECT
  COUNT(*) AS filas,
  COUNT(DISTINCT ticket_id) AS tickets,
  COUNT(DISTINCT CONCAT(ticket_id, '|', FORMAT_DATE('%F', DATE(fecha_hora_venta)))) AS tickets_dia
FROM `jakamedy-data-ia.demo_modelado.ventas_offline`;
