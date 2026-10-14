-- ============================================================================
-- PEDIDOS · CUARENTENA → CANDIDATA TIPADA (stg_pedidos_propuesta_llm) + SUITE DE TESTS
-- BigQuery Standard SQL
-- Origen: `jakamedy-data-ia.demo_calidad.raw_pedidos_quarantine`
-- Basado exclusivamente en: perfil ejecutado + política aprobada + esquema real.
-- ============================================================================
--
-- ASUNCIONES Y DECISIONES DE DISEÑO (explícitas, para revisión — nada de esto
-- cambia una regla de la política; cubre huecos que la política no especifica)
--
-- A1. "Duplicado idéntico" se detecta comparando los valores STRING crudos
--     (sin normalizar) de fecha_pedido, importe, categoria, cliente_id y
--     unidades para un mismo pedido_id. Si coinciden al 100% entre todas las
--     filas del pedido_id, NO es un conflicto. Si difiere cualquier campo,
--     es "mismo pedido_id con datos diferentes" → review.
-- A2. stg_pedidos_propuesta_llm se genera a grano de fila de origen: una fila
--     candidata por cada source_row_id, sin eliminar ninguna. Así la
--     reconciliación 1:1 (clean+review+reject = lote original) se cumple
--     por construcción para el conteo de filas. La deduplicación física de
--     duplicados idénticos (para respetar pedido_id como clave única) se
--     deja para la carga a la tabla final estrictamente tipada — ver bloque
--     OPCIONAL al final — usando QUALIFY/ROW_NUMBER, nunca en esta tabla.
-- A3. pedido_id vacío/nulo no está cubierto por la política. Al ser la clave
--     REQUIRED del contrato, se enruta a review con motivo explícito
--     ("pedido_id vacío o ausente"), nunca a reject ni a clean.
-- A4. Un importe no vacío pero no parseable como número (ni formato europeo
--     ni estándar) tampoco está cubierto por la política. Se enruta a review
--     con motivo explícito ("importe no parseable"), nunca se descarta ni se
--     manda a reject sin más.
-- A5. Un valor de categoria que ya viene en español canónico se acepta tal
--     cual (idempotencia del mapping aprobado). Un valor que no es ni
--     inglés-origen ni español-canónico se conserva tal cual en el campo
--     (para revisión humana, sin inventar un mapeo no aprobado) y fuerza
--     route=review.
-- A6. Valores que no caben en el tipo destino (importe/unidades no
--     numéricos, fecha no parseable) quedan NULL en stg_pedidos_propuesta_llm. El
--     valor crudo original siempre es recuperable vía source_row_id contra
--     raw_pedidos_quarantine — por eso se conserva esa columna.
--
-- ============================================================================


-- ============================================================================
-- 1) TRANSFORMACIÓN: raw_pedidos_quarantine (STRING) → stg_pedidos_propuesta_llm
--    Campos: contrato tipado + route (clean/review/reject) + reason
-- ============================================================================

CREATE OR REPLACE TABLE `jakamedy-data-ia.demo_calidad.stg_pedidos_propuesta_llm` AS

WITH raw AS (
  SELECT
    source_row_id,
    pedido_id,
    fecha_pedido,
    importe,
    categoria,
    cliente_id,
    unidades
  FROM `jakamedy-data-ia.demo_calidad.raw_pedidos_quarantine`
),

-- 1.1 Grupos por pedido_id (excluyendo pedido_id vacío/nulo, que se trata aparte)
--     y cuántas combinaciones DISTINTAS de datos crudos existen por pedido_id.
dup_groups AS (
  SELECT
    pedido_id,
    COUNT(*) AS filas_por_pedido,
    COUNT(DISTINCT CONCAT(
      COALESCE(fecha_pedido, ''), '|',
      COALESCE(importe,      ''), '|',
      COALESCE(categoria,    ''), '|',
      COALESCE(cliente_id,   ''), '|',
      COALESCE(unidades,     '')
    )) AS variantes_por_pedido
  FROM raw
  WHERE pedido_id IS NOT NULL AND TRIM(pedido_id) != ''
  GROUP BY pedido_id
),

dedup_check AS (
  SELECT
    r.*,
    d.filas_por_pedido,
    d.variantes_por_pedido
  FROM raw r
  LEFT JOIN dup_groups d USING (pedido_id)
),

-- 1.2 Normalización de importe: formato europeo (coma decimal, punto de
--     miles) se detecta por la presencia de una coma y se normaliza de forma
--     determinística; si no hay coma, se asume formato estándar (punto
--     decimal). Nunca se imputa un importe vacío.
importe_parsed AS (
  SELECT
    *,
    TRIM(importe) AS importe_trim,
    CASE
      WHEN TRIM(importe) IS NULL OR TRIM(importe) = '' THEN NULL
      -- REVISADO: primero quitar el símbolo € (viene embebido en el fichero),
      -- después separar miles y decimales
      WHEN STRPOS(TRIM(importe), CHR(8364)) > 0 THEN
        SAFE_CAST(REPLACE(REPLACE(REPLACE(TRIM(importe), CHR(8364), ''), '.', ''), ',', '.') AS NUMERIC)
      WHEN STRPOS(TRIM(importe), ',') > 0
        THEN SAFE_CAST(REPLACE(REPLACE(TRIM(importe), '.', ''), ',', '.') AS NUMERIC)
      ELSE SAFE_CAST(TRIM(importe) AS NUMERIC)
    END AS importe_num
  FROM dedup_check
),

-- 1.3 Fecha: parseo directo asumiendo ISO (YYYY-MM-DD). Cualquier otro
--     formato o valor no parseable devuelve NULL (SAFE) → review.
fecha_parsed AS (
  SELECT
    *,
    SAFE.PARSE_DATE('%Y-%m-%d', TRIM(fecha_pedido)) AS fecha_date
  FROM importe_parsed
),

-- 1.4 Categoria: mapping aprobado inglés→español + idempotencia si ya viene
--     en español canónico. Vacío se mantiene NULL (nullable, sin imputar).
--     Valor no reconocido se conserva tal cual (para revisión humana) y se
--     marca como no reconocido.
categoria_norm AS (
  SELECT
    *,
    -- REVISADO: mapping desde tabla UTF-8 para evitar literales con acentos en el fichero
    COALESCE(m.cat_map, TRIM(f.categoria)) AS categoria_canonica,
    CASE
      WHEN f.categoria IS NULL OR TRIM(f.categoria) = '' THEN TRUE
      WHEN m.cat_map IS NOT NULL THEN TRUE
      ELSE FALSE
    END AS categoria_reconocida
  FROM fecha_parsed f
  LEFT JOIN (SELECT categoria_raw, categoria_canonica AS cat_map FROM `jakamedy-data-ia.demo_calidad.category_mapping`) m
    ON TRIM(f.categoria) = m.categoria_raw
),

-- 1.5 Unidades: entero positivo o NULL (nullable). Cualquier otro valor
--     (no numérico, cero, negativo, decimal) se considera inválido.
unidades_norm AS (
  SELECT
    *,
    CASE
      WHEN unidades IS NULL OR TRIM(unidades) = '' THEN NULL
      WHEN REGEXP_CONTAINS(TRIM(unidades), r'^[0-9]+$')
           AND SAFE_CAST(TRIM(unidades) AS INT64) > 0
        THEN SAFE_CAST(TRIM(unidades) AS INT64)
      ELSE NULL
    END AS unidades_num,
    CASE
      WHEN unidades IS NULL OR TRIM(unidades) = '' THEN TRUE
      WHEN REGEXP_CONTAINS(TRIM(unidades), r'^[0-9]+$')
           AND SAFE_CAST(TRIM(unidades) AS INT64) > 0 THEN TRUE
      ELSE FALSE
    END AS unidades_validas
  FROM categoria_norm
),

-- 1.6 Flags de negocio (uno por regla de la política + huecos documentados)
flags AS (
  SELECT
    *,
    (pedido_id IS NULL OR TRIM(pedido_id) = '')            AS pedido_id_vacio,
    COALESCE(variantes_por_pedido > 1, FALSE)               AS es_conflicto_duplicado,
    (importe_trim IS NULL OR importe_trim = '')             AS importe_vacio,
    (importe_trim IS NOT NULL AND importe_trim != ''
      AND importe_num IS NULL)                              AS importe_no_parseable,
    (importe_num IS NOT NULL AND importe_num < 0)            AS importe_negativo,
    (importe_num IS NOT NULL AND importe_num > 90000)        AS importe_outlier,
    (fecha_pedido IS NOT NULL AND TRIM(fecha_pedido) != ''
      AND fecha_date IS NULL)                                AS fecha_invalida,
    (NOT categoria_reconocida)                               AS categoria_invalida,
    (NOT unidades_validas)                                   AS unidades_invalidas
  FROM unidades_norm
),

routed AS (
  SELECT
    source_row_id,
    pedido_id,
    fecha_date        AS fecha_pedido,
    importe_num       AS importe,
    categoria_canonica AS categoria,
    cliente_id,
    unidades_num       AS unidades,
    CASE
      WHEN importe_negativo THEN 'reject'
      WHEN pedido_id_vacio
        OR es_conflicto_duplicado
        OR importe_vacio
        OR importe_no_parseable
        OR importe_outlier
        OR fecha_invalida
        OR categoria_invalida
        OR unidades_invalidas
      THEN 'review'
      ELSE 'clean'
    END AS route,
    ARRAY_TO_STRING([
      IF(importe_negativo,        'importe negativo', NULL),
      IF(pedido_id_vacio,         'pedido_id vacío o ausente', NULL),
      IF(es_conflicto_duplicado,  'pedido_id duplicado con datos distintos', NULL),
      IF(importe_vacio,           'importe vacío', NULL),
      IF(importe_no_parseable,    'importe no parseable tras normalización', NULL),
      IF(importe_outlier,         'importe > 90000: revisión manual obligatoria', NULL),
      IF(fecha_invalida,          'fecha_pedido no cumple formato ISO (YYYY-MM-DD)', NULL),
      IF(categoria_invalida,      'categoria fuera del mapping aprobado', NULL),
      IF(unidades_invalidas,      'unidades no es un entero positivo', NULL)
    ], '; ') AS reason_raw
  FROM flags
)

SELECT
  source_row_id,
  pedido_id,
  fecha_pedido,
  importe,
  categoria,
  cliente_id,
  unidades,
  route,
  NULLIF(reason_raw, '') AS reason
FROM routed;


-- ============================================================================
-- 2) SUITE DE TESTS — convención "cero filas = correcto"
--    Cada SELECT debe devolver 0 filas. Si devuelve >0, el test ha fallado
--    y las filas devueltas son la evidencia para triage.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- TEST 1 — importe_clean_valido
-- Dimensión: Validez (rango y dominio numérico)
-- Severidad: CRÍTICA (bloqueante)
-- Justificación: el contrato exige importe NUMERIC REQUIRED sin NULL; la
-- política exige que negativos y vacíos nunca lleguen a clean, y que >90000
-- siempre pase por revisión manual. Cualquier fila 'clean' que viole esto
-- contaminaría la carga final.
-- ----------------------------------------------------------------------------
SELECT source_row_id, pedido_id, importe, route, reason
FROM `jakamedy-data-ia.demo_calidad.stg_pedidos_propuesta_llm`
WHERE route = 'clean'
  AND (importe IS NULL OR importe < 0 OR importe > 90000);


-- ----------------------------------------------------------------------------
-- TEST 2 — fecha_clean_valida
-- Dimensión: Validez (conformidad de formato)
-- Severidad: CRÍTICA (bloqueante)
-- Justificación: fecha_pedido es REQUIRED en el contrato destino. Una fecha
-- NULL en 'clean' solo puede ocurrir si el parseo ISO falló y la fila se
-- enrutó mal.
-- ----------------------------------------------------------------------------
SELECT source_row_id, pedido_id, fecha_pedido, route, reason
FROM `jakamedy-data-ia.demo_calidad.stg_pedidos_propuesta_llm`
WHERE route = 'clean'
  AND fecha_pedido IS NULL;


-- ----------------------------------------------------------------------------
-- TEST 3 — categoria_dominio_valido
-- Dimensión: Consistencia / Validez de dominio categórico
-- Severidad: ALTA (no bloquea el esquema por ser NULLABLE, pero corrompe
-- silenciosamente reporting por categoría si se cuela un valor fuera del
-- mapping aprobado)
-- Justificación: solo los 6 valores canónicos aprobados (o NULL) deben
-- llegar a 'clean'; cualquier otro valor debió forzar route=review.
-- ----------------------------------------------------------------------------
SELECT source_row_id, pedido_id, categoria, route, reason
FROM `jakamedy-data-ia.demo_calidad.stg_pedidos_propuesta_llm`
WHERE route = 'clean'
  AND categoria IS NOT NULL
  AND categoria NOT IN ('Electrónica','Hogar','Moda','Deporte','Belleza','Alimentación');


-- ----------------------------------------------------------------------------
-- TEST 4 — unicidad_pedido_id_en_clean
-- Dimensión: Unicidad (clave del contrato destino)
-- Severidad: CRÍTICA (bloqueante)
-- Justificación: pedido_id es la clave única del contrato. Dentro de
-- 'clean', dos filas con el mismo pedido_id solo son aceptables si son
-- duplicados idénticos (se resuelven después con dedup físico); cualquier
-- variante de datos distinta indica que un conflicto no fue detectado y
-- se coló como 'clean'.
-- ----------------------------------------------------------------------------
SELECT
  pedido_id,
  COUNT(*) AS n_filas,
  COUNT(DISTINCT CONCAT(
    CAST(fecha_pedido AS STRING), '|',
    CAST(importe      AS STRING), '|',
    COALESCE(categoria, ''),      '|',
    COALESCE(cliente_id, ''),     '|',
    CAST(unidades AS STRING)
  )) AS variantes
FROM `jakamedy-data-ia.demo_calidad.stg_pedidos_propuesta_llm`
WHERE route = 'clean'
GROUP BY pedido_id
HAVING variantes > 1;

-- TEST 4b — pedido_id_no_nulo_en_clean (complementario a unicidad)
-- Dimensión: Completitud de clave
-- Severidad: CRÍTICA
-- Justificación: la clave requerida no puede ser NULL/vacía en 'clean'.
SELECT source_row_id, pedido_id, route
FROM `jakamedy-data-ia.demo_calidad.stg_pedidos_propuesta_llm`
WHERE route = 'clean'
  AND (pedido_id IS NULL OR TRIM(pedido_id) = '');


-- ----------------------------------------------------------------------------
-- TEST 5 — unidades_clean_validas
-- Dimensión: Validez (rango)
-- Severidad: MEDIA (unidades es NULLABLE; un valor inválido no rompe el
-- esquema pero distorsiona cálculos de inventario/facturación aguas abajo)
-- Justificación: si unidades está presente en 'clean', debe ser entero > 0.
-- ----------------------------------------------------------------------------
SELECT source_row_id, pedido_id, unidades, route, reason
FROM `jakamedy-data-ia.demo_calidad.stg_pedidos_propuesta_llm`
WHERE route = 'clean'
  AND unidades IS NOT NULL
  AND unidades <= 0;


-- ----------------------------------------------------------------------------
-- TEST 6 — reconciliacion_lote
-- Dimensión: Completitud + Integridad referencial (1:1 con el origen)
-- Severidad: CRÍTICA (condición de parada del pipeline)
-- Justificación: la política exige que clean+review+reject reconcilie
-- exactamente con el lote original; y el contrato exige source_row_id para
-- reconciliación 1:1. Si este test falla, todo el resto de tests pierde
-- validez (hay filas perdidas, duplicadas o con route fuera de dominio).
-- ----------------------------------------------------------------------------
WITH origen AS (
  SELECT
    COUNT(*) AS n_origen,
    COUNT(DISTINCT source_row_id) AS n_origen_ids
  FROM `jakamedy-data-ia.demo_calidad.raw_pedidos_quarantine`
),
destino AS (
  SELECT
    COUNT(*) AS n_total,
    COUNT(DISTINCT source_row_id) AS n_total_ids,
    COUNTIF(route = 'clean')  AS n_clean,
    COUNTIF(route = 'review') AS n_review,
    COUNTIF(route = 'reject') AS n_reject,
    COUNTIF(route IS NULL OR route NOT IN ('clean','review','reject')) AS n_route_invalida
  FROM `jakamedy-data-ia.demo_calidad.stg_pedidos_propuesta_llm`
)
SELECT *
FROM origen, destino
WHERE n_origen != n_total
   OR n_origen_ids != n_total_ids
   OR n_origen != (n_clean + n_review + n_reject)
   OR n_route_invalida > 0;

-- TEST 6b — source_row_id_unico_en_salida (complementario a reconciliación)
-- Dimensión: Integridad referencial
-- Severidad: CRÍTICA
-- Justificación: cada source_row_id del origen debe aparecer EXACTAMENTE una
-- vez en stg_pedidos_propuesta_llm (nunca perdido, nunca duplicado) para que la
-- reconciliación 1:1 sea válida a nivel de fila individual.
SELECT source_row_id, COUNT(*) AS n_apariciones
FROM `jakamedy-data-ia.demo_calidad.stg_pedidos_propuesta_llm`
GROUP BY source_row_id
HAVING COUNT(*) != 1;


-- ----------------------------------------------------------------------------
-- TEST EXTRA (bonus, no solicitado explícitamente pero refuerza el punto 3
-- del encargo — "reason legible para review/reject")
-- TEST — reason_coherente_con_route
-- Dimensión: Trazabilidad / Auditabilidad
-- Severidad: MEDIA
-- Justificación: toda fila review/reject debe traer un motivo legible; toda
-- fila clean no debe traer motivo (evita ruido y confirma que el motor de
-- reglas y el route están sincronizados).
-- ----------------------------------------------------------------------------
SELECT source_row_id, pedido_id, route, reason
FROM `jakamedy-data-ia.demo_calidad.stg_pedidos_propuesta_llm`
WHERE (route IN ('review', 'reject') AND (reason IS NULL OR TRIM(reason) = ''))
   OR (route = 'clean' AND reason IS NOT NULL);


-- ============================================================================
-- 3) OPCIONAL / INFORMATIVO — fuera del alcance estrictamente pedido.
--    Cierra el uso de contrato_destino (incl. max_bad_records=0), mostrando
--    dónde se aplica la deduplicación física de duplicados idénticos antes
--    de respetar pedido_id como clave única en la tabla final.
-- ============================================================================

CREATE TABLE IF NOT EXISTS `jakamedy-data-ia.demo_calidad.pedidos_clean`
(
  pedido_id     STRING  NOT NULL,
  fecha_pedido  DATE    NOT NULL,
  importe       NUMERIC NOT NULL,
  categoria     STRING,
  cliente_id    STRING,
  unidades      INT64,
  source_row_id STRING
);

INSERT INTO `jakamedy-data-ia.demo_calidad.pedidos_clean`
SELECT pedido_id, fecha_pedido, importe, categoria, cliente_id, unidades, source_row_id
FROM (
  SELECT
    *,
    ROW_NUMBER() OVER (PARTITION BY pedido_id ORDER BY source_row_id) AS rn
  FROM `jakamedy-data-ia.demo_calidad.stg_pedidos_propuesta_llm`
  WHERE route = 'clean'
)
WHERE rn = 1;

-- Nota: max_bad_records=0 del contrato aplica al job de carga (bq load /
-- LOAD DATA) cuando el origen es un fichero externo. Aquí, al ser un INSERT
-- desde una tabla ya tipada, el equivalente es que el INSERT completo falla
-- si se violase algún NOT NULL — lo cual no debería ocurrir nunca, porque
-- route='clean' ya garantiza por construcción que fecha_pedido e importe
-- están completos (test 1 y test 2 lo verifican).
