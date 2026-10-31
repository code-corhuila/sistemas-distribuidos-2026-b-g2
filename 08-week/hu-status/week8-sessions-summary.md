# Resumen — Semana 8: Agile & DevOps + Planning

## Sesión 1 — Agile & DevOps for distributed teams

**Idea central:** un sistema distribuido lo construye un equipo que debe funcionar como un
sistema distribuido bien llevado — propiedad clara, lotes pequeños, retroalimentación rápida.

- **Ciclo Scrum:** el backlog priorizado alimenta un sprint backlog, se trabaja en un sprint
  fijo (1 semana), se revisa como incremento funcionando, y se mejora en la retrospectiva.
  Roles: Product Owner (qué/prioridad), Scrum Master (proceso/impedimentos), Equipo (cómo/construir).
- **Buena historia de usuario:** formato *"Como [rol], quiero [acción], para [beneficio]"*, con
  criterios de aceptación **verificables** (un test puede responder Sí/No). Una historia sin AC
  verificables es un deseo, no trabajo. Se prioriza con MoSCoW y se dimensiona con story points.
- **DevOps — "tú lo construyes, tú lo operas":** elimina el muro entre desarrollo y operación.
  Ciclo continuo Plan → Build → Test → Release → Deploy → Operate → Monitor, retroalimentando
  de vuelta al Plan. Es cultura antes que herramientas: releases pequeños y frecuentes,
  automatizar lo repetible, aprendizaje sin culpa ante fallas.
- **Coordinar un equipo distribuido:** propiedad clara por servicio/repo (RACI), lotes pequeños
  (ramas de corta vida, PRs frecuentes), retroalimentación rápida (CI en cada PR), comunicación
  asíncrona por escrito (ADRs, descripciones de PR, el tablero) para que nadie sea un bloqueo.
- **Métricas de flujo:** medir flujo, no ocupación — WIP (limitar trabajo en progreso), lead
  time (idea → hecho), cycle time, throughput. WIP subiendo + throughput bajando es la señal
  clásica de "todos ocupados, nada se entrega".
- **Escenario de advertencia — el héroe y el cuello de botella:** una persona toma 8 historias
  "para ir más rápido"; tres quedan a medio hacer al cierre del sprint, y solo ella entiende ese
  código. Solución: límite de WIP (ej. 2 por persona), pair programming en lo riesgoso, exigir
  PRs para que el conocimiento se disperse, dividir historias grandes.

## Sesión 2 — Planning: story mapping, estimación y compromiso de MVP 2

**Idea central:** a mitad del Corte 2, la planeación se afina — mapear el recorrido del
producto, estimar con honestidad, desenredar dependencias entre servicios, y comprometer solo
lo que realmente cabe.

- **Story mapping:** el recorrido del usuario se dibuja de izquierda a derecha (columna
  vertebral de actividades), con detalle/prioridad de arriba hacia abajo. La "línea de
  release" marca la rebanada más delgada de punta a punta que sí se entrega; lo que queda
  debajo espera. Mantiene al equipo construyendo un camino usable, no funcionalidades sueltas.
- **Estimar en relativo, no en horas:** tamaño/complejidad/incertidumbre en escala tipo
  Fibonacci (1,2,3,5,8,13) mediante *planning poker* — todos revelan a la vez, se discuten los
  valores atípicos (esa discusión es el verdadero valor). Un 8+ es señal de alerta: dividir
  antes de comprometer. La velocidad (puntos/sprint) sirve para pronosticar, nunca como meta a
  perseguir.
- **Desenredar dependencias entre servicios:** en un producto multi-servicio, las historias
  dependen entre sí a través de equipos/servicios. El interbloqueo clásico: dos servicios cada
  uno esperando el endpoint del otro. Se rompe con **contrato primero** — se acuerda la API
  ahora, se mockea, y ambos lados construyen contra el mock.
- **Comprometer con realismo:** comprometer, en puntos, lo equivalente a la velocidad real del
  equipo en historias "Must" que sirvan la meta del sprint, con margen para lo desconocido. Lo
  que sobra (Should/Could) se queda en el backlog. Sobre-comprometerse es la causa #1 de que un
  sprint fracase.
- **Escenario de advertencia — optimismo + dependencia oculta:** el equipo compromete 40 puntos
  (nunca ha hecho más de 25) asumiendo que el webhook de Pagos "va a estar listo". Al cuarto
  día no lo está, la mitad de las historias quedan bloqueadas, el sprint colapsa. Solución:
  comprometer cerca de la velocidad real; para la dependencia, acordar el contrato ya y
  construir contra un mock/stub; convertir la dependencia misma en una historia con dueño y
  fecha.

## Cómo se conecta con lo que hiciste esta semana

El trabajo que hicimos en `06-data`, `08-uml` y `07-api/guidelines.md` es, en esencia, la
aplicación práctica del punto más repetido en ambas sesiones: **"contrato primero"**. Cerrar
las decisiones de modelado de datos, formalizar el contrato de error de la API y dejar los
huecos declarados con dueño es exactamente la técnica que la Sesión 2 receta para romper el
interbloqueo entre servicios — se hizo antes de que exista una sola línea de código.
