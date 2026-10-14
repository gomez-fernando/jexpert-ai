-- q02 (cont.) · Assertions del modelo fct_ventas_diarias, ejecutadas a mano.
-- uniqueKey(fecha, tienda_nk): debe devolver 0 filas.
SELECT fecha, tienda_nk, COUNT(*) AS duplicados
FROM `jakamedy-data-ia.demo_ops.fct_ventas_diarias`
GROUP BY fecha, tienda_nk
HAVING COUNT(*) > 1;
