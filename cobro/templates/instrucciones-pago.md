<!--
PLANTILLA: instrucciones-pago.md
Úsala SOLO cuando el método NO es Stripe (Stripe se automatiza con el script).
Deja el bloque del método elegido y borra los demás. El usuario PEGA aquí su link/datos reales.
Estos son los pasos para que el USUARIO genere el cobro en su propia cuenta, y el texto
que el cliente verá embebido en la factura.
-->

# Cómo cobrar — {{cliente.nombre_negocio}} ({{fase_label}})

Monto a cobrar: **{{moneda}} {{total}}**

---

## Opción A — Mercado Pago (cliente local, paga en moneda local)

**Comisión:** ~3.79% + fijo. Aceptación máxima en AR, BR, CL, CO, MX, UY, PE.

Pasos para generar el link (en tu cuenta de Mercado Pago):
1. Entra a tu panel de Mercado Pago → **"Cobrar"** / **"Link de pago"** (también: *Tu negocio → Links de pago*).
2. Elige **"Crear link de pago"** y pon el monto **{{moneda}} {{total}}** y una descripción: *"{{fase_label}} — {{concepto_1.descripcion}}"*.
3. Genera el link y **cópialo**.
4. Pégalo en la factura (campo `{{link_pago}}`) y mándaselo al cliente.

> Pega aquí el link generado:
> **PEGA_TU_LINK_DE_MERCADO_PAGO**

---

## Opción B — PayPal (último recurso / el cliente solo tiene PayPal)

**Comisión:** ~6.5%–8.4% (la más cara). Ojo con retenciones/congelamientos.

Pasos:
1. Usa tu link de **PayPal.Me**: `paypal.me/{{paypal_usuario}}/{{total}}` — abre directo con el monto.
2. **O** desde la app/web: **"Enviar y solicitar" → "Solicitar"** → email del cliente → monto **{{moneda}} {{total}}**.
3. Manda el link/solicitud al cliente.

> Pega aquí el link:
> **PEGA_TU_LINK_DE_PAYPAL**

⚠️ Si vas a recibir USD viviendo en LATAM, considera mejor Stripe + retirar a **Wise** (mucha menos comisión).

---

## Opción C — Transferencia directa / SPEI (MX) / PIX (BR)

**Comisión:** ~0%. Mejor para cliente que ya confía y montos grandes. Sin link automático.

Pon estos datos en la factura y pídele al cliente que te mande el comprobante:

| Dato | Valor |
|---|---|
| Banco | {{banco}} |
| Titular | {{emisor.nombre}} |
| {{tipo_cuenta_label}} <!-- CLABE / N.º de cuenta / Alias / CBU / PIX key --> | {{numero_cuenta}} |
| Referencia / concepto | {{folio}} — {{fase_label}} |

> Pídele al cliente: *"En cuanto hagas la transferencia, mándame el comprobante por aquí y te confirmo."*
> No liberes accesos/entrega hasta confirmar que el dinero entró.

---

## Para recibir/convertir el dinero (cualquier método): Wise

Si cobras en USD y vives en LATAM, el patrón barato es: **cobras (Stripe/PayPal) → retiras a Wise → conviertes a tu moneda local a tasa real** (comisión 0.35%–2%, sin markup). Wise **no** es para cobrarle con tarjeta al cliente; es para mover/convertir tu dinero.
