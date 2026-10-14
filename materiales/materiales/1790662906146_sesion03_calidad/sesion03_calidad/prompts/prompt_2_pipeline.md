# Prompt 2 — Transformación y assertions

```text
Actúa como ingeniero de calidad de datos. Genera BigQuery Standard SQL para procesar una tabla de cuarentena STRING hacia una tabla candidata tipada y una suite de tests con la convención «cero filas = correcto».

Usa únicamente el perfil ejecutado, la política aprobada y el esquema real de las tablas. No cambies reglas, no inventes valores, no imputes campos vacíos y no presupongas columnas que no estén en el esquema.

Entrega:
1. Transformación raw_pedidos_quarantine → stg_pedidos_routed.
2. Campo route con valores clean, review o reject.
3. Campo reason legible para review/reject.
4. Tests de importe, fecha, categoría, unicidad, unidades y reconciliación.
5. Para cada test: dimensión, severidad y justificación.

<esquema_cuarentena>
Todas las columnas son STRING:
- source_row_id — identificador técnico único de cada fila del fichero
- pedido_id
- fecha_pedido
- importe
- categoria
- cliente_id
- unidades
</esquema_cuarentena>

<contrato_destino>
pedido_id STRING REQUIRED
fecha_pedido DATE REQUIRED      -- formato ISO en origen
importe NUMERIC REQUIRED        -- NULL si vacía
categoria STRING NULLABLE       -- valor canónico del mapping aprobado
cliente_id STRING NULLABLE
unidades INT64 NULLABLE         -- entero > 0
source_row_id STRING            -- se conserva para reconciliación 1:1
max_bad_records = 0
</contrato_destino>

<perfil_ejecutado>
filas=50000
filas_id_repetido=977
importe_vacio=2038
importe_europeo=15044
fecha_iso=50000
categoria_ingles=10170
outliers_mayor_90000=15
</perfil_ejecutado>

<politica_aprobada>
- Todos los importes están en EUR.
- Formato europeo inequívoco: normalizar determinísticamente.
- Importe vacío: review; nunca imputar.
- Importe negativo: reject.
- Fechas llegan en ISO (YYYY-MM-DD): parseo directo; cualquier otro formato → review.
- Mapping aprobado: Electronics→Electrónica, Home→Hogar, Fashion→Moda, Sports→Deporte, Beauty→Belleza, Grocery→Alimentación.
- pedido_id es clave única.
- Duplicado idéntico: deduplicar.
- Mismo pedido_id con datos diferentes: review.
- Importe >90000: warn y review; nunca modificar.
- clean + review + reject debe reconciliar con el lote original.
</politica_aprobada>

<origen>`jakamedy-data-ia.demo_calidad.raw_pedidos_quarantine`</origen>
```
