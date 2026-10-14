SELECT ticket_id, SUM(peso_atribucion) AS peso_total
FROM `jakamedy-data-ia.demo_modelado.atribucion_venta_campana`
GROUP BY ticket_id
HAVING ABS(SUM(peso_atribucion) - 1) > 0.0001;
