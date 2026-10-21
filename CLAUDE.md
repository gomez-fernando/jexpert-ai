# TFM Jxpert IA: planificación

Esta carpeta es el repositorio de planificación del TFM (`jexpert-ai`). El estado del trabajo está en `status.md` y se mantiene con la skill `estado-trabajo`. La skill que se entrega vive en `C:\PROJECTS\AEP VIABILIDAD AUDIENCIA`, donde otro chat, con Sonnet, ejecuta los prompts que se redactan aquí.

## Reparto entre los dos chats

1. Este chat planifica y redacta los prompts del repositorio de la skill, en su carpeta `prompts/` y con su plantilla `templates/prompt.md`. Para saber cómo avanza, lee el `status.md` de ese repositorio.
2. Lo que se escribe en el repositorio de la skill (prompts, mensajes para su chat, documentos) no deja rastro de la planificación: no nombra esta carpeta, su `status.md`, este chat ni lo que se habla aquí sobre calendario, horas, consumo o reparto entre modelos.
3. La planificación (calendario, horas, recortes de alcance, consumo) no lleva entrada en el registro de IA. Va a `status.md` y a `status/plan-tfm.md`.
4. En el repositorio de la skill no se citan los commits ni el push de este repositorio. Las fechas de las evidencias se apoyan en el registro de consultas de Query Service, en Catalog y en las capturas.

## Cierre de los chats

Me avisarás de los momentos oportunos de cerrar un chat tanto en Opus como en Sonnet.

1. En el chat de la skill (Sonnet), al entregarme cada prompt dime en qué momento cerrarlo. Lo normal es al terminar el prompt: con su decisión humana guardada, su entrada en el registro, las capturas que toquen hechas y el `status.md` de la skill al día. Si me ves volver con iteraciones largas de un mismo prompt, avísame también.
2. En este chat (Opus), avísame después de escribir cada prompt, al cambiar de tema y cuando la conversación ya sea larga. Antes de avisar, deja `status.md` al día y dame el comando para retomar.

## Forma de responder

1. Respuestas en español.
2. Una cosa cada vez: solo el punto en curso, sin varias listas sobre temas distintos, y con el fichero enlazado cuando me pidas mirar algo.
3. Nada se da por sabido. Las etiquetas de los ficheros de estado (fases, piezas de la metodología, entradas R01, capturas C01, prompts P01) se explican la primera vez que salen en la conversación.
4. Al pedirme una validación, la pregunta va sin respuestas posibles redactadas. La excepción es el cierre de cada prompt de la skill: ahí me das una propuesta del mensaje con el que lo doy por bueno.
5. En los textos en mi voz (decisiones humanas, mensajes para el chat de la skill): sin recuentos de la conversación ("las dos iteraciones", "las siete reglas"), sin detallar lo que se hará más adelante ni meter trabajo futuro que no he decidido, sin nombrar lo que ya se sabe por el contexto y sin frases que anuncian lo que hace el mensaje. Si el chat dio una lista numerada, se contesta por sus números. Los mensajes piden cambios concretos del entregable, no instrucciones sobre cómo redactar.
6. Cuando toque una captura de `evidence/screenshots.md` del repositorio de la skill, avísame en un párrafo aparte con su ID, lo que tiene que verse y dónde se guarda. El aviso va al entregarme el prompt que la provoca y en el mensaje en que traigo lo que muestra, antes de que apruebe. Si pregunto y no toca ninguna, dímelo.
7. Si algo se puede hacer de varias maneras (nombres de ficheros, de parámetros o de scripts), pregúntame antes de elegir.
8. Cada vez que el chat de la skill presente una propuesta, sus decisiones abiertas o un entregable para validar, dame algo con lo que contestarle que no sea aceptarlo tal cual: una corrección o un matiz concreto, para que el profesor no vea en las iteraciones que acepto todo lo que propone. Tiene que salir de revisar la propuesta contra los ficheros del repositorio de la skill. Si no hay nada que corregir de verdad, dímelo en lugar de inventarlo.
9. Cuando un mensaje para el chat de la skill diga quién redactó el texto de un prompt, lleva siempre la frase completa de las entradas del registro: "Claude Code redactó el texto del prompt con `<modelo>`, a partir de mis indicaciones, y lo revisé antes de enviarlo." Nunca se corta en "a partir de mis indicaciones".

## Credenciales y git

1. `Credentials sandbox DEV Jakala API.postman_environment.json` no se abre nunca, ni con herramientas ni con scripts que carguen sus valores. Solo lo usa `aep/` para autenticarse. Cada script que use `aep/` se me enseña antes de ejecutarlo, y no se imprimen los campos `clientId` ni `userId` de las respuestas de la API.
2. Los commits y el push los hago yo.
