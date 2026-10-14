# Sesión 3 — Ingesta, calidad y limpieza

La historia: un pipeline de ingesta productivizado falla con el lote de pedidos
(`16,93€` no es NUMERIC), se investiga en una cuarentena STRING, Vivento firma la
política de tratamiento, el pipeline seguro se ejecuta en BigQuery y se compara con un
limpiador ingenuo que infla los importes europeos 100× sin que nada lo avise.

## Estructura (solo lo que usa la sesión)

| Carpeta | Contenido |
|---|---|
| `data/` | `pedidos_incidente.csv` (el fichero del incidente), `pedidos_incidente_enriched.csv` (con `source_row_id`, fuente de la cuarentena), `pedidos_dorado.csv` (200 casos validados), `muestra.csv` (fila fallida + TABLESAMPLE para el prompt 1), `category_mapping.csv`, y los esquemas (`stg_pedidos_schema.json`, `quarantine_schema.json`, `golden_schema.json`, `residual_output_schema.json`). |
| `prompts/` | Los tres prompts de la sesión: triaje, pipeline seguro y residuo estructurado. |
| `output/` | Ensayos de esos prompts. **Pendiente:** volver a capturarlos sobre esta fixture. |
| `sql/` | Ficheros reales ejecutados en BigQuery `demo_calidad`: `11_profile_quarantine`, `12_pipeline_safe`, `13_validate_pipeline`, `14_naive_pipeline`, `15_eval_comparison`, `16_review_sample`, `17_muestra_aleatoria`. |
| `evidence/` | Logs y resultados observados: `load_attempt.txt` (el fallo), `quarantine_load.txt`, `golden_load.txt`, `category_mapping_load.txt`, `profile_quarantine.txt`, `pipeline_validation.txt`, `build_safe.txt`, `build_naive.txt`, `eval_comparison.txt`, `review_sample.txt`, `fixture_manifest.json`, `vivento_quality_policy.yaml`. |
| `scripts/` | `generate_fixture.py` (fixture) y `final_muestra.py` (deja la muestra lista para el prompt 1). |
| `_archivo_v1/`, `_archivo_v2/` | Historial físico de las dos versiones anteriores. Solo referencia. |

## BigQuery

Dataset: `jakamedy-data-ia.demo_calidad`. Tablas: `raw_pedidos_quarantine`,
`pedidos_dorado`, `category_mapping`, `stg_pedidos_routed` (+ vistas
`stg_pedidos_clean`, `review_pedidos`, `reject_pedidos`), `stg_pedidos_naive`.

## Cifras canónicas

- Lote: 50.000 filas. El load tipado falla atómicamente con el primer NUMERIC inválido.
- Perfil: 15.044 importes europeos · 2.038 vacíos · 977 filas con ID repetido ·
  10.170 categorías en inglés · 15 outliers · fechas 100 % ISO.
- Pipeline seguro: 46.068 clean · 3.932 review · 0 reject (suman exacto 50.000).
- Eval contra el dorado: naive 127/200 con **68 errores de campo silenciosos** ·
  seguro 200/200.

## Reproducir el incidente

```bat
cmd /c "bq --project_id=jakamedy-data-ia --location=EU load ^
  --source_format=CSV --skip_leading_rows=1 --max_bad_records=0 ^
  --schema=data\stg_pedidos_schema.json ^
  jakamedy-data-ia:demo_calidad.stg_pedidos ^
  data\pedidos_incidente.csv"

cmd /c "bq query --project_id=jakamedy-data-ia --location=EU --use_legacy_sql=false < sql\11_profile_quarantine.sql"
```
