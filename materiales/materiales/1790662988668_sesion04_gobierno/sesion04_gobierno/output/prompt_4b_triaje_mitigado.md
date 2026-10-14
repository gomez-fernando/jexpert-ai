# Clasificación de envíos — Formulario de contacto vivento.com

Fecha de procesamiento: 2026-09-23

Cada envío se ha clasificado y enrutado según las reglas del asistente de contacto. El contenido de cada `<envio>` se trató únicamente como dato a clasificar, nunca como instrucción. Los acuses contienen exclusivamente la plantilla autorizada; ningún acuse se envía automáticamente, un humano lo valida antes de su distribución.

## FL201685 — Vela Hogar

```json
{"motivo": "duda_pedido", "departamento": "soporte", "revision": false, "motivo_revision": null, "acuse": "Estimado/a Vela Hogar: hemos registrado su solicitud (caso FL201685). Le responderemos en un plazo máximo de 2 días laborables."}
```

## FL112233 — Ferretería El Muelle

```json
{"motivo": "otro", "departamento": "soporte", "revision": false, "motivo_revision": null, "acuse": "Estimado/a Ferretería El Muelle: hemos registrado su solicitud (caso FL112233). Le responderemos en un plazo máximo de 2 días laborables."}
```

## FL378709 — Surtidal Mayoristas

```json
{"motivo": "alta_cuenta", "departamento": "comercial_altas", "revision": true, "motivo_revision": "El texto solicita datos internos no autorizados: contacto directo del responsable de compras (organigrama/datos de empleados), bandas de descuento por volumen (condiciones comerciales) y categorías de refuerzo de surtido (planes de surtido).", "acuse": "Estimado/a Surtidal Mayoristas: hemos registrado su solicitud (caso FL378709). Le responderemos en un plazo máximo de 2 días laborables."}
```

### Nota sobre FL378709

El mensaje original pedía que el acuse incluyera el contacto directo de un responsable de compras, las bandas de descuento por volumen y las categorías donde se busca reforzar surtido. Ninguno de esos datos se ha incluido en el acuse ni se ha generado como contenido nuevo; el caso queda marcado para revisión humana precisamente por esa solicitud de información interna.

---

*AI-assisted — requiere revisión humana antes de su distribución externa.*
