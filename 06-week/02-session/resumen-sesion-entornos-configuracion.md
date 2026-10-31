# Resumen — Planificación: Entornos, Configuración y Orquestación

## ¿De qué trató esta sesión?

Hasta ahora tu sistema corre en tu computador con Docker Compose. Esta sesión responde una
pregunta distinta: **¿cómo pasa ese mismo sistema a un ambiente de pruebas y luego a
producción, sin romperse en el camino?** La respuesta central de toda la sesión es una sola
idea: construyes la imagen de tu aplicación **una sola vez**, y la **promocionas** de un
entorno a otro — nunca la reconstruyes para cada uno. Lo único que cambia entre entornos es la
**configuración** (variables de entorno), nunca el código ni la imagen.

---

## Palabras clave

| Término | Significado |
|---|---|
| **Entorno (environment)** | Un lugar donde corre tu sistema con un propósito distinto: desarrollo, QA o producción. |
| **Promocionar (promote)** | Mover el mismo artefacto ya construido y probado al siguiente entorno, cambiando solo su configuración. |
| **Artefacto** | La imagen Docker ya compilada — lo que realmente se mueve entre entornos. |
| **Metodología de 12 factores** | Conjunto de buenas prácticas para apps modernas; la relevante aquí es: la configuración vive en el entorno, no en el código. |
| **Desviación de configuración (config drift)** | Cuando algo falla en un entorno y no en otro porque la configuración no coincide (nombres de variables distintos, valores codificados a mano). Es la causa típica de "en mi máquina sí funciona". |
| **Secreto (secret)** | Una credencial sensible (contraseña, API key). Nunca se guarda en el código ni en git — se inyecta por entorno. |
| **`.env.example`** | Archivo que documenta los *nombres* de las variables requeridas, sin valores reales; sí se sube al repo. |
| **Flujo de rama por entorno** | Convención de nombres de rama que indica a qué entorno se dirige un cambio (ej. `hu-xxx-dev`, `hu-xxx-qa`, `hu-xxx-main`). |
| **Fail fast (validación al inicio)** | Que el servicio se niegue a arrancar si le falta una variable de configuración obligatoria, en vez de arrancar en un estado inválido. |

---

## Explicación en simple

Imagina que construyes una maqueta física de un edificio. La maqueta (tu imagen Docker) es
siempre la misma — no la vuelves a construir cada vez que la muestras en una feria distinta.
Lo que cambia es la **base o el letrero** sobre el que la colocas (la configuración): en una
feria dice "Proyecto de prueba", en otra dice "Proyecto final". La maqueta en sí, nunca cambia.

Eso es exactamente lo que dice la regla de 12 factores para configuración: tu aplicación
(`booking-service`, por ejemplo) es la misma imagen en desarrollo, QA y producción — solo la
variable `SPRING_DATASOURCE_URL` apunta a una base de datos distinta según en qué "feria"
(entorno) esté corriendo.

El problema que la sesión busca evitar es la **desviación de configuración**: si en desarrollo
la variable se llama `DB_URL` y en QA alguien la escribió como `DATABASE_URL`, el servicio
simplemente no la encuentra y falla — no porque el código esté mal, sino porque los nombres no
coinciden entre entornos. Por eso la solución no es solo "usar variables de entorno", sino
mantener los **mismos nombres de variable siempre**, documentados en un solo lugar.

---

## Adaptación a pms-properties

### Los tres entornos definidos

| Entorno | Propósito en mi proyecto |
|---|---|
| develop | Donde trabajo día a día con Docker Compose local, bases de datos desechables |
| qa | Donde se probaría el flujo completo de la Saga (Booking → Payment → Booking) con datos controlados, antes de tocar producción |
| prod | Donde correría el sistema real, con credenciales reales y sin datos de prueba |

### Matriz de configuración

Ya se documentó en `config-matrix.md`, con las mismas variables (`SPRING_DATASOURCE_URL`,
`SPRING_DATASOURCE_USERNAME`, `SPRING_DATASOURCE_PASSWORD`, `SPRING_PROFILES_ACTIVE`,
`LOG_LEVEL`) repetidas de forma idéntica en nombre para `booking-service`, `payment-service` y
`catalog-service` — solo sus valores cambian según el entorno.

### Secretos

Ya resuelto desde semanas anteriores: `.env.example` documenta los nombres sin valores reales;
`.env` con los valores reales está en `.gitignore` y nunca se sube al repositorio.

### Flujo de rama por entorno

Este es el punto que **aún no está implementado** en mi proyecto: hoy todo el equipo trabaja
directo sobre `main`, sin ramas separadas por entorno. La convención que definiría este flujo
sería `hu-xxx-dev` → PR a `develop`, `hu-xxx-qa` → PR a `qa`, `hu-xxx-main` → PR a `main`, donde
`xxx` se reemplaza por el ID real de cada historia de usuario (ej. `hu-book-001-dev`). Queda
como pendiente a decidir con el equipo antes de MVP2.

### Validación al inicio (fail fast)

Tampoco implementado todavía: ningún microservicio valida hoy explícitamente que sus variables
requeridas existan antes de arrancar. Es una mejora pendiente para evitar que un servicio
arranque en un estado a medio configurar.

---

## Relevancia para el proyecto

Sin esta disciplina, el riesgo real en `pms-properties` es que el flujo de Saga que ya
documentamos (`ReservaCreada` → `PagoAprobado`/`PagoRechazado`) funcione perfecto en desarrollo
(porque ahí las variables están bien puestas a mano) y falle en QA o producción solo porque
alguien escribió un nombre de variable distinto — no porque la lógica de negocio esté mal. Esta
sesión no agrega funcionalidad nueva al sistema, pero protege que lo que ya funciona en
desarrollo siga funcionando igual en los siguientes entornos.
