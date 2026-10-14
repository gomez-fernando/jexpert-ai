SELECT 'leads_crm' AS tabla, COUNT(*) AS filas FROM `jakamedy-data-ia.demo_discovery.leads_crm`
UNION ALL
SELECT 'leads_evento', COUNT(*) FROM `jakamedy-data-ia.demo_discovery.leads_evento`;
