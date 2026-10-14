SELECT pedido_id, cliente_id, importe
FROM `jakamedy-data-ia.demo_calidad.raw_pedidos_quarantine`
WHERE pedido_id IN ('P0045129','P0045479','P0041197','P0035556','P0043598','P0032200','P0011928')
ORDER BY pedido_id;
