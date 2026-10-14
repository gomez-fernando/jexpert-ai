-- q00 · Historial real de jobs del pipeline ingesta_diaria (evidencia demo B).
-- Lo que el agente consulta para saber CUANDO empezo a fallar el pipeline:
-- filtra por los jobs que tocan las tablas stg_ o fct_ de ingesta diaria.
SELECT
  job_id,
  job_type,
  state,
  creation_time,
  TIMESTAMP_DIFF(end_time, start_time, SECOND) AS duracion_s,
  total_bytes_processed,
  error_result.message AS error
FROM `jakamedy-data-ia.region-eu.INFORMATION_SCHEMA.JOBS_BY_PROJECT`
WHERE creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
  AND REGEXP_CONTAINS(query, r'demo_ops\.(stg|fct)_ingesta_diaria')
ORDER BY creation_time;
