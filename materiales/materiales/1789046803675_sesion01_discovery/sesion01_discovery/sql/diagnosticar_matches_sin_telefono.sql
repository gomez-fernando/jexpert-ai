-- Diagnóstico: ¿los 10 matches reales sin teléfono tienen nombre fonéticamente
-- compatible con su contraparte del CRM? Si pasa_soundex es FALSE en alguno,
-- la segunda regla de blocking.sql no lo recuperaría.
--
-- Se apoya en la tabla de verdad (`jakamedy-data-ia.demo_discovery.pares_esperados`),
-- no en la correspondencia de IDs.
SELECT
  c.id_lead AS crm_id,
  e.id_asistente AS evento_id,
  CONCAT(c.nombre, ' ', c.apellido) AS crm_nombre,
  e.nombre AS evento_nombre,
  SOUNDEX(UPPER(NORMALIZE_AND_CASEFOLD(CONCAT(c.nombre, ' ', c.apellido)))) AS soundex_crm,
  SOUNDEX(UPPER(NORMALIZE_AND_CASEFOLD(e.nombre))) AS soundex_evento,
  SOUNDEX(UPPER(NORMALIZE_AND_CASEFOLD(CONCAT(c.nombre, ' ', c.apellido))))
    = SOUNDEX(UPPER(NORMALIZE_AND_CASEFOLD(e.nombre))) AS pasa_soundex
FROM `jakamedy-data-ia.demo_discovery.pares_esperados` AS p
JOIN `jakamedy-data-ia.demo_discovery.leads_crm` AS c
  ON c.id_lead = p.crm_id
JOIN `jakamedy-data-ia.demo_discovery.leads_evento` AS e
  ON e.id_asistente = p.evento_id
WHERE e.telefono IS NULL OR TRIM(e.telefono) = ''
ORDER BY c.id_lead;
