# Python Hexagonal DDD + CQRS

Proyecto de ejemplo implementando **Arquitectura Hexagonal (Puertos y Adaptadores)**, **Domain-Driven Design (DDD)**, **CQRS (Command Query Responsibility Segregation)** y **Event-Driven Architecture** con Python y Flask.

## 📋 Tabla de Contenidos

- [Arquitectura](#arquitectura)
- [Flujos de la Aplicación](#flujos-de-la-aplicación)
  - [Flujo de Inicialización](#1-flujo-de-inicialización-de-la-aplicación)
  - [Flujo de Escritura (Commands)](#2-flujo-de-escritura-commands---crear-helloworld)
  - [Flujo de Lectura (Queries)](#3-flujo-de-lectura-queries---obtener-todos-los-helloworld)
  - [Flujo de Eventos de Dominio](#4-flujo-de-eventos-de-dominio)
  - [Flujo CQRS Completo](#5-flujo-cqrs-completo-con-command-bus-y-query-bus)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Documentación Adicional](#documentación-adicional)

## 🏗️ Arquitectura

El proyecto implementa una arquitectura en capas siguiendo los principios de Clean Architecture y Hexagonal Architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                   Infrastructure Layer                      │
│  (Controllers, Repositories, API Clients, Event Handlers)   │
├─────────────────────────────────────────────────────────────┤
│                    Application Layer                        │
│      (Use Cases, Commands, Queries, Handlers, Buses)        │
├─────────────────────────────────────────────────────────────┤
│                      Domain Layer                           │
│    (Entities, Value Objects, Domain Events, Interfaces)     │
└─────────────────────────────────────────────────────────────┘
```

**Regla de Dependencias (Dependency Rule):**
- Las dependencias apuntan **hacia adentro** (hacia el dominio)
- **Domain** → No depende de nada (núcleo puro)
- **Application** → Solo depende de Domain (nunca de Infrastructure)
- **Infrastructure** → Puede depender de Domain y Application
- **Inversión de Dependencias (DIP)**: Se usan interfaces en Domain/Application, implementadas en Infrastructure

**Ejemplos aplicados:**
- ✅ **Correcto**: `Application/UseCases/` importa `Shared/Domain/Events/EventDispatcherInterface.py`
- ❌ **Incorrecto**: `Application/UseCases/` importa `Shared/Infrastructure/Events/EventDispatcher.py`
- ✅ **Correcto**: `Application/UseCases/` usa `Application/Serializers/HelloWorldSerializer.py` para serialización
- ❌ **Incorrecto**: `Application/UseCases/` usa `Infrastructure/Persistence/Mappers/HelloWorldMapper.py`

### Patrones Implementados

- ✅ **Hexagonal Architecture** - Separación entre dominio e infraestructura
- ✅ **Domain-Driven Design** - Entidades, Value Objects, Aggregates
- ✅ **CQRS** - Separación de Commands (escritura) y Queries (lectura)
- ✅ **Event-Driven** - Domain Events con EventDispatcher
- ✅ **Dependency Injection** - DI Container con dependency-injector
- ✅ **Repository Pattern** - Abstracción de persistencia
- ✅ **Use Cases** - Lógica de aplicación encapsulada

---

## 🔄 Flujos de la Aplicación

### 1. Flujo de Inicialización de la Aplicación

**Archivo inicial**: `app/app.py`

```
app.py (Flask App)
  │
  ├─► configureLogs(app)
  │     └─► config/log.py
  │           └─► Configura logging con archivos rotativos
  │
  ├─► configureSignals(app)
  │     └─► config/signals.py
  │           └─► Configura signal handlers (SIGTERM, SIGINT)
  │
  ├─► configureEnvironment(app)
  │     └─► config/environment.py
  │           └─► Carga variables de entorno (.env)
  │
  ├─► configureDatabase(app)
  │     └─► config/database.py
  │           └─► Inicializa SQLAlchemy con MySQL/SQLite
  │
  ├─► init_container(app)
  │     └─► config/container.py
  │           ├─► Inicializa DI Container
  │           ├─► Registra repositorios (write/read)
  │           ├─► Registra buses (CommandBus, QueryBus)
  │           ├─► Registra handlers (Commands, Queries, Events)
  │           ├─► Registra use cases
  │           └─► Registra EventDispatcher y suscriptores
  │
  ├─► exceptionHandler(app)
  │     └─► config/exceptionHandler.py
  │           └─► Configura manejadores de excepciones globales
  │
  └─► configureControllers(app)
        └─► config/controllers.py
              ├─► Registra v1ControllerBase (/api/v1)
              ├─► Registra toolsController (/tools)
              └─► Registra Swagger UI (/api/docs)
```

**Responsabilidades por archivo:**

| Archivo | Función | Invoca a |
|---------|---------|----------|
| `app.py` | Punto de entrada, inicializa Flask | Todos los configuradores |
| `config/log.py` | Configura sistema de logs | - |
| `config/signals.py` | Maneja señales del sistema | - |
| `config/environment.py` | Carga variables de entorno | - |
| `config/database.py` | Inicializa SQLAlchemy | - |
| `config/container.py` | Configura Dependency Injection | Todas las clases del sistema |
| `config/exceptionHandler.py` | Maneja excepciones globales | - |
| `config/controllers.py` | Registra todos los blueprints | Controllers |

---

### 2. Flujo de Escritura (Commands) - Crear HelloWorld

**Endpoint**: `POST /api/v1/hello-world/`

**⚠️ CQRS con Command Bus implementado**: Este flujo usa CommandBus en lugar de Use Case directo.

```
1. Cliente HTTP (POST /api/v1/hello-world/)
   └─► Body: {"greeting": "Hello World"}
         │
         ▼
2. Infrastructure/Controller/HelloWorldController.py
   └─► create_hello_world()
         ├─► Valida request.get_json()
         ├─► Crea el comando CQRS
         │     └─► CreateHelloWorldCommand(greeting_text=data['greeting'])
         ├─► Obtiene Command Bus del container
         │     └─► current_app.container.command_bus()
         ├─► Despacha comando: command_bus.dispatch(command)
         └─► Retorna: ControllerBase.format_response({"id": entity_id, "greeting": ...}, 201)
               │
               ▼
3. Shared/Application/CommandBus.py
   └─► dispatch(command)
         ├─► Busca handler registrado: CreateHelloWorldHandler
         └─► Invoca: handler.handle(command)
               │
               ▼
4. Application/CommandHandlers/CreateHelloWorldHandler.py
   └─► handle(command: CreateHelloWorldCommand)
         ├─► Crea Value Object
         │     └─► GreetingValueObject.create(command.greeting_text)
         │           └─► Domain/HelloWorld/ValueObjects/GreetingValueObject.py
         │                 ├─► Valida: no vacío, longitud < 255
         │                 └─► Retorna: GreetingValueObject instance
         │
         ├─► Crea entidad de dominio
         │     └─► HelloWorld.create(greeting)
         │           └─► Domain/HelloWorld/HelloWorld.py
         │                 ├─► Crea instancia
         │                 └─► Registra evento: HelloWorldCreated
         │
         ├─► Persiste en repositorio
         │     └─► repository.save(hello_world)
         │           └─► Infrastructure/Repository/HelloWorldWriteRepository.py
         │                 ├─► Mapea a modelo: HelloWorldMapper.toModel()
         │                 ├─► Ejecuta: db.session.add(model)
         │                 ├─► Ejecuta: db.session.commit()
         │                 └─► Retorna: HelloWorld con ID asignado
         │
         ├─► Publica eventos de dominio
         │     └─► event_dispatcher.publish_multiple(eventos)
         │           └─► Shared/Infrastructure/Events/EventDispatcher.py
         │                 ├─► Busca suscriptores para cada evento
         │                 ├─► Invoca: subscriber.handle(event)
         │                 │     ├─► Application/EventHandlers/HelloWorldCreatedLogger.py
         │                 │     │     └─► logger.info("HelloWorld creado")
         │                 │     └─► Infrastructure/Projections/HelloWorldProjection.py
         │                 │           └─► Actualiza read models (eventual consistency)
         │                 └─► Continúa aunque un suscriptor falle
         │
         └─► Retorna ID de la entidad creada
               └─► return saved_entity.id
                     └─► El controller construye la respuesta
                           │
                           ▼
5. Cliente HTTP recibe
   └─► Status: 201 Created
   └─► Body: {"id": 1, "greeting": "Hello World"}
```

**Archivos involucrados (en orden):**

| # | Archivo | Responsabilidad | Siguiente paso |
|---|---------|-----------------|----------------|
| 1 | `Infrastructure/Controller/HelloWorldController.py` | Recibe HTTP request, crea comando | Command Bus |
| 2 | `Application/Commands/CreateHelloWorldCommand.py` | Comando inmutable con datos | Command Bus |
| 3 | `Shared/Application/CommandBus.py` | Despacha comando al handler | Command Handler |
| 4 | `Application/CommandHandlers/CreateHelloWorldHandler.py` | Ejecuta lógica de negocio | Value Object |
| 5 | `Domain/HelloWorld/ValueObjects/GreetingValueObject.py` | Valida reglas del greeting | Entidad |
| 6 | `Domain/HelloWorld/HelloWorld.py` | Entidad de dominio, registra eventos | Repositorio |
| 7 | `Infrastructure/Repository/HelloWorldWriteRepository.py` | Persiste en base de datos (CQRS Puro) | Event Dispatcher |
| 8 | `Shared/Infrastructure/Events/EventDispatcher.py` | Distribuye eventos a suscriptores | Event Handlers |
| 9 | `Application/EventHandlers/HelloWorldCreatedLogger.py` | Registra log del evento | - |
| 10 | `Infrastructure/Projections/HelloWorldProjection.py` | Actualiza read models | Controller |

---

### 3. Flujo de Lectura (Queries) - Obtener Todos los HelloWorld

**Endpoint**: `GET /api/v1/hello-world/`

**⚠️ CQRS Puro implementado**: Este flujo usa QueryBus en lugar del write repository.

```
1. Cliente HTTP (GET /api/v1/hello-world/)
         │
         ▼
2. Infrastructure/Controller/HelloWorldController.py
   └─► get_all_hello_world()
         ├─► Obtiene use case del container
         │     └─► current_app.container.get_all_hello_world_use_case()
         ├─► Ejecuta: use_case.execute()
         └─► Retorna: ControllerBase.format_response(result, 200)
               │
               ▼
3. Application/UseCases/HelloWorld/GetAllHelloWorldUseCase.py
   └─► execute()
         ├─► Crea Query
         │     └─► GetAllHelloWorldQuery()
         │
         ├─► Despacha al Query Bus
         │     └─► query_bus.dispatch(query)
         │           └─► Shared/Application/QueryBus.py
         │                 ├─► Busca handler: GetAllHelloWorldHandler
         │                 └─► Invoca: handler.handle(query)
         │
         ├─► Query Handler procesa
         │     └─► Application/QueryHandlers/GetAllHelloWorldHandler.py
         │           └─► Usa Read Repository (optimizado para lectura)
         │                 └─► read_repository.find_all()
         │                       └─► Infrastructure/Repository/HelloWorldReadRepository.py
         │                             ├─► Query SQL optimizada
         │                             ├─► Convierte a ReadModel
         │                             └─► Retorna: HelloWorldListReadModel
         │
         └─► Serializa lista desde ReadModel
               └─► [item.to_dict() for item in result.items]
                     └─► Retorna: [{"id": 1, "greeting": "..."}, ...]
                           │
                           ▼
4. Cliente HTTP recibe
   └─► Status: 200 OK
   └─► Body: [{"id": 1, "greeting": "Hello World"}, ...]
```

**Archivos involucrados (en orden):**

| # | Archivo | Responsabilidad | Siguiente paso |
|---|---------|-----------------|----------------|
| 1 | `Infrastructure/Controller/HelloWorldController.py` | Recibe HTTP request | Use Case |
| 2 | `Application/UseCases/HelloWorld/GetAllHelloWorldUseCase.py` | Crea Query y usa QueryBus | QueryBus |
| 3 | `Shared/Application/QueryBus.py` | Despacha query al handler correcto | Query Handler |
| 4 | `Application/QueryHandlers/GetAllHelloWorldHandler.py` | Ejecuta query sin lógica de dominio | Read Repository |
| 5 | `Infrastructure/Repository/HelloWorldReadRepository.py` | Consulta optimizada para lectura | ReadModel |
| 6 | `Application/ReadModels/HelloWorldListReadModel.py` | DTO para respuesta paginada | Controller |

---

### 4. Flujo de Eventos de Dominio

**Patrón Observer/Pub-Sub implementado**

```
1. Entidad registra evento
   └─► Domain/HelloWorld/HelloWorld.py
         └─► self.record_event(HelloWorldCreated(...))
               └─► Shared/Domain/Entities/EntityBase.py
                     └─► self._domain_events.append(event)
                           │
                           ▼
2. Use Case obtiene eventos
   └─► saved_entity.pull_domain_events()
         └─► Limpia lista y retorna eventos acumulados
               │
               ▼
3. EventDispatcher distribuye
   └─► Shared/Infrastructure/Events/EventDispatcher.py
         ├─► publish_multiple(events)
         │     └─► Para cada evento: publish(event)
         │
         ├─► Busca suscriptores por nombre del evento
         │     └─► self._subscribers[event_name]
         │
         └─► Llama handle() de cada suscriptor
               ├─► Application/EventHandlers/HelloWorldCreatedLogger.py
               │     └─► handle(event)
               │           └─► logger.info(f"HelloWorld creado - ID: {event.id}")
               │
               └─► Infrastructure/Projections/HelloWorldProjection.py
                     └─► handle(event)
                           ├─► Si HelloWorldCreated: _on_hello_world_created()
                           ├─► Si HelloWorldDeleted: _on_hello_world_deleted()
                           └─► Actualiza cache/índices/read models
```

**Suscriptores de Eventos:**

| Suscriptor | Archivo | Eventos Escuchados | Acción |
|------------|---------|-------------------|--------|
| **HelloWorldCreatedLogger** | `Application/EventHandlers/HelloWorldCreatedLogger.py` | `HelloWorldCreated` | Registra log de creación |
| **HelloWorldDeletedLogger** | `Application/EventHandlers/HelloWorldDeletedLogger.py` | `HelloWorldDeleted` | Registra log de eliminación |
| **HelloWorldProjection** | `Infrastructure/Projections/HelloWorldProjection.py` | `HelloWorldCreated`, `HelloWorldDeleted` | Sincroniza read models (CQRS) |

**Nota importante sobre Dependency Inversion Principle (DIP)**: 

El proyecto aplica DIP usando `EventDispatcherInterface` (capa Domain) que es implementada por `EventDispatcher` (capa Infrastructure). Esto permite que la capa de Aplicación dependa de abstracciones, no de implementaciones concretas:

```python
# ✅ Correcto - Use Case depende de la interfaz (Domain)
from Shared.Domain.Events.EventDispatcherInterface import EventDispatcherInterface

class CreateHelloWorldUseCase:
    def __init__(self, repository, event_dispatcher: EventDispatcherInterface):
        self.event_dispatcher = event_dispatcher  # Interfaz, no implementación

# ❌ Incorrecto - Use Case NO debe depender de Infrastructure
from Shared.Infrastructure.Events.EventDispatcher import EventDispatcher
```

El `EventDispatcher` soporta suscriptores que escuchan un único evento o múltiples eventos:

```python
# Suscriptor a un evento
def subscribed_to(self):
    return HelloWorldCreated

# Suscriptor a múltiples eventos (ej: Projections)
def subscribed_to(self):
    return [HelloWorldCreated, HelloWorldDeleted]
```

---

### 5. Flujo CQRS Completo (con Command Bus y Query Bus)

**CQRS separa las operaciones de escritura (Commands) de las de lectura (Queries)**

#### 5.1 Flujo de Command (Escritura)

**✅ CQRS Puro IMPLEMENTADO**: El flujo POST ahora usa Command Bus correctamente.

```
1. Controller recibe request de escritura
   └─► Infrastructure/Controller/HelloWorldController.py
         ├─► POST /api/v1/hello-world/
         ├─► Body: {"greeting": "Hello World"}
         └─► Crea comando y lo despacha
               │
               ▼
2. Crea Command (inmutable)
   └─► Application/Commands/CreateHelloWorldCommand.py
         ├─► @dataclass(frozen=True)
         ├─► greeting_text: str
         └─► Valida en __post_init__()
               │
               ▼
3. Despacha Command al Bus
   └─► command_bus = current_app.container.command_bus()
   └─► command_bus.dispatch(command)
         └─► Shared/Application/CommandBus.py
               ├─► Busca handler registrado por tipo
               ├─► Obtiene: self._handlers[CreateHelloWorldCommand]
               └─► Invoca: handler.handle(command)
                     │
                     ▼
4. Command Handler procesa (ej: Update/Delete)
   └─► Application/CommandHandlers/UpdateHelloWorldHandler.py
         ├─► Valida existencia con Read Repository
         │     └─► read_repository.find_by_id(id)  ⬅️ CQRS Puro
         │           └─► Solo para validación, NO para modificar
         │
         ├─► Crea Value Object: Greeting.create()
         ├─► Modifica Entidad: hello_world.greeting = new_greeting
         ├─► Persiste con Write Repository
         │     └─► repository.save(hello_world)  ⬅️ CQRS Puro
         │           └─► Infrastructure/Repository/HelloWorldWriteRepository.py
         │                 ├─► Solo métodos: save() y delete()
         │                 ├─► NO tiene findById() ni findAll()
         │                 └─► Optimizado SOLO para escritura
         │
         ├─► Publica eventos: event_dispatcher.publish_multiple()
         └─► Retorna resultado (ID o booleano)
               │
               ▼
5. Write Repository persiste (SOLO escritura)
   └─► Infrastructure/Repository/HelloWorldWriteRepository.py
         ├─► Métodos disponibles: save(), delete()
         ├─► Métodos ELIMINADOS: find_by_id(), find_all() ⬅️ CQRS Puro
         ├─► Mantiene integridad de dominio
         └─► Ejecuta: db.session.commit()
               │
               ▼
6. Projection sincroniza read models (eventual consistency)
   └─► Infrastructure/Projections/HelloWorldProjection.py
         ├─► Escucha: HelloWorldCreated, HelloWorldDeleted
         ├─► Actualiza read models en Read Repository
         ├─► Puede actualizar cache (Redis)
         └─► Puede indexar (Elasticsearch)
```

**✅ Separación CQRS Pura en Command Handlers:**

```python
# UpdateHelloWorldHandler recibe AMBOS repositorios
def __init__(
    self,
    repository: HelloWorldRepositoryInterface,      # Write Repository
    read_repository: HelloWorldReadRepository,     # Read Repository
    event_dispatcher: EventDispatcher
):
    self.repository = repository           # Para save()
    self.read_repository = read_repository # Para validaciones (find_by_id)
```

#### 5.2 Flujo de Query (Lectura)

```
1. Controller recibe request de lectura
   └─► Infrastructure/Controller/HelloWorldController.py
         │
         ▼
2. Crea Query (inmutable)
   └─► Application/Queries/GetAllHelloWorldQuery.py
         ├─► @dataclass(frozen=True)
         ├─► limit: Optional[int]
         ├─► offset: Optional[int]
         └─► Valida parámetros de paginación
               │
               ▼
3. Despacha Query al Bus
   └─► query_bus.dispatch(query)
         └─► Shared/Application/QueryBus.py
               ├─► Busca handler registrado por tipo
               ├─► Obtiene: self._handlers[GetAllHelloWorldQuery]
               └─► Invoca: handler.handle(query)
                     │
                     ▼
4. Query Handler procesa
   └─► Application/QueryHandlers/GetAllHelloWorldHandler.py
         ├─► NO tiene lógica de dominio
         ├─► Solo recupera datos
         └─► Usa: read_repository.find_all()
               │
               ▼
5. Read Repository consulta (optimizado)
   └─► Infrastructure/Repository/HelloWorldReadRepository.py
         ├─► Query SQL optimizada para lectura
         ├─► Puede usar índices específicos
         ├─► Puede hacer joins optimizados
         ├─► Convierte a: HelloWorldReadModel
         └─► Retorna: List[HelloWorldReadModel]
               │
               ▼
6. Read Model (DTO sin lógica)
   └─► Application/ReadModels/HelloWorldReadModel.py
         ├─► Puro DTO (Data Transfer Object)
         ├─► Sin comportamiento de dominio
         └─► Optimizado para serialización
               │
               ▼
7. Controller serializa respuesta
   └─► read_model.to_dict()
         └─► Retorna JSON al cliente
```

**Diferencias clave entre Write y Read:**

| Aspecto | Write (Commands) | Read (Queries) |
|---------|-----------------|---------------|
| **Objetivo** | Modificar estado | Solo consultar |
| **Repositorio** | `HelloWorldRepository` (write) ⬅️ **SOLO save() y delete()** | `HelloWorldReadRepository` (read) |
| **Modelo** | Entidad de dominio (`HelloWorld`) | DTO sin lógica (`HelloWorldReadModel`) |
| **Validaciones** | Reglas de negocio complejas | Solo validaciones de parámetros |
| **Eventos** | Publica eventos de dominio | NO publica eventos |
| **Transacciones** | Requiere transacciones ACID | Puede usar cache/réplicas |
| **Optimización** | Integridad de datos | Velocidad de lectura |
| **Separación CQRS Pura** | ✅ Write Repository sin métodos de lectura | ✅ Read Repository solo para queries |
| **Validaciones en Handlers** | Usa Read Repository para verificar existencia | N/A |

**✅ Implementación CQRS Pura:**

El proyecto implementa **CQRS Puro** con separación estricta:

- **Write Repository** (`HelloWorldRepository`):
  - ✅ Métodos: `save()`, `delete()`
  - ❌ Eliminados: `find_by_id()`, `find_all()`
  - Solo para operaciones de escritura (CUD)

- **Read Repository** (`HelloWorldReadRepository`):
  - ✅ Métodos: `find_by_id()`, `find_all()`, `search()`
  - Solo para operaciones de lectura
  - Optimizado con índices y queries específicas

- **Command Handlers** (UpdateHelloWorldHandler, DeleteHelloWorldHandler):
  - Inyectan **ambos repositorios**:
    - `repository` (write) para persistir
    - `read_repository` (read) para validaciones
  - Mantienen separación: lecturas usan read, escrituras usan write

---

## 📁 Estructura del Proyecto

```
app/
├── app.py                          # Punto de entrada Flask
├── config/                         # Configuración de la aplicación
│   ├── container.py               # DI Container (registra todos los componentes)
│   ├── controllers.py             # Registro de controllers/blueprints
│   ├── database.py                # Configuración de SQLAlchemy
│   ├── environment.py             # Variables de entorno
│   ├── exceptionHandler.py        # Manejo global de excepciones
│   ├── log.py                     # Configuración de logging
│   └── signals.py                 # Handlers de señales del sistema
│
├── Domain/                         # 🟢 Capa de Dominio (lógica de negocio)
│   └── HelloWorld/
│       ├── HelloWorld.py          # Entidad de dominio (Aggregate Root)
│       ├── HelloWorldRepositoryInterface.py  # Puerto (interfaz)
│       ├── Events/
│       │   ├── HelloWorldCreated.py         # Evento de dominio
│       │   └── HelloWorldDeleted.py         # Evento de dominio
│       ├── Exceptions/
│       │   └── IncorrectGreetingException.py
│       └── ValueObjects/
│           └── Greeting.py        # Value Object con validaciones
│
├── Application/                    # 🟡 Capa de Aplicación (casos de uso)
│   ├── UseCases/                  # Use Cases (legacy, compatibilidad)
│   │   └── HelloWorld/
│   │       ├── CreateHelloWorldUseCase.py
│   │       ├── GetAllHelloWorldUseCase.py
│   │       ├── GetHelloWorldByIdUseCase.py
│   │       └── DeleteHelloWorldUseCase.py
│   │
│   ├── Commands/                  # 🔵 CQRS - Commands (escritura)
│   │   ├── CreateHelloWorldCommand.py
│   │   ├── UpdateHelloWorldCommand.py
│   │   └── DeleteHelloWorldCommand.py
│   │
│   ├── CommandHandlers/           # 🔵 CQRS - Command Handlers
│   │   ├── CreateHelloWorldHandler.py
│   │   ├── UpdateHelloWorldHandler.py
│   │   └── DeleteHelloWorldHandler.py
│   │
│   ├── Serializers/               # Serialización para presentación
│   │   └── HelloWorldSerializer.py # Serializa entidades → dict/JSON
│   │                               # Solo: to_dict()
│   │
│   ├── Queries/                   # 🔵 CQRS - Queries (lectura)
│   │   ├── GetAllHelloWorldQuery.py
│   │   ├── GetHelloWorldByIdQuery.py
│   │   └── SearchHelloWorldQuery.py
│   │
│   ├── QueryHandlers/             # 🔵 CQRS - Query Handlers
│   │   ├── GetAllHelloWorldHandler.py
│   │   ├── GetHelloWorldByIdHandler.py
│   │   └── SearchHelloWorldHandler.py
│   │
│   ├── ReadModels/                # 🔵 CQRS - Read Models (DTOs)
│   │   ├── HelloWorldReadModel.py
│   │   └── HelloWorldListReadModel.py
│   │
│   └── EventHandlers/             # Event Subscribers
│       ├── HelloWorldCreatedLogger.py
│       └── HelloWorldDeletedLogger.py
│
├── Infrastructure/                 # 🔴 Capa de Infraestructura (adaptadores)
│   ├── Controller/
│   │   ├── HelloWorldController.py      # REST API Controller
│   │   └── MoviesController.py
│   │
│   ├── Repository/
│   │   ├── HelloWorldWriteRepository.py # ✅ Write Repository (CQRS Puro)
│   │   │                                 # Solo: save(), delete()
│   │   ├── HelloWorldReadRepository.py  # ✅ Read Repository (CQRS Puro)
│   │   │                                 # Solo: find_by_id(), find_all(), search()
│   │   └── ShowsRepository.py           # API externa
│   │
│   ├── Projections/               # 🔵 CQRS - Event-driven sync
│   │   └── HelloWorldProjection.py      # Sincroniza read models
│   │
│   └── Persistence/
│       ├── database.py            # Instancia de SQLAlchemy
│       ├── Mappers/
│       │   └── HelloWorldMapper.py      # Mapeo Domain ↔ DB Model
│       │                                # Solo: toDomain(), toModel()
│       └── SQLAlchemy/
│           └── HelloWorldModel.py       # Modelo de persistencia
│
└── Shared/                         # Componentes compartidos
    ├── Application/
    │   ├── CommandBus.py          # 🔵 CQRS - Command Bus
    │   ├── QueryBus.py            # 🔵 CQRS - Query Bus
    │   ├── CommandHandler.py      # 🔵 Interface ABC para Command Handlers
    │   └── QueryHandler.py        # 🔵 Interface ABC para Query Handlers
    │
    ├── Domain/
    │   ├── Entities/
    │   │   └── EntityBase.py      # Base para entidades (con eventos)
    │   ├── Events/
    │   │   ├── DomainEvent.py     # Base para eventos
    │   │   ├── DomainEventSubscriber.py  # Interfaz suscriptor
    │   │   └── EventDispatcherInterface.py  # 🔵 Interfaz (DIP)
    │   └── ValueObjects/
    │       └── StringValueObject.py
    │
    └── Infrastructure/
        ├── Controller/
        │   ├── Controller.py      # Base de controllers
        │   └── SwaggerController.py  # Documentación API
        └── Events/
            └── EventDispatcher.py  # Pub/Sub de eventos
```

---

## 📚 Documentación Adicional

### Guías Disponibles

- **[ARCHITECTURE_SUMMARY.md](doc/ARCHITECTURE_SUMMARY.md)** - 🆕 Resumen rápido de la arquitectura
  - Validación de patrones (Hexagonal, DDD, CQRS)
  - Estructura de capas visual
  - Interfaces clave
  - Guía para agregar nuevos módulos

- **[CQRS_MIGRATION.md](doc/CQRS_MIGRATION.md)** - Migración a CQRS Completo
  - Flujo POST refactorizado con Command Bus
  - Comparación antes/después
  - Componentes CQRS (Command, Handler, Bus)
  - Correcciones de imports circulares
  - Tests actualizados

- **[TESTING.md](doc/TESTING.md)** - Guía completa de testing
  - Tests unitarios e integración
  - Tests CQRS (Commands, Queries, Handlers, Buses)
  - Cobertura de código
  - Fixtures y mejores prácticas

- **[SWAGGER.md](doc/SWAGGER.md)** - Documentación de API
  - Configuración de Swagger UI
  - Documentación OpenAPI 3.0.3
  - Endpoints disponibles
  - Ejemplos de uso

### Conceptos Clave

#### Hexagonal Architecture (Puertos y Adaptadores)

- **Dominio** (núcleo): Lógica de negocio pura, sin dependencias externas
- **Puertos**: Interfaces que definen contratos (ej: `HelloWorldRepositoryInterface`)
- **Adaptadores**: Implementaciones concretas (ej: `HelloWorldRepository` con SQLAlchemy)

#### CQRS (Command Query Responsibility Segregation) - **Implementación Pura** ✅

El proyecto implementa **CQRS Puro** con separación estricta entre operaciones de escritura y lectura:

- **Commands**: Modifican estado (Create, Update, Delete)
  - Pasan por validaciones de dominio
  - Publican eventos de dominio
  - Usan **Write Repository** (solo `save()` y `delete()`)
  - **Validaciones** usan **Read Repository** para verificar existencia
  - Inyectan ambos repositorios cuando necesitan leer para validar
  
- **Queries**: Solo leen datos (Get, Search)
  - Sin lógica de negocio
  - Optimizadas para lectura
  - Usan **Read Repository** (solo métodos de consulta)
  - Retornan DTOs (Read Models)

**Separación en Repositorios:**

```python
# Write Repository - SOLO escritura
class HelloWorldRepository:
    def save(self, entity): ...    # ✅ Persistir
    def delete(self, id): ...       # ✅ Eliminar
    # ❌ NO tiene find_by_id() ni find_all()

# Read Repository - SOLO lectura  
class HelloWorldReadRepository:
    def find_by_id(self, id): ...   # ✅ Buscar por ID
    def find_all(...): ...          # ✅ Listar todos
    def search(...): ...            # ✅ Buscar con filtros
    # ❌ NO tiene save() ni delete()
```

**Validaciones en Command Handlers:**

```python
# UpdateHelloWorldHandler - Usa ambos repositorios
class UpdateHelloWorldHandler:
    def __init__(self, repository, read_repository, event_dispatcher):
        self.repository = repository              # Write Repository
        self.read_repository = read_repository    # Read Repository
    
    def handle(self, command):
        # 1. Validar existencia con Read Repository
        entity = self.read_repository.find_by_id(command.id)  # ✅ Lectura
        
        # 2. Modificar entidad (dominio)
        entity.greeting = new_greeting
        
        # 3. Persistir con Write Repository
        self.repository.save(entity)  # ✅ Escritura
```

**Beneficios de CQRS Puro:**
- ✅ Separación clara de responsabilidades
- ✅ Optimización independiente (write vs read)
- ✅ Escalabilidad: diferentes bases de datos para lectura/escritura
- ✅ Mantenibilidad: cambios en escritura no afectan lectura
- ✅ Consistencia eventual con Projections

#### Mappers vs Serializers - Separación de Responsabilidades

El proyecto utiliza **Mappers** y **Serializers** con responsabilidades claramente separadas:

**1. Infrastructure/Persistence/Mappers/HelloWorldMapper** (Mapper - Persistencia)
```python
class HelloWorldMapper:
    @staticmethod
    def toDomain(model: HelloWorldModel) -> HelloWorld:
        """DB Model → Domain Entity"""
        # Convierte modelo SQLAlchemy a entidad de dominio
        
    @staticmethod
    def toModel(entity: HelloWorld) -> HelloWorldModel:
        """Domain Entity → DB Model"""
        # Convierte entidad de dominio a modelo SQLAlchemy
```

**Responsabilidad:** Traducir entre modelos de persistencia (SQLAlchemy) y entidades de dominio.  
**Usado por:** Repositorios (Write/Read)

**2. Application/Serializers/HelloWorldSerializer** (Serializer - Presentación)
```python
class HelloWorldSerializer:
    @staticmethod
    def to_dict(entity: HelloWorld) -> dict:
        """Domain Entity → Dict/JSON"""
        # Serializa entidad para API/presentación
```

**Responsabilidad:** Serializar entidades de dominio para respuestas HTTP/JSON.  
**Usado por:** Use Cases, Controllers

**Regla arquitectónica:**
- ✅ Application layer **NUNCA** importa el mapper de Infrastructure
- ✅ Infrastructure layer **NUNCA** serializa a JSON/dict (responsabilidad de Application)
- ✅ **Mapper** = transformación bidireccional (Entity ↔ Model)
- ✅ **Serializer** = transformación unidireccional de salida (Entity → JSON)

#### Event-Driven Architecture

- **Domain Events**: Hechos que ocurrieron en el dominio
- **EventDispatcher**: Patrón Observer/Pub-Sub
- **Event Handlers**: Reaccionan a eventos (logging, notificaciones, etc.)
- **Projections**: Sincronización de read models (CQRS)
- **Projections**: Sincronizan read models (eventual consistency)

#### Dependency Injection

- **Container**: `config/container.py` gestiona todas las dependencias
- **Providers**: Factory, Singleton patterns
- **Registro automático**: Handlers se registran en buses al iniciar

---

## 🚀 Comandos Útiles

```bash
# Ejecutar aplicación
python app/app.py

# Ejecutar tests
pytest

# Tests con cobertura
pytest --cov=app --cov-report=html

# Tests específicos CQRS
pytest tests/unit/Application/ tests/unit/Shared/ -v

# Ver documentación API
# Abrir en navegador: http://localhost:5000/api/docs
```

---

## 🎯 Beneficios de esta Arquitectura

1. **Separación de Responsabilidades**: Cada capa tiene un propósito claro
2. **Testabilidad**: Fácil hacer tests unitarios con mocks
3. **Mantenibilidad**: Cambios en infraestructura no afectan dominio
4. **Escalabilidad**: Read y Write pueden escalar independientemente
5. **Flexibilidad**: Fácil cambiar base de datos o agregar cache
6. **Auditabilidad**: Domain Events registran todos los cambios
7. **Eventual Consistency**: Projections sincronizan modelos de lectura

---

**Proyecto desarrollado con ❤️ siguiendo principios de Clean Architecture y DDD**
