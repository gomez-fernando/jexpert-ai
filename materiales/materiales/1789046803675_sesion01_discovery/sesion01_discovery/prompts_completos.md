# Prompts completos — Sesión 1 (montados con material real)

Generado por `scripts/montar_prompts_s1.py` a partir de `data/`, `contexto_equipo.md`
y `output/pares_candidatos.json`. Los cuatro prompts van listos para pegar en Claude.

---

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
Nombre y Apellidos;Correo ElectrÃ³nico;TelÃ©fono;Empresa;Evento;Fecha
Rocío Serrano;rocio.serrano@acme.com;+34 612 345 678;Acme Retail;Feria ProSector Madrid 2026;14/05/2026
Alberto Molina;alberto.molina@nordika.com;+34 655 210 431;Nordika Moda;Feria ProSector Madrid 2026;14/05/2026
Inés Castillo;;612-884-207;Vela Hogar;Webinar: reposición inteligente de stock;2026-05-21
Marcos Vega;marcos.vega@gmeridiano.com;+34 698 114 552;Grupo Meridiano;Webinar: reposición inteligente de stock;21/05/2026
Claudia  Prieto;claudia.prieto@tecnoandar.com;;TecnoAndar;Feria ProSector Valencia 2026;03/06/26
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

<contexto_equipo>
# Equipo Data — Contexto del proyecto

## Convenciones de naming
- Columnas: snake_case; fechas en `_at` (timestamp) o `_date`; claves `*_id`.
- Booleanos: prefijo `is_` / `has_`.

## Glosario de negocio
- **Lead:** contacto no cualificado procedente de cualquier fuente.
- **Contacto:** lead cualificado vinculado a una cuenta (CRM). Lead ≠ contacto.

## Al interactuar con asistentes
- Nunca inventes valores: devuelve null + `requiere_revision = true`.
- Si falta información para una decisión, enumérala como DECISIÓN ABIERTA.
</contexto_equipo>

<crm>
id_lead,nombre,apellido,mail_contacto,tel,empresa,fecha_alta
3 filas de muestra:
L344942,Sergio,Gutiérrez,sergio.gutierrez@nordika.com,+34 646 617 554,Nordika Moda,2025-11-19
L850069,Laura,Álvarez,laura.alvarez@gmeridiano.com,+34 680 986 962,Grupo Meridiano,2025-09-14
L605407,Carmen,Fernández,carmen.fernandez@gmeridiano.com,+34 621 105 981,Grupo Meridiano,2025-08-14
</crm>

<evento>
id_asistente,nombre,email,telefono,empresa,evento,fecha
3 filas de muestra:
EV41850,Raúl Muñoz,raulmunoz@velahogar.es,+34640333375,Vela Hogar,Webinar: fiscalidad para pymes 2026,09/06/2026
EV82269,DIEGO GUTIÉRREZ,dgutierrez@gmeridiano.com,,Grupo Meridiano,Jornada de puertas abiertas Sevilla 2025,22/11/2025
EV21813,lucía garcía,lgarcia@acme.es,+34660969639,Acme Retail,Encuentro de clientes Vivento 2026,15/06/2026
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
    "empresa": "Acme Retail"
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
      "campos_en_conflicto": {"type": "array", "items": {"type": "string"}},
      "justificacion": {"type": "string", "maxLength": 280}
    },
    "required": ["par_id", "es_misma_entidad", "confianza", "campos_en_conflicto", "justificacion"],
    "additionalProperties": false
  }
}
</esquema_salida>

<pares>
[
  {
    "par_id": 1,
    "blocking_reason": "telefono_exacto",
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
      "empresa": "Acme Retail"
    }
  },
  {
    "par_id": 2,
    "blocking_reason": "telefono_exacto",
    "crm": {
      "id": "L291597",
      "nombre": "Javier Álvarez",
      "email": "javier.alvarez@velahogar.es",
      "telefono": "+34 654 953 861",
      "empresa": "Vela Hogar"
    },
    "evento": {
      "id": "EV36248",
      "nombre": "Javier Á.",
      "email": "jalvarez@velahogar.es",
      "telefono": "+34654953861",
      "empresa": "Vela Hogar"
    }
  },
  {
    "par_id": 3,
    "blocking_reason": "telefono_exacto",
    "crm": {
      "id": "L362032",
      "nombre": "Carlos Fernández",
      "email": "carlos.fernandez@acme.com",
      "telefono": "+34 610 664 974",
      "empresa": "Acme Retail"
    },
    "evento": {
      "id": "EV65554",
      "nombre": "Carlitos Fernández",
      "email": "cfernandez@acme.es",
      "telefono": "+34610664974",
      "empresa": "Acme Retail"
    }
  },
  {
    "par_id": 4,
    "blocking_reason": "telefono_exacto",
    "crm": {
      "id": "L390175",
      "nombre": "Lucía García",
      "email": "lucia.garcia@acme.com",
      "telefono": "+34 660 969 639",
      "empresa": "Acme Retail"
    },
    "evento": {
      "id": "EV21813",
      "nombre": "lucía garcía",
      "email": "lgarcia@acme.es",
      "telefono": "+34660969639",
      "empresa": "Acme Retail"
    }
  },
  {
    "par_id": 5,
    "blocking_reason": "telefono_exacto",
    "crm": {
      "id": "L501714",
      "nombre": "Marta Domínguez",
      "email": "marta.dominguez@gmeridiano.com",
      "telefono": "+34 685 113 894",
      "empresa": "Grupo Meridiano"
    },
    "evento": {
      "id": "EV68861",
      "nombre": "Marti Domínguez",
      "email": "mdominguez@gmeridiano.com",
      "telefono": "+34685113894",
      "empresa": "Grupo Meridiano"
    }
  },
  {
    "par_id": 6,
    "blocking_reason": "telefono_exacto",
    "crm": {
      "id": "L505206",
      "nombre": "Marta López",
      "email": "marta.lopez@tecnoandar.com",
      "telefono": "+34 654 932 806",
      "empresa": "TecnoAndar"
    },
    "evento": {
      "id": "EV75939",
      "nombre": "MARTA LÓPEZ",
      "email": "mlopez@tecnoandar.com",
      "telefono": "+34654932806",
      "empresa": "TecnoAndar"
    }
  },
  {
    "par_id": 7,
    "blocking_reason": "telefono_exacto",
    "crm": {
      "id": "L532486",
      "nombre": "Carmen Álvarez",
      "email": "carmen.alvarez@tecnoandar.com",
      "telefono": "+34 671 517 415",
      "empresa": "TecnoAndar"
    },
    "evento": {
      "id": "EV48468",
      "nombre": "CARMEN ÁLVAREZ",
      "email": "calvarez@tecnoandar.com",
      "telefono": "+34671517415",
      "empresa": "TecnoAndar"
    }
  },
  {
    "par_id": 8,
    "blocking_reason": "telefono_exacto",
    "crm": {
      "id": "L605407",
      "nombre": "Carmen Fernández",
      "email": "carmen.fernandez@gmeridiano.com",
      "telefono": "+34 621 105 981",
      "empresa": "Grupo Meridiano"
    },
    "evento": {
      "id": "EV86787",
      "nombre": "carmen fernández",
      "email": "cfernandez@gmeridiano.com",
      "telefono": "+34621105981",
      "empresa": "Grupo Meridiano"
    }
  },
  {
    "par_id": 9,
    "blocking_reason": "telefono_exacto",
    "crm": {
      "id": "L610556",
      "nombre": "Pablo Muñoz",
      "email": "pablo.munoz@tecnoandar.com",
      "telefono": "+34 688 216 555",
      "empresa": "TecnoAndar"
    },
    "evento": {
      "id": "EV74265",
      "nombre": "Pablo Muñoz",
      "email": "pmunoz@tecnoandar.com",
      "telefono": "+34688216555",
      "empresa": "TecnoAndar"
    }
  },
  {
    "par_id": 10,
    "blocking_reason": "telefono_exacto",
    "crm": {
      "id": "L612209",
      "nombre": "Javier Navarro",
      "email": "javier.navarro@gmeridiano.com",
      "telefono": "+34 634 361 273",
      "empresa": "Grupo Meridiano"
    },
    "evento": {
      "id": "EV58386",
      "nombre": "Javi Navarro",
      "email": "jnavarro@gmeridiano.com",
      "telefono": "+34634361273",
      "empresa": "Grupo Meridiano"
    }
  }
]
</pares>
```
