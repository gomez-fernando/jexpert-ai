# Equipo Data — Contexto para calidad e ingesta (S3)

Versión acotada del contexto del equipo para la sesión de ingesta y calidad de pedidos.

## Naming y arquitectura
- Capas de ingesta: `raw` (datos tal cual entran), `stg` (limpios y tipados, stg_pedidos), `gold` (modelo final).
- Los tests de calidad operan entre `raw` y `stg`. 
- SQL Dialect: BigQuery Standard SQL. No usar backticks innecesarios.

## Gestión de la calidad (Reglas del equipo)
1. **La calidad no repara, aísla:** si una fila incumple una regla grave, no intentamos adivinar el valor original (ej. no imputar importes ni fechas inventadas). Se levanta una alerta o se envía a revisión.
2. **Nulos controlados:** preferimos un `NULL` + flag de revisión que un string vacío, `"OTRO"` o un número por defecto mágico como `9999`.
3. **Tests deterministas:** los tests en BQ deben estar escritos como consultas que devuelven *cero filas* si todo está bien. Toda fila devuelta por el test es una infracción.

## Glosario específico del feed de pedidos
- **Feed de pedidos:** archivo CSV que el ERP envía diariamente.
- **Drift:** cambio no avisado en el esquema o semántica del feed.
- **Outlier:** valor atípico (ej. importe muy alto). Se flaggea, no se borra.
