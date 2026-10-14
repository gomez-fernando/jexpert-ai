-- evidencia demo B · paso 2: esquemas REALES de la fuente y del destino
SELECT table_name, ordinal_position, column_name, data_type
FROM `jakamedy-data-ia.demo_ops.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name IN ('stg_ingesta_diaria', 'fct_ingesta_diaria')
ORDER BY table_name, ordinal_position;
