# gold.fct_atribucion_venta_campana

Fuente: catálogo interno de Vivento · Generado a partir del DDL del modelo v2 y el glosario del proyecto · 2026-09-23

## Descripción de tabla

Registra el reparto del crédito de cada venta entre las campañas de marketing que impactaron al contacto antes de la compra. Cada fila representa el peso de crédito asignado a una campaña para un ticket de venta, según el modelo de atribución aplicado (first_touch, last_touch o lineal) y la ventana de días considerada. Para cada ticket_id, la suma de los pesos de todas sus campañas es igual a 1, bajo la configuración de atribución vigente.

## Columnas

- **ticket_id**: identifica el ticket de venta al que se le está asignando crédito de atribución (FK → gold.fct_venta.ticket_id).
- **sk_campana**: identifica la campaña de marketing a la que se asigna una parte del crédito de la venta (FK → gold.dim_campana.sk_campana).
- **sk_fecha**: clave de fecha asociada al registro de atribución (FK → gold.dim_fecha.sk_fecha). PENDIENTE: confirmar con owner si representa la fecha del touchpoint de campaña, la fecha de la venta u otra fecha de referencia.
- **modelo_atribucion**: modelo de atribución aplicado para calcular el peso de esta fila (valores vigentes: first_touch, last_touch, lineal).
- **ventana_dias**: número de días previos a la compra que se consideraron como ventana de atribución para incluir los touchpoints de campaña.
- **peso_atribucion**: proporción del crédito de la venta asignada a la campaña indicada; la suma de peso_atribucion por ticket_id es igual a 1 en la configuración vigente cargada.

## Preguntas de negocio que responde

1. ¿Qué campañas contribuyeron a cada venta y qué peso de crédito recibió cada una, según el modelo de atribución aplicado?
2. ¿Qué modelo de atribución (first_touch, last_touch, lineal) resulta más favorable para evaluar el desempeño de una campaña o marca?
3. ¿Durante cuántos días antes de la compra siguen influyendo las campañas en la decisión del cliente, según la ventana de atribución configurada?
