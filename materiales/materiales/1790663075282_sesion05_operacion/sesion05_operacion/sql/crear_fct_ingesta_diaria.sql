-- DDL de la tabla destino del pipeline ingesta_diaria (demo B).
-- Canon: fct_* siempre incremental/particionada por fecha, cluster por clave de negocio.
CREATE TABLE IF NOT EXISTS `jakamedy-data-ia.demo_ops.fct_ingesta_diaria` (
  registro_nk STRING NOT NULL,   -- registro_id de la fuente, casteado a STRING (sufijo _nk)
  fecha       DATE   NOT NULL,   -- fecha del registro en origen
  importe     FLOAT64 NOT NULL,  -- importe_total / total_importe de la fuente
  tienda_nk   STRING NOT NULL
)
PARTITION BY fecha
CLUSTER BY tienda_nk
OPTIONS (
  description = 'Hechos de ingesta diaria de tienda. Grano: un registro del fichero diario del equipo origen.'
);
