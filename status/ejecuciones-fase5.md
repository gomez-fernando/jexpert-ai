# Ejecuciones de la fase 5

Ejecuciones de la skill con sandbox para la comparación, en el repositorio de la skill (`C:\PROJECTS\AEP VIABILIDAD AUDIENCIA`). Salió de `status.md` el 2026-10-28. Las fichas (`run.md`), la puntuación y el cálculo los hace el P10, a partir de lo que deja cada carpeta.

## Procedimiento

Acordado con el usuario el 2026-10-27. La skill está instalada copiándola en `.claude/skills/audience-feasibility` (orden del README), y esa copia no entra en los commits hasta que el P10 la excluya con `.gitignore`. Cada ejecución usa dos terminales de PowerShell en VS Code, las dos en la raíz del repositorio: la de la izquierda para las marcas y la de la derecha para la sesión de Claude Code. No se usa el panel de la extensión, que arranca en Auto y con otro esfuerzo.

1. En la izquierda, preparar la carpeta y la función `marca`, que añade a `notes.md` una línea con la hora UTC y el texto:

   ```powershell
   Set-Location "C:\PROJECTS\AEP VIABILIDAD AUDIENCIA"
   $carpeta = "evidence\runs\2026-10-28_skill-T04"
   New-Item -ItemType Directory -Force $carpeta | Out-Null
   $notas = "$carpeta\notes.md"
   function marca($texto) { "- $((Get-Date).ToUniversalTime().ToString('yyyy-MM-dd HH:mm:ss')) UTC. $texto" | Add-Content -Encoding utf8 $notas; Get-Content $notas -Tail 1 }
   ```

   La carpeta lleva la fecha del día en que se ejecuta.

2. En la derecha, lanzar la sesión con el comando del protocolo:

   ```powershell
   Set-Location "C:\PROJECTS\AEP VIABILIDAD AUDIENCIA"
   $env:FORCE_PROMPT_CACHING_5M = '1'; claude --model claude-sonnet-5-5 --effort high --permission-mode default --disallowedTools "Read(./test-cases/expected/**)" "PowerShell(*test-cases*expected*)"
   ```

3. Comprobar la cabecera (claude-sonnet-5-5 with high effort), que la línea de debajo de la caja no ponga auto mode, `/status` y `/usage` con la línea Usage a cero, y marcar `Comprobaciones: ...`.
4. Marcar `Envío del mensaje` y enviar `/audience-feasibility Valora la petición de test-cases/requests/<fichero>. Escribe el script de consultas en evidence/runs/<carpeta>/.`
5. En cada pausa, marcar `Pausa: <lo que pide>`, contestar (opción 1 en los permisos, nunca las de no volver a preguntar ni permitir todas las ediciones; "Sí" a la confirmación de scripts) y marcar `Fin de pausa`. En T01 a T03 hubo cuatro pausas: crear `queries.py`, confirmar los dos scripts, ejecutar la comprobación de la configuración y ejecutar `queries.py`.
6. Al llegar la respuesta, marcar `Respuesta recibida, inicio de la revisión`. No contestar lo que ofrezca al final (escribir la ficha, otro script). Leerla, marcar los errores vistos y marcar `Fin de la revisión` al terminar.
7. Captura solo en T01 (C08). En T02 a T04 no hay.
8. `/usage` y marcar los tokens de cada línea de Usage by model y la línea Total cost con las duraciones. Claude da las marcas rellenas si el usuario le pasa la captura.
9. `/export evidence/runs/<carpeta>/conversation.txt`, comprobar en la izquierda con `Test-Path` y `Select-String -Pattern "test-cases.expected"` y marcar el resultado.
10. `/exit` y cerrar la terminal de la derecha.

## Resultados

| Petición | Carpeta | Envío, respuesta y fin de la revisión (UTC) | Tokens de claude-sonnet-5-5 (entrada, salida, lectura y escritura de caché) | Coste con la página | Total cost |
| --- | --- | --- | --- | --- | --- |
| T01 | `2026-10-27_skill-T01` | 20:58:07, hacia 21:07:43 (marcada a las 21:09:43 "unos 2 minutos antes") y entre 21:10:55 y 21:14:43 (marcada después) | 4.5k, 18.4k, 866.6k y 95.4k, más `claude-haiku-4-5` con 440 y 13 | 0,52 USD | 0,91 USD |
| T02 | `2026-10-27_skill-T02` | 21:58:29, 22:13:51 y 22:17:05 | 4.0k, 28.4k, 786.1k y 85.3k | 0,58 USD | 0,99 USD |
| T03 | `2026-10-27_skill-T03` | 22:37:06, 22:50:07 y 22:53:05 | 4.0k, 12.9k, 803.7k y 83.4k | 0,43 USD | 0,76 USD |
| T04 | `2026-10-28_skill-T04` | 16:15:20, antes de las 16:30:43 (marcada a las 16:32:41) y 16:40:21 | 4.1k, 13.5k, 694.0k y 166.1k | 0,63 USD | 1,05 USD |

Total cost sale exacto en las cuatro con los precios de Sonnet 4.5, lo que confirma la I09 con datos de las fichas.

En T04, la quinta pausa (reescribir `output.json`) está marcada de 16:27:27 a 16:27:42 UTC, pero el permiso ya estaba en pantalla a las 16:22:55 (hora de la captura que el usuario pasó a Claude), así que duró al menos 4 minutos y 47 segundos. La respuesta ya había llegado a las 16:30:43 (otra captura) y está marcada a las 16:32:41. El envío y el fin de la revisión son exactos, así que el total no cambia, pero sí el reparto entre tiempo de la skill y tiempo humano. La escritura de caché de T04 (166.1k) es casi el doble que la de T01 a T03: con caché de 5 minutos, la pausa larga la habría hecho caducar y se volvió a escribir (sin confirmar). Sin esos unos 81k tokens, T04 costaría unos 0,43 USD, como T03, que también es no viable con solo Q1. El `notes.md` del commit `2c38ee9` no lleva esa marca, y el usuario decide el 2026-10-28 dejarlo así.

Cada carpeta tiene `notes.md`, `queries.py` y `conversation.txt`. T01 y T02 tienen además `output.json`; T03 no, porque su comando no guardó la salida y el resultado de su única consulta está en `conversation.txt`.

## Pendiente de las ejecuciones

- En `notes.md` de T02, las dos marcas que faltaban (las comprobaciones, a las 21:57:40 UTC, y el fin de la pausa del permiso para ejecutar `queries.py`, a las 22:09:01) se añadieron a mano con hora exacta y sin decir que son posteriores. 22:09:01 es el inicio de la primera consulta en `output.json`, es decir, un límite y no la hora marcada, y 21:57:40 no tiene registro detrás. Claude recomendó reescribirlas diciendo que se añadieron después, como la del fin de la revisión de T01, y el usuario decide el 2026-10-28 dejarlas así.
- T04 se ejecutó el 2026-10-28, con sus cuatro ficheros (`notes.md`, `queries.py`, `output.json` y `conversation.txt`, sin `test-cases/expected`), y está en el commit `2c38ee9` (2026-10-28 17:53:21 hora local, con push y sin la copia de la skill). Su `notes.md` acaba en la marca de las 16:52:31 UTC (búsqueda de `test-cases/expected`, sin resultados), y no lleva las horas reales de la quinta pausa y de la respuesta ni la incidencia del primer `/export`. El usuario decide el 2026-10-28 dejarlo así.
- T01 a T03 y la C08 están en el commit `0473f78`, con push. Desde el P10 (2026-10-28), `.gitignore` excluye `.claude/skills/audience-feasibility/` y los commits se pueden hacer con `git add -A`.

## Decisiones de las ejecuciones y del P10

Salieron de `status.md` el 2026-10-29.

- 2026-10-28: las dos marcas de `notes.md` de T02 añadidas a mano (líneas 1 y 10) se quedan como están, sin decir que son posteriores. El P10 escribe la ficha de T02 con `notes.md` tal cual. Decide el usuario, después de que Claude recomendara indicarlo.
- 2026-10-28: el `notes.md` de T04 se queda como está, sin las marcas que propuso Claude (horas reales de la quinta pausa y de la respuesta, e incidencia del primer `/export` enviado como mensaje). El P10 escribe la ficha de T04 con `notes.md` tal cual. Decide el usuario.
- 2026-10-28: el prompt de los resultados de la comparación se llama `prompts/P10-comparison-results.md`. Decide el usuario.
- 2026-10-28: el P10 analiza el 0 de T02 comparando el SQL de Q2 con el de la consulta `e99ea0e7` del 2026-10-14, que saca del registro de Query Service con un script de `aep/` (con su ficha, por la regla 1 de Evidencias de la skill), y no repite T02, porque su tamaño no puntúa. Decide el usuario, a propuesta de Claude.
- 2026-10-28: el escenario pesimista del modo manual (la mitad de cada tiempo por unidad: 48,5, 56,5, 36,5 y 36,5 minutos) va en una sección nueva de resultado de `protocol.md`, debajo de Mediciones, anotado como añadido después de medir y sin cambiar el método. Cada ejecución lleva su entrada del registro (R21 a R24), como pide la regla 4 de Evidencias de la skill, y la propuesta del P10 lleva solo lo que el usuario tiene que validar, sin el texto de las fichas, para ahorrar tiempo. Decide el usuario, a propuesta de Claude.
- 2026-10-28: en el P10, la ejecución de T01 termina a las 21:07:43 (la línea 11 de su `notes.md` dice que la respuesta llegó unos 2 minutos antes de la marca), T02 tiene un solo error que se escapa, porque la respuesta avisa del 0 y lo deja pendiente, y el coste de Data Distiller es 0 sin volver a comprobarlo. Decide el usuario, a propuesta de Claude.
- 2026-10-28: no se hace un prompt para confirmar la causa del 0 de T02 ni para cambiar la skill con lo que dejan I10 a I12: quedan como límites conocidos, por el tiempo hasta la entrega. Consta en la decisión humana del P10. Decide el usuario, a propuesta de Claude.

## Hallazgos para el P10

- T01: la skill no calcula la audiencia completa porque S1.C2 (saldo de puntos) no tiene umbral; lanza Q1 (contraste de la base, 7.730), Q2 (Valencia, 1.322) y Q3 (consentimiento de email, 1.330) entre las 21:05:34 y las 21:06:11 UTC.
- T01: la è de València salió como ? en `output.json` al redirigir con `Tee-Object` en PowerShell; la consulta se envió bien. Es una incidencia. En T02 la skill fijó UTF-8 y no pasó.
- T02: Q2 (S1.C1, solicitudes denegadas cruzadas con la base por email) dio 0 clientes, y el catálogo da 2.958. La skill lo deja como comprobación pendiente, con la hipótesis de que los emails que casan son de solicitudes aceptadas, y ofrece otro script, que no se pidió. El 2.958 sale de la consulta `e99ea0e7-8d28-4d8c-8bb5-c463fc08bb9e` del 2026-10-14 (I06 y `evidence/runs/2026-10-14_catalog/run.md`), cuyo SQL no está en el repositorio y sí en `effectiveSQL` del registro de Query Service. Q2 cruza `_valuelabemeaptrsd.ApplicationDetails.Email` con `personalEmail.address` con `lower(trim())` en los dos lados y da 0, pero Q4 (solo high_risk, que es una parte de las denegadas) da 1, y las dos no pueden estar bien a la vez (causa sin confirmar). El tamaño no puntúa en la respuesta esperada de T02, así que repetirla no cambia su nota.
- La copia de `.claude/skills/audience-feasibility` es idéntica a `skills/audience-feasibility/`, cuyo último commit es `ab60f71` (2026-10-20): es la versión de la skill de las cuatro ejecuciones (comprobado el 2026-10-28).
- T03: no viable, solo Q1 de contraste de la base; la skill ofrece calcular el subsegmento, que no se pidió.
- La regla `PowerShell(*python.exe *)` del P04 casa con `& .\.venv\Scripts\python.exe`: resuelve una de las dudas abiertas del `status.md` de la skill desde el 2026-10-20.
- Los IDs de las respuestas son Q1, Q2... de la skill, no los de Query Service: las consultas se localizan en el registro por su hora UTC, como en la C04b.
- Al final de T01 la sesión preguntó si escribía la ficha y la entrada del registro (por la regla 4 de registro del `CLAUDE.md` de la skill), y no se le contestó. Las entradas del registro de estas ejecuciones las tiene que resolver el P10.
- La C08 se hizo a las 22:29 hora local del 2026-10-27 sobre `conversation.txt` de T01 (líneas 329 a 371), con el Reloj, porque la sesión ya estaba cerrada: Claude dio mal el orden de los pasos. Su pie lo tiene que decir.
- T04: no viable, solo Q1 de contraste de la base (7.730, de 16:21:39 a 16:21:52 UTC del 2026-10-28). En la revisión de las capturas no falla ningún punto de los visibles. Da el aviso del valor de la última carga en S2.C2 y no en S1.C2, aunque la comprobación 4 de `verdict-criteria.md` lo pide para los dos (atributos de estado, valor actual), y marca "hecho" la propuesta de subsegmentos, que la respuesta esperada marca "inferencia". Ninguno de los dos puntúa. Añade D2 (trabajar con los subsegmentos o esperar al cruce).
- T04: el primer `/export` se envió al modelo como mensaje (había algo delante de la barra) y contestó que no puede ejecutarlo. Ese intercambio sale al final de `conversation.txt` y gastó tokens después de anotar `/usage`. Claude propuso una marca de incidencia, y el usuario decide no añadirla.
- Las reglas 1, 2 y 4 de Evidencias del `CLAUDE.md` de la skill piden el mismo día de cada ejecución de la skill con `test-cases/` su ficha `run.md`, sus incidencias en `evidence/incidents.md` y su entrada en `ai-usage-log.md` con la decisión humana. T01 a T03 (2026-10-27) ya no llegan, y T04 solo si el P10 las escribe el 2026-10-28. El `status.md` de la skill sigue en 2026-10-27 porque una ejecución solo es hito cuando deja su ficha (regla 6 de `update-status`), y se pondrá al día cuando el P10 las escriba.
- T04: después de ejecutar `queries.py`, la skill intenta sobrescribir `output.json` con Write (da error) y pide permiso para reescribirlo en UTF-8 sin BOM con PowerShell (`New-Object Text.UTF8Encoding` fuera de la lista de ConstrainedLanguage). Es una pausa más que en T01 a T03. Si Write hubiera funcionado, `output.json` lo habría escrito el modelo y no el script; el P10 tiene que mirar qué pretendía escribir.
- El comando con que la skill ejecuta `queries.py` cambia entre ejecuciones (`Tee-Object`, `Out-File -Encoding utf8`, sin guardar la salida), como prevé el límite 6 del README.
