# Resumen — Persistencia distribuida y Release MVP 2

## 1. Persistencia en sistemas distribuidos: saga, outbox, CQRS

### Database-per-service y persistencia políglota
Cada servicio es dueño de su base de datos; ningún otro servicio la lee directamente. Esto permite despliegue y escalado independientes, cambios de esquema sin coordinar con otros equipos, y elegir el motor adecuado para cada caso (Postgres para órdenes, un document store para catálogo, Redis para sesiones).

### No hay transacción global: la saga
No es posible envolver "reservar stock + cobrar + confirmar la orden" en una sola transacción ACID entre servicios. En su lugar se usa una **saga**: una secuencia de transacciones locales, cada una con su compensación para deshacerla si un paso posterior falla.

- **Orquestación:** un coordinador dirige los pasos (reservar → cobrar → confirmar) y dispara la compensación si alguno falla.
- **Coreografía:** los servicios reaccionan a eventos de otros (`OrderPlaced` → `StockReserved` → `PaymentDone` → confirmar), sin un coordinador central.

### Publicar eventos de forma confiable: el outbox
El **dual-write problem**: si el servicio guarda el estado en su BD y luego publica el evento al broker como dos pasos separados, un fallo entre ambos deja el estado sin su evento (o viceversa).

El patrón **outbox** lo resuelve: el evento se escribe en una tabla outbox dentro de la **misma transacción** que el cambio de estado; un *relay* separado lee esa tabla y publica al broker. Así la escritura es atómica y ningún evento se pierde, aunque el broker lo reciba con *at-least-once delivery* (lo que exige consumidores **idempotentes**).

### Lecturas rápidas: CQRS
CQRS separa el modelo de escritura (comandos, el agregado) del modelo de lectura (consultas, una vista desnormalizada construida a partir de los eventos). El modelo de lectura es **eventualmente consistente**: se actualiza poco después de la escritura. Hay que diseñar para ese retraso (por ejemplo, mostrando un estado "procesando") en vez de simular consistencia inmediata.

### Escenario típico: el evento perdido
Orders guarda la orden y la aplicación se cae antes de publicar `OrderPlaced`; Inventory nunca reserva el stock y la orden queda atascada. La solución es el outbox: orden y evento se escriben en una sola transacción, y un relay publica de forma confiable. La consistencia entre servicios se logra con **sagas + outbox + idempotencia**, nunca fingiendo que existe una transacción distribuida.

### Errores comunes
- Forzar una transacción ACID única entre servicios (2PC en todas partes).
- Dual-write (BD y luego broker) sin outbox → eventos perdidos.
- Consumidores no idempotentes bajo entrega at-least-once.
- Esperar que el modelo de lectura esté instantáneamente consistente.

---

## 2. Release — MVP 2 (sistema integrado)

### Qué cambia respecto a MVP 1
MVP 1 era un servicio corriendo solo. MVP 2 es un **sistema distribuido integrado**: varios servicios comunicándose por contratos, consistencia entre ellos vía saga + outbox, y configuración/secretos manejados por ambiente. El release debe demostrar no solo el camino feliz, sino también el camino de falla y de consistencia.

### Promoción y tag
El incremento se promueve `develop → qa → main` (flujo por ambiente), se verifica en `qa` con configuración similar a producción, y se etiqueta `v2.0.0` en `main`. Las imágenes construidas desde ese tag, corridas con configuración de producción, son el release.

### Checklist de Definition of Done para MVP 2
- Criterios de aceptación de todas las historias comprometidas, cumplidos.
- Pruebas unitarias + de integración + de contrato en verde (cobertura declarada ≤ medida).
- `docker compose up` levanta todo el sistema, con health checks.
- Un flujo cruzado entre servicios funciona de punta a punta (ej. crear orden → reservar stock → cobrar).
- Se demuestra un **camino de falla**: un paso falla y la saga compensa (no se cobra sin stock).
- Eventos confiables (outbox), consumidores idempotentes (seguros ante reentrega).
- Configuración por ambiente; **sin secretos** en git ni en las imágenes.
- Versión etiquetada (`v2.0.0`), CHANGELOG y ADR actualizados.

### La demo debe incluir una falla
Un demo que solo muestra el camino feliz no es un release de sistemas distribuidos. Hay que recorrer el flujo completo por el gateway, mostrar los datos persistidos en la BD de cada servicio, y luego inyectar una falla (detener un servicio, o enviar un evento duplicado) para mostrar que la saga compensa o que el consumidor idempotente ignora el duplicado.

### Retrospectiva → Corte 3
Al cerrar el Corte 2, la retro se enfoca en el dolor de integración: arranque inestable, contratos que no coinciden, bugs de consistencia. Cada hallazgo se vuelve ítem de backlog. El Corte 3 se centra en operar el sistema: observabilidad, despliegue, seguridad, CI/CD, y el release final.

### Errores comunes
- Demostrar solo el camino feliz (sin prueba de falla/consistencia).
- No etiquetar versión ni actualizar el CHANGELOG → no reproducible.
- Que la consistencia "funcione" solo porque nada falló durante la demo.
- Saltarse la retro → el dolor de integración se repite en el Corte 3.

### Cómo se evalúa MVP 2
Más allá de la funcionalidad, se pesa la arquitectura (contratos respetados, saga/outbox correctos, sin BD compartida), la calidad del código (pruebas incluyendo contrato/integración) y el cumplimiento de Scrum (backlog, ceremonias, flujo por ambiente). La evidencia individual de estado de HU en cada fork alimenta la nota personal.
