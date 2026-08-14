# OdontoSys

## Sistema Distribuido para la Gestión de un Consultorio Odontológico

---

# 1. Descripción del proyecto

**OdontoSys** es un sistema distribuido orientado a la gestión integral de un consultorio odontológico.

El sistema permitirá administrar los principales procesos relacionados con la atención de pacientes, incluyendo la gestión de usuarios, pacientes, citas, atención clínica, tratamientos y facturación.

La solución estará desarrollada bajo una **arquitectura basada en microservicios**, donde cada servicio tendrá una responsabilidad específica y contará con independencia lógica y de persistencia.

El sistema utilizará diferentes tecnologías de backend, bases de datos y mecanismos de comunicación con el objetivo de demostrar conceptos propios de **Sistemas Distribuidos**, como desacoplamiento, comunicación síncrona y asíncrona, tolerancia a fallos, escalabilidad y consistencia eventual.

---

# 2. Objetivo general

Diseñar e implementar una solución distribuida para la gestión de un consultorio odontológico, aplicando conocimientos de ingeniería de sistemas en el diseño de arquitecturas de microservicios, seguridad, comunicación entre servicios, gestión independiente de datos y analítica, buscando demostrar las características y beneficios de una arquitectura distribuida.

---

# 3. Alcance

El sistema permitirá gestionar:

- Autenticación y autorización de usuarios.
- Gestión de roles y permisos.
- Gestión de pacientes.
- Gestión de citas y agenda odontológica.
- Historias clínicas.
- *Odontogramas.*
- Diagnósticos y tratamientos.
- Facturación y pagos.
- Comunicación síncrona mediante APIs REST.
- Comunicación asíncrona mediante RabbitMQ.
- Extracción y carga de información para analítica.
- Análisis general del comportamiento del consultorio.

El proyecto se enfocará principalmente en demostrar la arquitectura distribuida y los conceptos asociados a ella.

No se contempla inicialmente la integración con pasarelas de pago reales, facturación electrónica, aseguradoras o sistemas externos de salud.

---

# 4. Arquitectura general

La solución estará compuesta por cuatro microservicios principales de negocio, un servicio de autenticación y un componente de analítica.

```text
                              ODONTOSYS
                                  │
                                  ▼
                           ┌──────────────┐
                           │ API GATEWAY  │
                           └──────┬───────┘
                                  │
                       ┌──────────▼──────────┐
                       │   AUTH SERVICE      │
                       │    Spring Boot      │
                       └──────────┬──────────┘
                                  │
                              JWT / RBAC
                                  │
          ┌───────────────────────┼────────────────────────┐
          │                       │                        │
          ▼                       ▼                        ▼
   ┌─────────────┐         ┌─────────────┐          ┌─────────────┐
   │  PACIENTES  │         │    CITAS    │          │   CLÍNICO   │
   │ Spring Boot │         │ Spring Boot │          │     Go      │
   └──────┬──────┘         └──────┬──────┘          └──────┬──────┘
          │                       │                        │
          ▼                       ▼                        ▼
      PostgreSQL              PostgreSQL                MongoDB


                         ┌─────────────────┐
                         │   FACTURACIÓN   │
                         │   Spring Boot   │
                         └────────┬────────┘
                                  │
                                  ▼
                              PostgreSQL


                         ┌─────────────────┐
                         │    RabbitMQ     │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │    ANALÍTICA    │
                         │  Go/Python/Java │
                         └─────────────────┘
```

---

# 5. Microservicios y responsables

## 5.1 Auth Service

**Tecnología:** Spring Boot  
**Responsable:** **Harold Camilo Barrera Giraldo**

### Responsabilidad

Este servicio será responsable de la gestión de identidad y seguridad del sistema.

### Funcionalidades principales

- Registro de usuarios.
- Inicio de sesión.
- Generación y validación de JWT.
- Refresh Tokens.
- Gestión de roles.
- Gestión de permisos.
- Autenticación multifactor (MFA).
- Gestión de sesiones.
- Gestión de dispositivos.
- Control de acceso.

### Roles principales

El sistema manejará inicialmente:

- Paciente.
- Odontólogo.
- Administrador.

El servicio Auth será el encargado de definir y administrar los roles y permisos, mientras que cada microservicio será responsable de aplicar los permisos correspondientes a sus propios recursos.

---

## 5.2 Microservicio de Pacientes

**Tecnología:** Spring Boot  
**Base de datos:** PostgreSQL  
**Responsable:** **Daniel Perez**

### Responsabilidad

Gestionar la información general y administrativa de los pacientes.

### Funcionalidades principales

- Registrar pacientes.
- Actualizar información.
- Consultar pacientes.
- Gestionar información de contacto.
- Gestionar contactos de emergencia.
- Consultar información básica relacionada con el paciente.

El servicio será propietario de su propia base de datos y ningún otro microservicio accederá directamente a ella.

---

## 5.3 Microservicio de Citas

**Tecnología:** Spring Boot  
**Base de datos:** PostgreSQL  
**Responsable:** **Bryan Smith Bedoya**

### Responsabilidad

Gestionar la agenda y las citas odontológicas.

### Funcionalidades principales

- Crear citas.
- Consultar disponibilidad.
- Reprogramar citas.
- Cancelar citas.
- Confirmar asistencia.
- Cambiar estados de las citas.
- Consultar agenda de los odontólogos.

### Estados posibles

```text
PROGRAMADA
CONFIRMADA
EN_ATENCION
FINALIZADA
CANCELADA
NO_ASISTIO
```

El microservicio será independiente de la base de datos de los demás servicios.

---

## 5.4 Microservicio Clínico

**Tecnología:** Go  
**Base de datos:** MongoDB  
**Responsable:** **Luis Ignacio Bonilla**

### Responsabilidad

Gestionar la información relacionada con la atención odontológica.

### Funcionalidades principales

- Historia clínica.
- Odontograma.
- Diagnósticos.
- Tratamientos.
- Procedimientos.
- Evolución de la atención.
- Registro de consultas odontológicas.

### Uso de MongoDB

MongoDB será utilizado debido a que la información clínica puede presentar estructuras variables dependiendo del paciente, diagnóstico o tratamiento.

Esto permitirá aplicar **persistencia políglota**, utilizando diferentes tecnologías de almacenamiento según las necesidades de cada dominio.

---

## 5.5 Microservicio de Facturación

**Tecnología:** Spring Boot  
**Base de datos:** PostgreSQL  
**Responsable:** **Juan Diego Mora**

### Responsabilidad

Gestionar los procesos económicos relacionados con la atención odontológica.

### Funcionalidades principales

- Generación de facturas.
- Consulta de facturas.
- Registro de pagos.
- Consulta de saldos.
- Métodos de pago.
- Historial de pagos.

Los pagos serán inicialmente simulados y no se contempla una integración con una pasarela de pagos real.

---

## 5.6 Componente de Analítica

**Tecnología:** Go / Python / Java  
**Responsable:** **Luis Ignacio Bonilla**

### Responsabilidad

El componente de analítica tendrá un alcance enfocado en la **extracción, carga y análisis general de la información generada por el sistema**.

No se busca inicialmente implementar modelos predictivos o inteligencia artificial, sino obtener información que permita conocer el comportamiento del consultorio y su evolución.

### Extracción

Se extraerá información de los diferentes microservicios, principalmente relacionada con:

- Pacientes.
- Citas.
- Tratamientos.
- Facturación.
- Pagos.

La extracción se realizará a partir de los mecanismos definidos por la arquitectura, evitando el acceso directo a las bases de datos de otros microservicios.

### Carga

La información extraída será transformada cuando sea necesario y posteriormente cargada en una estructura destinada al análisis.

El objetivo será contar con información consolidada que permita realizar consultas y generar indicadores sin afectar directamente las bases de datos operacionales.

### Análisis

El componente de analítica permitirá responder preguntas generales sobre el rendimiento del consultorio:

- ¿Cuántas citas se realizaron este mes y cómo se comparan con el mes anterior?
- ¿Cuánto dinero se generó este mes y cómo se compara con el mes anterior?
- ¿Qué tratamientos generan mayores ingresos?
- ¿Cuántos pacientes nuevos se registraron este mes?

El objetivo será obtener una visión general de la evolución de las citas, los ingresos y los tratamientos que generan mayor rentabilidad, permitiendo identificar si el consultorio está mejorando con respecto a periodos anteriores.

De esta manera se podrá determinar si el consultorio presenta una tendencia de **crecimiento, estabilidad o disminución**.

### Ejemplo

```text
              Microservicios
                    │
                    ▼
              Extracción
                    │
                    ▼
                Transformación
                    │
                    ▼
                  Carga
                    │
                    ▼
             Datos consolidados
                    │
                    ▼
                 Análisis
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
      Mes actual         Mes anterior
          │                   │
          └─────────┬─────────┘
                    ▼
             Comparación
                    │
                    ▼
             Tendencia
                    │
                    ▼
       Crecimiento / Estabilidad /
             Disminución
```

El resultado podrá sera presentado mediante un dashboard con indicadores y gráficos básicos.

---

