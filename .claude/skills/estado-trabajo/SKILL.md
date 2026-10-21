---
name: estado-trabajo
description: Mantenimiento de status.md, el estado vivo de la planificación del TFM, para poder retomarla en un chat nuevo. Usar cuando ejecute /estado-trabajo, cuando pida actualizar o guardar el estado, cuando diga que cierro la sesión o que abro un chat nuevo, y después de cada hito sin que lo pida.
---

# Estado de la planificación (status.md)

`status.md` guarda lo necesario para retomar la planificación en un chat nuevo: dónde está, qué sigue, qué se ha decidido y qué se ha descartado. El detalle que no cabe va en `status/`, un `.md` por tema, y `status.md` lo enlaza en una línea.

## Secciones

Título, Última actualización, Fecha límite, Punto actual, Siguiente paso, Decisiones tomadas, Líneas descartadas, Pendiente, Datos clave, Lectura para retomar y Cronología. Las secciones sin contenido se quitan, salvo Punto actual, Siguiente paso y Cronología.

## Retomar

1. Con `/estado-trabajo` al principio de una conversación, leer `status.md` y después los ficheros de Lectura para retomar. El resto de `status/` solo cuando el tema lo pida.
2. Si algún fichero de la carpeta o el `status.md` del repositorio de la skill es más reciente que la Última actualización, avisar de que el estado puede estar desfasado y decir cuáles.
3. Resumir en dos o tres líneas el punto actual y el siguiente paso, y confirmar antes de actuar.

## Actualizar

1. Después de cada hito (una decisión, un prompt escrito, un hallazgo que cambia el plan, una línea descartada), al cerrar la sesión, cuando diga que abro un chat nuevo y cuando use `/estado-trabajo` con el trabajo en curso.
2. Si mi mensaje acaba en pregunta o pido solo análisis, no se toca, salvo que la pregunta sea sobre el propio estado del trabajo. Lo que haya salido se recoge en el siguiente turno en que se pueda editar.
3. Editar por partes con `Edit`. En cada actualización: fecha de hoy en Última actualización, Punto actual y Siguiente paso reescritos, Fecha límite y los sufijos "Espera a ... desde ..." de Pendiente revisados, dudas resueltas pasadas a Decisiones tomadas o a Líneas descartadas, pendientes hechos marcados con `[x]` y una línea por hito añadida a la Cronología.
4. Al terminar una actualización pensada para abrir un chat nuevo, dar en una línea el comando para retomar: `/estado-trabajo status.md`.

## Criterios

1. Tope de unas 150 líneas. Si se pasa, quitar primero los pendientes hechos y después mover el detalle a un fichero de `status/`. Las decisiones que otras sustituyen van a `status/decisiones-superadas.md`, con la que las sustituye.
2. La Cronología no se recorta, pero se parte: cuando pase de unas 30 líneas, los hitos anteriores a los dos últimos días de trabajo se mueven al final de `status/cronologia.md`, y la primera línea de la sección dice hasta qué fecha llega ese fichero. Las entradas no se reescriben.
3. Lectura para retomar lista solo los ficheros imprescindibles, en orden.
4. Punto actual y Siguiente paso bastan para que un chat nuevo sepa qué hacer leyendo solo la Lectura para retomar.
5. Cada decisión lleva fecha, motivo y quién la toma si no fui yo. Cada línea descartada dice por qué. Lo que sea deducción va marcado "(sin confirmar)".
6. Fechas absolutas (`2026-10-21`). Nunca credenciales ni valores del fichero de credenciales.
7. El mantenimiento se hace sin preguntar y sin contarlo. Revisar la ortografía antes de darlo por terminado.
