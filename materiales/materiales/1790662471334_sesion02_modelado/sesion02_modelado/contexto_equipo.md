# Equipo Data — Contexto para modelado (S2)

Versión acotada de `EQUIPO_DATA.md` para la sesión de modelado. No incluye el modelo
canónico ni referencias a tablas gold existentes: el modelo se diseña en clase.

## Naming

- Datasets: raw, staging, silver, gold.
- Hechos: fct_*; dimensiones: dim_*; puentes: bridge_*.
- Surrogate keys: sk_*.
- Claves naturales: *_nk.
- Fechas de vigencia: fecha_desde, fecha_hasta, flag_vigente.

## Glosario

- Lead: contacto todavía no cualificado.
- Contacto: entidad canónica de persona.
- Campaña: unidad de inversión con vigencia y canal.
- Interacción: evento de un contacto con una campaña.
- Venta: ticket offline completo.

## Reglas de diseño

- No inventes fuentes, campos ni entidades.
- Declara el grano de cada hecho.
- Enumera DECISIONES ABIERTAS.
- No decidas source of truth ni métricas por nosotros.
