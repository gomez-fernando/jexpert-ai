# Equipo Data — Política de calidad

Política firmada por el equipo. Toda tabla nueva de producción cumple esto ANTES
de nacer. En los workflows de ingesta se ejecuta como pasos de assertion.

## Assertions obligatorias (toda `fct_`)

- **uniqueKey** de la clave: cero duplicados o la ejecución va a rojo.
- **nonNull** de clave y fecha: cero nulos o la ejecución va a rojo.
- Implementación: pasos del workflow cuyo SQL devuelve filas SOLO si hay
  violación. La validación comprueba `totalRows = 0` (no `rows`: con cero
  filas no existe). Un workflow en verde solo significa algo si las assertions
  pasaron.

## Reglas operativas

- El fallo de una assertion **no es un warning**: detiene la ejecución y
  alerta al canal del equipo, como cualquier otro fallo.
- Un test determinista vale más que mil revisiones a ojo: lo verificable por
  escrito, no lo opinable.
- Si una fuente empieza a degradarse sin romper (nulos que crecen, importes
  que derivan), eso se monitoriza como TENDENCIA, no como umbral absoluto.
