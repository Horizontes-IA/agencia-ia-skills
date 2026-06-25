<!--
PLANTILLA: recordatorios-pago.md
La cadena educada que escala si el cliente se atrasa con el pago.
El usuario copia/pega el mensaje del día que toca y reemplaza {{...}}.
Cadencia y tono vienen de la investigación (agencias reales). Mantén el tono cordial pero firme.
-->

# Recordatorios de pago — {{cliente.nombre_negocio}} ({{folio}})

> **Tu mejor defensa es el anticipo.** Con 50/50 nunca entregas sin haber cobrado la mitad,
> así que el riesgo máximo es el saldo. **No liberes el acceso/puesta en marcha final hasta que el saldo entre.**
> Si firmaron contrato (`/contrato`), ahí está el recargo por mora y la pausa de servicio — cítalo si toca.

Monto pendiente: **{{moneda}} {{total}}** · Venció: **{{fecha_vencimiento}}**
Link de pago: **{{link_pago}}**

---

## 1) Día del vencimiento — recordatorio amable

> Hola {{cliente.contacto}} 👋 Te paso un recordatorio rápido: hoy es la fecha de tu {{fase_label}}
> de **{{moneda}} {{total}}** para arrancar/continuar con {{cliente.nombre_negocio}}.
> Aquí está el link para pagar en un clic: {{link_pago}}
> Cualquier duda me dices. ¡Gracias!

---

## 2) +3 días — seguimiento suave

> Hola {{cliente.contacto}}, ¿todo bien? Vi que aún no entra el pago de la {{fase_label}}.
> ¿Hubo algún problema con el link o prefieres otro método (transferencia, Mercado Pago)?
> Apenas se cubra, sigo avanzando. Link: {{link_pago}}

---

## 3) +7 días — recordatorio firme

> Hola {{cliente.contacto}}, te escribo para regularizar el pago de la {{fase_label}}
> (**{{moneda}} {{total}}**), que sigue pendiente desde el {{fecha_vencimiento}}.
> Para poder mantener/avanzar el proyecto necesito cerrar este punto. Si ya lo enviaste,
> mándame el comprobante; si no, aquí está el link: {{link_pago}}
> Quedo atento para no tener que pausar el servicio.

---

## 4) +14 días — pausa de servicio

> Hola {{cliente.contacto}}, no he recibido el pago de la {{fase_label}} pese a los recordatorios.
> A partir de hoy **pauso el monitoreo/avance** hasta regularizar el pago, según lo acordado.
> En cuanto se cubra reactivo todo de inmediato. Link: {{link_pago}}
> Si hay algo que deba saber de tu lado, con gusto lo platicamos.

---

### Notas para ti (no se las mandes al cliente)
- Manda los recordatorios **uno por uno**, en el día que toca. No spamees.
- Para el **retainer**, lo ideal es **cobro recurrente automático** (suscripción Stripe): casi nunca llegas a esta cadena.
- Si tras +14 días no paga y firmaron contrato, aplica la cláusula de mora/terminación. Si no hubo anticipo (no debió pasar), aprende: la próxima, **anticipo primero**.
