# Equipo Data — KPIs y grano acordados

Definiciones firmadas por el equipo a lo largo del proyecto. Antes de crear o
tocar un modelo `fct_`, comprueba aquí si tu tabla afecta a alguna de estas
definiciones. Los cambios en este documento solo los mergea un humano con
aprobación del owner del KPI.

## Definiciones vigentes

| KPI | Grano | Definición | Notas |
|---|---|---|---|
| Ventas diarias por tienda | tienda × día | tickets, unidades, importe_total, tickets_campana | Fuente: `stg_ventas_offline` |
| ROI por campaña y mes | campaña × mes | (ingresos atribuidos − gasto) / gasto | La atribución y el gasto viven en el modelo de campañas; las ventas offline con `campana_id` alimentan el lado de ingresos |

## Reglas de modelado derivadas

- Toda `fct_` nueva documenta en cabecera: **grano**, fuente, owner, y su
  relación con estos KPIs (si la hay).
- `campana_id` puede venir VACÍO: no se imputa. Las métricas de campaña y las
  totales se separan (`tickets_campana` cuenta solo tickets con campaña).
- Particionado por fecha y cluster por la clave de negocio más consultada,
  como manda el canon operativo (`contexto_equipo.md`).

## Lo que NO está decidido

Si tu tabla sugiere un KPI nuevo o un cambio de grano de uno existente, eso no
lo decide el autor del modelo: se abre como DECISIÓN ABIERTA para el owner.
