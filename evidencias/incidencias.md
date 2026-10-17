# Incidencias

Cada incidencia lleva su fecha, lo que pasó, la causa, cómo se resolvió y dónde se puede comprobar. Las horas van en UTC.

## I01. La API respondía 403 "User region is missing"

Fecha: 2026-10-10.

Todas las llamadas a la API de Platform respondían 403 con el código `403027`, aunque el token se obtenía bien. El fichero de credenciales de Postman guarda los permisos (`SCOPES`) como una lista, y se estaban enviando a IMS como un parámetro repetido. IMS concede entonces solo el primero, y sin los demás la API rechaza todas las llamadas.

Se resolvió enviando los permisos en un solo parámetro separados por comas. El paquete `aep/` lo hace siempre (`aep/config.py`, función `_normalize_scopes`) y lo explica en `aep/README.md`.

## I02. La API de descriptores devolvía solo 300 resultados

Fecha: 2026-10-10.

`/data/foundation/schemaregistry/tenant/descriptors` corta la respuesta en 300 descriptores y no ofrece más páginas, así que faltaban identidades y relaciones de muchos schemas. Se resolvió pidiendo cada schema con la cabecera `Accept: application/vnd.adobe.xed-full-desc+json; version=1`, que devuelve sus descriptores junto al schema. `scripts/extract_catalog.py` lo hace así.

## I03. El control de permisos de Claude Code bloqueó el script de las copias

Fecha: 2026-10-14.

El usuario autorizó crear las 11 copias de BBank que faltaban. El script que las lanzaba (`ejecuciones/2026-10-14_copias-bbank/ctas_submit.py`) fue bloqueado por el control automático de permisos de Claude Code, que no dio el motivo. No se creó nada.

El usuario revisó el script y lo lanzó él mismo desde PowerShell. Las 11 consultas quedaron en cola a las 14:53 UTC. Sus IDs están en `ejecuciones/2026-10-14_copias-bbank/ficha.md`.

## I04. Catalog no devuelve más de un esquema observado por llamada

Fecha: 2026-10-14.

Al pedir a Catalog la lista de las copias con sus campos (`observableSchema`), la API respondió 400: "Users are not allowed to load more than 1 observable schema at a time". Se resolvió listando primero los datasets solo con su nombre y pidiendo después los campos de cada uno por separado, como hace `scripts/extract_catalog.py`.

## I05. Los recuentos aproximados de valores distintos se desviaban

Fecha: 2026-10-14.

La primera versión del extractor del catálogo contaba los valores distintos con `approx_count_distinct`. El resultado se desviaba hasta un 4 %, y en algún caso daba más valores distintos que filas: `applicationID` salía con 41.430 en un dataset de 40.414 filas, y `personID` con 7.439 en una base de 7.730 clientes. Se cambió a `count(distinct)`, que es exacto, y con estos volúmenes no tarda más.

La salida de esa primera versión se sobrescribió al repetir la extracción el mismo día, así que estas cifras solo quedan aquí. Desde entonces, cada ejecución que sirve de evidencia guarda su salida en su propia carpeta de `ejecuciones/`.

## I06. Las solicitudes denegadas no llevan cliente

Fecha: 2026-10-14.

En el catálogo, el motivo de rechazo de `fdg_tfm_bbank_applications` salía con una cobertura del 0 % en clientes. Las consultas de comprobación confirmaron que ninguna de las 29.886 solicitudes denegadas lleva `profileID`, el campo que las une con la base de clientes. Las 10.528 aceptadas sí lo llevan.

Las denegadas solo se pueden atribuir a un cliente por el email: 2.958 clientes de la base tienen alguna. Se añadió al extractor el cruce por email y la explicación a `catalogo/notas.csv`. Es una de las situaciones que la skill tiene que detectar en una petición.

Las consultas de comprobación están en el registro de Query Service del 2026-10-14, entre las 15:53 y las 15:55 UTC. Las dos que lo demuestran son `e4004fed-3555-4229-b318-47a85e9b76a9` (solicitudes por estado, con y sin cliente) y `e99ea0e7-8d28-4d8c-8bb5-c463fc08bb9e` (emails de las solicitudes que están en la base). El detalle está en `ejecuciones/2026-10-14_catalogo/ficha.md`.

## I07. El registro de consultas no trae el SQL en el campo `sql`

Fecha: 2026-10-17.

La primera versión del script de coste no encontró ninguna consulta del TFM entre las 4.211 de la sandbox, porque buscaba el texto de cada consulta en el campo `sql`. El listado de `GET /data/foundation/query/queries` no trae ese campo, y al pedir una consulta por su ID llega vacío. El SQL está en `effectiveSQL`. Se cambió el script para leer `effectiveSQL`, y con esa versión aparecieron las 207 consultas del TFM.

Antes, una primera ejecución se paró a los 5 minutos porque no mostraba ningún avance. La versión guardada muestra el avance por página y descarta las páginas repetidas. El detalle está en `ejecuciones/2026-10-17_coste-consultas/ficha.md`.
