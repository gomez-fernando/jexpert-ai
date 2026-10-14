# Primer catálogo de BBank

Fecha: 2026-10-14, de 15:50 a 15:58 UTC.

Lanzado por Claude Code desde el equipo del usuario, con `scripts/extract_catalog.py`, sobre las 12 copias `fdg_tfm_bbank_*` de la sandbox `dev` de Jakala. Solo lecturas.

## Qué se ejecutó

1. Primera extracción, de 15:50:58 a 15:52:40 UTC: 66 consultas, sin errores. Su salida se sobrescribió con la segunda (incidencia I05 de `../../incidencias.md`).
2. Comprobaciones de lo que se vio en la primera, de 15:53:38 a 15:54:50 UTC, con `comprobaciones_catalogo.py`:

   | Comprobación | Consulta | Resultado |
   | --- | --- | --- |
   | Solicitudes por estado, con y sin cliente | `e4004fed-3555-4229-b318-47a85e9b76a9` | 10.528 aceptadas, todas con cliente. 29.886 denegadas, ninguna con cliente |
   | Emails de las solicitudes que están en la base | `e99ea0e7-8d28-4d8c-8bb5-c463fc08bb9e` | Las aceptadas cruzan con 7.354 clientes y las denegadas con 2.958 |
   | Nombre de los cinco productos de las solicitudes | `6f778092-8c6c-4814-87bb-6726d4751a4e` | Dos cuentas de ahorro y tres tarjetas de crédito |
   | Filas de fidelización por cliente | `4940983a-ce88-4c8f-b5ac-c4bcab3a8b3c` | 500 clientes con dos filas y 2 con una |
   | Clientes de fidelización con puntos distintos en sus filas | `ecae5cf1-0dbc-4974-842c-1f515a16ce75` | Ninguno |
   | Emails de la web sin `profile_id` que están en la base | `2b09ed8d-cab6-44be-9342-6c54c38f605b` | 7.686 clientes |

3. Cambios en el script por lo comprobado: recuentos exactos (I05) y cruce por email (I06). Notas escritas a mano en `catalogo/notas.csv`.
4. Segunda extracción, la que queda en `catalogo/2026-10-14/`, de 15:56:01 a 15:58:09 UTC: 69 consultas, sin errores. Su salida por pantalla está en `extraccion.log`, con la hora local del equipo (UTC+2) y la ruta de salida acortada.

## Resultado

El catálogo de las 12 copias, con seis ficheros: `catalogo.csv`, `datasets.csv`, `relaciones.csv`, `eventos_por_mes.csv`, `catalogo.md` y `extraccion.json`. Las cifras coinciden con el inventario de la sandbox del 2026-10-10: filas, clientes y cruces entre datasets.

## Fechado

Las consultas de las tres partes están en el registro de Query Service del 2026-10-14 con su hora. La primera de la segunda extracción es `5ff88724-9aaf-4d4a-ae3a-56d9a60f3c11` (15:56:48 UTC) y la última, `5dafefc3-f8cd-4674-873b-6e01ac628db2` (15:58:03 UTC).
