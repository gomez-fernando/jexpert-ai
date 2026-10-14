# Prompt 1 — Triaje del lote fallido

```text
Actúa como ingeniero de datos durante un incidente de ingesta.

El load job de BigQuery ha fallado antes de escribir en staging. Analiza exclusivamente la evidencia incluida. No corrijas registros, no inventes prevalencias y no afirmes que un patrón afecta al lote completo a partir de la muestra.

Entrega:
1. Causa bloqueante demostrada por el log.
2. Riesgos adicionales visibles en la muestra, expresados como sospechas.
3. Consultas BigQuery de perfilado para medir cada sospecha sobre la tabla de
   cuarentena (sus campos son STRING).
4. Preguntas para Vivento que permitan decidir el tratamiento.
5. Controles operativos que deben mantenerse mientras se investiga.

<contrato_fisico>
pedido_id STRING REQUIRED
fecha_pedido DATE REQUIRED
importe NUMERIC REQUIRED
categoria STRING NULLABLE
cliente_id STRING NULLABLE
unidades INT64 NULLABLE
max_bad_records = 0
</contrato_fisico>

<error_load>
Invalid NUMERIC value: "16,93€"
line_number: 2
column_name: importe
column_type: NUMERIC
CSV table encountered too many errors; max bad: 0
La tabla de destino no fue creada.
</error_load>

<muestra>
pedido_id,fecha_pedido,importe,categoria,cliente_id,unidades
P0006487,2026-04-27,"16,93€",Belleza,CT000087,3
P0032200,2025-01-11,"20,72€",Deporte,CT000001,1
P0011928,2025-02-17,106.27,Alimentación,CT000001,1
P0045129,2026-03-13,"463,77€",Deporte,CT000001,1
P0045479,2025-06-21,"336,27€",Grocery,CT000001,1
P0012698,2025-10-03,423.99,Sports,CT000001,1
P0009813,2025-06-01,51.89,Electrónica,CT000001,1
P0028524,2026-03-19,232.65,Moda,CT000001,1
P0011821,2026-06-27,262.04,Deporte,CT000001,1
P0011342,2025-06-16,"267,32€",Belleza,CT000001,1
P0021758,2025-09-30,591.67,Deporte,CT000001,1
P0031427,2025-07-03,598.02,Deporte,CT000001,1
P0032658,2025-03-17,"718,92€",Deporte,CT000001,1
P0001227,2026-05-31,867.08,Belleza,CT000001,1
P0025851,2025-11-27,251.82,Hogar,CT000001,1
</muestra>

<table_cuarentena>`jakamedy-data-ia.demo_calidad.raw_pedidos_quarantine`</table_cuarentena>
```

Nota de producción: la muestra es la fila concreta del fallo (line_number 2 del job)
más 14 filas seleccionadas con `TABLESAMPLE`. Es lo que cualquier ingeniero pegaría
en un chat sin pensar en curaduría: las sospechas que faltan salen después del perfil.
