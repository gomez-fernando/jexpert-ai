# Evidencias del TFM

Esta carpeta guarda la evidencia de operación que pide la Guía de alumnos TFM: ejecuciones fechadas, incidencias y su resolución, capturas y la comparación de la tarea sin y con la skill. Se rellena durante el trabajo, no al final, para que cada evidencia tenga la fecha en que ocurrió.

## Contenido

| Ruta | Contenido |
| --- | --- |
| `ejecuciones/` | Una carpeta por ejecución, con el nombre `AAAA-MM-DD_descripcion`. Cada una lleva su `ficha.md` y los ficheros que produjo o usó |
| `incidencias.md` | Las incidencias del trabajo, con su fecha, causa, resolución y la evidencia que las respalda |
| `capturas.md` | Las capturas que necesita el documento, la afirmación que respalda cada una y su pie |
| `capturas/` | Los ficheros de las capturas, con el nombre de su identificador (`C01.png`) |
| `comparacion/` | El protocolo de la comparación sin y con la skill, las peticiones de prueba y las mediciones |

El registro de uso de IA está en `registro-ia.md`, en la raíz del repositorio.

## Ficha de cada ejecución

Cada `ficha.md` recoge:

- Fecha y hora de inicio y fin, en UTC, que es como las registra Adobe.
- Quién la lanzó y desde dónde: equipo, sandbox y versión del código (el commit).
- Qué se ejecutó, con el comando o el script.
- El resultado y las comprobaciones que se hicieron.
- Dónde se puede verificar la fecha: IDs de las consultas en el registro de Query Service, IDs de datasets o lotes, o el commit.
- Las incidencias, con un enlace a `incidencias.md`.

## Fechado de las evidencias

Una fecha escrita a mano no demuestra nada por sí sola. Cada evidencia se apoya en al menos uno de estos registros, ordenados de más a menos fiable:

1. El registro de consultas de Query Service de la sandbox. Cada consulta queda con su ID y la hora del servidor de Adobe, y no se puede modificar. La ficha cita los IDs o la ventana de tiempo de la ejecución, y cualquiera con acceso a la sandbox puede localizarlas con `GET /data/foundation/query/queries` filtrando por la fecha de creación. `scripts/extract_catalog.py` guarda la hora de inicio y fin en `extraccion.json` para esto.
2. Los metadatos de Catalog: la fecha de creación de cada dataset y de cada lote, que también pone Adobe.
3. El historial del repositorio en GitHub. Se hace commit y push al cerrar cada día de trabajo. La fecha del commit la pone el equipo del usuario, pero cada push queda registrado con su hora en la página Activity del repositorio.
4. Las capturas, con la fecha visible en la propia herramienta o en el reloj del sistema.
5. El registro de las sesiones de Claude Code, donde cada mensaje lleva su hora. Es un fichero local, así que sirve de apoyo y no como única prueba.

Las ejecuciones de la skill sin acceso a la sandbox no dejan rastro en Adobe. Para esas, la fecha se apoya en el push a GitHub del mismo día, en la captura y en el registro de la sesión.

## Datos sensibles

Las evidencias no llevan credenciales, tokens ni valores de datos personales. Los datos de BBank son ficticios, pero las capturas y los ficheros muestran solo recuentos de los campos de nombre, email, teléfono, DNI o IBAN, igual que el catálogo.
