# Estado: TFM Jakala (acelerador de proyectos)

Última actualización: 2026-10-14

Fecha límite: 2026-10-30, entrega del TFM (fecha confirmada por el usuario el 2026-10-14)

## Punto actual

El TFM es una skill que decide si una petición de audiencia se puede crear, con dos modos (con y sin acceso a la sandbox, porque Roberto Fuertes López no lo tiene), sobre la sandbox `dev` de Jakala y los datos de BBank, un banco ficticio. La entrega es el 2026-10-30 y el plan, con sus siete fases, está en `status/plan-tfm.md`.

Las fases 1 y 2 están cerradas: las 12 copias `fdg_tfm_bbank_*` (2,24 horas de clúster de las 2.000 de la licencia) y el catálogo en `catalogo/2026-10-14/`, generado con `scripts/extract_catalog.py` y commiteado por el usuario en `c13649a`. Lo más importante del catálogo para la skill es que las solicitudes denegadas solo se atribuyen a clientes por el email.

Antes de empezar la skill quedó preparado el cumplimiento de la guía: `evidencias/` (fichas fechadas con el registro de Query Service, incidencias I01 a I06, capturas previstas y protocolo de la comparación), `documento/esqueleto-memoria.md` y el registro de IA con diez entradas. El repositorio y su historial ya no tienen referencias al proyecto de trabajo del usuario: lo que no se entrega está en `privado/`, fuera de git, y `jexpert-ai` se recreó en GitHub con el historial limpio (`21f8a7c`). Falta que el usuario revise la decisión humana del registro y haga las capturas C01 a C03.

## Siguiente paso

Fase 3 de `status/plan-tfm.md`, del 2026-10-17 al 2026-10-21 (se puede adelantar): escribir la skill en `skills/viabilidad-audiencia/` (`SKILL.md`, carpeta `referencias/` y README), con sus dos modos sobre `catalogo/2026-10-14/catalogo.csv` y la referencia de forma de `materiales/materiales/1790663075282_sesion05_operacion/sesion05_operacion/skills/generar-pipeline-workflows/SKILL.md`. Al empezar, pedir al usuario la captura C06 de `evidencias/capturas.md` (la instrucción a Claude Code y la propuesta). Cada ejecución de la skill deja su ficha en `evidencias/ejecuciones/` y cada intercambio relevante, su entrada en `registro-ia.md`, el mismo día. Al cerrar la fase, revisión con el usuario para la decisión humana. No dependen de eso mirar el dashboard de licencia hacia el 2026-10-17 ni las capturas C01 a C03.

## Decisiones tomadas

- 2026-10-01: el TFM va por la vía del acelerador de proyectos y no por la de discovery de datos. Es la que mejor acogida tiene entre quienes califican los trabajos.
- 2026-10-01: el trabajo vive en una carpeta del entorno de trabajo del usuario, para poder reutilizar su material de CDP. El contenido es de un repositorio personal, separado del de su proyecto de trabajo.
- 2026-10-01: la ejecución del acelerador se plantea sobre CX Enterprise Coworker, la herramienta de IA de Adobe anunciada ese mismo día. Resuelve el problema de compliance de usar herramientas de IA no aprobadas sobre el entorno del cliente. El diseño y la preparación se hacen fuera de ella.
- 2026-10-01: el acelerador cubre solo CDP, no proyectos de datos de Jakala en general.
- 2026-10-01: todo se anonimiza. El objetivo es una skill reutilizable en otros proyectos, así que no puede depender de ningún nombre de cliente, dataset, audiencia ni destino reales. Los nombres propios entran como parámetros de un fichero de configuración.
- 2026-10-01: el entregable se escribe en español.
- 2026-10-01: esta carpeta es un repo git propio con rama `main`. El usuario hace los commits, el push y el alta del remoto a mano. El `.gitignore` solo deja fuera ruido de Python, del sistema y del editor: `materiales/` y `status.md` sí entran en el repo.
- 2026-10-01: el desarrollo se hace entero fuera de Coworker y a Coworker solo se llevan las versiones finales. Antes de construir nada se gasta un piloto de calibración de 10 a 15 inputs sobre un flujo real, porque el motor no es el mismo y un prompt afinado fuera no se comporta igual dentro.
- 2026-10-01: en el acelerador, cada empresa del grupo con su propia web y sus datasets es el parámetro `{negocio}`, que se rellena en el fichero de configuración. Ninguna query de la skill lleva el nombre escrito a mano.
- 2026-10-01: el repo de `JEXPERT` será privado, así que no hace falta sanear `status.md` ni `materiales/` antes del primer push.
- 2026-10-01: el objetivo es un trabajo de calidad suficiente, no el mejor del curso. El alcance se dimensiona para que quede bien sin dedicarle horas de más, y ante la duda se recorta antes que ampliar.
- 2026-10-01: las evidencias son un vídeo del piloto, grabado sin editar y solo como respaldo, y cuatro o cinco capturas para la memoria. Las capturas tienen que incluir resultados, no solo lo que se le escribe a Coworker, porque un trabajo con solo entradas parece no ejecutado.
- 2026-10-01: en la memoria se explica qué aporta la skill al proyecto y no qué le falta a las de Adobe, porque su contenido no se puede leer y esa afirmación no se podría demostrar.
- 2026-10-02: se intenta hacer un vídeo, que es opcional y puntúa. Amplía la decisión del 2026-10-01 que lo dejaba solo como respaldo sin editar, y deja sin decidir si va montado. El usuario no busca estar entre los dos mejores trabajos, que son los que deben llevar vídeo. Si saliera entre ellos y no pudiera grabarlo, por ejemplo por quedarse sin créditos de AEP, lo explicará y competirá sin vídeo.
- 2026-10-02: el registro de uso de IA recoge de forma veraz todas las herramientas usadas, también Claude Code. Cada entrada se anota enmascarada, sin esquemas, datasets ni nombres reales del proyecto de trabajo del usuario. Todo lo que se envíe a un modelo para el TFM se anonimiza antes, como ya se decidió el 2026-10-01 y exige la guía.
- 2026-10-02: los datos del proyecto de trabajo del usuario se quedan en su entorno y no entran en este repositorio. Decide el usuario.
- 2026-10-02: las normas del cliente del usuario y de Jakala no permiten enviar datos desde la cuenta personal del usuario. Para el TFM no se abren ni se pegan datos reales en el asistente. Las skills llevan parámetros y ejemplos sintéticos, y un fichero real solo entra enmascarado por un script local que ejecuta el usuario. El mecanismo concreto, incluidas las reglas de denegación de lectura en la configuración, está sin confirmar.
- 2026-10-02: la propuesta de tipo de acelerador, tarea a medir y calendario no se prepara todavía. Decide el usuario. Superada ese mismo día al elegirse la skill de viabilidad de audiencias.
- 2026-10-02: antes de la skill del TFM se construye una skill real de viabilidad de audiencias para el proyecto de trabajo del usuario, fuera de este repositorio. Motivo: tener otra herramienta útil en el trabajo y saber, con una skill real, qué datos anonimizar y cuántos inputs de Coworker necesita una ejecución. Decide el usuario. Superada el 2026-10-14.
- 2026-10-02: de la skill del trabajo a la del TFM pasan el método y lo aprendido, no los ficheros, y la del TFM se hace sin ningún dato real: catálogo, peticiones y respuestas esperadas inventados. Decide el usuario.
- 2026-10-02: el TFM deja de ejecutarse en Coworker como vía principal y se desarrolla y prueba en Claude con datos inventados. Nadie, incluido el profesor, va a ejecutar dentro del entorno del proyecto, y casi todos los alumnos usan cuenta personal. Coworker queda como extra opcional y sustituye a lo decidido el 2026-10-01 sobre ejecutar en Coworker. Decide el usuario.
- 2026-10-02: la skill del TFM decide si una audiencia se puede crear a partir de un catálogo de atributos y una petición, y deja fuera la validación contra AEP porque el profesor no tiene acceso. Lista las comprobaciones que quedarían pendientes, sin ejecutarlas. Decide el usuario.
- 2026-10-02: se entregan al profesor dos catálogos ya preparados, de sectores distintos, y la prueba con uno propio es opcional. La skill comprueba primero el formato del catálogo. La complejidad sube con peticiones ricas (varios bloques, condiciones que se pisan, casos límite) y no con funciones añadidas. Decide el usuario.
- 2026-10-02: las afirmaciones generales sobre Adobe de la skill se escriben desde la documentación pública, con enlace y fecha de comprobación, y lo no comprobado se marca como a verificar.
- 2026-10-02: la línea base manual se declara como estimación marcada, con su supuesto, y no como medida, porque el usuario no tiene tiempo de cronometrarla. La guía admite estimaciones marcadas y no una línea base inventada. Queda por fijar la base de la estimación.
- 2026-10-10: en la sandbox de aprendizaje de Jakala (`dev`) se puede ejecutar con la cuenta personal de Claude. Lo autoriza Roberto Fuertes López. Es una excepción a la norma recogida el 2026-10-02 que solo cubre esa sandbox: para el entorno del cliente no cambia nada.
- 2026-10-10: Roberto Fuertes López da por buena la propuesta de acelerador de `dudas-roberto.md` para el TFM. No hay respuestas por separado a cada una de las cinco dudas del fichero.
- 2026-10-10: el TFM se hace sobre la sandbox `dev` de Jakala y no sobre el proyecto de trabajo del usuario. Decide el usuario. Queda por revisar lo decidido el 2026-10-02 sobre datos inventados y sin validación contra AEP.
- 2026-10-10: el código para la API de Platform y Query Service es el paquete `aep/` de esta carpeta, independiente del entorno de trabajo del usuario para poder presentarlo con el TFM. Lee las credenciales del fichero de Postman y se ejecuta con un `.venv` propio. Decide el usuario.
- 2026-10-10: el catálogo de la skill sale de los datos que ya hay en la sandbox `dev`, y lo que falte se crea en ella. Se dejan de usar los catálogos inventados. Decide el usuario.
- 2026-10-10: todo el contenido de esta carpeta va al GitHub personal (`jexpert-ai`) salvo las credenciales, que excluye el `.gitignore` con `*.postman_environment.json`. Decide el usuario.
- 2026-10-11: la base del catálogo es la línea DemoCJA BCR de BBank con sus tablas de apoyo, y los datos se usan tal cual. Los huecos (movimientos de tarjeta, evolución del saldo, importe de las solicitudes, propensión sin cruce) sirven como casos de petición no viable. Decide el usuario.
- 2026-10-11: el catálogo que se genere se guarda en el repositorio con su fecha de extracción, porque la sandbox es compartida. Decide el usuario.
- 2026-10-11: los datasets de la base se copian con CTAS sobre los schemas existentes, con el prefijo `fdg_tfm_bbank_`. No se copian los schemas. Primero una sola copia de prueba. Decide el usuario.
- 2026-10-11: el script reutilizable será `scripts/extract_catalog.py`, con `--datasets` (regex, por defecto `^fdg_tfm_bbank_`), `--out-dir` (por defecto `catalogo/AAAA-MM-DD/`) y `--full-inventory` como alternativa. Decide el usuario.
- 2026-10-14: se crean las 11 copias que faltan, también `fdg_tfm_bbank_productinteractions` y `fdg_tfm_bbank_atminfo`, que se iban a dejar fuera por aportar poco al catálogo. Con 2.000 horas de licencia, el coste deja de ser un criterio y así el catálogo tiene todo BBank. Decide el usuario.
- 2026-10-14: la skill del TFM no espera a la del proyecto de trabajo del usuario, porque la entrega es el 2026-10-30. Sustituye a lo decidido el 2026-10-02 de construir antes la del trabajo, y deja sin objeto recoger sus lecciones para el TFM. Decide el usuario.
- 2026-10-14: la skill funciona en dos modos. Con credenciales de la sandbox calcula el tamaño exacto con Query Service sobre las copias, y sin ellas, que es como la probará Roberto Fuertes López, estima el tamaño con los recuentos por valor del catálogo. Sustituye a lo decidido el 2026-10-02 de dejar fuera la validación contra AEP, porque la skill hace más con la sandbox. Decide el usuario.
- 2026-10-14: la comparación sin y con la skill usa un lote de cinco o seis peticiones redactadas como correo de negocio. Las horas a mano salen de cronometrar una petición y estimar el resto por pasos calibrados con esa medida, y la calidad, de una lista de puntos común a los dos modos. Cambia lo decidido el 2026-10-02 de no cronometrar nada. Detalle en `status/plan-tfm.md`. Decide el usuario.
- 2026-10-14: el coste de Data Distiller del TFM sale del registro de consultas (`computeMetrics.clusterVMHours`) y no del dashboard de licencia, porque da el consumo de cada consulta con su ID y en el momento. Decide el usuario.
- 2026-10-14: el formato del catálogo es `catalogo.csv` (un atributo por fila) con `datasets.csv`, `relaciones.csv`, `eventos_por_mes.csv`, `catalogo.md` y `extraccion.json`, y las notas manuales van en `catalogo/notas.csv`. Lo propone Claude al escribir el script, con el "hazlo" del usuario, y queda pendiente de su revisión.
- 2026-10-14: con `--full-inventory`, la carpeta por defecto es `inventario/AAAA-MM-DD/` y no `catalogo/AAAA-MM-DD/`, y `inventario/` entra en el `.gitignore`. Motivo: el inventario lleva los nombres de los datasets de las POC de clientes de Jakala, que se excluyeron el 2026-10-10 y no deben subir a GitHub. Cambia el valor por defecto aprobado el 2026-10-11. Lo propone Claude y queda pendiente de revisión del usuario.
- 2026-10-14: los datasets de POC de la sandbox quedan fuera por completo, también de las conversaciones: no se vuelven a mencionar al usuario. Las copias `fdg_tfm_bbank_*` no tienen relación con ellos. Decide el usuario.
- 2026-10-14: la skill va en `skills/viabilidad-audiencia/`, con `SKILL.md`, una carpeta `referencias/` y el README. Lo confirma el usuario con un "vale".
- 2026-10-14: el cumplimiento de la guía se prepara antes de la skill, con evidencias generadas durante el trabajo, una revisión del usuario al cerrar cada fase para el análisis crítico y el registro de IA anotado el mismo día. Detalle en `status/plan-tfm.md`. Decide el usuario ("Es MUY IMPORTANTE respetar y cumplir lo que se pide en la guía del TFM").
- 2026-10-14: las fechas de las evidencias se apoyan en el registro de consultas de Query Service (ID y hora del servidor), los metadatos de Catalog, el push diario a GitHub y la fecha visible en las capturas, por ese orden. Las horas se anotan en UTC. Lo propone Claude a una pregunta del usuario. Un sello de tiempo de una autoridad externa (RFC 3161) se dejó como opción, sin adoptar.
- 2026-10-14: se sacan del repositorio todas las referencias al proyecto de trabajo del usuario y a sus equipos. Lo que hace falta para trabajar y no se entrega queda en `privado/`, fuera de git, con la copia completa del `status.md` anterior a la limpieza. Decide el usuario.
- 2026-10-14: se reescribe el historial de git: `status.md`, `dudas-roberto.md` y la transcripción de la sesión 4 se quitan de todos los commits con `git filter-repo`, y sus versiones limpias entran en el commit `a45d87c`. Los cinco commits anteriores conservan su fecha y cambian de identificador. En GitHub hay que borrar el repo y crearlo de nuevo, porque tras un force push la página Activity sigue enlazando el estado anterior. La copia del historial anterior está en `privado/` (`historial-anterior-2026-10-14.bundle` y `git-anterior-2026-10-14/`). Decide el usuario.
- 2026-10-14: el registro de IA pasa de una tabla única a una tabla por entrada, porque los seis campos no caben en una fila legible. Las entradas R01 a R09 se reconstruyen del estado y de los registros de sesión, con la decisión humana pendiente de revisión del usuario.

## Líneas descartadas

- Pedir al equipo del proyecto de trabajo del usuario que reserve una parte de los créditos de Coworker para el TFM. El usuario lo descarta el 2026-10-01. No insistir, y planificar contando con que el saldo puede agotarse sin aviso.
- Anonimizar con el propio asistente, o fiar la protección de los datos a los ajustes de privacidad de la cuenta. Todo lo que lee el asistente viaja a los servidores de Anthropic, y para anonimizar un dato antes habría que leerlo. La norma del cliente y de Jakala tampoco depende de ese ajuste. No seguir por ahí.
- Validar el acelerador del TFM contra el AEP del proyecto de trabajo del usuario. El profesor no tiene acceso a ese AEP y su licencia de Data Distiller estaba casi agotada (según Adobe, las horas las gastan las consultas batch, no las lecturas interactivas). No seguir por ahí. No aplica a la sandbox `dev` de Jakala, que se usa desde el 2026-10-10.

## Pendiente

- [ ] Solo si se usa Coworker, que es opcional desde el 2026-10-02: probar la subida de un `SKILL.md` mínimo, comprobar hasta dónde llegan las skills de Adobe en un caso real de CDP, pedir los tres permisos del dashboard de monitorización de Agentic AI, fijar el presupuesto de inputs por fase (unos 400 como máximo a 25 créditos por input) y medir el coste real de un input, también de uno que ejecute SQL o lance un agente, porque Adobe no define qué cuenta como input.
- [ ] Comprobar en el campus las instrucciones de entrega.
- [ ] Revisar la decisión humana de las entradas R01 a R10 de `registro-ia.md` y completarla con el porqué. Lo hace el usuario.
- [ ] Hacer las capturas C01 y C02 y recortar y guardar la C03 (`evidencias/capturas.md`). Lo hace el usuario.
- [ ] Hacer commit y push al cerrar cada día de trabajo, para que GitHub registre la fecha. Lo hace el usuario.
- [ ] Escribir la skill con sus dos modos, sus ficheros de referencia y el README (fase 3).
- [ ] Escribir las cinco o seis peticiones de prueba con su respuesta esperada (fase 4).
- [ ] Cronometrar de principio a fin una petición resuelta a mano, para calibrar la estimación de las horas a mano (fase 5).
- [ ] Estimar cuántas peticiones de viabilidad hay al año en un proyecto de CDP y el coste por hora, para el beneficio anual (fase 5).
- [ ] Mirar el dashboard de uso de licencia hacia el 2026-10-17. Si Compute hours ha subido unas 2,2 horas desde las 0,232 del 2026-10-14, el dashboard y el registro de consultas miden lo mismo con retraso, y el documento puede explicarlo. Lo hace el usuario.

## Datos clave

- Repo git propio en rama `main`, con el remoto `jexpert-ai` en GitHub desde 2026-10-02 (privado, según lo decidido el 2026-10-01). La carpeta `privado/` queda fuera del repo, con el contexto del entorno de trabajo del usuario que no se entrega.
- CX Enterprise Coworker (créditos, consumo, licencia, personalizaciones y skills de Adobe) tiene su detalle fuera del repositorio desde el 2026-10-14. Es un extra opcional desde el 2026-10-02, y con él sus pendientes (subida de `SKILL.md`, prueba de las skills de Adobe, permisos del dashboard, presupuesto y coste de inputs).
- Data Distiller en la sandbox `dev`: el registro de consultas (`/data/foundation/query/queries`) da `computeMetrics.clusterVMHours` en cada consulta batch. Cada CTAS o `INSERT INTO` gasta entre 0,10 y 0,37 horas aunque escriba una fila, las fallidas también consumen y pasan unos 13 minutos en cola, aunque varias lanzadas a la vez esperan en paralelo. Que esa cifra sea la que descuenta la licencia está sin confirmar, pero es la que usa el TFM como coste desde el 2026-10-14.
- Licencia de la organización de Jakala, según la captura del dashboard de uso de licencia que pasó el usuario el 2026-10-14: Compute hours 2.000 contratadas y 0,232 consumidas (0 %), AI credits 19.400 de 10.000 (194 %) y Addressable audience 8.352 de 6.000 (139 %).
- Requisitos de la guía y del profesor (qué es un acelerador, entregables obligatorios, prueba sin y con acelerador, criterios de nota, convenciones para la skill, skill de referencia del curso y regla de datos) en `status/requisitos-tfm.md`.
- Paquete `aep/` (README en `aep/README.md`), instalado en modo editable en el `.venv` de esta carpeta, con `credentials_path` y `sandbox` en lugar de `environment`. Credenciales OAuth de la sandbox `dev` en `Credential in JAKADEMY JXpert API.postman_environment.json`, que el `.gitignore` excluye.
- Inventario de la sandbox `dev` del 2026-10-10 en `status/inventario-sandbox-dev.md`, con el acceso a la API y sus particularidades al final. Los datos extraídos están en `status/sandbox-dev/`, fuera del repo.
- Roberto Fuertes López, profesor del Track Data de Jxpert IA y quien corrige el TFM, Jakala. No tiene acceso a la sandbox `dev` (lo dice el usuario el 2026-10-14). Mario Trapello, Jakala, fijó lo que hay que entregar según el profesor (rol sin confirmar).

## Lectura para retomar

1. `status/plan-tfm.md`, con las fases, las fechas, el diseño de la skill y de la comparación y cómo se cumple la guía.
2. `evidencias/README.md`, con dónde va cada evidencia y cómo se fecha.
3. `status/requisitos-tfm.md`, con los requisitos de la guía y del profesor.
4. `status/inventario-sandbox-dev.md`, con lo que hay en la sandbox y los atributos de BBank ya perfilados.
5. `status/copias-bbank.md`, con las sentencias, los IDs y las comprobaciones de las 12 copias.
6. `aep/README.md`, para usar la API de Platform y Query Service sobre la sandbox `dev`.
7. `dudas-roberto.md`, con la propuesta de acelerador que Roberto Fuertes López dio por buena el 2026-10-10.
8. `materiales/materiales/1790663075282_sesion05_operacion/sesion05_operacion/`, con la skill y el README de ejemplo del curso.
9. `materiales/materiales/Guia de alumnos TFM.docx` y `materiales/clases/Jxpert IA Aplicada - Track Data -  Sesion 6 - TFM.vtt`, solo si hay duda sobre algún requisito.
10. `privado/contexto-trabajo.md`, fuera del repositorio, con el material de referencia del entorno de trabajo del usuario y el contexto que no se entrega.

Las rutas son relativas a esta carpeta.

## Cronología

- 2026-10-01: Adobe comunica que CX Enterprise Coworker ya está disponible y el usuario confirma que tiene acceso.
- 2026-10-01: se abre el trabajo, se crea su carpeta y se decide la vía del acelerador.
- 2026-10-01: se fijan alcance (solo CDP), anonimización, idioma (español) y versionado (repo git propio en la carpeta).
- 2026-10-01: se documenta el presupuesto de la prueba de Coworker, 10.000 créditos a 25 por input de chat.
- 2026-10-01: se revisa el consumo de la prueba de Coworker en el dashboard de uso de licencia. El de monitorización de Agentic AI no aparece en la UI, lo más probable es que falten permisos.
- 2026-10-01: se descubre que Coworker admite skills propias en Customizations, lo que abre la vía de entregar el acelerador instalado en la herramienta.
- 2026-10-01: la pantalla de Customizations confirma los ámbitos personal y de organización, el botón de alta y 187 skills de Adobe ya instaladas.
- 2026-10-01: el alta de skills acepta `SKILL.md` o un paquete comprimido, así que el acelerador se puede escribir entero fuera de Coworker y subirlo. Las fichas de las skills de Adobe no muestran su contenido.
- 2026-10-01: se cierra el formato de las evidencias y se acuerda que los materiales de las clases llegan como siete transcripciones `.vtt`.
- 2026-10-02: llegan los materiales a `materiales/`: seis transcripciones, cinco `.zip` y la Guía de alumnos TFM. Se leen la guía, las seis transcripciones y la estructura de los `.zip`.
- 2026-10-02: la entrega queda en 2026-10-31 según el profesor, sin confirmar en el campus. La guía añade requisitos que el estado no recogía: registro de uso de IA, evidencia de operación fechada, justificación cuantitativa y verificación por otra persona.
- 2026-10-02: el usuario decide intentar el vídeo y no preparar todavía la propuesta de acelerador. Queda abierto el alcance del registro de uso de IA.
- 2026-10-02: se cierra el alcance del registro de uso de IA: veraz, con todas las herramientas usadas y las entradas enmascaradas.
- 2026-10-02: se crea `registro-ia.md` sin entradas. El usuario decide que los datos de su proyecto de trabajo se queden en su entorno, y queda pendiente moverlos desde este `status.md`.
- 2026-10-02: se confirma que las normas del cliente del usuario y de Jakala no permiten enviar datos desde la cuenta personal, y se descarta anonimizar con el propio asistente. Se releen las páginas de Adobe: 25 créditos fijos por input, sin relación con tokens, sin definición de input y con tarifa temporal.
- 2026-10-02: se revisan los trabajos del usuario en su proyecto de CDP en busca de aceleradores posibles y el usuario elige la viabilidad de peticiones de audiencia. Decide construirla antes como skill real para ese proyecto, fuera de este repositorio.
- 2026-10-02: el usuario decide hacer el TFM con una versión genérica de esa skill, con datos inventados y en Claude, y Coworker pasa a extra opcional. Se anotan las dudas para Roberto Fuertes López en `dudas-roberto.md`.
- 2026-10-02: primer commit y push de `jexpert-ai`, que el usuario confirma como privado.
- 2026-10-02: se añade a `dudas-roberto.md` el contexto de la propuesta, y el catálogo real de atributos del proyecto de trabajo sale de esta carpeta.
- 2026-10-10: llegan las credenciales de la sandbox de aprendizaje de Jakala, con autorización de Roberto para usar la cuenta personal de Claude. Se comprueba que sirven para la API de Platform y para Query Service.
- 2026-10-10: Roberto Fuertes López da por buena la propuesta de acelerador. El usuario decide hacer el TFM sobre la sandbox `dev` de Jakala y no sobre su proyecto de trabajo.
- 2026-10-10: el `.gitignore` pasa a excluir `*.postman_environment.json` y se crea el paquete `aep/` con su `.venv`, probado contra `dev` con la API de Platform y Query Service.
- 2026-10-10: el usuario decide sacar el catálogo de la sandbox. Se inventaría `dev` entera (733 datasets, 412 schemas en uso, 453 audiencias), se cuentan las filas de los 493 datasets con datos y se perfilan campo a campo los 64 de BBank, Snowclub y Luma. BBank queda como única familia aprovechable.
- 2026-10-11: el usuario confirma la base del catálogo y plantea copiar los datasets. Se prepara la propuesta de 12 copias en `status/copias-bbank.md`.
- 2026-10-11: se crea y se valida la copia de prueba `fdg_tfm_bbank_branch` (0,37 horas de clúster, 15 minutos). En `dev` las consultas batch de usuarios suman 3,8 horas desde el 2026-03-30.
- 2026-10-14: el usuario descomprime los cinco `.zip` de `materiales/materiales/` y saca del repo `status/coworker.md`, que llevaba datos de su proyecto de trabajo. Todo queda en el commit `578c5ef`.
- 2026-10-14: el dashboard de uso de licencia de Jakala da 2.000 horas de Data Distiller y 0,232 consumidas. El usuario decide crear las 11 copias restantes. El clasificador de permisos de Claude Code bloquea el script que las lanza y no se crea ninguna.
- 2026-10-14: el usuario ejecuta el script y las 11 consultas CTAS quedan en cola a las 14:53 UTC.
- 2026-10-14: las 11 consultas terminan en `SUCCESS` a las 15:07 UTC, con 1,87 horas de clúster en total.
- 2026-10-14: se comprueban las 11 copias y todas coinciden con su origen. Solo cambia en Catalog el formato de `_id` en `fdg_tfm_bbank_atmtransactions` y `fdg_tfm_bbank_productinteractions`, con los mismos valores.
- 2026-10-14: el usuario confirma la entrega el 2026-10-30, que tiene hechos los quizes de las sesiones 1 a 5 y que Roberto Fuertes López no tiene acceso a la sandbox. Se acuerda el plan de trabajo, que queda en `status/plan-tfm.md`, y los requisitos pasan de Datos clave a `status/requisitos-tfm.md`.
- 2026-10-14: se escribe `scripts/extract_catalog.py` y se genera el catálogo en `catalogo/2026-10-14/` (127 segundos, sin errores). Se confirma que las solicitudes denegadas no llevan `profileID` y solo cruzan con la base por email (2.958 clientes). Fase 2 cerrada.
- 2026-10-14: se prueba `--full-inventory`: 749 datasets, 509 con datos, 255 segundos y sin errores, en `inventario/2026-10-14/`, que git ignora.
- 2026-10-14: el usuario commitea el script, el catálogo y el `.gitignore` (`c13649a`, 16:12 UTC).
- 2026-10-14: se prepara el cumplimiento de la guía: `evidencias/` con cuatro fichas de ejecución fechadas con el registro de Query Service, seis incidencias, trece capturas previstas y el protocolo de la comparación; el esqueleto de la memoria y el registro de IA con diez entradas. `scripts/extract_catalog.py` pasa a guardar la hora de inicio y fin en UTC y a mostrar rutas relativas.
- 2026-10-14: se sacan de los ficheros del repositorio las referencias al proyecto de trabajo del usuario y a sus equipos (`status.md`, `dudas-roberto.md` y la transcripción de la sesión 4). Se comprueba que no queda ninguna, tampoco nombres de su lista de contactos. El contexto que no se entrega pasa a `privado/`. Los cinco commits del historial siguen teniéndolas.
- 2026-10-14: se reescribe el historial (`a45d87c` es el commit con las versiones limpias) y se comprueba que ningún commit tiene referencias al proyecto de trabajo del usuario ni nombres de su lista de contactos. El remoto `origin` apunta otra vez a `jexpert-ai` en GitHub, sin subir nada.
- 2026-10-14: el usuario borra y recrea `jexpert-ai` en GitHub, commitea los cambios de la tarde (`21f8a7c`, 26 ficheros) y sube el historial reescrito. Se comprueba que GitHub tiene el mismo commit que el repo local, que no entra nada de `privado/` ni de `inventario/` y que el commit no tiene referencias al proyecto de trabajo del usuario.
