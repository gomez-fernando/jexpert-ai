# Prompt 3 — Residuo estructurado

```text
Actúa como asistente de triaje para una cola humana de calidad de datos.

Recibes únicamente casos ya clasificados por reglas deterministas. No elijas
entre filas duplicadas, no imputes importes vacíos y no "corrijas" un outlier
por parecer alto.

Devuelve un array JSON que cumpla <json_schema>. El motivo debe citar la
evidencia y tener como máximo 200 caracteres.

<json_schema>
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "source_row_id": {"type": "string"},
      "pedido_id": {"type": "string"},
      "case_type": {"enum": ["importe_vacio", "duplicado_conflictivo", "outlier"]},
      "normalized_value": {"type": ["string", "number", "null"]},
      "requires_review": {"const": true},
      "recommended_action": {"enum": ["human_review", "ask_source"]},
      "reason": {"type": "string", "maxLength": 200}
    },
    "required": ["source_row_id", "pedido_id", "case_type", "normalized_value", "requires_review", "recommended_action", "reason"]
  }
}
</json_schema>

<cases>
R0000018 | P0000018 | fecha=2025-05-24 | importe=111.91 | categoria=Alimentación | pedido_id repetido con datos diferentes
R0000004 | P0000004 | fecha=2026-04-09 | importe=[vacío] | categoria=Alimentación | importe vacío
R0007031 | P0007031 | fecha=2025-04-27 | importe=165819.98 | categoria=Electrónica | importe superior a 90000 EUR
</cases>
```
