# Output del prompt 1 — Triaje (ensayo real, fixture actual)

> Capturado el 2026-09-22 ejecutando prompts/prompt_1_triage.md con Claude.
> Contenido íntegro. Una nota de lectura: la sospecha del punto 2 sobre la
> concentración de cliente_id (.CT000001. en la muestra) quedó **refutada por el
> perfil** — ejecuta sql/20_profile_cliente_concentration.sql: 50.000 filas, 320
> clientes distintos; es un artefacto del TABLESAMPLE. Es la demostración del
> patrón: el modelo sospecha, el perfil decide.

## 1. Causa bloqueante demostrada por el log

El load job falló al parsear la fila 2 del CSV
(`P0006487,2026-04-27,"16,93€",Belleza,CT000087,3`): el valor `"16,93€"` en la
columna `importe` no es un NUMERIC válido para BigQuery, porque usa coma como
separador decimal y añade el símbolo `€`, mientras que BigQuery espera
notación con punto decimal y solo caracteres numéricos.

Como `max_bad_records = 0`, la tolerancia a errores es cero: un único
registro inválido basta para que el job aborte completo. Al ser una carga
atómica, no se escribió ninguna fila en staging y la tabla de destino no se
creó ("La tabla de destino no fue creada"). Esto es exactamente lo que
reporta el log; no hay ambigüedad sobre la causa bloqueante.

---

## 2. Riesgos adicionales visibles en la muestra (sospechas, no confirmadas)

Estas observaciones están limitadas a las 15 filas de la muestra. No se puede
afirmar que describan el lote completo; solo indican qué merece perfilado
sobre la tabla de cuarentena.

- **Formato de `importe` mixto**: en la muestra, 6 filas usan coma decimal +
  símbolo `€` (p. ej. `16,93€`) y 9 filas usan punto decimal sin símbolo (p.
  ej. `106.27`). Se sospecha que el fichero mezcla registros de dos orígenes
  o exportadores con locale distinto, y no solo un typo puntual.
- **`categoria` con idiomas mezclados**: conviven valores en español
  (Belleza, Deporte, Alimentación, Electrónica, Moda, Hogar) con valores en
  inglés (Grocery, Sports) que parecen equivalentes semánticos de categorías
  ya presentes en español. Se sospecha una taxonomía no unificada entre
  fuentes, no una categoría nueva legítima.
- **Concentración anómala de `cliente_id`**: 14 de las 15 filas comparten el
  mismo `cliente_id` (`CT000001`), y solo una fila usa un valor distinto
  (`CT000087`). Se sospecha un valor por defecto/placeholder o un fallo de
  resolución de cliente (p. ej. join fallido contra el maestro de clientes),
  aunque también podría ser coincidencia de la muestra.
- **Posibles artefactos de formato adicionales no visibles en esta
  muestra**: dado que el exportador aparentemente aplica formato "moneda" en
  algunas filas, no se puede descartar que existan también separadores de
  miles, espacios no separables u otros símbolos de divisa en el resto del
  lote.

No se ha detectado en la muestra ningún problema evidente en `pedido_id` o
`fecha_pedido` (ambos con formato consistente `PXXXXXXX` y `YYYY-MM-DD`
respectivamente), ni valores nulos en campos NULLABLE.

---

## 3. Consultas de perfilado sobre la tabla de cuarentena

Todos los campos de cuarentena son STRING, así que el perfilado trabaja sobre
texto crudo, sin castear.

### Medir la mezcla de formatos en `importe`

```sql
SELECT
  CASE
    WHEN REGEXP_CONTAINS(importe, r'^\d+,\d{2}€$') THEN 'coma_decimal_con_euro'
    WHEN REGEXP_CONTAINS(importe, r'^\d+\.\d{2}$')  THEN 'punto_decimal_sin_simbolo'
    ELSE 'otro_formato'
  END AS patron_importe,
  COUNT(*) AS n_filas,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS pct_sobre_cuarentena
FROM `jakamedy-data-ia.demo_calidad.raw_pedidos_quarantine`
GROUP BY patron_importe
ORDER BY n_filas DESC;
```

### Detectar artefactos adicionales en `importe`

Símbolos de moneda, separadores de miles, espacios, caracteres inesperados:

```sql
SELECT
  COUNTIF(REGEXP_CONTAINS(importe, r'€'))                 AS con_simbolo_euro,
  COUNTIF(REGEXP_CONTAINS(importe, r','))                 AS con_coma,
  COUNTIF(REGEXP_CONTAINS(importe, r'\.'))                AS con_punto,
  COUNTIF(REGEXP_CONTAINS(importe, r'\s'))                AS con_espacio,
  COUNTIF(NOT REGEXP_CONTAINS(importe, r'^[0-9.,€\s]+$')) AS con_caracter_no_esperado,
  COUNT(*)                                                 AS total_filas
FROM `jakamedy-data-ia.demo_calidad.raw_pedidos_quarantine`;
```

### Medir la mezcla de idiomas en `categoria`

```sql
SELECT categoria, COUNT(*) AS n_filas
FROM `jakamedy-data-ia.demo_calidad.raw_pedidos_quarantine`
GROUP BY categoria
ORDER BY n_filas DESC;
```

### Medir la concentración de `cliente_id`

```sql
SELECT
  cliente_id,
  COUNT(*) AS n_filas,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS pct_sobre_cuarentena
FROM `jakamedy-data-ia.demo_calidad.raw_pedidos_quarantine`
GROUP BY cliente_id
ORDER BY n_filas DESC
LIMIT 20;
```

```sql
SELECT
  COUNT(*) AS total_filas,
  COUNT(DISTINCT cliente_id) AS clientes_distintos,
  ROUND(COUNT(DISTINCT cliente_id) * 100.0 / COUNT(*), 4) AS pct_valores_distintos
FROM `jakamedy-data-ia.demo_calidad.raw_pedidos_quarantine`;
```

### Verificar consistencia de `fecha_pedido`

```sql
SELECT
  COUNTIF(REGEXP_CONTAINS(fecha_pedido, r'^\d{4}-\d{2}-\d{2}$'))     AS formato_iso_ok,
  COUNTIF(NOT REGEXP_CONTAINS(fecha_pedido, r'^\d{4}-\d{2}-\d{2}$')) AS formato_no_iso,
  COUNT(*) AS total_filas
FROM `jakamedy-data-ia.demo_calidad.raw_pedidos_quarantine`;
```

### Verificar consistencia de `unidades`

```sql
SELECT
  COUNTIF(unidades IS NULL) AS unidades_nulas,
  COUNTIF(unidades IS NOT NULL AND SAFE_CAST(unidades AS INT64) IS NULL) AS unidades_no_numericas,
  COUNT(*) AS total_filas
FROM `jakamedy-data-ia.demo_calidad.raw_pedidos_quarantine`;
```

---

## 4. Preguntas para Vivento

- ¿El fichero de origen combina exports de sistemas o mercados distintos con
  locale numérico diferente (coma vs. punto decimal para `importe`)? ¿Cuál es
  el formato canónico que Vivento considera correcto?
- ¿Es esperado que `importe` incluya el símbolo `€`, o es un defecto del
  proceso que genera el CSV (p. ej. exportación desde una hoja con formato de
  celda "moneda" aplicado)?
- ¿La taxonomía de `categoria` debe estar siempre en español? Si aparecen
  valores en inglés como "Grocery" o "Sports", ¿corresponden a un
  canal/integración distinto que aún no está mapeado a la taxonomía interna?
- ¿Por qué la mayoría de los pedidos de este lote comparten el mismo
  `cliente_id`? ¿Es un valor esperado (p. ej. cliente genérico/anónimo) o
  indica un fallo de resolución contra el maestro de clientes?
- ¿Qué sistema u origen produjo exactamente este lote y hubo alguna unión o
  consolidación de fuentes antes de generarlo?
- Una vez identificado el origen del problema, ¿el tratamiento preferido es
  reprocesar con normalización en el pipeline, descartar y solicitar
  reenvío del fichero corregido, o cargar a una tabla intermedia para
  revisión manual antes de promover a staging?

---

## 5. Controles operativos a mantener durante la investigación

- No relanzar el load job sin cambios: fallará de nuevo por el mismo motivo y
  puede ocultar que hay más de un patrón de error.
- No subir ni relajar `max_bad_records` como parche: enmascararía filas
  defectuosas en lugar de resolver la causa.
- No editar ni normalizar registros del fichero origen o de la muestra: la
  evidencia debe permanecer intacta para el análisis y para la revisión de
  Vivento.
- Aislar el fichero de este lote (mantenerlo en cuarentena, sin
  sobrescribir) para que lotes posteriores no se mezclen con este.
- Registrar el incidente con el log de error completo y el timestamp del
  intento fallido, para trazabilidad.
- No crear manualmente la tabla de destino ni insertar filas parciales sin
  acuerdo: al no haberse escrito nada en staging, cualquier inserción manual
  podría generar estados inconsistentes.
- Avisar a los consumidores downstream de la tabla de staging de que el
  refresco de este lote no se completó, para evitar que dashboards o
  procesos asuman datos actualizados.
- Vigilar si llegan lotes posteriores con el mismo patrón de error, para
  determinar si es un problema puntual de este fichero o sistémico del
  proceso de origen.
