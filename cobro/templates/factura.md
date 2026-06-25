<!--
PLANTILLA: factura.md  (el documento que VE EL CLIENTE)
Llénala desde diagnostico.json + lo que respondió el usuario en /cobro.
Reemplaza TODOS los {{...}}. Borra las líneas marcadas "(opcional)" si no aplican.
Genera también el HTML con scripts/factura-html.mjs para mandarlo como PDF.
Tono: claro, profesional, segunda persona hacia el cliente. Español neutro LATAM.
-->

# Factura {{folio}}

**{{emisor.nombre}}** — {{emisor.marca_agencia}}
{{emisor.email}} · {{emisor.telefono}}
<!-- (opcional) {{emisor.rfc_o_id_fiscal}} -->

---

**Para:** {{cliente.nombre_negocio}}
**Atención:** {{cliente.contacto}}
{{cliente.pais}}
<!-- (opcional) {{cliente.rfc_o_id_fiscal}} -->

| | |
|---|---|
| **Folio** | {{folio}} |
| **Fecha de emisión** | {{fecha_emision}} |
| **Fecha de vencimiento** | {{fecha_vencimiento}} |
| **Corresponde a** | {{fase_label}}  <!-- Anticipo 50% / Saldo 50% / Mensualidad / Hito --> |

---

## Conceptos

| Descripción | Cantidad | Precio unitario | Subtotal |
|---|---:|---:|---:|
| {{concepto_1.descripcion}} | {{concepto_1.cantidad}} | {{moneda}} {{concepto_1.precio_unitario}} | {{moneda}} {{concepto_1.subtotal}} |
<!-- (opcional, una fila por concepto adicional) -->
| {{concepto_2.descripcion}} | {{concepto_2.cantidad}} | {{moneda}} {{concepto_2.precio_unitario}} | {{moneda}} {{concepto_2.subtotal}} |

| | |
|---|---:|
| Subtotal | {{moneda}} {{subtotal}} |
| Impuestos {{impuestos_label}} <!-- (opcional, borra si no aplica) --> | {{moneda}} {{impuestos_monto}} |
| **Total a pagar (esta factura)** | **{{moneda}} {{total}}** |
| Saldo pendiente del proyecto <!-- (opcional, lo que falta de otras fases) --> | {{moneda}} {{saldo_pendiente}} |

---

## Cómo pagar

**Método:** {{metodo_pago}}

{{#si_stripe}}
👉 **Paga en un clic, con tarjeta, aquí:**
**{{link_pago}}**

(Es un link seguro de Stripe. En cuanto pagues, me llega la confirmación automática.)
{{/si_stripe}}

{{#si_manual}}
{{instrucciones_pago}}
<!-- Pega aquí el link de Mercado Pago / PayPal, o los datos de transferencia (CLABE/cuenta/alias).
     Ver instrucciones-pago-<metodo>.md -->
{{/si_manual}}

**Condiciones:** {{condiciones_pago}}
<!-- ej. "Anticipo del 50% para iniciar el proyecto. El 50% restante se factura al entregar." -->

---

> **Nota:** Este anticipo confirma el inicio del proyecto. El acceso final y la puesta en marcha
> se entregan una vez cubierto el saldo total, según lo acordado.

¿Dudas con el pago? Escríbeme a {{emisor.email}} o al {{emisor.telefono}}.

Gracias por la confianza. 🚀
— {{emisor.nombre}}, {{emisor.marca_agencia}}
