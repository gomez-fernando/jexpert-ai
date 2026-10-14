# Prueba del inventario completo

Fecha: 2026-10-14, de 15:58 a 16:02 UTC.

Lanzado por Claude Code desde el equipo del usuario, con `scripts/extract_catalog.py --full-inventory`, sobre la sandbox `dev` de Jakala. Solo lecturas. Su objetivo era probar el modo `--full-inventory` del script, no usar el resultado en el TFM.

## Resultado

749 datasets, de los que 509 tienen datos, y todos los que tienen datos con su recuento. 255 segundos y sin errores. El resumen está en `inventario_resumen.json` y la salida por pantalla en `inventario.log`, con la hora local del equipo (UTC+2).

El fichero completo se queda en `inventario/2026-10-14/`, fuera del repositorio, porque lleva los nombres de todos los datasets de una sandbox compartida.

Los 1.954 schemas son todos los schemas propios de la sandbox, incluidos los que Adobe crea de forma automática para cada dataset. Se comprobó que no hay repetidos en la paginación.

## Fechado

509 consultas en el registro de Query Service del 2026-10-14, una por dataset con datos, desde `1502ef48-c3e5-4026-b302-ea2e082448ca` (15:58:43 UTC) hasta `32664d19-b37c-4fce-bbdf-4837365bb12f` (16:02:31 UTC).
