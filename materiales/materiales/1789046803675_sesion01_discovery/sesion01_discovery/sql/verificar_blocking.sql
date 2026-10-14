-- Verifica que blocking.sql produce exactamente lo diseñado:
--   20 telefono_exacto            (20 matches, 0 falsos positivos)
--   10 nombre_empresa_sin_telefono (10 matches, 0 falsos positivos)
--   10 nombre_parecido_y_empresa   (0 matches, 10 falsos positivos)
--
-- La verdad NO se deduce de los IDs (los identificadores de origen no
-- codifican la identidad): se contrasta con la tabla de verdad.
-- Requiere cargar data/pares_esperados.json como
-- `jakamedy-data-ia.demo_discovery.pares_esperados`
-- (columnas: crm_id STRING, evento_id STRING, es_misma_entidad BOOL).
WITH candidate_pairs AS (
  SELECT
    c.id_lead AS crm_id,
    e.id_asistente AS evento_id,
    'telefono_exacto' AS blocking_reason,
    1 AS priority
  FROM `jakamedy-data-ia.demo_discovery.leads_crm` AS c
  JOIN `jakamedy-data-ia.demo_discovery.leads_evento` AS e
    ON REGEXP_REPLACE(c.tel, r'[^0-9]', '') = REGEXP_REPLACE(e.telefono, r'[^0-9]', '')

  UNION ALL

  SELECT
    c.id_lead,
    e.id_asistente,
    CASE
      WHEN (e.telefono IS NULL OR TRIM(e.telefono) = '')
        AND NORMALIZE_AND_CASEFOLD(CONCAT(c.nombre, ' ', c.apellido)) = NORMALIZE_AND_CASEFOLD(e.nombre)
      THEN 'nombre_empresa_sin_telefono'
      ELSE 'nombre_parecido_y_empresa'
    END,
    CASE
      WHEN NORMALIZE_AND_CASEFOLD(CONCAT(c.nombre, ' ', c.apellido)) = NORMALIZE_AND_CASEFOLD(e.nombre) THEN 2
      ELSE 3
    END
  FROM `jakamedy-data-ia.demo_discovery.leads_crm` AS c
  JOIN `jakamedy-data-ia.demo_discovery.leads_evento` AS e
    ON c.empresa = e.empresa
    AND SOUNDEX(UPPER(NORMALIZE_AND_CASEFOLD(CONCAT(c.nombre, ' ', c.apellido)))) = SOUNDEX(UPPER(NORMALIZE_AND_CASEFOLD(e.nombre)))
    AND COALESCE(REGEXP_REPLACE(c.tel, r'[^0-9]', ''), '') != COALESCE(REGEXP_REPLACE(e.telefono, r'[^0-9]', ''), '')
), limited AS (
  SELECT *
  FROM candidate_pairs
  ORDER BY priority, crm_id, evento_id
  LIMIT 40
), classified AS (
  SELECT
    l.*,
    p.crm_id IS NOT NULL AS es_match_esperado
  FROM limited AS l
  LEFT JOIN `jakamedy-data-ia.demo_discovery.pares_esperados` AS p
    ON p.crm_id = l.crm_id AND p.evento_id = l.evento_id
)
SELECT
  blocking_reason,
  COUNT(*) AS candidatos,
  COUNTIF(es_match_esperado) AS matches_esperados,
  COUNTIF(NOT es_match_esperado) AS falsos_positivos,
  STRING_AGG(CONCAT(crm_id, '/', evento_id), ', ' ORDER BY crm_id, evento_id) AS pares
FROM classified
GROUP BY blocking_reason
ORDER BY MIN(priority);
