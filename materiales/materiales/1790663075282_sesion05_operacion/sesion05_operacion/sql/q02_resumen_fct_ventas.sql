-- q02 (cont.) · Resumen de la tabla materializada + recuento de nulos en claves
-- (nonNull). Nulos debe ser 0.
SELECT
  COUNT(*)                     AS filas,
  COUNT(DISTINCT fecha)        AS dias,
  COUNT(DISTINCT tienda_nk)    AS tiendas,
  ROUND(SUM(importe_total), 2) AS importe_total,
  SUM(tickets)                 AS tickets,
  COUNTIF(fecha IS NULL OR tienda_nk IS NULL) AS claves_nulas
FROM `jakamedy-data-ia.demo_ops.fct_ventas_diarias`;
