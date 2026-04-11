Hay que resolver 2 problemas.
- Mundo de bloques
- Torres de Hanoi

### Objetivos de Mundo de bloques 
> [!PDF|yellow] [[Práctica 2 - STRIPS.pdf#page=2&selection=2,0,3,21&color=yellow|Práctica 2 - STRIPS, p.2]]
> > Utilizar STRIPS para obtener un plan que resuelva ambos escenarios del mundo de bloques.

Solo hay 2 posibles estados, dos posibles configuraciones iniciales de bloques. Y debemos construir un "plan" que en esencia es **determinar** la secuencia de movimientos que se le deben hacer a los bloques para conseguir el output esperado. Para conseguir esa secuencia de movimiento de los bloques usaremos lo que sea que sea STRIPS.

> [!PDF|yellow] [[Práctica 2 - STRIPS.pdf#page=2&selection=4,0,5,47&color=yellow|Práctica 2 - STRIPS, p.2]]
> > Implementar un agente que tenga integrado el planificador y sea capaz de resolver ambos escenarios siguiendo el plan.

¿Qué significa "implementar un agente"?
>Un agente es una entidad que dado un contexto es capaz de tomar decisiones autónomas.

Entonces se debe construir una entidad (como debe mantener estado interno dicha entidad debe ser una **clase**, que estado interno debe mantener? -> )que llame a STRIPS para conseguir la secuencia de movimientos de bloques que debe aplicar, luego ejecuta esas funciones para mover los bloques
┌─────────────────────────────────────────┐
│           AGENTE (Cuerpo + Cerebro)                  │
├─────────────────────────────────────────┤
│  ┌──────────────┐    ┌──────────────┐          │
│  │  Planificador     │    │ Actuadores      │           │
│  │  (STRIPS)           │    │ (Ejecutor)         │           │
│  └──────┬───────┘    └──────┬───────┘           │
│               │                               │                          │
│              ▼                              ▼                         │
│  ┌─────────────────────────────────┐         │
│  │     Modelo del Dominio                      │         │
│  │  (reglas, acciones, estado)                  │         │
│  └─────────────────────────────────┘         │
└─────────────────────────────────────────┘
Lo que el agente hace:
1. Piensa: Llama a STRIPS → obtiene plan de acciones
2. Actúa: Ejecuta cada acción del plan en el entorno simulado
3. Muestra: Actualiza y visualiza el estado después de cada acción