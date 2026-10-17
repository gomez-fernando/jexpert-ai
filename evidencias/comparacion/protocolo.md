# Protocolo de la comparación sin y con la skill

Redactado el 2026-10-14, antes de medir nada, como piden los apartados 4 y 6 de la Guía de alumnos TFM. Los puntos marcados como pendientes se cierran antes de la primera medición. Desde ese momento el protocolo no se cambia. Si hubiera que cambiarlo, se anota aquí el cambio, con su fecha y su motivo.

## Tarea

Responder a una petición de audiencia de un equipo de negocio. Para cada segmento de la petición hay que decir si se puede crear, con qué atributos, qué condiciones no se pueden cubrir y por qué, qué decisiones tiene que tomar negocio y qué queda pendiente de comprobar.

## Datos

Los mismos en los dos modos:

- El lote de peticiones de `peticiones/`: cuatro: una que se puede crear, una que se puede crear con matices y dos que no. Están redactadas como un correo de negocio, en lenguaje libre y con alguna ambigüedad. Pendiente de la fase 4.
- El catálogo de `catalogo/2026-10-14/`.
- Las copias `fdg_tfm_bbank_*` de la sandbox `dev`, para las consultas.

## Resultado correcto

Cada petición tiene su respuesta esperada, escrita antes de ejecutar ningún modo y guardada junto a la petición. La calidad se mide igual en los dos modos, con esta lista de puntos:

1. El veredicto de cada segmento.
2. El atributo que cubre cada condición.
3. Los huecos, es decir, las condiciones que no se pueden cubrir.
4. Los avisos de cobertura y de valores vacíos.
5. Las decisiones que tiene que tomar negocio.

La nota de calidad es el porcentaje de puntos acertados. Se puntúa a mano, en la tabla de Mediciones. También se cuentan los errores que se escapan: lo que la respuesta da por bueno y no lo es.

## Modo manual

- Lo hace el usuario, con la UI de AEP y Query Service y sin asistentes de IA.
- Se cronometra de principio a fin una sola petición, con la hora de inicio y de fin en UTC. Pendiente de elegir cuál; se propone una de complejidad media.
- El tiempo del resto de peticiones se estima por pasos, calibrados con esa medida: entender la petición, buscar cada condición en los datasets, lanzar una consulta por condición para ver cuántos clientes la cumplen, redactar la respuesta y revisarla. Se presenta como estimación, con su supuesto.

## Modo con la skill

- Lo hace el usuario con Claude Code y la skill.
- Por cada petición se mide por separado el tiempo de ejecución (desde que se lanza hasta que la skill responde) y el de revisión humana (hasta dar la respuesta por buena), con las horas en UTC.
- La comparación principal usa el modo con acceso a la sandbox, porque el modo manual también la consulta. El modo sin acceso, que es el que probará Roberto Fuertes, se ejecuta con una o dos peticiones del lote para demostrar que funciona, y no entra en la comparación. Lo confirma el usuario el 2026-10-17.

## Entorno

El equipo del usuario, la sandbox `dev` de la organización de Jakala y Claude Code. Cada medición anota el modelo y la versión de la skill (el commit).

## Costes

- Modelo: los tokens de cada ejecución, que constan en el registro de la sesión de Claude Code, por el precio público de la API en la fecha, con la fuente. Lo decide el usuario el 2026-10-17, en lugar de la parte proporcional de la suscripción.
- Data Distiller: las `clusterVMHours` del registro de consultas, decidido el 2026-10-14. Las consultas de tamaño de la skill son lecturas interactivas. Según Adobe no consumen horas, y el 2026-10-17 se comprobó en el registro de consultas: ninguna de las 195 lecturas del TFM hechas hasta ese día tiene `computeMetrics` (`../ejecuciones/2026-10-17_coste-consultas/`). La preparación del entorno consumió 2,24 horas, una sola vez: 0,37 de la copia de prueba y 1,87 de las otras 11, comprobado también ese día.
- Licencias e infraestructura: la licencia de AEP existe con y sin la skill, así que no es un coste incremental. La de Claude se imputa según lo que se decida para el modelo.
- Coste por hora del usuario: pendiente de declarar, con su fuente.

## Beneficio anual

Beneficio neto anual estimado = (horas humanas ahorradas por ejecución × coste por hora - coste incremental de IA y herramientas por ejecución) × ejecuciones anuales.

Las horas ahorradas descuentan la revisión humana. Las ejecuciones anuales (cuántas peticiones de viabilidad hay al año en un proyecto de CDP) son una estimación con su supuesto. Pendiente.

## Mediciones

Una fila por petición y modo. Las horas van en UTC.

| Fecha | Petición | Modo | Quién | Inicio y fin de la ejecución | Inicio y fin de la revisión | Puntos acertados | Errores que se escapan | Coste | Notas |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
