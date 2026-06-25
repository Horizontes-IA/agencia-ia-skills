# CONTRATO DE PRESTACIÓN DE SERVICIOS DE AUTOMATIZACIÓN CON IA

<!--
INSTRUCCIONES DE LLENADO (borra este bloque al entregar):
- Reemplaza TODO lo que está {{entre llaves dobles}} con los datos reales del trato.
- Si un campo no aplica, NO lo dejes en blanco: bórralo o pon "No aplica".
- Bloques [[OPCIONAL: ...]] se incluyen solo si aplica al trato; si no, bórralos completos.
- El Anexo A (alcance) se autollena del diagnostico.json/propuesta si existen.
- Disclaimer final: NO lo borres. Es un modelo, no asesoría legal.
-->

**Folio:** {{FOLIO}} · **Fecha:** {{FECHA}} · **Lugar:** {{CIUDAD_PAIS}}

---

## 1. Partes

Este Contrato de Prestación de Servicios (el **"Contrato"**) se celebra entre:

- **El Proveedor:** {{NOMBRE_LEGAL_AGENCIA}}, con identificación fiscal {{RFC_NIT_RUC_CEDULA}}, domicilio en {{DOMICILIO_AGENCIA}}, representado por {{REPRESENTANTE_AGENCIA}} (en adelante, el **"Proveedor"**).

- **El Cliente:** {{NOMBRE_LEGAL_CLIENTE}}, con identificación fiscal {{RFC_NIT_RUC_CEDULA_CLIENTE}}, domicilio en {{DOMICILIO_CLIENTE}}, representado por {{REPRESENTANTE_CLIENTE}} (en adelante, el **"Cliente"**).

Ambas partes pueden ser referidas individualmente como una **"Parte"** y conjuntamente como las **"Partes"**.

## 2. Objeto y naturaleza de la relación

El Proveedor prestará al Cliente servicios profesionales de **diseño, construcción, configuración y puesta en marcha de sistemas de automatización con inteligencia artificial** (los **"Servicios"**), conforme al alcance descrito en el **Anexo A**.

Las Partes reconocen y aceptan que este es un contrato de **prestación de servicios profesionales independientes**. **No existe relación laboral, de subordinación, ni de dependencia** entre el Proveedor y el Cliente. El Proveedor presta sus Servicios con plena autonomía técnica y de horario, con sus propios medios, y es responsable de sus propias obligaciones fiscales y de seguridad social.

## 3. Alcance de los Servicios

El alcance específico, los entregables, las revisiones incluidas y los límites del trabajo se detallan en el **Anexo A — Alcance del Trabajo**, que forma parte integral de este Contrato.

Cualquier trabajo, automatización, integración o funcionalidad que **no esté expresamente listado en el Anexo A** se considera **fuera de alcance** y requiere una **Orden de Cambio** por escrito (cláusula 6) con su correspondiente ajuste de precio y plazo.

## 4. Entregables y plazos

El Proveedor entregará lo descrito en el Anexo A conforme al siguiente calendario de hitos:

| Hito | Entregable | Plazo estimado |
|---|---|---|
| 1 — Inicio | {{HITO_1}} | {{PLAZO_1}} |
| 2 — Entrega/Revisión | {{HITO_2}} | {{PLAZO_2}} |
| 3 — Puesta en marcha (go-live) | {{HITO_3}} | {{PLAZO_3}} |

Los plazos son estimados de buena fe y **se pausan automáticamente** mientras el Proveedor esté esperando información, accesos, aprobaciones o pagos por parte del Cliente. El tiempo de espera del lado del Cliente no cuenta contra los plazos del Proveedor.

## 5. Precio, forma de pago y pago tardío

**5.1 Precio.** El precio total por los Servicios del Anexo A es de **{{MONEDA}} {{PRECIO_TOTAL}}** ({{PRECIO_TOTAL_LETRA}}).

**5.2 Estructura de pago por hitos.** El precio se paga así:

| Pago | Momento | Porcentaje | Monto |
|---|---|---|---|
| Anticipo | Al firmar este Contrato (antes de iniciar) | {{PCT_ANTICIPO}} % | {{MONEDA}} {{MONTO_ANTICIPO}} |
| Hito de entrega | Al entregar para revisión | {{PCT_ENTREGA}} % | {{MONEDA}} {{MONTO_ENTREGA}} |
| Puesta en marcha | Al go-live / aprobación final | {{PCT_GOLIVE}} % | {{MONEDA}} {{MONTO_GOLIVE}} |

> Estructura recomendada por el mercado para este tipo de proyecto: **30/40/30** (o **50/50** en proyectos chicos). El Proveedor **no inicia trabajo hasta recibir el anticipo**. La entrega final / accesos de producción se liberan **contra el pago del saldo**.

**5.3 Moneda y método.** Los pagos se realizan en **{{MONEDA}}** vía **{{METODO_PAGO}}** (por ejemplo, link de pago, transferencia o Wise). Las comisiones de la pasarela y los impuestos aplicables corren por cuenta de **{{QUIEN_ABSORBE_COMISIONES}}**.

**5.4 Pago tardío.** Si el Cliente no paga un monto vencido en la fecha acordada, se aplicará un recargo de **{{RECARGO_MORA}}** (por ejemplo, 1% por día de retraso o un % mensual sobre el saldo). Adicionalmente, transcurridos **{{DIAS_PAUSA}} días** de retraso, el Proveedor podrá **pausar la prestación del servicio y el mantenimiento** hasta que el pago se regularice, sin que ello constituya incumplimiento del Proveedor.

## 6. Órdenes de cambio y revisiones

**6.1 Revisiones incluidas.** El Anexo A incluye **{{NUM_REVISIONES}}** ronda(s) de revisión sobre cada entregable. Revisiones adicionales se cotizan por separado.

**6.2 Órdenes de cambio.** Todo cambio de alcance, función nueva o ajuste que vaya más allá de lo pactado en el Anexo A se documenta en una **Orden de Cambio escrita** (puede ser por correo o mensaje, con confirmación de ambas Partes) que especifique el trabajo adicional, el precio adicional y el nuevo plazo. **Ningún cambio de alcance se ejecuta sin Orden de Cambio aprobada por escrito.** Los acuerdos verbales no obligan a ninguna Parte.

## 7. Costos de herramientas, APIs y suscripciones

**7.1 Cuentas a nombre del Cliente.** Los servicios de terceros que consume la automatización (por ejemplo: OpenAI/Anthropic, n8n/Make, Twilio/WhatsApp, Cloudflare, Composio, bases de datos) se contratan **a nombre del Cliente y con su medio de pago**. Estos costos **NO están incluidos** en el precio de la cláusula 5 y son responsabilidad del Cliente.

**7.2 Naturaleza variable del consumo.** El Cliente entiende que el costo de las APIs de IA se cobra **por uso** (llamadas / tokens) y, por tanto, **es variable** y depende del volumen real de operación.

**7.3 Tope de uso y sobreconsumo.** Las Partes acuerdan un tope estimado de consumo de **{{TOPE_USO}}** (por ejemplo, {{TOPE_USO_DETALLE}}). Si el uso real supera ese tope de forma sostenida, el Proveedor lo notificará y las Partes acordarán por escrito el ajuste correspondiente. El Proveedor **no es responsable** por sobrecostos derivados de un volumen de uso superior al estimado.

## 8. Propiedad intelectual

**8.1 Entregable final — del Cliente, tras el pago completo.** Una vez que el Cliente haya **pagado la totalidad** del precio acordado, los entregables finales construidos específicamente para el Cliente (configuraciones, flujos y código a la medida descritos en el Anexo A) le pertenecen de forma exclusiva. **La propiedad intelectual NO se transfiere hasta que el pago esté completo**; mientras haya saldo pendiente, el Proveedor retiene la titularidad de lo entregado.

**8.2 Herramientas preexistentes del Proveedor — del Proveedor.** El Proveedor **retiene la propiedad** de sus herramientas, plantillas, metodologías, librerías de prompts, componentes reutilizables y flujos (workflows) **preexistentes o de uso general** que utilice para prestar los Servicios. Sobre estos, el Proveedor otorga al Cliente una **licencia de uso** no exclusiva, perpetua e intransferible, limitada a operar la solución contratada. El Cliente no adquiere la propiedad de la "caja de herramientas" del Proveedor.

**8.3 Derechos morales.** El reconocimiento de autoría (derechos morales) es **irrenunciable** conforme a la legislación aplicable y permanece con su autor; la cesión de la cláusula 8.1 es **{{TIPO_CESION}}** (total o parcial), con alcance territorial **{{TERRITORIO_CESION}}** y duración **{{DURACION_CESION}}**.

## 9. Confidencialidad

Cada Parte se obliga a **no divulgar ni usar para fines ajenos a este Contrato** la información confidencial de la otra (datos de negocio, clientes, precios, métodos, prompts, código, accesos y cualquier información marcada o razonablemente entendible como confidencial).

Esta obligación **subsiste por {{PLAZO_CONFIDENCIALIDAD}}** (típico: 2 a 3 años) después de terminada la relación. Tratándose de **secretos comerciales**, la obligación es **indefinida** mientras la información siga siendo secreta y valiosa. La confidencialidad es **mutua**: aplica por igual al Proveedor y al Cliente.

## 10. Accesos a sistemas y manejo de datos

**10.1 Acceso por autorización revocable.** Para operar la automatización, el Proveedor accederá a sistemas y datos del Cliente (por ejemplo: correo, CRM, WhatsApp, hojas de cálculo). Estos accesos se otorgan mediante **autorización segura y revocable (OAuth, gestionada con Composio)** — el Cliente **autoriza con un clic y NO entrega contraseñas**.

**10.2 Uso limitado.** El Proveedor usará los accesos **únicamente para construir y operar la automatización contratada**, y para ningún otro fin.

**10.3 Roles bajo ley de datos.** Para efectos de la legislación de protección de datos aplicable, el **Cliente actúa como responsable/controlador** de los datos personales y el **Proveedor como encargado/procesador**, tratando los datos solo según las instrucciones del Cliente.

**10.4 Seguridad y borrado.** El Proveedor mantendrá los accesos y credenciales de forma segura y **aislados**. El Cliente **puede revocar cualquier acceso en cualquier momento**. **Al terminar este Contrato, el Proveedor ejecutará la revocación de todos los accesos** (`node connect.mjs revoke <cliente> <app>`) y **borrará** las credenciales y datos del Cliente que estén en su poder, salvo lo que deba conservar por obligación legal.

## 11. No entrenamiento de modelos con datos del Cliente

El Proveedor **no entrenará ni afinará (fine-tune) ningún modelo de IA con los datos del Cliente** sin su aprobación previa y por escrito. Cuando la automatización envíe datos a APIs de terceros (por ejemplo, OpenAI o Anthropic), lo hará bajo los términos de dichos proveedores, que **no utilizan los datos enviados por API para entrenar sus modelos**.

## 12. Descargo sobre resultados de IA (uso aceptable)

**12.1 Outputs probabilísticos.** El Cliente reconoce que los sistemas de IA producen resultados **probabilísticos**: pueden contener errores o "alucinaciones" (respuestas que parecen correctas pero no lo son). El Proveedor entrega la automatización **funcionando**, pero **no garantiza que la IA nunca se equivoque**.

**12.2 Revisión humana.** Los resultados generados por la IA **requieren revisión humana antes de cualquier uso de consecuencias**. El Cliente es responsable de revisar los resultados antes de actuar sobre ellos.

**12.3 Uso aceptable.** La automatización **no debe usarse para tomar decisiones automáticas de alto impacto sin revisión humana** (por ejemplo: contratación, otorgamiento de crédito, decisiones médicas o legales). El Proveedor no es responsable por el uso que el Cliente dé a los resultados fuera de este marco.

**12.4 Sin garantía de resultados específicos.** El Proveedor entrega la solución operando según el Anexo A. No garantiza métricas de negocio específicas (ventas, leads, ahorro) que dependan de factores fuera de su control.

[[OPCIONAL: incluir solo si hay retainer/mantenimiento contratado]]
## 13. Mantenimiento y soporte (retainer)

**13.1 Servicio continuo.** A partir del go-live, el Proveedor prestará un servicio de mantenimiento por **{{MONEDA}} {{MONTO_RETAINER}} / mes**, cobrado **por adelantado al inicio de cada mes**.

**13.2 Qué incluye.** {{ALCANCE_RETAINER}} (por ejemplo: monitoreo, corrección de errores, ajuste de prompts/flujos, actualización de modelos, pequeños ajustes y el reporte mensual).

**13.3 Qué NO incluye.** Funciones nuevas o automatizaciones adicionales **no** están incluidas en el retainer y se tratan como Orden de Cambio (cláusula 6).

**13.4 Vigencia y cancelación.** El retainer es mensual y renovable. Cualquier Parte puede cancelarlo con **{{AVISO_CANCELACION_RETAINER}}** de aviso por escrito.
[[/OPCIONAL]]

## 14. Limitación de responsabilidad

La responsabilidad total del Proveedor frente al Cliente por cualquier reclamo derivado de este Contrato **se limita al monto total efectivamente pagado por el Cliente** por los Servicios. **En ningún caso** el Proveedor será responsable por **daños indirectos, incidentales, especiales o consecuenciales** (por ejemplo, lucro cesante o pérdida de datos por causas ajenas al Proveedor).

Esta limitación **no aplica** a los casos en que la ley no permita limitarla, como el **dolo o la negligencia grave** del Proveedor.

## 15. Indemnización

Cada Parte indemnizará y mantendrá libre de daño a la otra frente a reclamos de terceros derivados de **su propio incumplimiento, negligencia o violación de la ley**. En particular, el Cliente responde por la **licitud de los datos y del uso** que da a la automatización, y el Proveedor por **infracciones de propiedad intelectual** atribuibles al trabajo que él construyó.

## 16. Terminación

**16.1 Por aviso.** Cualquier Parte puede terminar este Contrato con **{{AVISO_TERMINACION}}** (típico: 15 a 30 días) de aviso por escrito.

**16.2 Por incumplimiento.** Cualquier Parte puede terminar de forma **inmediata** si la otra incurre en incumplimiento grave y no lo subsana dentro de **{{DIAS_SUBSANAR}} días** de habérsele notificado.

**16.3 Cargo por cancelación (kill fee).** Si el Cliente cancela el proyecto cuando ya está en curso, **pagará el trabajo realizado hasta la fecha** más un cargo por cancelación de **{{KILL_FEE}}** (por ejemplo, el % del hito en curso). El anticipo **no es reembolsable**.

**16.4 Efectos.** Al terminar: (a) el Cliente paga lo devengado; (b) el Proveedor entrega lo construido **si el saldo está cubierto**; (c) el Proveedor **revoca todos los accesos y borra los datos** del Cliente (cláusula 10.4).

## 17. Ley aplicable y resolución de disputas

Este Contrato se rige por las leyes de **{{JURISDICCION}}**. Ante cualquier controversia, las Partes intentarán resolverla de **buena fe** mediante negociación directa; si no llegan a acuerdo en **{{DIAS_NEGOCIACION}} días**, se someterán a **{{MECANISMO_DISPUTA}}** (mediación y, en su caso, arbitraje vinculante en {{SEDE_ARBITRAJE}}, más rápido y económico que un juicio).

## 18. Disposiciones generales

- **Acuerdo íntegro:** este Contrato y sus Anexos son el acuerdo completo entre las Partes y sustituyen cualquier acuerdo previo.
- **Modificaciones:** solo por escrito firmado por ambas Partes.
- **Independencia de cláusulas:** si una cláusula resulta inválida, las demás siguen vigentes.
- **Cesión:** ninguna Parte puede ceder este Contrato sin consentimiento escrito de la otra.
- **Notificaciones:** se hacen a los correos {{CORREO_AGENCIA}} y {{CORREO_CLIENTE}}.

## 19. Anexos

- **Anexo A — Alcance del Trabajo** (entregables, automatizaciones, revisiones y lo que NO incluye).
[[OPCIONAL: — **Anexo B — Propuesta/Cotización del {{FECHA_PROPUESTA}}** (referencia de precio y alcance comercial).]]

---

## Firmas

Las Partes manifiestan que han leído y entendido este Contrato y lo firman de conformidad.

| El Proveedor | El Cliente |
|---|---|
| | |
| Firma | Firma |
| {{REPRESENTANTE_AGENCIA}} | {{REPRESENTANTE_CLIENTE}} |
| {{NOMBRE_LEGAL_AGENCIA}} | {{NOMBRE_LEGAL_CLIENTE}} |
| Fecha: ____________ | Fecha: ____________ |

---

> **Aviso importante — esto no es asesoría legal.** Este documento es un **modelo de trabajo** preparado como punto de partida, no constituye asesoría jurídica. Las leyes de prestación de servicios, propiedad intelectual y protección de datos **varían según el país**. Para tratos de monto alto o de riesgo elevado, **haz que un abogado de tu país lo revise** antes de firmar.
