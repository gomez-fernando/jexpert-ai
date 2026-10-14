# Plan de trabajo del TFM

Acordado con el usuario el 2026-10-14. La entrega es el 2026-10-30. Los requisitos de la guía y del profesor están en `requisitos-tfm.md`, en esta misma carpeta.

## Fases

| Fase | Fechas | Resultado |
| --- | --- | --- |
| 1. Copias de BBank | 2026-10-14 | Hecha. 12 copias `fdg_tfm_bbank_*` en la sandbox `dev`, comprobadas contra su origen (`copias-bbank.md`) |
| 2. Catálogo | 2026-10-15 y 2026-10-16 | Hecha el 2026-10-14. `scripts/extract_catalog.py` y el catálogo en `catalogo/2026-10-14/` |
| 3. Skill | 2026-10-17 a 2026-10-21 | `SKILL.md`, ficheros de referencia y README |
| 4. Peticiones de prueba | En paralelo con la fase 3 | Cinco o seis peticiones con su respuesta esperada |
| 5. Comparación sin y con la skill | 2026-10-22 a 2026-10-25 | Horas, calidad y costes de los dos modos |
| 6. Evidencias | Durante las fases 3 a 5 | Ejecuciones fechadas con sus incidencias, capturas con pie y entradas del registro de uso de IA |
| 7. Documento y entrega | 2026-10-26 a 2026-10-29, entrega el 2026-10-30 | Documento de 15 páginas como máximo, README para que otra persona instale la skill, repo `jexpert-ai` reproducible y vídeo opcional |

## Cumplimiento de la guía

Acordado con el usuario el 2026-10-14, antes de empezar la skill. Las evidencias se generan mientras se trabaja y no al final, porque la guía pide ejecuciones fechadas con sus incidencias reales y decisiones que el usuario pueda explicar.

| Requisito de la guía | Cómo se cubre | Quién lo hace |
| --- | --- | --- |
| Documento de 15 páginas como máximo, con la estructura del apartado 5 | `documento/esqueleto-memoria.md`, con las ocho secciones y el reparto de páginas, que se rellena al cerrar cada fase | Claude prepara los hechos y los borradores, y el usuario escribe o corrige el análisis |
| Capturas con un pie que diga qué se ve, qué demuestra y de qué fecha es | `evidencias/capturas.md`, con cada captura que hace falta, la sección que respalda y el pie redactado. Claude avisa en el momento de hacerla | El usuario hace las capturas |
| Repositorio reproducible | La skill, `scripts/extract_catalog.py`, el catálogo con su fecha, las peticiones de prueba con su respuesta esperada y un script que compara las respuestas | Claude |
| Evidencia de operación e incidencias | `evidencias/ejecuciones/`, con una ficha por ejecución fechada, y `evidencias/incidencias.md` | Claude, y el usuario lo valida |
| Comparación sin y con la skill | `evidencias/comparacion/protocolo.md`, escrito antes de medir | Los dos. El usuario cronometra la petición hecha a mano |
| Registro de uso de IA | `registro-ia.md`, con los seis campos de la guía y una entrada por intercambio relevante, anotada el mismo día | Claude prepara cada entrada y el usuario escribe la decisión humana |
| Artefacto instalable | README con instrucciones, configuración, ejemplo, pruebas y límites conocidos | Claude lo escribe, y el usuario u otra persona lo prueba desde cero |

El análisis crítico es del usuario. Al cerrar cada fase hay una revisión corta: Claude enseña qué ha hecho, qué ha comprobado y qué no, y el usuario decide qué acepta, qué cambia y por qué. Lo que diga va tal cual al campo de decisión humana del registro de IA, y de ahí sale la sección de conclusiones y límites.

La skill separa en sus respuestas los hechos, las inferencias y las preguntas abiertas, y marca lo que no ha podido comprobar, como pide el apartado 8 de la guía. Así sus respuestas sirven de captura de evidencia.

Las fechas de las evidencias se apoyan en registros que no dependen del usuario, sobre todo el registro de consultas de Query Service, como explica `evidencias/README.md`. Al cerrar cada día de trabajo, el usuario hace commit y push a GitHub.

## Catálogo

El script lee las copias y genera el catálogo de atributos. De cada atributo recoge la ruta, la cobertura, los valores con su recuento, el dataset de origen, la ventana de datos, el significado del valor vacío y notas. Los recuentos por valor son los que usa la skill para estimar tamaños cuando no tiene acceso a la sandbox.

Parámetros aprobados el 2026-10-11: `--datasets` (regex, por defecto `^fdg_tfm_bbank_`), `--out-dir` (por defecto `catalogo/AAAA-MM-DD/`) y `--full-inventory` como alternativa. El catálogo se guarda en el repo con su fecha de extracción, porque la sandbox es compartida.

La extracción del 2026-10-14 (`catalogo/2026-10-14/`, 127 segundos y sin errores) deja seis ficheros:

- `catalogo.csv`, un atributo por fila. Es el formato que leerá la skill y el que tendría que seguir un catálogo propio.
- `datasets.csv`, `relaciones.csv` y `eventos_por_mes.csv`, con los datasets, los cruces entre ellos y los eventos y clientes de cada mes.
- `catalogo.md`, la versión para leer.
- `extraccion.json`, con la fecha, la sandbox, la base de clientes y los errores.

El script elige como base de clientes el dataset de perfil con más filas y su identidad primaria (`fdg_tfm_bbank_profiledata`, `personID`, namespace `TRBbankProfileID`), y calcula la cobertura en clientes sobre esa base. Los cruces salen de las identidades y relaciones de los schemas y de los campos de email. Los datos personales y los identificadores solo llevan el recuento, sin valores.

Las notas que no se pueden sacar de los datos (significado del valor vacío y avisos) están en `catalogo/notas.csv`, escrito a mano solo con lo comprobado, y el script las añade al catálogo.

Lo que deja ver el catálogo y sirve para las peticiones de prueba:

- Ninguna de las 29.886 solicitudes denegadas lleva `profileID`. Solo se pueden atribuir a un cliente por el email, que casa con 2.958 clientes de la base. "Clientes con una tarjeta denegada" es, por tanto, una petición viable con matices.
- La navegación web cruza con 6.782 clientes por `profile_id` y con 7.727 por email.
- En `fdg_tfm_bbank_loyalty`, 500 de los 502 clientes están en dos filas idénticas.
- `fdg_tfm_bbank_propensity` no cruza con ningún cliente.
- Las operaciones de cajero van de 2006 a 2024 y las interacciones con producto, de 2018 a 2025, fuera de la ventana del resto de eventos (2025-10 a 2026-07).

## Skill

Lee una petición de audiencia escrita por negocio y el catálogo. Comprueba primero el formato del catálogo, parte la petición en condiciones, busca cada condición en el catálogo y devuelve:

- El veredicto: viable, viable con matices o no viable.
- El atributo que cubre cada condición.
- Lo que no se puede cubrir y por qué.
- Las decisiones que tiene que tomar negocio.
- Las comprobaciones que quedan pendientes.

Propone y no escribe nada en AEP.

Funciona de dos formas, porque Roberto Fuertes López va a probarla por su cuenta y no tiene acceso a la sandbox:

- Con credenciales de la sandbox, calcula con Query Service el número exacto de clientes de la audiencia y de cada condición, sobre las copias. Son lecturas interactivas, que según Adobe no gastan horas de Data Distiller.
- Sin credenciales, trabaja solo con el catálogo del repo. Da un tamaño aproximado con los recuentos por valor del catálogo, marcado como estimación porque supone que las condiciones son independientes, y deja como pendientes las comprobaciones exactas.

Lo que Roberto no pueda ejecutar se demuestra en el documento con ejecuciones fechadas y capturas, o en el vídeo.

Una petición viable con matices sería "clientes de Madrid con una tarjeta denegada que llegaron por la campaña de Black Friday", porque las denegadas solo se atribuyen a clientes por el email. Una no viable, "clientes cuyo saldo ha bajado en los últimos tres meses", porque no hay histórico del saldo. Los huecos conocidos de los datos (movimientos de tarjeta, evolución del saldo, importe de las solicitudes y propensión sin cruce con los clientes) sirven para las peticiones no viables.

## Peticiones de prueba

Cinco o seis peticiones: dos viables, dos viables con matices y dos no viables. Se redactan como un correo de negocio, en lenguaje libre y con alguna ambigüedad, y no como una lista de condiciones. Cada una lleva su respuesta esperada.

Un ejemplo es "clientes que empezaron a contratar una tarjeta en la web en los dos últimos meses y no la terminaron, sin solicitudes rechazadas por sospecha de fraude, que acepten email y con saldo alto". Cruza cuatro datasets, el consentimiento de email solo existe para el 32,7 % de los clientes y el saldo alto no está definido.

## Comparación sin y con la skill

- Se usa el mismo lote de peticiones en los dos modos.
- Las horas a mano salen de cronometrar de principio a fin una sola petición resuelta a mano y de estimar el resto por pasos, calibrados con esa medida. Los pasos son entender la petición, buscar cada condición en los datasets, lanzar una query por condición para ver cuántos clientes la cumplen, redactar la respuesta y revisarla. El tiempo de cada petición depende de su número de condiciones. Va marcado como estimación con su supuesto.
- Con la skill se miden por separado las horas de ejecución y las de revisión humana.
- La calidad se mide con la misma lista de puntos en los dos modos, frente a la respuesta esperada: veredicto, atributo de cada condición, huecos detectados, avisos de cobertura y de valores vacíos, y decisiones para negocio. La nota es el porcentaje de puntos acertados.
- El coste de Data Distiller sale del registro de consultas (`computeMetrics.clusterVMHours`), con el ID de cada consulta. La preparación gastó 0,37 horas en la copia de prueba y 1,87 en las otras 11.
- Para el beneficio anual hay que estimar cuántas peticiones de viabilidad hay al año en un proyecto de CDP y el coste por hora, las dos con su supuesto.
