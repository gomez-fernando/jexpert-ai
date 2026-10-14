-- PLANTILLA DEL EQUIPO — modelo SQL (staging o fct incremental).
-- Uso: copiar, renombrar y ajustar SOLO la sección CONFIG de la cabecera.
-- El SQL se versiona en el repo; el workflow lo ejecuta con jobs.query.
--
-- CONFIG (documentar SIEMPRE antes del SQL):
--   grano:  <una fila por ...>
--   fuente: <dataset.tabla_origen>
--   owner:  equipo-data
--
-- STAGING (stg_<fuente>): espejo normalizado con auditoría — canon:
--   _fuente STRING (fichero origen) y _cargado_en TIMESTAMP.

CREATE OR REPLACE TABLE `jakamedy-data-ia.demo_ops.stg_<fuente>` AS
SELECT
  CAST(<columna_id> AS STRING) AS <clave>_nk,   -- claves naturales: sufijo _nk, STRING
  <columna_fecha>              AS fecha,
  <resto_de_columnas>,
  "<uri_del_fichero_gs>"       AS _fuente,      -- canon: auditoría
  CURRENT_TIMESTAMP()          AS _cargado_en
FROM `jakamedy-data-ia.demo_ops.raw_<fuente>`;

-- FCT (fct_<nombre>): SIEMPRE incremental, particionada por fecha y cluster
-- por la clave de negocio. La guarda MAX(fecha) es la que la hace incremental.

/*
CREATE TABLE IF NOT EXISTS `jakamedy-data-ia.demo_ops.fct_<nombre>` (
  <clave>_nk  STRING NOT NULL,
  fecha       DATE   NOT NULL,
  <metricas>
)
PARTITION BY fecha
CLUSTER BY <clave>_nk
OPTIONS (description = 'Grano: <...>. Fuente: demo_ops.stg_<fuente>.');

INSERT INTO `jakamedy-data-ia.demo_ops.fct_<nombre>` (...)
SELECT ...
FROM `jakamedy-data-ia.demo_ops.stg_<fuente>`
WHERE fecha > COALESCE(
  (SELECT MAX(fecha) FROM `jakamedy-data-ia.demo_ops.fct_<nombre>`),
  DATE '1900-01-01'
);
*/
