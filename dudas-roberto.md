### Contexto de la propuesta

Propongo como acelerador una skill que decide si se puede crear una audiencia en el CDP de Adobe. Recibe una petición de segmentos escrita por un equipo de negocio y un catálogo de atributos de la plataforma, y devuelve para cada segmento si es viable, con qué atributos, el nivel de complejidad (baja, media o alta), las condiciones que se cumplen y las decisiones que hay que pedir al equipo solicitante.

Es una tarea que repito en mi trabajo. Contestar una petición a mano implica que la persona tiene que localizar los atributos, entender qué significan, conocer su cobertura y la ventana de datos que guardan, y redactar una respuesta que pueda leer el equipo de negocio.

La skill no se conecta a la plataforma. El conocimiento del proyecto va en ficheros: un catálogo con la descripción, los valores, el tipo y la ruta de cada atributo, más su cobertura, su origen y frecuencia de actualización, su ventana de datos y el significado del nulo. La skill actúa de router: lee la petición, localiza en el catálogo los atributos que hacen falta y razona la viabilidad. Lo que solo se podría comprobar en la plataforma, como el tamaño de cada audiencia, sale marcado como pendiente y la skill no lo ejecuta. Antes de nada comprueba que el catálogo tenga el formato esperado.

El informe de salida está pensado para pasarlo al equipo de negocio. Llevaría una tabla por segmento y una lista de decisiones abiertas, sin datos técnicos ni plazos.

Para que cualquiera pueda probarla sin acceso a ningún proyecto no uso ningún dato real. Entrego tres catálogos de ejemplo inventados, de sectores distintos, con peticiones y respuestas esperadas. Se pueden probar con ellos o con un catálogo propio en el mismo formato. Todo se desarrolla y se prueba en Claude con una cuenta personal, y no se ejecuta dentro del entorno de ningún proyecto. Con la plantilla del catálogo, cualquier proyecto de CDP de Adobe puede adaptarla, y las afirmaciones generales sobre Adobe salen de la documentación pública, con su enlace.

Para la comparación sin y con acelerador uso la misma petición y el mismo catálogo, con las horas de ejecución y de revisión por separado. La calidad se mide contra la respuesta esperada con criterios explícitos: viabilidad y complejidad de cada segmento, decisiones abiertas, atributos que no existen en el catálogo y pendientes marcados. El tiempo manual será una estimación con su supuesto, no una medida verificada y cronometrada.

### Dudas

1. ¿Se admite como acelerador una skill que no ejecuta consultas ni llamadas contra la plataforma y que trabaja solo con un catálogo de atributos y una petición en texto? Esta solución es la que veo viable en mi caso que trabajo con la plataforma de Adobe CDP y no tengo cuenta corporativa del cliente para ejecutar realmente dentro del entorno.

2. La evidencia de operación (ejecuciones fechadas con sus incidencias), ¿puede salir de ejecuciones sobre datos inventados con una cuenta personal, dado que la guía pide enmascarar los datos reales antes de enviarlos a cualquier asistente?

3. ¿Con qué herramienta se va a probar el acelerador y en qué formato se espera recibirlo para instalarlo con el README?

4. Si se entregan tres catálogos de ejemplo ya preparados, ¿basta para probarlo o prefieres Robert, escribir uno propio con el mismo formato?

5. Entiendo que la documentación del paso a paso tiene que ser con capturas de pantalla de algunas partes de la iteración con el agente mientras se desarrolla la skill. Y luego se puede hacer un vídeo al final mostrando cómo funciona la skill. ¿Es correcto así?

