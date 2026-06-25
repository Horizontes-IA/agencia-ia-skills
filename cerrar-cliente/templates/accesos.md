# Accesos del cliente — {{NOMBRE_NEGOCIO}}

> Resumen de las cuentas que el cliente debe conectar para construir su sistema.
> Generado con `/conectar-cliente` (Composio OAuth): el cliente da **1 clic y autoriza con su propia
> cuenta**, sin pasarte contraseñas y sin pelear con 2FA / Google sign-on. Revocable cuando termine el trato.
> Para Claude: llena la tabla con los links reales que devolvió `connect.mjs`. NUNCA pegues la API key ni IDs internos.

- **userId del cliente (la llave de todas sus conexiones):** `{{USER_ID_CLIENTE}}`
- **Comando base:** `node ~/.claude/skills/conectar-cliente/connect.mjs link {{USER_ID_CLIENTE}} <app>`

## Cuentas a conectar (del alcance)

| App | Para qué la necesito | Link para el cliente | Estado |
|---|---|---|---|
| {{APP_1}} | {{PARA_QUE_1}} | {{LINK_1}} | ⏳ pendiente |
| {{APP_2}} | {{PARA_QUE_2}} | {{LINK_2}} | ⏳ pendiente |
| {{APP_3}} | {{PARA_QUE_3}} | {{LINK_3}} | ⏳ pendiente |

> Estado: ⏳ pendiente · ✅ conectado. Verifica con:
> `node ~/.claude/skills/conectar-cliente/connect.mjs estado {{USER_ID_CLIENTE}} <app>`
> o lista todo lo conectado con: `... apps {{USER_ID_CLIENTE}}`

## Mensaje listo para mandar al cliente

> (Va dentro del mensaje de kickoff, sección "Lo único que necesito de tu lado". Aquí queda por si lo
> mandas suelto.)

Hola {{NOMBRE_CONTACTO_CLIENTE}}, para construir tu sistema necesito conectar estas cuentas.
No me pasas contraseñas: das un clic y autorizas tú con tu propia cuenta (seguro y revocable).

{{LISTA_DE_LINKS_BULLET}}

Con eso me destrabas todo. Si alguno te marca algo raro, mándame captura y lo vemos.

## Al terminar el trato (offboarding)

Cuando el proyecto cierre (o el cliente cancele el retainer), revoca los accesos y borra datos:

```bash
node ~/.claude/skills/conectar-cliente/connect.mjs revoke {{USER_ID_CLIENTE}} <app>
```

(Esto está atado a la cláusula de accesos del contrato: al terminar, se revoca y se borran datos.)
