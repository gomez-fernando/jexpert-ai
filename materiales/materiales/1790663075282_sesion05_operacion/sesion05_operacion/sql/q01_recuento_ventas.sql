-- q01 (cont.) · Recuento de control tras la carga y la normalizacion.
SELECT 'raw_ventas_offline' AS tabla, COUNT(*) AS filas,
       MIN(fecha) AS fecha_min, MAX(fecha) AS fecha_max
FROM `jakamedy-data-ia.demo_ops.raw_ventas_offline`
UNION ALL
SELECT 'stg_ventas_offline', COUNT(*), MIN(fecha), MAX(fecha)
FROM `jakamedy-data-ia.demo_ops.stg_ventas_offline`;
