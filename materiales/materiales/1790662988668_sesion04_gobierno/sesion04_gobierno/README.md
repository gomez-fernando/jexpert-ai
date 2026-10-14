# Sesión 4 — Gobierno, privacidad y trazabilidad

Repositorio reproducible de la sesión 4 del track **IA aplicada a Data Management**.
El material utiliza exclusivamente datos sintéticos del cliente ficticio Vivento.

## Recorrido

1. `data/formularios_web.csv` contiene 55 envíos sintéticos al formulario de contacto.
2. `scripts/enmascarar_formularios.py` trata PII conocida antes de reutilizar el texto.
3. `prompts_completos.md` contiene los cinco prompts utilizados en clase.
4. `output/prompt_*.md` conserva las respuestas observadas de los ensayos.
5. `sql/informe_roi_campana_mes.sql` es la consulta analizada en la demo de lineage.
6. `contexto_gobierno_s04.md` recoge la política propuesta y las decisiones pendientes de owner.

## Estructura

```text
sesion04_gobierno/
├── README.md
├── contexto_gobierno_s04.md
├── prompts_completos.md
├── data/
│   └── formularios_web.csv
├── output/
│   ├── formularios_web_enmascarado.csv
│   ├── manifest_enmascarado.txt
│   ├── manifest_formularios.txt
│   ├── prompt_1_documentacion.md
│   ├── prompt_2_lineage.md
│   ├── prompt_3_politica_pii.md
│   ├── prompt_4a_triaje_normales.md
│   ├── prompt_4a_triaje_ataque.md
│   └── prompt_4b_triaje_mitigado.md
├── scripts/
│   ├── generar_formularios_s4.py
│   └── enmascarar_formularios.py
├── sql/
│   └── informe_roi_campana_mes.sql
└── _archivo_v1/
    └── material descartado de reseñas y tickets
```

## Regeneración de datos

Desde la raíz del proyecto:

```text
python repo_demo/sesion04_gobierno/scripts/generar_formularios_s4.py
python repo_demo/sesion04_gobierno/scripts/enmascarar_formularios.py
```

Ambos scripts ejecutan sus comprobaciones antes de escribir. Los conteos quedan registrados
en `output/manifest_formularios.txt` y `output/manifest_enmascarado.txt`.

## Límites de la demostración de PII

`enmascarar_formularios.py` es una pieza didáctica: cubre formatos y frases conocidos del
conjunto sintético. No es un detector universal ni demuestra ausencia total de PII. En un
proyecto real se usarían detectores aprobados dentro del entorno controlado, con pruebas de
recall y revisión del riesgo residual.

Los tokens opacos no tienen tabla de reversión. El dato original permanece en el sistema
operativo; una persona autorizada vuelve al caso original cuando necesita tratarlo.

## Canal para datos reales

El curso usa datos sintéticos. En un proyecto real, los datos personales solo pueden enviarse
a un asistente cuando el cliente ha autorizado el canal y la finalidad, y están definidos los
controles de acceso, retención y auditoría. Minimizar el número de filas reduce exposición,
pero no deja de ser tratamiento de PII.
