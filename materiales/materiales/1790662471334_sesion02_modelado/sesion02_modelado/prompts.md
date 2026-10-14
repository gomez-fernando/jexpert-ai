# Prompts de la Sesión 2

El contenido de `<contexto_equipo>` es `contexto_equipo.md` (versión acotada, sin el
modelo canónico). Los `<fuentes>` se componen de las cabeceras de `data/*.csv`, tres
filas de muestra por fuente y los outputs reales de `sql/01`–`06` (carpeta `output/q0*.txt`).

## 1. Modelo v1

```text
Tarea: propón un modelo dimensional inicial para el caso descrito.

Contexto:
- El destino analítico es BigQuery.
- Las convenciones y el glosario están en <contexto_equipo>.
- Las fuentes y sus resultados de profiling están en <fuentes>.
- Las preguntas que debe responder el modelo están en <preguntas_negocio>.

Entregable:
1. Hechos candidatos. Para cada uno:
   - nombre;
   - grano declarado: «una fila representa...»;
   - clave natural o de negocio;
   - medidas;
   - dimensiones relacionadas.
2. Dimensiones candidatas:
   - clave natural;
   - surrogate key;
   - atributos principales;
   - estrategia histórica si aplica.
3. Relaciones y cardinalidades.
4. Lista de DECISIONES ABIERTAS. No las resuelvas.
5. Riesgos o datos que faltan para responder las preguntas de negocio.
6. ERD en Mermaid.

Reglas:
- No inventes entidades ni campos que no aparezcan en las fuentes.
- No diseñes producto: no existe una fuente de líneas de ticket.
- No pongas campana_id directamente en la venta si la relación procede de la tabla de atribución.
- Conserva la trazabilidad de IDs de origen mediante identity_crosswalk.
- No propongas todavía particionado ni clustering.
- No inventes la definición de ROI.

<contexto_equipo>
[contenido de contexto_equipo.md]
</contexto_equipo>

<preguntas_negocio>
- ROI por campaña y mes.
- Ingresos netos atribuidos por segmento en el momento de la venta.
- Funnel de interacciones por campaña.
- Ventas sin identificar y sin atribuir.
</preguntas_negocio>

<fuentes>
[esquemas reales + 3 filas de muestra + outputs de queries 1–6]
</fuentes>
```

## 2. Iteración v2

```text
Revisa la propuesta v1 utilizando exclusivamente las decisiones aprobadas de <decisiones_firmadas>.

Devuelve:
1. Un diff v1 → v2 con elementos añadidos, eliminados y modificados.
2. El modelo v2 completo:
   - hechos y grano;
   - dimensiones y estrategia histórica;
   - bridges;
   - claves naturales y surrogate;
   - relaciones y cardinalidades.
3. Las decisiones que siguen abiertas.
4. Un ERD Mermaid compilable.

Reglas:
- No inventes nuevas entidades.
- No resuelvas la definición de ROI: sigue abierta.
- No propongas particionado o clustering todavía.
- Conserva identity_crosswalk como artefacto de integración.

<propuesta_v1>
[OUTPUT BRUTO V1 — output/modelo_v1.md]
</propuesta_v1>

<decisiones_firmadas>
[TABLA DE DECISIONES FIRMADAS]
</decisiones_firmadas>
```

## 3. DDL y tests

```text
Genera BigQuery Standard SQL para materializar el modelo v2 aprobado.

Entregables:
1. DDL de dimensiones, hechos y bridge.
2. SQL de carga SCD2 para la dimensión de historia del segmento (la del modelo v2).
3. Tests SQL que devuelvan cero filas para:
   - unicidad del grano;
   - claves obligatorias;
   - integridad referencial;
   - intervalos SCD2 solapados;
   - más de una fila vigente por contacto;
   - pesos de atribución que no sumen 1.
4. DECISIONES ABIERTAS que impidan generar una pieza correctamente.
5. Diccionario de datos de las tablas gold_*: para cada tabla, descripción de una
   línea, grano, clave, y cada columna con tipo y definición de negocio. Marca las
   decisiones abiertas que afecten a cada pieza; no las resuelvas.

Reglas:
- Usa los nombres y tipos del modelo v2.
- No inventes columnas.
- El diccionario se deriva del DDL: toda tabla y columna del DDL debe aparecer
  documentada, ni más ni menos.
- No generes la query de ROI todavía.
- No propongas particionado o clustering sin patrones de consulta y volumetría.

<modelo_v2>
[MODELO APROBADO — output/modelo_v2.md]
</modelo_v2>
```

## 4. Query ROI (tras firmar el contrato semántico)

Se ejecuta solo después de la tabla de decisiones de la métrica. El resultado mostrado
en el deck será el observado tras materializar `gold_*`, nunca una cifra narrativa, y
lleva reconciliación manual de una campaña.

```text
Genera BigQuery Standard SQL para la métrica de <contrato>.

Entregables:
1. La query reproducible, ejecutable sobre las tablas gold_* materializadas.
2. Un plan de reconciliación manual: qué se suma a mano y contra qué se compara.
3. Los casos límite de <contrato> cubiertos uno a uno (la query se ajusta al contrato,
   no al revés).

Reglas:
- La métrica se deriva íntegramente de <contrato>; no inventes definiciones.
- Usa los nombres del DDL real (<ddl_gold>).
- Cada cláusula del contrato queda reflejada una única vez en la query.

<contrato>
[CONTRATO FIRMADO — output/roi_campana_mes.yaml]
</contrato>

<ddl_gold>
[DDL REAL — output/ddl_modelo_v2.sql, tras el ensayo del prompt 3]
</ddl_gold>
```
