# Docker Compose y Orquestación — Explicación de la Sesión

> Este documento explica, en lenguaje sencillo, de qué trató la sesión de esta semana,
> qué significa cada término nuevo, y cómo se aplicó todo eso a tu proyecto (pms-properties).

---

## 1. ¿De qué trató esta sesión, en una frase?

Hasta la semana pasada aprendiste a meter **un** servicio dentro de **un** contenedor Docker.
Esta semana el problema cambió: tu sistema no tiene un solo contenedor, tiene **varios** (tres
microservicios + tres bases de datos), y esos contenedores necesitan:

1. Arrancar en el orden correcto.
2. Saber "encontrarse" entre sí (hablarse sin usar IPs fijas).
3. Saber cuándo el otro **realmente** está listo para recibir peticiones (no solo "encendido").
4. Comportarse distinto en tu computador (desarrollo) que en un servidor real (producción).

Docker Compose es la herramienta que resuelve estos cuatro problemas para un sistema que corre
en una sola máquina. Esta sesión te enseña a usarla bien, no solo a que "funcione".

---

## 2. Explicación de los términos nuevos

### Contenedor
Ya lo conoces de la semana pasada: es una "cajita" que empaqueta tu aplicación con todo lo que
necesita para correr, de forma idéntica en cualquier computador.

### Servicio (en Docker Compose)
Es la definición de **un** contenedor dentro del archivo `docker-compose.yml`. Por ejemplo,
`booking-service` es un "servicio" que Compose sabe cómo construir y levantar. Un servicio no es
lo mismo que un contenedor: el servicio es la *receta declarada en el archivo*, el contenedor es
la instancia que realmente corre cuando ejecutas `docker-compose up`.

### Red compartida (network)
Todos los contenedores de tu sistema necesitan estar "conectados" entre sí para poder hablarse.
Docker Compose crea automáticamente una red privada (en tu proyecto se llama `pmsnet`) donde
todos los servicios pueden verse.

### DNS por nombre de servicio
Es la forma en que los contenedores se encuentran dentro de esa red. En vez de que
`booking-service` tenga que saber la dirección IP exacta de `booking-db` (que además cambia
cada vez que reinicias los contenedores), simplemente le habla por su **nombre**:
`booking-db:5432`. Docker traduce ese nombre a la IP correcta automáticamente, como si fuera
una libreta de contactos interna.

### `depends_on`
Es una instrucción dentro de `docker-compose.yml` que le dice a Docker "arranca primero este
otro contenedor, antes que yo". El problema (y la razón de toda esta sesión) es que
`depends_on` **por sí solo solo garantiza el orden de encendido, no que el otro contenedor ya
esté listo para trabajar**.

### Healthcheck (comprobación de salud)
Es un comando que Docker ejecuta periódicamente *dentro* de un contenedor para preguntarle
"¿ya estás realmente listo?" — no solo "¿ya arrancaste?". Por ejemplo, para una base de datos
PostgreSQL, el comando `pg_isready` verifica que la base de datos ya puede aceptar conexiones,
no solo que el proceso está corriendo.

### `condition: service_healthy`
Es la combinación de las dos anteriores: le dice a Docker "no arranques este servicio hasta que
el otro no solo haya *iniciado*, sino que su healthcheck confirme que está *sano/listo*". Esta es
la corrección real al problema de `depends_on`.

### Volumen
Es un espacio de almacenamiento fuera del contenedor donde vive la información permanente (como
los datos de una base de datos). Los contenedores son "desechables" — se pueden borrar y
recrear en cualquier momento — pero los volúmenes sobreviven a eso. Por eso, aunque hagas
`docker-compose down` y vuelvas a levantar todo, tus datos siguen ahí.

### Archivo base + overrides por entorno
En vez de tener un solo `docker-compose.yml` gigante que editas a mano cada vez que pasas de tu
computador (desarrollo) a un servidor real (producción), se usan archivos adicionales que
*sobrescriben* o *añaden* configuración encima del archivo base:
- `docker-compose.override.yml` se aplica **automáticamente** cuando corres `docker-compose up`
  sin nada más — pensado para desarrollo local.
- `compose.prod.yml` se aplica solo si lo pides explícitamente
  (`docker-compose -f docker-compose.yml -f compose.prod.yml up`) — pensado para producción.

### Orquestador (ej. Kubernetes)
Docker Compose funciona muy bien mientras todo corre en **una sola máquina**. Un orquestador
entra en juego cuando tu sistema crece tanto que necesitas repartirlo entre **varios
servidores**, con capacidades como reiniciar automáticamente un contenedor que se cayó,
actualizar servicios sin tumbar el sistema, o crecer automáticamente cuando hay más tráfico.
Kubernetes es el orquestador más conocido. Esta semana **no** lo implementamos — solo se
explicó como el siguiente paso lógico cuando Compose ya no alcanza.

---

## 3. El problema central de la semana, explicado con una analogía

Imagina que `booking-service` es un cocinero, y `booking-db` es el mercado donde compra los
ingredientes.

- **Con solo `depends_on` (como estaba tu proyecto antes):** el cocinero sale de su casa apenas
  ve que el mercado *abrió la puerta* — pero el mercado todavía está acomodando las cajas, no
  hay nada en los estantes. El cocinero llega, no encuentra nada, y su día falla.

- **Con `depends_on: condition: service_healthy` (lo que hicimos esta semana):** el cocinero
  espera una señal específica — "ya está todo acomodado, puedes entrar a comprar" — antes de
  salir de su casa. Esa señal es el healthcheck.

Esto explica por qué tu `docker-compose.yml` de la semana pasada podía fallar de forma
**inconsistente**: a veces el mercado (la base de datos) se acomodaba rápido y todo funcionaba
por pura suerte; otras veces (especialmente en un entorno más lento, como en integración
continua) el cocinero llegaba antes de tiempo y todo el sistema fallaba al arrancar.

---

## 4. Cómo se aplicó todo esto a pms-properties

### Antes (semana pasada)

Tu `docker-compose.yml` tenía esto:

```yaml
booking-service:
  depends_on:
    - booking-db
```

Esto solo le decía a Docker "arranca `booking-db` antes que `booking-service`" — pero no
verificaba que `booking-db` ya pudiera aceptar conexiones. Era exactamente el error que la
sesión describe como "un camino que recorrerás en la vida real": funciona en tu computador
(porque tu base de datos suele arrancar rápido), pero falla de forma random en otro entorno.

### Ahora (esta semana)

Le agregamos un `healthcheck` real a cada base de datos:

```yaml
booking-db:
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U ${BOOKING_DB_USER}"]
    interval: 5s
    timeout: 5s
    retries: 5
```

Y cambiamos `depends_on` para que espere esa señal de salud, no solo el arranque:

```yaml
booking-service:
  depends_on:
    booking-db:
      condition: service_healthy
```

Hicimos exactamente lo mismo para `payment-db`/`payment-service` (con `pg_isready`, porque
también es PostgreSQL) y para `catalog-db`/`catalog-service` (con `mongosh --eval
"db.adminCommand('ping')"`, porque esa base de datos es MongoDB, no PostgreSQL — el comando de
verificación cambia según el motor de base de datos).

También le agregamos un healthcheck a cada **microservicio**, no solo a las bases de datos,
reutilizando el endpoint `/health` que ya habías construido en la Semana 04 (el "esqueleto
andante"):

```yaml
booking-service:
  healthcheck:
    test: ["CMD-SHELL", "curl -f http://localhost:8081/health || exit 1"]
```

Esto es útil para etapas futuras: si en algún momento tienes varias instancias de
`booking-service`, o si otro sistema necesita saber si tu servicio está sano, ya tienes esa
respuesta lista.

### Separación por entornos

Creamos `docker-compose.override.yml` para que, cuando tú o tus compañeros simplemente corran
`docker-compose up` en su computador, el sistema arranque automáticamente en modo desarrollo
(`SPRING_PROFILES_ACTIVE=dev`).

Y creamos `compose.prod.yml` como un archivo aparte, que **nadie ejecuta sin querer** — solo se
activa si explícitamente se pide con `-f compose.prod.yml`, y ahí configuramos cosas propias de
producción, como límites de memoria por contenedor. Las contraseñas y credenciales, en ambos
casos, siguen viniendo del `.env` — nunca se escriben directamente en estos archivos.

### Un detalle técnico que tuvimos que resolver

El healthcheck de cada microservicio usa el comando `curl` para preguntarle a su propio
endpoint `/health` si está vivo. El problema es que la imagen base que usábamos
(`eclipse-temurin:21-jre`) no trae `curl` instalado por defecto — así que tuvimos que agregar
esta línea al `Dockerfile` de cada servicio:

```dockerfile
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
```

Esto instala `curl`, lo usa, y luego borra los archivos temporales de instalación para que la
imagen final siga siendo pequeña (recuerda el principio de la Semana 05: imágenes pequeñas,
sin herramientas innecesarias).

---

## 5. Cómo se ve el resultado, en la práctica

Cuando ejecutas `docker-compose up --build` ahora, el comportamiento correcto que debes ver es:

1. Arrancan primero `booking-db`, `payment-db`, `catalog-db`.
2. Docker espera y verifica, cada pocos segundos, que cada una responda "estoy sana" mediante
   su healthcheck.
3. **Solo cuando** las tres bases de datos están marcadas como `healthy`, Docker empieza a
   levantar `booking-service`, `payment-service` y `catalog-service`.
4. Si detienes todo con `docker-compose down` y lo vuelves a levantar, los datos de las bases
   de datos siguen ahí (porque viven en volúmenes, no dentro de los contenedores), y el mismo
   orden seguro se repite cada vez — el arranque es **determinista**, ya no depende de la
   suerte o de qué tan rápida sea tu máquina ese día.

---

## 6. Por qué esto le importa a tu proyecto específicamente

Tu sistema no es un solo servicio — es un ejemplo real de arquitectura distribuida con Saga
(Booking → Payment → Booking, vía eventos). Si `payment-service` intenta arrancar y conectarse
a `payment-db` antes de que esté lista, no solo falla un contenedor: **rompe la cadena completa
del flujo de reserva** que documentaste en `domain-events.md`, porque ese servicio no podría ni
siquiera empezar a escuchar el evento `ReservaCreada`. Por eso esta sesión, aunque parece "solo
configuración de Docker", protege directamente la confiabilidad del flujo de negocio central de
tu MVP1.
