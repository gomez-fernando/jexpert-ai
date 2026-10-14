# Registro de uso de IA

Recoge los intercambios con modelos de IA que afectaron a decisiones, código, reglas o resultados del TFM, según el apartado 7 de la Guía de alumnos TFM. No transcribe cada conversación: cada entrada es un intercambio relevante, con los seis campos que propone la guía.

Las entradas van enmascaradas, sin secretos, datos personales ni nombres reales del proyecto de trabajo del usuario. Las horas van en UTC.

Las entradas R01 a R09 se reconstruyeron el 2026-10-14 a partir del estado del trabajo (`status.md`) y de los registros de las sesiones de Claude Code. En la decisión humana figura lo que quedó anotado como decidido por el usuario, con sus palabras cuando están registradas. El usuario la revisa y la completa con su criterio. Desde R10, cada entrada se anota el mismo día.

## R01. Elección de la vía y del alcance

| Campo | Contenido |
| --- | --- |
| Fecha y tarea | 2026-10-01. Decidir la vía del TFM y su alcance. |
| Herramienta o modelo | Claude Code, con el modelo `claude-opus-5` según el registro de la sesión. |
| Entrada relevante | Explicación del usuario sobre el TFM y sus dos vías, y documentación pública de la herramienta de IA de Adobe (CX Enterprise Coworker). |
| Salida utilizada | Propuesta de ir por la vía del acelerador, limitada a CDP, anonimizada, en español y en un repositorio git propio. |
| Verificación | No aplica: son decisiones de enfoque, sin un resultado que comprobar. |
| Decisión humana | El usuario elige la vía del acelerador porque es la que mejor acogida tiene entre quienes califican, y limita el alcance a CDP. Pendiente de revisión del usuario. |

## R02. Requisitos del TFM

| Campo | Contenido |
| --- | --- |
| Fecha y tarea | 2026-10-02. Extraer los requisitos de la entrega. |
| Herramienta o modelo | Claude Code, con el modelo `claude-sonnet-5-5` según el registro de la sesión. |
| Entrada relevante | Guía de alumnos TFM y transcripciones de las seis sesiones del curso. |
| Salida utilizada | Resumen de requisitos, hoy en `status/requisitos-tfm.md`, con los entregables obligatorios: documento de 15 páginas, capturas, repositorio, evidencia fechada, justificación cuantitativa y este registro. |
| Verificación | El 2026-10-14 se releyó la guía completa y se contrastó con el resumen. Coincide, y la fecha de entrega (2026-10-30) la confirmó el usuario. |
| Decisión humana | El usuario toma el resumen como referencia y decide intentar el vídeo, que es opcional. Pendiente de revisión del usuario. |

## R03. Elección del acelerador

| Campo | Contenido |
| --- | --- |
| Fecha y tarea | 2026-10-02. Elegir qué acelerador construir. |
| Herramienta o modelo | Claude Code, con el modelo `claude-sonnet-5-5` según el registro de la sesión. |
| Entrada relevante | Los trabajos del usuario en un proyecto de CDP, revisados en su entorno de trabajo. No se reproducen aquí. |
| Salida utilizada | Lista de aceleradores posibles. El usuario elige la skill que decide si una petición de audiencia se puede crear. La propuesta para el profesor está en `dudas-roberto.md`. |
| Verificación | Roberto Fuertes López da por buena la propuesta el 2026-10-10. |
| Decisión humana | El usuario elige la viabilidad de audiencias porque es una tarea que repite en su trabajo. Pendiente de revisión del usuario. |

## R04. Acceso a la sandbox y paquete `aep/`

| Campo | Contenido |
| --- | --- |
| Fecha y tarea | 2026-10-10. Conectar con la sandbox `dev` de Jakala por API y por Query Service. |
| Herramienta o modelo | Claude Code, con el modelo `claude-opus-5-5`. |
| Entrada relevante | El fichero de credenciales de la sandbox, leído por scripts que no muestran secretos ni tokens, y los errores de la API. |
| Salida utilizada | El paquete `aep/` con su README. La corrección del envío de los permisos a IMS (incidencia I01). |
| Verificación | Token, lectura de Catalog y Schema Registry, `select 1` y 758 tablas visibles en Query Service, el 2026-10-10. |
| Decisión humana | El usuario decide hacer el TFM sobre la sandbox `dev`, con la autorización de Roberto Fuertes López, y que el paquete sea independiente de su repositorio de trabajo para presentarlo con el TFM. Pendiente de revisión del usuario. |

## R05. Inventario de la sandbox

| Campo | Contenido |
| --- | --- |
| Fecha y tarea | 2026-10-10. Ver qué datos hay en la sandbox para sacar de ellos el catálogo. |
| Herramienta o modelo | Claude Code, con el modelo `claude-opus-5-5`. |
| Entrada relevante | Metadatos de la sandbox por API y recuentos por Query Service. De los campos con datos personales no se guardaron valores. |
| Salida utilizada | `status/inventario-sandbox-dev.md`, con BBank como única familia de datos aprovechable y la línea DemoCJA BCR como base. |
| Verificación | Recuentos y cruces entre datasets lanzados en Query Service el 2026-10-10. |
| Decisión humana | El 2026-10-11, el usuario elige la línea DemoCJA BCR de BBank como base del catálogo y decide usar los datos tal cual, con sus huecos como casos de petición no viable. Pendiente de revisión del usuario. |

## R06. Copia de prueba

| Campo | Contenido |
| --- | --- |
| Fecha y tarea | 2026-10-10 (ya 2026-10-11 en España). Probar a copiar un dataset para no depender de datasets de otros alumnos. |
| Herramienta o modelo | Claude Code, con el modelo `claude-opus-5-5`. |
| Entrada relevante | Las sentencias de copia propuestas en `status/copias-bbank.md`. |
| Salida utilizada | La copia `fdg_tfm_bbank_branch` (`evidencias/ejecuciones/2026-10-10_copia-prueba/`). |
| Verificación | Mismo schema, 11 filas en el origen y en la copia y 0 diferencias de contenido. Consulta `2c4be3db-706b-4318-9d73-017867e9b705`. |
| Decisión humana | El usuario autoriza solo esta copia, decide no copiar los schemas y espera al resultado para decidir el resto. Pendiente de revisión del usuario. |

## R07. Copias de BBank

| Campo | Contenido |
| --- | --- |
| Fecha y tarea | 2026-10-14. Crear las 11 copias restantes. |
| Herramienta o modelo | Claude Code, con el modelo `claude-opus-5-5`. |
| Entrada relevante | La captura del dashboard de uso de licencia (Compute hours: 2.000 contratadas, 0,232 consumidas) y las sentencias de `status/copias-bbank.md`. |
| Salida utilizada | Los scripts de `evidencias/ejecuciones/2026-10-14_copias-bbank/`. Claude recomendaba 9 copias; con la licencia a la vista, recomendó las 11. |
| Verificación | Las 11 consultas terminaron en `SUCCESS`. Cada copia tiene las mismas filas que su origen y 0 diferencias de contenido. |
| Decisión humana | "Haz con las 11. Empieza ya." El control de permisos de Claude Code bloqueó el script (incidencia I03) y el usuario lo lanzó él mismo. Pendiente de revisión del usuario. |

## R08. Plan de trabajo y diseño de la comparación

| Campo | Contenido |
| --- | --- |
| Fecha y tarea | 2026-10-14. Planificar el TFM hasta la entrega y diseñar la comparación sin y con la skill. |
| Herramienta o modelo | Claude Code, con el modelo `claude-opus-5-5`. |
| Entrada relevante | El estado del trabajo y los requisitos de la guía. |
| Salida utilizada | `status/plan-tfm.md`: siete fases, la skill con dos modos (con y sin acceso a la sandbox), un lote de peticiones redactadas como correo de negocio, una petición cronometrada a mano y la calidad medida con una lista de puntos. |
| Verificación | Contrastado con los apartados 4 y 6 de la guía. |
| Decisión humana | "Ok a todas tus propuestas." Sobre la skill: "Si la skill hace más, es mejor. Roberto Fuertes no tiene acceso a la sandbox". Sobre el coste de Data Distiller: "la que sea más fiable, que creo que es la del registro de consultas". La entrega es el 30 de octubre. Pendiente de revisión del usuario. |

## R09. Extractor del catálogo

| Campo | Contenido |
| --- | --- |
| Fecha y tarea | 2026-10-14. Escribir `scripts/extract_catalog.py` y generar el catálogo de las copias. |
| Herramienta o modelo | Claude Code, con el modelo `claude-opus-5-5`. |
| Entrada relevante | Los parámetros del script aprobados el 2026-10-11, el inventario del 2026-10-10 y los schemas y campos de las copias. Solo recuentos, sin valores de datos personales. |
| Salida utilizada | El script, `catalogo/2026-10-14/` y `catalogo/notas.csv`. Sobre la primera versión se corrigieron los recuentos aproximados (incidencia I05) y se añadió el cruce por email (incidencia I06). Claude propuso además el formato del catálogo y que el inventario completo se guarde fuera del repositorio. |
| Verificación | Las cifras coinciden con el inventario del 2026-10-10. Seis consultas de comprobación (`evidencias/ejecuciones/2026-10-14_catalogo/ficha.md`). |
| Decisión humana | "Si el siguiente paso es la fase 2 [...] hazlo." Pendiente de que el usuario revise el formato del catálogo y la carpeta del inventario. |

## R10. Cumplimiento de la guía

| Campo | Contenido |
| --- | --- |
| Fecha y tarea | 2026-10-14. Preparar el trabajo para cumplir las directrices de la guía antes de escribir la skill. |
| Herramienta o modelo | Claude Code, con el modelo `claude-opus-5-5`. |
| Entrada relevante | La Guía de alumnos TFM completa. |
| Salida utilizada | La carpeta `evidencias/` (fichas de ejecución, incidencias, capturas y protocolo de la comparación), el esqueleto de la memoria (`documento/esqueleto-memoria.md`), este registro con las entradas anteriores y el método para fechar las evidencias con el registro de Query Service. |
| Verificación | Los requisitos se contrastaron con la lista de comprobación del apartado 10 de la guía. Las horas de las fichas se comprobaron en el registro de Query Service. |
| Decisión humana | "Es MUY IMPORTANTE respetar y cumplir lo que se pide en la guía del TFM." "Prepara las cosas." Pendiente de revisión del usuario. |
