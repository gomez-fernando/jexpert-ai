# Política de tratamiento de PII — fuentes Vivento (dim_contacto, contactos.csv, formularios_web.csv)

**Alcance:** `gold.dim_contacto`, `contactos.csv` (CRM) y `formularios_web.csv` (web).
**Fecha:** 2026-09-23 · **Estado:** propuesta, pendiente de validación por los owners marcados abajo.

**Nota sobre el dato de entrada:** esta propuesta se ha construido solo con el esquema y las dos muestras ya pseudonimizadas. No ha sido necesario ver dato crudo: la clasificación de un campo como PII y el tratamiento que le corresponde son propiedades del *tipo* de campo (email, teléfono, nombre, texto libre…), no de sus valores concretos. La única duda que el esquema no puede resolver por sí solo es si `empresa` contiene alguna vez el nombre de una persona física (autónomos/profesionales individuales); no se necesita dato real para decidir la regla, solo para confirmar si el caso existe — se deja marcado como PENDIENTE en el punto 1.

---

## 1. Campos con PII

### 1.1 PII estructurada (columnas)

| Fuente | Campo | Tipo de dato personal | Identificador directo/indirecto |
|---|---|---|---|
| `gold.dim_contacto`, `contactos.csv` | `nombre`, `apellido` | Identidad | Directo |
| `gold.dim_contacto`, `contactos.csv` | `email` | Contacto | Directo |
| `gold.dim_contacto`, `contactos.csv` | `telefono` | Contacto | Directo |
| `gold.dim_contacto`, `contactos.csv` | `contacto_id` | Identificador de negocio 1:1 con una persona | Indirecto (reidentifica vía CRM) |
| `formularios_web.csv` | `email` | Contacto | Directo |
| `gold.dim_contacto`, `contactos.csv` | `fecha_alta` | Metadato temporal | Cuasi-identificador (baja severidad) |
| `formularios_web.csv` | `fecha` | Metadato temporal | Cuasi-identificador (baja severidad) |
| `gold.dim_contacto`, `contactos.csv`, `formularios_web.csv` | `empresa` | Dato organizativo | Indirecto **solo si** la empresa es un autónomo cuyo nombre comercial coincide con el nombre de una persona física — **PENDIENTE: owner** confirmar si existen estos casos en Vivento |

**No PII** (no identifican por sí mismas y no se tratan en esta política): `sk_contacto` (clave surrogate interna del warehouse, sin significado fuera de él), `envio_id`, `pedido_id`, `motivo`. Estas sí actúan como *claves de unión* hacia registros personales, por lo que quedan sujetas a las reglas generales de minimización del punto 3, aunque no requieran pseudonimización propia.

### 1.2 PII embebida en texto libre

| Fuente | Campo | Riesgo |
|---|---|---|
| `formularios_web.csv` | `texto` | Alto: campo de texto abierto que puede contener nombres, teléfonos, emails, direcciones, números de pedido, y ocasionalmente datos sensibles incidentales (salud, situación personal) mencionados por el propio contacto |

La muestra dada (`«Queremos saber el estado del pedido. Mejor por teléfono: [TELEFONO], preguntad por [PERSONA].»`) confirma que la capa determinista ya aplica una sustitución de entidades (NER) sobre este campo antes de que salga de esa capa. Esta política asume esa sustitución como parte del pipeline y añade las reglas de qué hacer con el resultado y con sus fallos (falsos negativos de NER).

---

## 2. Tratamiento por campo

| Campo | Tratamiento | Detalle |
|---|---|---|
| `nombre`, `apellido` | **Prohibir salida en claro** fuera del sistema operativo de origen (CRM) | No se replican en claro a `gold`, a catálogos, a muestras ni a prompts. Si un caso de uso necesita nombrar al contacto (p. ej. personalización de campaña), se resuelve dentro del sistema operativo, nunca en la capa analítica. — **PENDIENTE: owner** confirmar si existe un caso de negocio que obligue a mantener `nombre`/`apellido` en `gold.dim_contacto`; si no lo hay, se recomienda excluir estas columnas del modelo gold en vez de pseudonimizarlas. |
| `email` | **Pseudonimizar** (hash determinista + sal del proyecto) para almacenamiento y cruces; **enmascarar** para cualquier muestra o visualización humana | Normalizar el valor (minúsculas, sin espacios) antes de hashear, y usar la **misma sal y el mismo email normalizado como clave de resolución de identidad** en `dim_contacto`, `contactos.csv` y `formularios_web.csv`. Esto es lo que permite unir un envío de `formularios_web.csv` (que no tiene `contacto_id`) con un contacto del CRM sin exponer el email real. Máscara de referencia: `l***@tecnoandar.com` (primera letra + dominio visibles), igual que la muestra. |
| `telefono` | **Enmascarar** para cualquier salida humana o a modelo; el valor completo solo vive en el sistema operativo de origen | Máscara de referencia: `+34 *** *** 805` (prefijo de país + últimos dígitos), igual que la muestra. No se pseudonimiza con hash porque no se usa como clave de unión; si en algún momento se necesitara como clave de unión, aplicar el mismo esquema de hash+sal que `email`. |
| `contacto_id` | **Pseudonimizar** (hash determinista + sal del proyecto) | Igual criterio que `email`: mismo algoritmo y sal en todas las fuentes que lo usen, para que siga siendo válido como clave de unión tras la pseudonimización. Formato de referencia: `h_417ba743`, igual que la muestra. |
| `fecha_alta`, `fecha` | **Libre / agregar cuando proceda** | No son identificadores por sí mismos. En análisis internos de uso restringido pueden viajar como fecha exacta; en cualquier salida agregada de mayor difusión (dashboards ampliamente compartidos, reporting externo) se recomienda generalizar a mes o trimestre para reducir el riesgo de combinación con otros cuasi-identificadores. |
| `empresa` | **Libre**, con excepción marcada | Dato organizativo, no personal en el caso general B2B. Excepción: si corresponde a un autónomo/profesional individual, tratar como identidad directa (mismo régimen que `nombre`/`apellido`). — **PENDIENTE: owner** decidir si se necesita un flag `es_persona_fisica` en el modelo para poder aplicar esta excepción de forma sistemática. |
| `sk_contacto`, `envio_id`, `pedido_id`, `motivo` | **Libre** | No PII. Sujetos solo a las reglas generales de minimización (no combinar más campos de los necesarios en una misma salida) del punto 3. |
| `texto` (formularios_web) | **Prohibir la versión cruda; pseudonimizar mediante redacción NER antes de cualquier uso** | Solo la versión ya redactada (post-NER, con placeholders `[PERSONA]`, `[TELEFONO]`, etc.) puede almacenarse en `gold`, aparecer en catálogo o viajar a un modelo. El texto crudo no sale nunca de la capa determinista. Dado que la detección NER no es perfecta, tratar el texto redactado igualmente como dato **confidencial** (no público) y someterlo a auditoría periódica por muestreo para medir la tasa de fugas residuales (falsos negativos de NER). — **PENDIENTE: owner** definir frecuencia y tamaño de la muestra de auditoría, y qué se hace cuando se detecta una fuga (¿se re-procesa el histórico?). |

**Principio general (minimización, RGPD):** cuando el mismo resultado se pueda obtener con un dato agregado o anonimizado en vez de pseudonimizado, se prefiere la agregación/anonimización, porque es irreversible y no depende de custodiar una sal. La pseudonimización con hash+sal se reserva para los campos que de verdad necesitan seguir siendo una clave de unión (`email`, `contacto_id`).

---

## 3. Reglas para muestras en prompts

Qué puede viajar a un modelo (Claude o cualquier otro) y en qué forma:

1. **Nunca en claro:** `nombre`, `apellido`, `email` completo, `telefono` completo, `contacto_id` crudo, `texto` sin redactar. Esto aplica igual a prompts de producción, pruebas, debugging y few-shot examples — no hay excepción por ser "solo una prueba".
2. **Formas permitidas:** identificadores hasheados (`h_417ba743`), email enmascarado (`l***@dominio.com`), teléfono enmascarado (`+34 *** *** 805`), texto libre ya redactado por NER, y cualquier campo marcado como "Libre" en el punto 2.
3. **Minimización de filas:** cada prompt debe incluir solo las filas estrictamente necesarias para la tarea, no un extracto amplio "por si acaso". — **PENDIENTE: owner** fijar un tope numérico de referencia (p. ej. ≤5 filas para debugging/few-shot); mientras no se fije, se aplica el criterio de "el mínimo necesario".
4. **Riesgo de combinación:** aunque cada campo individual esté tratado, combinar varios campos pseudonimizados/enmascarados en el mismo prompt (p. ej. email enmascarado + empresa + fecha_alta exacta) puede volver a identificar a una persona si la empresa tiene muy pocos contactos. Antes de combinar campos de baja cardinalidad en un mismo prompt, revisar si esa combinación reduce el conjunto a una sola persona; si es así, generalizar uno de los campos (p. ej. fecha a mes) o quitar `empresa` de esa combinación.
5. **Dominio de email:** el dominio de la máscara (`@tecnoandar.com`) es en sí mismo información de negocio (identifica la empresa del contacto), no un dato personal adicional; se mantiene visible salvo que el propio dominio identifique a un autónomo (ver excepción de `empresa` en el punto 2).
6. **Salidas del modelo:** las mismas reglas se aplican a lo que el modelo devuelve. Si una respuesta del modelo reconstruye o infiere un dato prohibido (p. ej. "adivina" un email a partir del contexto), esa respuesta se descarta y no se reenvía ni se guarda en claro.

---

## 4. Canal autorizado y registro de prompts/respuestas

- **Canal:** todo prompt que incluya datos de estas fuentes (aunque sea en forma pseudonimizada/enmascarada) debe enviarse únicamente a través de la cuenta/entorno corporativo de Jakala autorizado para este proyecto, nunca desde una cuenta personal o un servicio de IA no aprobado por IT Security. — **PENDIENTE: owner** confirmar el identificador exacto de esa cuenta/endpoint (workspace, proyecto de API, o entorno concreto) para dejarlo referenciado aquí.
- **Registro obligatorio:** todo prompt y toda respuesta que toquen estas fuentes deben quedar registrados (log), incluyendo timestamp, usuario/proceso emisor y la fuente de datos implicada. — **PENDIENTE: owner** definir sistema de log, periodo de retención y quién tiene acceso a esos logs.
- **Los logs no son una vía de escape:** el registro debe conservar las formas ya tratadas (hash/máscara/texto redactado), no debe convertirse en un segundo almacén de datos en claro. Si un log llegara a capturar un dato en claro por error (p. ej. un fallo de la capa de redacción), ese log se trata como incidente de seguridad, no como registro normal.
- **Terceros:** queda excluido enviar estos datos, en cualquier forma, a plugins o skills de terceros no aprobados por IT Security, conforme a la política general de la organización.

---

## 5. Quién aprueba qué

| Decisión | Aprobador propuesto |
|---|---|
| Publicar en el catálogo un campo o tabla nueva que contenga PII | **PENDIENTE: owner** (rol de Data Owner de Vivento + Gobierno del Dato/DPO de Jakala) |
| Revertir un hash (reidentificar), p. ej. para atender una solicitud de derechos RGPD (acceso, rectificación, supresión) o soporte al cliente | **PENDIENTE: owner** — se propone que requiera aprobación conjunta del Data Owner de Vivento y de Legal/DPO de Jakala, con motivo y alcance registrados, y que quien reciba la solicitud original no sea quien ejecuta la reversión en solitario (doble control) |
| Custodia de la sal de pseudonimización (quién puede generarla/rotarla) | **PENDIENTE: owner** |
| Excepciones puntuales a esta política (p. ej. enviar un campo normalmente prohibido para un caso de uso concreto) | **PENDIENTE: owner** — se propone que toda excepción quede documentada por escrito, con fecha de caducidad, y aprobada por el responsable de seguridad de la información o el DPO, no solo por el equipo de datos |
| Revisión y actualización periódica de esta política | **PENDIENTE: owner** |

---

*Este documento es una propuesta técnica de tratamiento de datos personales. No sustituye la validación legal formal.*

AI-generated — requires JAKALA Legal/Finance review before use.
