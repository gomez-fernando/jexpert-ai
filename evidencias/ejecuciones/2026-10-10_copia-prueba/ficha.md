# Copia de prueba de BBank

Fecha: 2026-10-10, de 23:03 a 23:18 UTC. En España ya era 2026-10-11, y con esa fecha aparece en `status.md` y en `status/copias-bbank.md`.

Lanzada por Claude Code con la autorización del usuario, desde el equipo del usuario, sobre la sandbox `dev` de Jakala.

## Qué se ejecutó

Una sola copia, la del dataset más pequeño, para probar la vía antes de copiar el resto:

```sql
CREATE TABLE fdg_tfm_bbank_branch WITH (schema='Training_BBank_Branch_sch_AbelPerez') AS (
  SELECT branchAddress, branchID FROM training_bbank_branch_ds_abelperez
)
```

## Resultado

| Comprobación | Resultado |
| --- | --- |
| Dataset creado | `fdg_tfm_bbank_branch` (`6acac72535953e0d1770b5d7`) |
| Schema | El mismo que el origen, `Training_BBank_Branch_sch_AbelPerez` |
| Perfil e identidades | Sin habilitar |
| Filas | 11 en el origen y 11 en la copia |
| Contenido | 0 diferencias en los dos sentidos, comparando cada fila como JSON |
| Duración | 878 segundos, unos 13 de ellos en cola |
| Consumo | 0,37 `clusterVMHours` |

## Fechado

- Consulta `2c4be3db-706b-4318-9d73-017867e9b705` en el registro de Query Service: creada a las 23:03:49 UTC y terminada en `SUCCESS` a las 23:18:28 UTC del 2026-10-10.
- Fecha de creación del dataset en Catalog: 2026-10-10.

Los scripts de esta ejecución no se conservaron en el repositorio. La sentencia es la de arriba, y las comprobaciones son las mismas que las de `../2026-10-14_copias-bbank/ctas_verify.py`.
