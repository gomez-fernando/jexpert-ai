SELECT reason, COUNT(*) AS filas
FROM `jakamedy-data-ia.demo_calidad.stg_pedidos_propuesta_llm`
WHERE route = 'review'
GROUP BY reason
ORDER BY filas DESC
LIMIT 20;
