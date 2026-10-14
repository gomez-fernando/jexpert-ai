# Prompts de la Sesión 1

## 1. Perfilado de la fuente recién llegada

```text
Tarea: inspecciona este fichero que nos acaba de entregar el cliente.

Entregable:
1. Esquema propuesto: nombre normalizado, tipo y ejemplos por columna.
2. Anomalías detectadas: encoding, delimitadores, formatos mezclados y columnas cuyo propósito no está claro.
3. PREGUNTAS PARA EL CLIENTE: todo lo que no se pueda deducir del fichero.

Reglas:
- No supongas el significado de una columna ambigua.
- Distingue observaciones verificables de hipótesis.
- No corrijas todavía los datos.

<muestra>
[pegar la cabecera y las cinco filas de leads_evento_recien_llegado.csv]
</muestra>
```

## 2. Mapping CRM ↔ evento

```text
Propón un mapping columna a columna entre ambos esquemas.
Usa el glosario y las convenciones de contexto_equipo.md.

Para cada campo devuelve:
- origen CRM;
- origen eventos;
- destino propuesto;
- transformación necesaria;
- confianza;
- decisión abierta, si existe.

No equipares dos campos solo porque sus nombres se parezcan.
No decidas qué fuente es autoritativa.

<crm>
id_lead, nombre, apellido, mail_contacto, tel, empresa, fecha_alta
</crm>

<evento>
id_asistente, nombre, email, telefono, empresa, evento, fecha
</evento>
```

## 3. Primer intento abierto sobre un candidato

```text
Analiza este par de registros y dime si corresponde a la misma persona.
Explica el motivo.

<par>
{
  "crm": {
    "id": "L226555",
    "nombre": "Marta Gómez",
    "email": "marta.gomez@acme.com",
    "telefono": "+34 668 698 200",
    "empresa": "Acme Retail"
  },
  "evento": {
    "id": "EV21749",
    "nombre": "Marti Gómez",
    "email": "mgomez@acme.es",
    "telefono": "+34668698200",
    "empresa": "Acme Retail",
    "evento": "Jornada de puertas abiertas Sevilla 2025"
  }
}
</par>
```

## 4. Resolución estructurada de candidatos

```text
Tarea: decide si cada par de registros candidatos corresponde a la misma persona real. Responde conforme al esquema de salida proporcionado.

Contexto: estamos deduplicando leads entre un CRM y los asistentes a un evento. Un lead es la misma entidad si persona y organización coinciden, aunque el canal de contacto difiera.

Reglas:
- El email es una señal fuerte, pero dominios distintos de la misma empresa no descartan el match.
- Los nombres con iniciales o diminutivos cuentan como coincidencia parcial.
- `es_misma_entidad` contiene tu mejor decisión; `confianza` indica la seguridad en esa decisión, no una probabilidad calibrada.
- Si la confianza es inferior a 0.8, el caso pasará a revisión humana, sea cual sea la decisión propuesta.
- La justificación debe citar campos concretos.
- No inventes datos que no estén en el par.
- Devuelve solo JSON, sin texto alrededor.

<esquema_salida>
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "par_id": {"type": "integer"},
      "es_misma_entidad": {"type": "boolean"},
      "confianza": {"type": "number", "minimum": 0, "maximum": 1},
      "campos_en_conflicto": {
        "type": "array",
        "items": {"type": "string"}
      },
      "justificacion": {"type": "string", "maxLength": 280}
    },
    "required": [
      "par_id",
      "es_misma_entidad",
      "confianza",
      "campos_en_conflicto",
      "justificacion"
    ],
    "additionalProperties": false
  }
}
</esquema_salida>

<pares>
[pegar entre 10 y 20 filas devueltas por blocking.sql]
</pares>
```
