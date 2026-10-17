# Registro de uso de IA

Recoge los intercambios con modelos de IA que afectaron a decisiones, código, reglas o resultados del TFM, según el apartado 7 de la Guía de alumnos TFM. No transcribe cada conversación: cada entrada es un intercambio relevante, con los seis campos que propone la guía.

Las entradas van enmascaradas, sin secretos, datos personales ni nombres reales de mi proyecto de trabajo. Las horas van en UTC.

Claude reconstruyó las entradas R01 a R09 el 2026-10-14 a partir del estado del trabajo (`status.md`) y de los registros de las sesiones de Claude Code. En la decisión humana figura lo que quedó anotado como decidido por mí, con mis palabras cuando están registradas, y después la reviso y la completo con mi criterio. Desde R10, cada entrada se anota el mismo día.

## R01. Elección de la vía y del alcance

| Campo | Contenido |
| --- | --- |
| Fecha y tarea | 2026-10-01. Decidir la vía del TFM y su alcance. |
| Herramienta o modelo | Claude Code, con el modelo `claude-opus-5` según el registro de la sesión. |
| Entrada relevante | Mi explicación sobre el TFM y sus dos vías, y documentación pública de la herramienta de IA de Adobe (CX Enterprise Coworker). |
| Salida utilizada | Propuesta de ir por la vía del acelerador, limitada a CDP, anonimizada, en español y en un repositorio git propio. |
| Verificación | No aplica: son decisiones de enfoque, sin un resultado que comprobar. |
| Decisión humana | Elegí la vía del acelerador porque es la que mejor acogida tiene entre quienes califican y porque permite hacer un TFM mucho más completo e interesante. Limité el alcance a CDP porque es donde se construyen las audiencias en el ecosistema de Adobe, por lo que no hace falta usar más herramientas para este TFM que estará dedicado a la optimización y automatización de la evaluación de si es posible o no crear determinadas audiencias en base a los requisitos planteados por negocio. |

## R02. Requisitos del TFM

| Campo | Contenido |
| --- | --- |
| Fecha y tarea | 2026-10-02. Extraer los requisitos de la entrega. |
| Herramienta o modelo | Claude Code, con el modelo `claude-sonnet-5-5` según el registro de la sesión. |
| Entrada relevante | Guía de alumnos TFM y transcripciones de las seis sesiones del curso. |
| Salida utilizada | Resumen de requisitos, hoy en `status/requisitos-tfm.md`, con los entregables obligatorios: documento de 15 páginas, capturas, repositorio, evidencia fechada, justificación cuantitativa y este registro. |
| Verificación | El 2026-10-14 se releyó la guía completa y se contrastó con el resumen. Coincide, y la fecha de entrega (2026-10-30) la confirmé yo. |
| Decisión humana | Tomé el resumen como referencia y decidí intentar el vídeo, que es opcional, porque es una evidencia con más peso para presentar en el TFM. |

## R03. Elección del acelerador

| Campo | Contenido |
| --- | --- |
| Fecha y tarea | 2026-10-02. Elegir qué acelerador construir. |
| Herramienta o modelo | Claude Code, con el modelo `claude-sonnet-5-5` según el registro de la sesión. |
| Entrada relevante | Mis trabajos en un proyecto de CDP, revisados en mi entorno de trabajo. No se reproducen aquí. |
| Salida utilizada | Lista de aceleradores posibles, de la que elegí la skill que decide si una petición de audiencia se puede crear. La propuesta para el profesor está en `dudas-roberto.md`. |
| Verificación | Roberto Fuertes da por buena la propuesta el 2026-10-10. |
| Decisión humana | Elegí la viabilidad de audiencias porque es una tarea que repito en mi trabajo. |

## R04. Acceso a la sandbox y paquete `aep/`

| Campo | Contenido |
| --- | --- |
| Fecha y tarea | 2026-10-10. Conectar con la sandbox `dev` de Jakala por API y por Query Service. |
| Herramienta o modelo | Claude Code, con el modelo `claude-opus-5-5`. |
| Entrada relevante | Quiero que las credenciales de la sandbox estén bien protegidas. El fichero de Postman con las credenciales se queda en mi equipo y fuera de git, para que no suba a GitHub ni entre en la copia de entrega. Tú no puedes leerlo de ninguna forma: ni con Read, Grep o Glob, ni con comandos de shell. Para eso, añade reglas de denegación en la configuración de Claude Code y un hook que bloquee cualquier comando que lo nombre. El único que puede usarlo es el paquete aep/, para autenticarse. Revisa que envíe el client secret solo a Adobe IMS, que use el token solo en las cabeceras y en la conexión a Query Service, y que no imprima ni registre ninguno de los dos. Haz también que, al imprimir la configuración, se oculten client_id, client_secret, api_key y org_id. Quiero que tú solo veas los resultados y los errores de las llamadas. Como un script podría abrir el fichero sin nombrarlo, enséñame antes cualquier script que use `aep/`. El paquete `aep/` no pasa el client secret ni los tokens a Claude: lee las credenciales del fichero de Postman en mi equipo, envía el client secret solo a Adobe IMS para obtener el token y usa el token solo en las cabeceras de las llamadas. Tampoco imprime ni registra esos valores, así que Claude solo ve resultados y errores. En esta tarea recibió el error 403 (`403027`) que devolvía la API de Platform en todas las llamadas (incidencia I01). La configuración de `aep/` oculta el client secret, client_id, api_key y org_id cuando se imprimen, para que un script no pueda mostrarlo por error. |
| Salida utilizada | Un hook en la configuración de Claude Code que deniega cualquier comando de shell que nombre el fichero de credenciales. Se suma a las reglas de denegación de lectura que ya existían. También, el cambio en `aep/config.py` que oculta client_id, client_secret, api_key y org_id al imprimir la configuración. Además, la revisión de `aep/`: el client secret solo va a Adobe IMS, en el cuerpo de la petición, y el token solo en las cabeceras y en la conexión a Query Service, sin imprimir ni registrar ninguno de los dos. Por último, la comprobación de que ningún registro de sesión de Claude Code ni fichero temporal del equipo guarda el contenido del fichero de credenciales. |
| Verificación | El hook bloqueó un comando de prueba que nombraba el fichero y dejó pasar un comando normal. Al imprimir una configuración de aep/ con valores falsos, ninguno de los cuatro campos aparece, y el paquete sigue pudiendo usarlos. Ninguna prueba abrió el fichero de credenciales. En los registros de sesión de Claude Code ninguna salida muestra la configuración con el secreto. La búsqueda del contenido del fichero en esos registros y en la carpeta temporal de Claude no dio ninguna coincidencia. Las dos búsquedas se hicieron solo con recuentos, sin mostrar ninguna línea. |
| Decisión humana | Decidí hacer el TFM sobre la sandbox `dev` después de consultar con Roberto Fuertes sobre los entornos y las posibilidades que tenía para desarrollar el acelerador. También decidí que el paquete `aep/` fuera propio del repositorio del TFM, sin depender de código de otros proyectos, para presentarlo e instalarlo con el TFM. Pedí estas protecciones a partir de mi experiencia con datos sensibles en otros proyectos. |

## R05. Inventario de la sandbox

| Campo | Contenido |
| --- | --- |
| Fecha y tarea | 2026-10-10. Ver qué datos hay en la sandbox para sacar de ellos el catálogo. |
| Herramienta o modelo | Claude Code, con el modelo `claude-opus-5-5`. |
| Entrada relevante | Metadatos de la sandbox por API y recuentos por Query Service. De los campos con datos personales no se guardaron valores. |
| Salida utilizada | `status/inventario-sandbox-dev.md`, con BBank como única familia de datos aprovechable y la línea DemoCJA BCR como base. |
| Verificación | Recuentos y cruces entre datasets lanzados en Query Service el 2026-10-10. |
| Decisión humana | El 2026-10-11 elegí la línea DemoCJA BCR de BBank como base del catálogo porque es la copia más completa: tiene clientes con ingresos, productos y consentimientos, y su navegación web, sus solicitudes y sus entregas, todo unido por el mismo identificador de cliente. Eso permite probar peticiones que combinan varios datasets, que es lo que pide negocio en un proyecto real de CDP. Las otras opciones de la sandbox, Snowclub y Luma, son demasiado pequeñas. Decidí usar los datos tal cual, con sus huecos como casos de petición no viable. |

## R06. Copia de prueba

| Campo | Contenido |
| --- | --- |
| Fecha y tarea | 2026-10-10 (ya 2026-10-11 en España). Probar a copiar un dataset para no depender de datasets de otros alumnos. |
| Herramienta o modelo | Claude Code, con el modelo `claude-opus-5-5`. |
| Entrada relevante | Las sentencias de copia propuestas en `status/copias-bbank.md`. |
| Salida utilizada | La copia `fdg_tfm_bbank_branch` (`evidencias/ejecuciones/2026-10-10_copia-prueba/`). |
| Verificación | Mismo schema, 11 filas en el origen y en la copia y 0 diferencias de contenido. Consulta `2c4be3db-706b-4318-9d73-017867e9b705`. |
| Decisión humana | Autoricé solo esta copia para comprobar primero que salía idéntica al original y cuánto consumía de Data Distiller, antes de lanzar el resto. Decidí no copiar los schemas porque las copias pueden usar los que ya existen, y así no creo objetos de más en una sandbox compartida. |

## R07. Copias de BBank

| Campo | Contenido |
| --- | --- |
| Fecha y tarea | 2026-10-14. Crear las 11 copias restantes. |
| Herramienta o modelo | Claude Code, con el modelo `claude-opus-5-5`. |
| Entrada relevante | La captura del dashboard de uso de licencia (Compute hours: 2.000 contratadas, 0,232 consumidas) y las sentencias de `status/copias-bbank.md`. |
| Salida utilizada | Los scripts de `evidencias/ejecuciones/2026-10-14_copias-bbank/`. Claude recomendaba 9 copias; con la licencia a la vista, recomendó las 11. |
| Verificación | Las 11 consultas terminaron en `SUCCESS`. Cada copia tiene las mismas filas que su origen y 0 diferencias de contenido. |
| Decisión humana | "Hazlo con las 11, esas son las que vamos a usar." Decidí crear también `fdg_tfm_bbank_productinteractions` y `fdg_tfm_bbank_atminfo`, que Claude proponía dejar fuera por aportar poco al catálogo. Con 2.000 horas de licencia y 0,232 consumidas, el coste dejó de ser un limitante, así el catálogo tiene todo BBank. El control de permisos de Claude Code bloqueó el script (incidencia I03) y lo lancé yo manualmente. |

## R08. Plan de trabajo y diseño de la comparación

| Campo | Contenido |
| --- | --- |
| Fecha y tarea | 2026-10-14. Planificar el TFM hasta la entrega y diseñar la comparación sin y con la skill. |
| Herramienta o modelo | Claude Code, con el modelo `claude-opus-5-5`. |
| Entrada relevante | El estado del trabajo y los requisitos de la guía. |
| Salida utilizada | `status/plan-tfm.md`: siete fases, la skill con dos modos (con y sin acceso a la sandbox), un lote de peticiones redactadas como correo de negocio, una petición cronometrada a mano y la calidad medida con una lista de puntos. |
| Verificación | Contrastado con los apartados 4 y 6 de la guía. |
| Decisión humana | Ok, me parece adecuado tener dos modos, así hay más flexibilidad en cuanto a poder probarla. Además Roberto Fuertes no tiene acceso a la sandbox. Sobre el costo de Data Distiller vamos a obtenerlo del registro de consultas porque da el consumo de cada consulta con su ID y en el momento. |

## R09. Extractor del catálogo

| Campo | Contenido |
| --- | --- |
| Fecha y tarea | 2026-10-14. Escribir `scripts/extract_catalog.py` y generar el catálogo de las copias. |
| Herramienta o modelo | Claude Code, con el modelo `claude-opus-5-5`. |
| Entrada relevante | Los parámetros del script aprobados el 2026-10-11, el inventario del 2026-10-10 y los schemas y campos de las copias. Solo recuentos, sin valores de datos personales. |
| Salida utilizada | El script, `catalogo/2026-10-14/` y `catalogo/notas.csv`. Sobre la primera versión se corrigieron los recuentos aproximados (incidencia I05) y se añadió el cruce por email (incidencia I06). Claude propuso además el formato del catálogo y que el inventario completo se guarde fuera del repositorio. |
| Verificación | Las cifras coinciden con el inventario del 2026-10-10. Seis consultas de comprobación (`evidencias/ejecuciones/2026-10-14_catalogo/ficha.md`). |
| Decisión humana | "Si el siguiente paso es la fase 2 [...] hazlo." Doy por bueno el formato del catálogo, porque es mejor tener las notas separadas para evitar perderlas en una nueva extracción. Me parece bien separar el inventario del catálogo. El catálogo es lo que lee la skill y se entrega con su fecha, y el inventario solo sirve para explorar la sandbox, así que no hace falta que esté en el repositorio. |

## R10. Cumplimiento de la guía

| Campo | Contenido |
| --- | --- |
| Fecha y tarea | 2026-10-14. Preparar el trabajo para cumplir las directrices de la guía antes de escribir la skill. |
| Herramienta o modelo | Claude Code, con el modelo `claude-opus-5-5`. |
| Entrada relevante | La Guía de alumnos TFM completa. |
| Salida utilizada | La carpeta `evidencias/` (fichas de ejecución, incidencias, capturas y protocolo de la comparación), el esqueleto de la memoria (`documento/esqueleto-memoria.md`), este registro con las entradas anteriores y el método para fechar las evidencias con el registro de Query Service. |
| Verificación | Los requisitos se contrastaron con la lista de comprobación del apartado 10 de la guía. Las horas de las fichas se comprobaron en el registro de Query Service. |
| Decisión humana | "Es MUY IMPORTANTE respetar y cumplir lo que se pide en la guía del TFM." Decido preparar las evidencias antes de la skill y no al final, porque la guía pide ejecuciones fechadas con sus incidencias reales y es más fácil recogerlas mientras voy trabajando en lugar de reconstruirlas después. |

## R11. Coste de Data Distiller por la API

| Campo | Contenido |
| --- | --- |
| Fecha y tarea | 2026-10-17. Sacar del registro de consultas de Query Service el coste en horas de clúster de todas las consultas del TFM. |
| Herramienta o modelo | Claude Code, con el modelo `claude-opus-5-5`. |
| Entrada relevante | Mi captura del dashboard de uso de licencia en la vista Development, con los datos recogidos por última vez el 2026-10-10. Mi petición de sacar el coste por la API en lugar de con el dashboard, y mi autorización para que `aep/` use el fichero de credenciales. El registro de consultas de la sandbox `dev`, sin los campos `clientId` ni `userId`. |
| Salida utilizada | El script `coste_consultas.py` y su salida: 207 consultas del TFM desde el 2026-10-10, 12 CTAS con 2,2383 horas de clúster y 195 lecturas interactivas sin `computeMetrics`. La ficha de la ejecución (`evidencias/ejecuciones/2026-10-17_coste-consultas/`), la incidencia I07 y el cambio en el protocolo de la comparación. |
| Verificación | Las horas de las 12 CTAS coinciden con las que se anotaron al crearlas, el 2026-10-10 y el 2026-10-14. Cada consulta se puede localizar por su ID en el registro de Query Service. |
| Decisión humana | Decidí sacar el coste del registro de consultas y no del dashboard de uso de licencia. El dashboard tenía los datos de desarrollo de hace una semana y mezcla todos los sandboxes de desarrollo de la organización, mientras que el registro da lo que gasta cada consulta del TFM, con su ID. Acepto el resultado. Preparar el entorno costó 2,24 horas de clúster de las 2.000 contratadas, y en el registro las lecturas no consumen horas, así que las consultas de tamaño de la skill no añaden coste de Data Distiller. Revisé el dashboard de uso de licencia y vi que tiene un selector Production/Development. La C03 se tomó en la vista Production, y en la vista Development, que es donde cuenta la sandbox `dev`, los datos se recogieron por última vez el 2026-10-10. Por eso mantengo la C03 con el pie corregido, solo como prueba de las 2.000 horas contratadas, y dejo de usar el dashboard para el coste, que saco del registro de consultas. |


