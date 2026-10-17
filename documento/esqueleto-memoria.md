# Esqueleto de la memoria del TFM

La memoria cuenta el caso de principio a fin en unas 10 páginas, con las capturas dentro, por debajo de las 15 que pone como máximo la guía. Sigue la estructura del apartado 5 de la Guía de alumnos TFM. El reparto deja media página de margen.

Cada sección se rellena al cerrar la fase de la que sale su contenido. Los hechos y las cifras los prepara Claude a partir de las evidencias, y el análisis (qué se acepta, qué no, por qué, qué queda sin demostrar) lo escribe el usuario.

| Sección | Páginas | Sale de | Capturas | Estado |
| --- | --- | --- | --- | --- |
| 1. Resumen y objetivo | 0,5 | `dudas-roberto.md`, `status/plan-tfm.md` | | Pendiente |
| 2. Fuentes y contexto | 1 | `status/inventario-sandbox-dev.md`, `catalogo/2026-10-14/` | C01 | Pendiente |
| 3. Método y ciclo | 2 | `status/plan-tfm.md`, la skill, `registro-ia.md` | C05, C06 | Pendiente |
| 4. Calidad y gobierno | 1 | Las pruebas de la skill, `evidencias/README.md` | C10 | Pendiente |
| 5. Operación | 1 | `evidencias/ejecuciones/`, `evidencias/incidencias.md` | C02, C04, C09, C12 | Pendiente |
| 6. Resultados | 1,5 | Las respuestas de la skill frente a las esperadas | C07, C08, C13 | Pendiente |
| 7. Justificación cuantitativa | 1,5 | `evidencias/comparacion/` | C03, C11 | Pendiente |
| 8. Conclusiones y límites | 1 | Revisión del usuario al cerrar cada fase | | Pendiente |

## 1. Resumen y objetivo

El problema (responder a mano si una petición de audiencia se puede crear), el alcance (una skill para CDP de Adobe, probada sobre BBank), el resultado que se busca y sus límites.

## 2. Fuentes y contexto

La sandbox `dev` de Jakala y por qué se eligió BBank. Las copias y su motivo. El catálogo: qué recoge, cómo se genera y qué huecos tienen los datos.

## 3. Método y ciclo

Las fases del trabajo, el diseño de la skill (pasos, ficheros de referencia y los dos modos), cómo se construyó con Claude Code y las decisiones importantes, con lo que se aceptó y lo que se corrigió de las propuestas del modelo.

## 4. Calidad y gobierno

Las pruebas de la skill y su resultado. Cómo se tratan los datos personales: el catálogo no muestra sus valores, la skill solo lee y propone, y las copias no están habilitadas para perfil.

## 5. Operación

Cómo se ejecuta la skill y el extractor del catálogo, el historial de ejecuciones fechadas y las incidencias con su resolución.

## 6. Resultados

Las respuestas de la skill en las peticiones de prueba, frente a las esperadas, separando lo medido de lo estimado.

## 7. Justificación cuantitativa

La comparación sin y con la skill según `evidencias/comparacion/protocolo.md`: horas de ejecución y de revisión, calidad, costes, supuestos y beneficio anual estimado.

## 8. Conclusiones y límites

Qué queda demostrado y qué no, los riesgos y los siguientes pasos. Lo escribe el usuario a partir de sus revisiones de cada fase.

## Lista de comprobación antes de entregar

Del apartado 10 de la guía:

- [ ] El documento no supera las 15 páginas y explica el trabajo de principio a fin.
- [ ] Las decisiones importantes están justificadas y las dudas no resueltas se identifican.
- [ ] Las capturas están dentro del documento, son legibles y explican qué evidencia aporta cada una.
- [ ] El repositorio contiene lo necesario para reproducir el trabajo.
- [ ] Las pruebas de calidad y las comprobaciones relevantes se pueden ejecutar y revisar.
- [ ] Hay evidencia fechada de operación e incidencias, no solo una ejecución final satisfactoria.
- [ ] La comparación de horas y costes distingue medidas de estimaciones e incluye los costes pertinentes.
- [ ] El registro de IA permite seguir las propuestas importantes y su verificación.
- [ ] El vídeo, si se incluye, muestra el sistema funcionando de extremo a extremo.
- [ ] La fecha y las instrucciones de entrega están comprobadas en el campus.
