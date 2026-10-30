# Ejecución sin sandbox (P11)

Procedimiento de la ejecución de la skill en el modo sin sandbox con T01, en una instalación nueva desde el README, que va antes de enviar el P11 (`prompts/P11-catalog-only-install.md` del repositorio de la skill). Lo fija Claude el 2026-10-29, por delegación del usuario. El P11 se envía el mismo día de la ejecución, porque la regla 1 de Evidencias del `CLAUDE.md` de la skill pide la ficha ese día. Si la ejecución no es el 2026-10-29, hay que cambiar la fecha de la carpeta aquí y en el punto 4 de `<ejecucion>` del P11.

## Procedimiento

Dos terminales de PowerShell en VS Code: la de la izquierda para las marcas y la instalación, y la de la derecha para la sesión de Claude Code en el clon.

1. C10, en cualquier momento antes de enviar el P11: `evidence/comparison/protocol.md` en la vista previa (Ctrl+Shift+V), en la tabla de Mediciones, con Puntos acertados y Errores que se escapan de las cuatro filas con la skill y el Reloj de Windows. Se guarda en `evidence/screenshots/C10.png`.
2. En la izquierda, preparar la carpeta y la función `marca`:

   ```powershell
   Set-Location "C:\PROJECTS\AEP VIABILIDAD AUDIENCIA"
   $carpeta = "C:\PROJECTS\AEP VIABILIDAD AUDIENCIA\evidence\runs\2026-10-29_skill-T01-catalog-only"
   New-Item -ItemType Directory -Force $carpeta | Out-Null
   $notas = "$carpeta\notes.md"
   function marca($texto) { "- $((Get-Date).ToUniversalTime().ToString('yyyy-MM-dd HH:mm:ss')) UTC. $texto" | Add-Content -Encoding utf8 $notas; Get-Content $notas -Tail 1 }
   ```

3. En la izquierda, clonar e instalar con las órdenes de Instalación del README:

   ```powershell
   $clon = "C:\PROJECTS\audience-feasibility-install-test"
   git clone https://github.com/gomez-fernando/AEP-viabilidad-audience.git $clon
   Set-Location $clon
   $commit = git log -1 --format="%h %ad" --date=iso
   $cred = Test-Path ".\*.postman_environment.json"; $venv = Test-Path ".\.venv"
   New-Item -ItemType Directory -Force .claude\skills | Out-Null
   Copy-Item -Recurse -Force skills\audience-feasibility .claude\skills\
   $n = (Get-ChildItem -Recurse -File .claude\skills\audience-feasibility).Count
   marca "Instalación: clon de GitHub en $clon, commit $commit. Fichero de credenciales: $cred. .venv: $venv. Skill copiada con las órdenes de PowerShell de Instalación del README: $n ficheros en .claude\skills\audience-feasibility."
   ```

   Lo esperado es `False`, `False` y 7 ficheros.

4. En la derecha, lanzar la sesión en el clon con el comando del protocolo y aceptar la confianza en la carpeta:

   ```powershell
   Set-Location "C:\PROJECTS\audience-feasibility-install-test"
   $env:FORCE_PROMPT_CACHING_5M = '1'; claude --model claude-sonnet-5-5 --effort high --permission-mode default --disallowedTools "Read(./test-cases/expected/**)" "PowerShell(*test-cases*expected*)"
   ```

5. Comprobar la cabecera (claude-sonnet-5-5 with high effort), que no ponga auto mode, `/status` y `/usage` a cero.
6. `/skills` y escribir `audience` para filtrar. Con `audience-feasibility` en la lista, hacer la C13: las dos terminales (la izquierda con el clon y la copia, la derecha con la lista) y el Reloj de Windows. Se guarda en `evidence/screenshots/C13.png`. Cerrar con Esc, sin pulsar Espacio ni Enter sobre la skill, que le cambian la visibilidad. Marcar `Comprobaciones: ...` con la versión de `/status` y que `/skills` muestra la skill (C13).
7. Marcar `Envío del mensaje` y enviar `/audience-feasibility Valora la petición de test-cases/requests/T01-reward-campaign.md.`, sin pedir modo.
8. En cada pausa, marcar `Pausa: <lo que pide>` y `Fin de pausa`. Lo de la comprobación de la configuración se aprueba con la opción 1. Si pide instalar dependencias, crear el `.venv` o escribir la ficha, `status.md` o el registro, se contesta No y se marca. Si tras la comprobación se para o pregunta qué modo usar, enviar `Usa el modo sin sandbox.` y marcarlo con el motivo.
9. Al llegar la respuesta, marcar `Respuesta recibida, inicio de la revisión`. No contestar lo que ofrezca al final. Comprobar que dice modo sin sandbox, que la estimación lleva su supuesto y su rango, y que hay comprobaciones pendientes. Marcar los errores vistos y `Fin de la revisión`.
10. `/usage` y marcar los tokens de cada línea de Usage by model y la línea Total cost.
11. `/export conversation.txt`, que lo escribe en la raíz del clon. En la izquierda:

    ```powershell
    Copy-Item "$clon\conversation.txt" $carpeta
    Test-Path "$carpeta\conversation.txt"
    Select-String -Path "$carpeta\conversation.txt" -Pattern "test-cases.expected"
    ```

    Marcar el resultado. Después, `/exit` y cerrar la terminal de la derecha.

12. C07: abrir `evidence/runs/2026-10-29_skill-T01-catalog-only/conversation.txt` en VS Code, en la parte de la respuesta con el modo usado, el tamaño estimado con su fórmula, su supuesto y su rango, y las comprobaciones pendientes si caben, con los números de línea y el Reloj de Windows. Se guarda en `evidence/screenshots/C07.png`. Marcar `C07: líneas X a Y`.
13. Enviar el P11 en una sesión normal del chat de la skill, en modo plan, el mismo día. El clon se puede borrar cuando el P11 esté cerrado: no está en ningún repositorio.

## Ejecución del 2026-10-29

Lo que pasó, para revisar la propuesta del P11 contra `notes.md` y `conversation.txt` de `evidence/runs/2026-10-29_skill-T01-catalog-only/`.

1. La instalación se marcó a las 23:39:30 UTC del 2026-10-28 (00:39 hora local del 2026-10-29) y el resto de marcas van del 00:19 al 01:43 UTC del 2026-10-29. La carpeta lleva la fecha local, y lo explica una marca. La marca de la instalación se tomó unos minutos después de clonar, porque la función `marca` no estaba creada.
2. Clon en el commit `b885377`, sin fichero de credenciales ni `.venv`, con los 7 ficheros de la skill copiados. VS Code activaba en cada terminal el `.venv` del repositorio de la skill, que tiene `aep/` en modo editable apuntando a la carpeta con las credenciales. La terminal de la sesión se lanzó tras `deactivate`, con el Python global (`C:\PYTHON313\python.exe`, sin `aep`), y lo dice la marca de comprobaciones.
3. La cabecera de la sesión avisaba de "1 setup issue: install · /doctor" (se ve en la C13). La marca de `/doctor` se quedó con TEXTO, la de la versión con VERSION (corregida con otra marca: 2.1.168) y la de errores vistos con el texto de ejemplo. El usuario decide no corregir las de `/doctor` y errores.
4. Pausas: tres comandos de PowerShell de solo lectura, crear `check_config.py` y `query_sql.py` en `%TEMP%\audience-feasibility-T01` (el segundo antes de ejecutar la comprobación, como `queries.py` en T04), una confirmación por texto a la que el usuario contestó "confirmo" (línea 112 de `conversation.txt`) y el permiso para ejecutar `check_config.py` con el Python global y `PYTHONPATH` en el clon. La comprobación dio `AEPConfigError` y la skill eligió sola el modo sin sandbox. `query_sql.py` no se ejecutó. `query_sql.py` añadía una Q4 (S1.C1 y S1.C3 juntas) que la skill reconoce fuera de su tabla de consultas.
5. La respuesta da S1 viable. Tamaño: E1 1.322 (Valencia y València), E2 1.330 (consentimiento y), E3 sin estimación por el umbral (como máximo 500), E4 227,5 con rango de 0 a 1.322, E5 sin estimación puntual, con cota de 227,5 y rango de 0 a 500, y E6 sin atributo. Decisiones D1 (umbral), D2 (lectura de aceptación de comunicaciones) y D3 (fuente del gasto con tarjeta), y cinco comprobaciones pendientes. Termina avisando de la C07 y ofreciendo completar su pie en `screenshots.md`, y no se contestó.
6. `/usage`: 4.0k de entrada, 19.2k de salida, 718.9k de lectura de caché y 241.6k de escritura de caché, sin línea de `claude-haiku-4-5`, Total cost 1,42 USD con el aviso de modelos desconocidos, 1h 23m 9s de reloj y 73 líneas añadidas. La escritura de caché es casi el triple que en T01 a T03; la causa más probable es la caducidad de la caché de 5 minutos en las pausas largas (sin confirmar).
7. `conversation.txt` se exportó con `/export` y no nombra `test-cases/expected`.
8. Capturas: la C10 a las 0:33, la C13 a la 1:17 y la C07 a las 2:42 (horas locales del 2026-10-29). La C07 enseña las líneas 284 a 349 de `conversation.txt` y se repitió sin el explorador de VS Code, que mostraba el nombre del fichero de credenciales; ese nombre no sale en ningún fichero del repositorio de la skill.

## Decisiones del P11

Tomadas por Claude el 2026-10-29, por delegación del usuario ("no tengo tiempo, decide tú"). En el repositorio de la skill se presentan como del usuario, sin decir que las delegó.

1. La petición es T01, la única viable con tamaño estimable: Valencia (1.322 en el catálogo, igual que en la ejecución con sandbox) y el consentimiento de email, con el saldo sin umbral. T03 y T04 no estiman nada y T02 usaría los 2.958 de la nota que puso en duda el 0 de la I11.
2. El P11 completa Ejemplo y Pruebas del README de la skill, pendientes desde el P06, para que no recaigan en el prompt de la memoria.
3. La instalación nueva es un clon de GitHub sin fichero de credenciales ni `.venv`, y la skill elige el modo sola. Si no lo elige, se pide en la misma sesión.
4. La sesión se lanza con el comando del protocolo, para que no pueda leer `test-cases/expected/` y los tokens sean comparables.
5. La puntuación de esta ejecución va solo en su ficha y no en Mediciones, porque el modo sin sandbox no entra en la comparación.
6. El P11 también completa la fila de la C10, como pedía `status.md`.
7. Las entradas del registro son R26 (la ejecución) y R27 (el P11).

## Revisión de la propuesta del P11

El 2026-10-29 la sesión del P11 presenta la propuesta: 13 de 13 puntos, 0 errores, 0,8759 USD (cuadra con los precios de Costes), una incidencia nueva I13 (escribir el script de consultas antes de saber el modo) y siete decisiones abiertas. Claude la revisa contra `notes.md`, `conversation.txt`, la respuesta esperada, `protocol.md`, `mode-sandbox.md`, la C13 y las fichas de T01 y T04, y propone contestar ok con estos cambios:

1. I13: solo es gasto la pausa de escribir `query_sql.py` (líneas 15 y 16 de `notes.md`), porque `check_config.py` hace falta para elegir el modo. La causa no es que `mode-sandbox.md` no lo diga: su línea 3 dice que desde Sentencias permitidas solo se aplica en el modo con sandbox, y la skill no lo siguió.
2. Tipo de cambio: el del 2026-10-28 (1,1133), como último publicado al escribir la ficha, en lugar de esperar al del 2026-10-29 (sale hacia las 16:00 hora de Madrid). Las fichas de T01 a T04 usaron el del día de la ejecución, consultado después; aquí esperar retrasaría el cierre del P11, y el coste en EUR de esta ejecución no se usa en ningún cálculo.
3. Prefijo `(.venv)` de la C13: es de la terminal de la izquierda (la de la instalación), en la que VS Code activó el `.venv` del repositorio de la skill. La sesión se lanzó en la derecha tras desactivarlo.
4. El resto de decisiones abiertas (marcas de plantilla de `notes.md`, fin de la ejecución a las 01:05:13 como límite superior con pausas de 7:01, no cambiar la skill por I13, alcance de la instalación en un clon completo y puntuación solo en la ficha y citada desde Pruebas), ok.

El usuario envía la respuesta tal cual. En el entregable, Claude encuentra tres fallos y los pone en el mensaje de cierre: Ejemplo del README dice "en un equipo sin el fichero de credenciales" (fue el equipo del usuario, en un clon sin el fichero), el paso 2 de Cómo repetir las pruebas hace depender el modo del fichero de credenciales y no de que `aep/` cargue la configuración (Elección del modo de `SKILL.md`), y la ficha da seis pausas sin decir que hubo una más sin marca, el permiso para ejecutar `check_config.py` (dato del usuario durante la ejecución). Los enlaces relativos del README se dejan como están.
