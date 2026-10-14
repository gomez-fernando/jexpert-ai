# Output del prompt 3 — Triaje del residuo (ensayo real, fixture actual)

> Capturado el 2026-09-22 ejecutando `prompts/prompt_3_residual.md` con Claude.
> Los tres casos pasan el JSON Schema (`data/residual_output_schema.json`).
> Casos reales tomados de `evidence/review_sample.txt` sobre el lote actual.

---

# Triaje de calidad de datos

Casos clasificados por reglas deterministas. No se eligen filas duplicadas, no se imputan importes vacíos y no se corrigen outliers.

```json
[
  {
    "source_row_id": "R0000018",
    "pedido_id": "P0000018",
    "case_type": "duplicado_conflictivo",
    "normalized_value": null,
    "requires_review": true,
    "recommended_action": "human_review",
    "reason": "pedido_id P0000018 aparece repetido con datos distintos entre filas; no se elige automáticamente cuál registro es correcto."
  },
  {
    "source_row_id": "R0000004",
    "pedido_id": "P0000004",
    "case_type": "importe_vacio",
    "normalized_value": null,
    "requires_review": true,
    "recommended_action": "ask_source",
    "reason": "importe vacío en fecha=2026-04-09, categoría=Alimentación; no se imputa, se debe solicitar el dato a la fuente."
  },
  {
    "source_row_id": "R0007031",
    "pedido_id": "P0007031",
    "case_type": "outlier",
    "normalized_value": 165819.98,
    "requires_review": true,
    "recommended_action": "human_review",
    "reason": "importe 165819.98 EUR supera el umbral de 90000 EUR en categoría Electrónica; valor no corregido, requiere revisión."
  }
]
```

---
*AI-assisted — requires human review before distribution.*
