# Session Notes — Building a Service: Structure, Layers, and Walking Skeleton

## Self-check answers

**Question 1.** The composition root is where...
Correct answer: **Concrete adapters are selected and injected (DIP).**

**Question 2.** A walking skeleton is...
Correct answer: **The thinnest end-to-end slice that actually works.**

**Question 3.** `new PostgresRepo()` inside a use case is...
Correct answer: **A DIP violation (inject the port instead).**

**Question 4.** Folder design should...
Correct answer: **Reveal the architecture (domain / application / adapters).**

**Question 5.** Building the domain, database, and HTTP protocol separately and integrating them at the end is...
Correct answer: **The big-bang anti-pattern; integrate from day one instead.**

**Question 6.** "Validated at runtime" means the service...
Correct answer: **Starts with a real database and responds to a request (not just compiles).**

---

## This week's exercise, applied to my project (pms-properties)

Chosen service: **booking-service** (Core Domain, per the Domain Map). This is the walking skeleton: the thinnest slice that runs end-to-end against a real PostgreSQL database, before adding the full Saga logic.

### 1. Folder layout (hexagonal)

booking-service/
domain/
reserva/
Reserva.java
EstadoReserva.java
ReservaId.java
port/
ReservaRepository.java (port — interface only)
shared/
valueobject/
DateRange.java
Money.java
application/
reserva/
usecase/
CrearReservaUseCase.java
adapters/
in/
http/
HealthController.java
ReservaController.java
out/
persistence/
JpaReservaRepository.java (implements the port)
ReservaEntity.java (JPA entity, infrastructure only)
ReservaJpaRepositoryAdapter.java
config/
CompositionRoot.java (wires adapters into use cases)
BookingServiceApplication.java (Spring Boot main class)
tests/
unit/
domain/ReservaTest.java
integration/
persistence/ReservaRepositoryIT.java (Testcontainers)

Dependencies point inward: `adapters -> application -> domain`. Nothing in `domain/` imports Spring, JPA, or HTTP types.

### 2. Health endpoint (walking skeleton entry point)

```java
// adapters/in/http/HealthController.java
@RestController
public class HealthController {

    @GetMapping("/health")
    public ResponseEntity<Map<String, String>> health() {
        return ResponseEntity.ok(Map.of("status", "UP", "service", "booking-service"));
    }
}
```

### 3. Minimal persistent entity through the full stack

```java
// domain/reserva/port/ReservaRepository.java — the PORT (pure domain, no framework imports)
package com.pmsproperty.booking.domain.reserva.port;

public interface ReservaRepository {
    Optional<Reserva> porId(ReservaId id);
    void guardar(Reserva reserva);
}
```

```java
// adapters/out/persistence/ReservaEntity.java — JPA lives ONLY here, never in domain/
package com.pmsproperty.booking.adapters.out.persistence;

@Entity
@Table(name = "reservas")
public class ReservaEntity {
    @Id
    private UUID id;
    private UUID propiedadId;
    private UUID usuarioId;
    private LocalDate fechaInicio;
    private LocalDate fechaFin;
    private BigDecimal montoTotal;
    private String estado;
    // getters/setters — infrastructure mapping only
}
```

```java
// adapters/out/persistence/ReservaJpaRepositoryAdapter.java — implements the domain PORT
package com.pmsproperty.booking.adapters.out.persistence;

@Component
public class ReservaJpaRepositoryAdapter implements ReservaRepository {

    private final SpringDataReservaRepository jpaRepo; // Spring Data interface

    public ReservaJpaRepositoryAdapter(SpringDataReservaRepository jpaRepo) {
        this.jpaRepo = jpaRepo;
    }

    @Override
    public Optional<Reserva> porId(ReservaId id) {
        return jpaRepo.findById(id.valor()).map(this::toDomain);
    }

    @Override
    public void guardar(Reserva reserva) {
        jpaRepo.save(toEntity(reserva));
    }

    private Reserva toDomain(ReservaEntity e) { /* mapping */ return null; }
    private ReservaEntity toEntity(Reserva r) { /* mapping */ return null; }
}
```

### 4. Composition root — wiring at the edge (DIP in practice)

```java
// config/CompositionRoot.java
@Configuration
public class CompositionRoot {

    @Bean
    public CrearReservaUseCase crearReservaUseCase(ReservaRepository reservaRepository) {
        // The concrete adapter (ReservaJpaRepositoryAdapter) is chosen here,
        // in ONE place — never with `new` inside a use case.
        return new CrearReservaUseCase(reservaRepository);
    }
}
```

```java
// application/reserva/usecase/CrearReservaUseCase.java
public class CrearReservaUseCase {

    private final ReservaRepository reservaRepository; // depends on the PORT, not on JPA

    public CrearReservaUseCase(ReservaRepository reservaRepository) {
        this.reservaRepository = reservaRepository;
    }

    public ReservaId ejecutar(UUID propiedadId, UUID usuarioId, DateRange fechas, Money total) {
        Reserva reserva = Reserva.crear(propiedadId, usuarioId, fechas, total);
        reservaRepository.guardar(reserva);
        return reserva.getId();
    }
}
```

### 5. Real database in a container (runtime-validated, not just "compiles")

```yaml
# docker-compose.yml (booking-service local dev)
services:
  booking-db:
    image: postgres:16
    environment:
      POSTGRES_DB: booking
      POSTGRES_USER: booking_user
      POSTGRES_PASSWORD: ${DB_PASSWORD} # via environment variable, no secrets in the file
    ports:
      - "5432:5432"

  booking-service:
    build: .
    depends_on:
      - booking-db
    environment:
      SPRING_DATASOURCE_URL: jdbc:postgresql://booking-db:5432/booking
      SPRING_DATASOURCE_USERNAME: booking_user
      SPRING_DATASOURCE_PASSWORD: ${DB_PASSWORD}
    ports:
      - "8081:8080"
```

**Definition of Done for this week's skeleton:** `docker-compose up` starts a real PostgreSQL container and the booking-service; `GET /health` returns `200 { "status": "UP" }`; a minimal `POST /reservas` (without Saga logic yet) persists a `Reserva` row through the full path controller -> use case -> domain -> port -> JPA adapter -> real database. Next week's planning session will scope the remaining MVP 1 endpoints on top of this structure.
