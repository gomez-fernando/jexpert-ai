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
