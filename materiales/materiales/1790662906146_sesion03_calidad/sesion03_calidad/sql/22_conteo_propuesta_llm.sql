SELECT route, COUNT(*) AS filas
FROM `jakamedy-data-ia.demo_calidad.stg_pedidos_propuesta_llm`
GROUP BY route ORDER BY route;
