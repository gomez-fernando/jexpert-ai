SELECT contacto_id, COUNT(*) AS filas_vigentes
FROM `jakamedy-data-ia.demo_modelado.segmentos_contacto_hist`
WHERE flag_vigente
GROUP BY contacto_id
HAVING COUNT(*) != 1;
