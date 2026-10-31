# Docker Compose y Orquestación — Resumen Técnico (Semana 06)

## Objetivo de la sesión

Esta semana trabajé en llevar la orquestación local de `pms-properties` de un `docker-compose.yml`
funcional pero frágil, a uno con arranque **determinista**: los tres microservicios
(`booking-service`, `payment-service`, `catalog-service`) ahora esperan a que sus respectivas
bases de datos estén realmente listas antes de intentar conectarse, en lugar de asumirlo por el
orden de arranque de los contenedores.

## Problema identificado

El `docker-compose.yml` de la semana anterior usaba `depends_on` en su forma simple:

```yaml
booking-service:
  depends_on:
    - booking-db
```

Esto solo garantiza **orden de arranque** del contenedor, no que el servicio dentro de él esté
listo para aceptar conexiones. Un contenedor de PostgreSQL puede reportarse como "iniciado"
mientras todavía está inicializando sus archivos de datos; si `booking-service` intenta
conectarse en ese instante, la conexión falla. Este comportamiento es no determinista: puede
funcionar en un computador rápido y fallar en CI o en una máquina más lenta.

## Solución implementada

**1. Healthchecks reales en cada base de datos**, para que Docker pueda verificar disponibilidad
real y no solo el estado del proceso:

```yaml
booking-db:
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U ${BOOKING_DB_USER}"]
    interval: 5s
    timeout: 5s
    retries: 5
```

Se usó `pg_isready` para las dos bases PostgreSQL (`booking-db`, `payment-db`) y
`mongosh --eval "db.adminCommand('ping')"` para la base MongoDB (`catalog-db`), ya que el
comando de verificación depende del motor de base de datos.

**2. `depends_on` con condición de salud**, reemplazando el `depends_on` simple:

```yaml
booking-service:
  depends_on:
    booking-db:
      condition: service_healthy
```

Con esto, Docker Compose bloquea el arranque de cada microservicio hasta que su base de datos
reporte `healthy`, no solo `started`.

**3. Healthchecks a nivel de microservicio**, reutilizando el endpoint `/health` construido en
la Semana 04 (walking skeleton):

```yaml
booking-service:
  healthcheck:
    test: ["CMD-SHELL", "curl -f http://localhost:8081/health || exit 1"]
    interval: 10s
    timeout: 5s
    retries: 5
    start_period: 15s
```

Esto requirió instalar `curl` en la etapa de runtime del `Dockerfile` (la imagen base
`eclipse-temurin:21-jre` no lo incluye por defecto):

```dockerfile
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
```

**4. Separación de configuración por entorno**, siguiendo el patrón archivo base + overrides:

- `docker-compose.override.yml`: se aplica automáticamente en desarrollo local
  (`docker-compose up`), define `SPRING_PROFILES_ACTIVE=dev`.
- `compose.prod.yml`: se aplica explícitamente (`-f docker-compose.yml -f compose.prod.yml`),
  define `SPRING_PROFILES_ACTIVE=prod` y límites de recursos por contenedor.

Las credenciales de base de datos permanecen externalizadas vía `.env` en ambos casos; ningún
archivo de Compose contiene secretos.

## Verificación

Ejecuté `docker-compose up --build` y confirmé el siguiente orden de arranque:

1. `booking-db`, `payment-db`, `catalog-db` arrancan primero.
2. Docker espera hasta que cada una reporte `healthy` vía su healthcheck.
3. Solo entonces arrancan `booking-service`, `payment-service`, `catalog-service`.
4. Los datos persisten en volúmenes nombrados (`booking-db-data`, etc.) tras `docker-compose down`
   y un nuevo `up`.

## Relevancia para el proyecto

Este cambio protege directamente el flujo del patrón Saga documentado en `domain-events.md`
(Booking → Payment → Booking vía `ReservaCreada`/`PagoAprobado`/`PagoRechazado`): si
`payment-service` arrancara antes de que `payment-db` esté lista, el servicio ni siquiera podría
inicializar su listener de eventos, rompiendo la cadena completa de la Saga desde el arranque del
sistema. Un arranque no determinista en desarrollo también se traduciría en fallos intermitentes
al correr el sistema en integración continua.

## Pendientes

- Los endpoints `/health` de `payment-service` y `catalog-service` aún no están implementados;
  sus healthchecks fallarán hasta que existan.
- Los límites de memoria en `compose.prod.yml` son valores provisionales, sin pruebas de carga
  reales que los respalden.
- Se mantiene Docker Compose como solución de orquestación para el MVP1 (un solo host); migrar a
  un orquestador tipo Kubernetes solo se justificará si se necesita múltiples hosts,
  auto-recuperación o autoescalado.

## Archivos modificados/creados

- `docker-compose.yml` (actualizado — healthchecks + `depends_on` con condición)
- `docker-compose.override.yml` (nuevo — configuración de desarrollo)
- `compose.prod.yml` (nuevo — configuración de producción)
- `booking-service/Dockerfile`, `payment-service/Dockerfile`, `catalog-service/Dockerfile`
  (actualizados — se agregó `curl` en la etapa de runtime)
