# Capturas

La guía pide que cada captura respalde una afirmación concreta del documento y lleve un pie que diga qué se ve, qué demuestra y en qué fecha o ejecución se obtuvo. Esta lista dice qué captura hace falta, para qué sección y con qué pie, para hacerla en el momento en que ocurre y no reconstruirla al final.

Las capturas las hace el usuario y se guardan en `capturas/` con el nombre de su identificador (`C01.png`). Ninguna muestra credenciales ni valores de nombres, emails, teléfonos, DNI o IBAN. Si la fecha no sale en la propia herramienta, que se vea el reloj del sistema.

El pie es un borrador: se ajusta a lo que se vea en la captura real y se completa la fecha.

| ID | Fase | Qué capturar | Sección del documento | Pie | Estado |
| --- | --- | --- | --- | --- | --- |
| C01 | 1 | Lista de datasets de la sandbox `dev` en la UI de AEP, filtrada por `fdg_tfm_bbank_`, con la fecha de creación | Fuentes y contexto | Las 12 copias de BBank en la sandbox `dev`, creadas el 2026-10-10 (la de prueba) y el 2026-10-14 (las otras 11), en las que se apoya la skill. | Pendiente. Sirve aunque se haga más tarde, porque la fecha de creación la muestra AEP |
| C02 | 1 | Registro de consultas de Query Service en la UI de AEP con las 11 consultas del 2026-10-14 en estado Success | Operación | Las 11 consultas que crearon las copias el 2026-10-14, lanzadas a las 14:53 UTC y terminadas con éxito entre las 15:00 y las 15:07 UTC. | Pendiente. Sirve aunque se haga más tarde |
| C03 | 1 | Dashboard de uso de licencia, recortado a la fila de Compute hours | Justificación cuantitativa | Uso de Data Distiller en la organización el 2026-10-14: 2.000 horas contratadas y 0,232 consumidas. | Tomada el 2026-10-14. Falta recortarla y guardarla como `C03.png` |
| C04 | 2 | Terminal con una ejecución completa de `scripts/extract_catalog.py`, de la primera línea al resumen final | Operación | Extracción del catálogo del AAAA-MM-DD: 12 datasets en N segundos, sin errores, con la hora de inicio y fin que localiza sus consultas en el registro de Query Service. | Pendiente, en la próxima extracción |
| C05 | 2 | `catalogo.md` en la vista previa, por la tabla de cruces y la fila de `rejectionReason` | Método y ciclo | El catálogo del 2026-10-14 muestra que las solicitudes denegadas no tienen cliente y solo se pueden atribuir por email: la skill tiene que avisar de ello en una petición. | Pendiente |
| C06 | 3 | La petición del usuario a Claude Code para escribir la skill y la propuesta que devuelve | Método y ciclo | Instrucción con las cinco piezas de la guía (tarea, contexto, límites, formato de salida y verificación) y propuesta inicial de la skill, del AAAA-MM-DD. | Pendiente, al empezar la fase 3 |
| C07 | 3 | Una respuesta de la skill sin acceso a la sandbox: petición, veredicto, hechos, inferencias, preguntas abiertas y comprobaciones pendientes | Resultados | La skill responde a una petición solo con el catálogo y marca como estimación el tamaño de la audiencia. | Pendiente |
| C08 | 3 | Una respuesta de la skill con acceso a la sandbox, con las consultas de tamaño y sus IDs | Resultados | Con acceso a la sandbox, la skill calcula el tamaño exacto y cita las consultas, que se pueden localizar en el registro de Query Service. | Pendiente |
| C09 | 3 | Una respuesta errónea de la skill frente a la esperada y la misma petición después de corregirla | Operación | Incidencia del AAAA-MM-DD: la skill se equivocó en X, se corrigió Y y la respuesta pasó a coincidir con la esperada. | Pendiente, cuando ocurra |
| C10 | 4 y 5 | Salida del script que compara las respuestas de la skill con las esperadas | Calidad y gobierno | Resultado de las pruebas del AAAA-MM-DD: N de M puntos acertados en las peticiones de prueba. | Pendiente |
| C11 | 5 | El usuario resolviendo a mano la petición cronometrada, en AEP o Query Service, con la hora visible | Justificación cuantitativa | Modo manual de la comparación: la petición X resuelta sin asistente entre las HH:MM y las HH:MM UTC del AAAA-MM-DD. | Pendiente |
| C12 | 6 | Página Activity del repositorio en GitHub con los push de cada día | Operación | Historial de trabajo del TFM: un push por día de trabajo entre el 2026-10-02 y el AAAA-MM-DD. | Pendiente, al final |
| C13 | 7 | Instalación de la skill desde cero siguiendo el README | Resultados | La skill se instala y responde siguiendo solo el README, sin explicaciones adicionales. | Pendiente |
