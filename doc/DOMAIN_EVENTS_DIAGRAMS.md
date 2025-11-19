# Diagrama de Flujo - Sistema de Eventos de Dominio

## 🔄 Flujo Completo: Crear HelloWorld con Eventos

```mermaid
sequenceDiagram
    participant Client
    participant Controller
    participant UseCase as CreateHelloWorldUseCase
    participant Entity as HelloWorld (Aggregate)
    participant Repository
    participant Dispatcher as EventDispatcher
    participant Handler1 as HelloWorldCreatedLogger
    participant Handler2 as EmailHandler (futuro)

    Client->>Controller: POST /helloworld {"name": "World"}
    
    Controller->>Container: get create_hello_world_use_case()
    Container-->>Controller: use_case instance
    
    Controller->>UseCase: execute("World")
    
    Note over UseCase: 1. Crear entidad
    UseCase->>Entity: HelloWorld.create(Greeting("World"))
    Entity-->>UseCase: hello_world instance
    
    Note over UseCase: 2. Persistir
    UseCase->>Repository: save(hello_world)
    Repository-->>UseCase: saved_entity (con ID=123)
    
    Note over UseCase: 3. Marcar como creado
    UseCase->>Entity: mark_as_created(123)
    Note over Entity: Registra HelloWorldCreated<br/>en _domain_events[]
    Entity-->>UseCase: void
    
    Note over UseCase: 4. Extraer eventos
    UseCase->>Entity: pull_domain_events()
    Entity-->>UseCase: [HelloWorldCreated(123, "World")]
    Note over Entity: Limpia _domain_events[]
    
    Note over UseCase: 5. Publicar eventos
    UseCase->>Dispatcher: publish_multiple(events)
    
    par Notificar handlers en paralelo
        Dispatcher->>Handler1: handle(HelloWorldCreated)
        Note over Handler1: logger.info("HelloWorld creado...")
        Handler1-->>Dispatcher: void
    and
        Dispatcher->>Handler2: handle(HelloWorldCreated)
        Note over Handler2: email_service.send(...)
        Handler2-->>Dispatcher: void
    end
    
    Dispatcher-->>UseCase: void
    
    Note over UseCase: 6. Serializar y retornar
    UseCase->>UseCase: HelloWorldSerializer.to_dict(saved_entity)
    UseCase-->>Controller: {"id": 123, "greeting": "World"}
    
    Controller-->>Client: HTTP 201 {"id": 123, "greeting": "World"}
```

## 🏗️ Arquitectura de Componentes

```mermaid
graph TB
    subgraph Domain["🎯 DOMAIN LAYER"]
        DomainEvent[DomainEvent<br/>Base Class]
        HelloWorldCreated[HelloWorldCreated<br/>Event]
        HelloWorldDeleted[HelloWorldDeleted<br/>Event]
        AggregateRoot[AggregateRootBase<br/>- record_event<br/>- pull_domain_events]
        HelloWorld[HelloWorld<br/>Aggregate Root]
        
        DomainEvent -.->|hereda| HelloWorldCreated
        DomainEvent -.->|hereda| HelloWorldDeleted
        AggregateRoot -.->|usa| DomainEvent
        HelloWorld -.->|hereda| AggregateRoot
        HelloWorld -->|registra| HelloWorldCreated
    end
    
    subgraph Application["⚙️ APPLICATION LAYER"]
        UseCase[CreateHelloWorldUseCase]
        Dispatcher[EventDispatcher<br/>- subscribe<br/>- publish]
        Subscriber[DomainEventSubscriber<br/>Interface]
        LoggerHandler[HelloWorldCreatedLogger]
        EmailHandler[EmailHandler]
        
        Subscriber -.->|implementa| LoggerHandler
        Subscriber -.->|implementa| EmailHandler
        Dispatcher -->|notifica| LoggerHandler
        Dispatcher -->|notifica| EmailHandler
    end
    
    subgraph Infrastructure["🔧 INFRASTRUCTURE"]
        Repository[HelloWorldRepository]
        Container[DI Container]
    end
    
    UseCase -->|usa| HelloWorld
    UseCase -->|usa| Repository
    UseCase -->|publica en| Dispatcher
    Container -->|inyecta| UseCase
    Container -->|registra| LoggerHandler
    Container -->|configura| Dispatcher
    
    style Domain fill:#e1f5ff
    style Application fill:#fff4e1
    style Infrastructure fill:#f0f0f0
```

## 📊 Estados de un Evento

```mermaid
stateDiagram-v2
    [*] --> Registrado: record_event()
    Registrado --> Acumulado: Más eventos...
    Acumulado --> Extraído: pull_domain_events()
    Extraído --> Publicado: dispatcher.publish()
    Publicado --> Manejado: handler.handle()
    Manejado --> [*]
    
    note right of Registrado
        Evento acumulado en
        _domain_events[]
    end note
    
    note right of Extraído
        Lista copiada y limpiada
        de la entidad
    end note
    
    note right of Publicado
        Dispatcher notifica a
        todos los handlers
    end note
```

## 🎭 Patrón Observer/Pub-Sub

```mermaid
graph LR
    subgraph Publisher
        Aggregate[HelloWorld<br/>Aggregate Root]
        UseCase[Use Case]
    end
    
    subgraph Mediator
        Dispatcher[EventDispatcher<br/>Singleton]
    end
    
    subgraph Subscribers
        H1[Logger Handler]
        H2[Email Handler]
        H3[Analytics Handler]
        H4[Audit Handler]
    end
    
    Aggregate -->|1. record_event| Event[HelloWorldCreated]
    Event -->|2. pull_domain_events| UseCase
    UseCase -->|3. publish| Dispatcher
    Dispatcher -->|4. notify| H1
    Dispatcher -->|4. notify| H2
    Dispatcher -->|4. notify| H3
    Dispatcher -->|4. notify| H4
    
    style Dispatcher fill:#ffeb3b
    style Event fill:#4caf50,color:#fff
```

## 🔀 Ciclo de Vida de un Agregado con Eventos

```mermaid
graph TD
    A[🎬 Inicio] --> B[Crear Agregado]
    B --> C{¿Operación<br/>de Negocio?}
    C -->|Sí| D[Ejecutar Lógica]
    D --> E[record_event]
    E --> F{¿Más<br/>operaciones?}
    F -->|Sí| C
    F -->|No| G[Persistir en BD]
    G --> H[pull_domain_events]
    H --> I[Publicar Eventos]
    I --> J[Handlers Ejecutan]
    J --> K[🏁 Fin]
    
    style E fill:#4caf50,color:#fff
    style H fill:#2196f3,color:#fff
    style I fill:#ff9800,color:#fff
```

## 📦 Estructura de Archivos con Eventos

```
app/
├── Shared/
│   ├── Domain/
│   │   ├── Events/
│   │   │   ├── DomainEvent.py              ← Base para eventos
│   │   │   └── DomainEventSubscriber.py    ← Interface handler
│   │   └── Entities/
│   │       └── EntityBase.py               ← AggregateRootBase
│   └── Infrastructure/
│       └── Events/
│           └── EventDispatcher.py          ← Despachador
│
├── Domain/
│   └── HelloWorld/
│       ├── Events/
│       │   ├── HelloWorldCreated.py        ← Evento específico
│       │   └── HelloWorldDeleted.py        ← Evento específico
│       └── HelloWorld.py                   ← Aggregate Root
│
├── Application/
│   ├── EventHandlers/
│   │   ├── HelloWorldCreatedLogger.py      ← Handler
│   │   └── HelloWorldDeletedLogger.py      ← Handler
│   └── UseCases/
│       └── HelloWorld/
│           ├── CreateHelloWorldUseCase.py  ← Publica eventos
│           └── DeleteHelloWorldUseCase.py  ← Publica eventos
│
└── config/
    └── container.py                        ← Registra handlers
```

## 🧪 Testing - Flujo de Verificación

```mermaid
graph TD
    T1[Test Unitario:<br/>Evento se Registra] --> V1{✓}
    T2[Test Unitario:<br/>Dispatcher Llama Handler] --> V2{✓}
    T3[Test Unitario:<br/>Handler Ejecuta Lógica] --> V3{✓}
    T4[Test Integración:<br/>Flujo Completo] --> V4{✓}
    
    V1 --> R[Resultado:<br/>Sistema Funcional]
    V2 --> R
    V3 --> R
    V4 --> R
    
    style T1 fill:#e3f2fd
    style T2 fill:#e3f2fd
    style T3 fill:#e3f2fd
    style T4 fill:#bbdefb
    style R fill:#4caf50,color:#fff
```

## ⚡ Comparación: Sin Eventos vs Con Eventos

### Sin Eventos (Antes) ❌

```mermaid
graph LR
    UseCase[Use Case] --> Repo[Repository]
    UseCase --> Logger[Log Manual]
    UseCase --> Email[Email Manual]
    UseCase --> Stats[Stats Manual]
    
    style UseCase fill:#ff5252,color:#fff
```

**Problemas:**
- Alto acoplamiento
- Use Case con muchas responsabilidades
- Difícil de testear
- No extensible

### Con Eventos (Después) ✅

```mermaid
graph LR
    UseCase[Use Case] --> Repo[Repository]
    UseCase --> Dispatcher[Event Dispatcher]
    Dispatcher --> H1[Logger Handler]
    Dispatcher --> H2[Email Handler]
    Dispatcher --> H3[Stats Handler]
    
    style UseCase fill:#4caf50,color:#fff
    style Dispatcher fill:#ffeb3b
```

**Beneficios:**
- Bajo acoplamiento
- Use Case enfocado
- Fácil de testear
- Altamente extensible

---

## 📌 Conceptos Clave Visualizados

### 1. Evento = Pasado

```
❌ INCORRECTO          ✅ CORRECTO
CreateHelloWorld  →   HelloWorldCreated
DeleteHelloWorld  →   HelloWorldDeleted
UpdateHelloWorld  →   HelloWorldUpdated
```

### 2. Handler = Reacción

```
Evento               →    Handler
HelloWorldCreated    →    Logger escribe en archivo
                     →    Email envía notificación
                     →    Analytics incrementa contador
                     →    Audit guarda en EventStore
```

### 3. Dispatcher = Mediador

```
Publisher             Mediator              Subscribers
   │                     │                      │
   ├─────publish────────▶│                      │
   │                     ├───────notify────────▶│ Handler 1
   │                     ├───────notify────────▶│ Handler 2
   │                     └───────notify────────▶│ Handler 3
```

---

**Este diagrama visual complementa la documentación completa en `DOMAIN_EVENTS_DOCUMENTATION.md`**
