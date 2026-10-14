WITH candidate_pairs AS (
  SELECT
    c.id_lead AS crm_id,
    e.id_asistente AS evento_id,
    CONCAT(c.nombre, ' ', c.apellido) AS crm_nombre,
    e.nombre AS evento_nombre,
    c.mail_contacto AS crm_email,
    e.email AS evento_email,
    c.tel AS crm_telefono,
    e.telefono AS evento_telefono,
    c.empresa AS crm_empresa,
    e.empresa AS evento_empresa,
    'telefono_exacto' AS blocking_reason,
    1 AS priority
  FROM `jakamedy-data-ia.demo_discovery.leads_crm` AS c
  JOIN `jakamedy-data-ia.demo_discovery.leads_evento` AS e
    ON REGEXP_REPLACE(c.tel, r'[^0-9]', '') = REGEXP_REPLACE(e.telefono, r'[^0-9]', '')

  UNION ALL

  SELECT
    c.id_lead,
    e.id_asistente,
    CONCAT(c.nombre, ' ', c.apellido),
    e.nombre,
    c.mail_contacto,
    e.email,
    c.tel,
    e.telefono,
    c.empresa,
    e.empresa,
    CASE
      WHEN (e.telefono IS NULL OR TRIM(e.telefono) = '')
        AND NORMALIZE_AND_CASEFOLD(CONCAT(c.nombre, ' ', c.apellido)) = NORMALIZE_AND_CASEFOLD(e.nombre)
      THEN 'nombre_empresa_sin_telefono'
      ELSE 'nombre_parecido_y_empresa'
    END AS blocking_reason,
    CASE
      WHEN NORMALIZE_AND_CASEFOLD(CONCAT(c.nombre, ' ', c.apellido)) = NORMALIZE_AND_CASEFOLD(e.nombre) THEN 2
      ELSE 3
    END AS priority
  FROM `jakamedy-data-ia.demo_discovery.leads_crm` AS c
  JOIN `jakamedy-data-ia.demo_discovery.leads_evento` AS e
    ON c.empresa = e.empresa
    AND SOUNDEX(UPPER(NORMALIZE_AND_CASEFOLD(CONCAT(c.nombre, ' ', c.apellido)))) = SOUNDEX(UPPER(NORMALIZE_AND_CASEFOLD(e.nombre)))
    AND COALESCE(REGEXP_REPLACE(c.tel, r'[^0-9]', ''), '') != COALESCE(REGEXP_REPLACE(e.telefono, r'[^0-9]', ''), '')
)
SELECT * EXCEPT (priority)
FROM candidate_pairs
ORDER BY priority, crm_id, evento_id
LIMIT 40;
