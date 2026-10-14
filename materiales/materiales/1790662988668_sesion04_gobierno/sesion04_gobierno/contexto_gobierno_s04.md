# Contexto de gobierno — Sesión 4 (Vivento)

Política de tratamiento de PII y reglas de salida. Redactada con asistencia a
partir del esquema y de muestras ya tratadas — sin dato crudo. La salida utilizada
está en `output/prompt_3_politica_pii.md`.

**Estado:** propuesta técnica. Las decisiones marcadas ☐ quedan pendientes de
firma por el owner antes de publicarse. No sustituye la validación legal.

## Fuentes cubiertas

`gold.dim_contacto` · `contactos.csv` (CRM) · `formularios_web.csv` (web)

## Campos sensibles y tratamiento

| Campo | Tratamiento |
|---|---|
| `nombre`, `apellido` | Prohibido en claro fuera del CRM operativo |
| `email` | Pseudonimizar (hash determinista + sal) para cruces; enmascarar (`l***@dominio`) para humanos |
| `telefono` | Enmascarar (`+34 *** *** 805`); valor completo solo en origen |
| `contacto_id` | Pseudonimizar (hash determinista + sal, misma en todas las fuentes) |
| `fecha_alta`, `fecha` | Libre en uso interno; agregar a mes/trimestre en difusión amplia |
| `empresa` | Libre salvo autónomos — ☐ confirmar si existen y añadir flag `es_persona_fisica` |
| `sk_contacto`, `envio_id`, `pedido_id`, `motivo` | No PII; reglas generales de minimización |
| `texto` (formularios web) | Crudo prohibido fuera de la capa determinista; solo viaja la versión enmascarada (`scripts/enmascarar_formularios.py`) |

Principio: si lo mismo se obtiene agregado o anonimizado, se prefiere a lo
pseudonimizado (es irreversible y no depende de custodiar una sal).

## Reglas para muestras en prompts

1. Nunca en claro: nombre, apellido, email completo, teléfono completo,
   `contacto_id` crudo, `texto` sin enmascarar. Vale para producción, pruebas y
   debugging; no hay excepción "solo es una prueba".
2. Formas permitidas: hash (`h_417ba743`), máscaras, texto ya enmascarado por
   la capa determinista, campos libres.
3. Mínimo de filas necesarias por tarea — ☐ fijar tope de referencia.
4. Ojo a la combinación: email enmascarado + empresa + fecha puede reidentificar
   en empresas con pocos contactos; generalizar o quitar un campo.
5. Lo mismo aplica a las salidas del modelo: si reconstruye un dato prohibido,
   se descarta y no se guarda.

## Canal autorizado y registro

- Solo cuenta/endpoint corporativo autorizado por IT Security — ☐ referencia exacta.
- Todo prompt y respuesta que toque estas fuentes queda registrado (timestamp,
  emisor, fuente) — ☐ sistema de log, retención y acceso.
- Los logs guardan las formas tratadas, nunca un dato en claro; si un log
  captura claro por error, es incidente de seguridad.
- Nada a plugins/skills de terceros no aprobados.

## Aprobaciones (doble control donde aplica)

- Publicar campo/tabla con PII en catálogo — ☐ Data Owner Vivento + DPO.
- Reversión de un hash (derechos RGPD, soporte) — ☐ aprobación conjunta, motivo
  registrado; quien recibe la solicitud no ejecuta solo.
- Custodia y rotación de la sal — ☐.
- Excepciones documentadas con fecha de caducidad — ☐ responsable de seguridad/DPO.
- Revisión periódica de esta política — ☐.
