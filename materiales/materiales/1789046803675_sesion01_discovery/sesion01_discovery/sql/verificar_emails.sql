SELECT
  'leads_crm' AS tabla,
  COUNT(*) AS filas,
  COUNTIF(mail_contacto IS NULL OR mail_contacto = '') AS emails_vacios,
  COUNTIF(LENGTH(mail_contacto) != BYTE_LENGTH(mail_contacto)) AS emails_no_ascii
FROM `jakamedy-data-ia.demo_discovery.leads_crm`
UNION ALL
SELECT
  'leads_evento',
  COUNT(*),
  COUNTIF(email IS NULL OR email = ''),
  COUNTIF(LENGTH(email) != BYTE_LENGTH(email))
FROM `jakamedy-data-ia.demo_discovery.leads_evento`;
