CREATE TEMP TABLE fila_error AS
-- La fila que abortó el job (line_number 2 del CSV = P0006487, 16,93€)
SELECT pedido_id, fecha_pedido, importe, categoria, cliente_id, unidades
FROM `jakamedy-data-ia.demo_calidad.raw_pedidos_quarantine`
WHERE pedido_id = 'P0006487';

CREATE TEMP TABLE azar AS
SELECT pedido_id, fecha_pedido, importe, categoria, cliente_id, unidades
FROM `jakamedy-data-ia.demo_calidad.raw_pedidos_quarantine`
TABLESAMPLE SYSTEM (10 PERCENT);

SELECT * FROM fila_error
UNION ALL
SELECT * FROM azar
LIMIT 15;
