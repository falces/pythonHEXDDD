# 📐 Resumen de Arquitectura - Python HEX DDD CQRS

## ✅ Estado de Validación (Actualizado: 04 Dic 2025)

| Patrón | Estado | Notas |
|--------|--------|-------|
| **Arquitectura Hexagonal** | ✅ Completo | Capas bien separadas |
| **DDD** | ✅ Completo | Aggregate Roots, Value Objects, Domain Events, Entities |
| **CQRS** | ✅ Completo | CommandBus + QueryBus con interfaces |
| **Arquitectura Modular** | ✅ Completo | Módulos independientes (HelloWorld, Admin, Admin2) |
| **Dependency Inversion** | ✅ Completo | Todas las dependencias usan interfaces |
| **Tests** | ✅ 281+ pasando | 90%+ cobertura |

---

## 🏗️ Módulos del Sistema

### Módulo HelloWorld (Principal)
- Ubicación: `app/Domain/HelloWorld/`, `app/Application/`, `app/Infrastructure/`
- Entidad: `HelloWorld` (Aggregate Root)
- CQRS: Commands, Queries, Handlers completos
- Events: `HelloWorldCreated`, `HelloWorldUpdated`, `HelloWorldDeleted`

### Módulo Admin (Hexagonal/DDD/CQRS)
- Ubicación: `app/Admin/` (estructura autocontenida)
- Entidad: `User` (Aggregate Root) con `UserAddress` (Entidad hija)
- CQRS Completo:
  - Commands User: `CreateUserCommand`, `UpdateUserCommand`, `DeleteUserCommand`
  - Commands Address: `AddUserAddressCommand`, `UpdateUserAddressCommand`, `RemoveUserAddressCommand`
  - Queries: `GetUserByIdQuery`, `GetAllUsersQuery`
- Events: `UserCreated`, `UserAddressAdded`, `UserAddressRemoved`
- Value Objects: `UsernameValueObject`, `EmailValueObject`, `UuidValueObject`
- Validators: `CreateUserValidator`, `UpdateUserValidator`, `AddUserAddressValidator`, `UpdateUserAddressValidator`
- Base Repository: `BaseWriteRepository` (manejo centralizado de errores)

### Módulo Admin2 (Arquitectura Simple)
- Ubicación: `app/Admin2/` (3 archivos)
- Arquitectura tradicional sin DDD/CQRS/Hexagonal
- Estructura: `models.py`, `services.py`, `controller.py`
- CRUD completo en ~150 líneas de código

---

## 🏗️ Estructura de Capas

```
┌─────────────────────────────────────────────────────────────────┐
│                    Infrastructure Layer                         │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐  │
│  │ Controllers      │  │ Repositories     │  │ Persistence  │  │
│  │ (HTTP Adapters)  │  │ (Implementations)│  │ (SQLAlchemy) │  │
│  └────────┬─────────┘  └────────┬─────────┘  └──────────────┘  │
└───────────┼─────────────────────┼───────────────────────────────┘
            │                     │
            │                     │ implements
            ▼                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Application Layer                            │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐  │
│  │ Commands/Queries │  │ CommandHandlers  │  │ QueryHandlers│  │
│  │ (DTOs inmutables)│  │ (impl. interface)│  │ (impl. interf)│  │
│  └──────────────────┘  └────────┬─────────┘  └──────┬───────┘  │
│  ┌──────────────────┐           │                   │          │
│  │ CommandBus      │◄───────────┘                   │          │
│  │ QueryBus        │◄───────────────────────────────┘          │
│  └──────────────────┘                                          │
│  ┌──────────────────┐  ┌──────────────────┐                    │
│  │ ReadModels      │  │ EventHandlers    │                    │
│  │ (proyecciones)  │  │ (side effects)   │                    │
│  └──────────────────┘  └──────────────────┘                    │
└─────────────────────────────────────────────────────────────────┘
            │                     ▲
            │ depends on          │ implements
            ▼                     │
┌─────────────────────────────────────────────────────────────────┐
│                      Domain Layer (Core)                        │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐  │
│  │ Aggregate Roots  │  │ Value Objects    │  │ Domain Events│  │
│  │ (HelloWorld)     │  │ (Greeting, etc.) │  │ (Created,etc)│  │
│  └──────────────────┘  └──────────────────┘  └──────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Repository Interfaces (Ports)               │  │
│  │  HelloWorldRepositoryInterface (Write)                   │  │
│  │  HelloWorldReadRepositoryInterface (Read)                │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Flujo CQRS

### Commands (Escritura)

```
Controller
    │
    ▼
CreateHelloWorldCommand (frozen dataclass)
    │
    ▼
CommandBus.dispatch(command)
    │
    ▼ (busca handler por tipo)
CreateHelloWorldHandler : CommandHandler (ABC)
    │
    ├─→ GreetingValueObject.create() [Domain]
    ├─→ HelloWorld.create()          [Domain]
    ├─→ repository.save()            [Interface → Impl]
    └─→ event_dispatcher.publish()   [Domain Events]
    │
    ▼
return entity_id (int)
    │
    ▼
Controller consulta QueryBus para obtener datos completos (opcional)
```

### Queries (Lectura)

```
Controller
    │
    ▼
GetAllHelloWorldQuery (frozen dataclass)
    │
    ▼
QueryBus.dispatch(query)
    │
    ▼ (busca handler por tipo)
GetAllHelloWorldHandler : QueryHandler (ABC)
    │
    └─→ read_repository.find_all()   [Interface → Impl]
    │
    ▼
return List[HelloWorldReadModel]
```

---

## 🎯 Interfaces Clave

### Handler Interfaces (ABCs)

```python
# app/Shared/Application/CommandHandler.py
class CommandHandler(ABC):
    @abstractmethod
    def handle(self, command: Any) -> Any:
        pass

# app/Shared/Application/QueryHandler.py
class QueryHandler(ABC):
    @abstractmethod
    def handle(self, query: Any) -> Any:
        pass
```

### Repository Interfaces (Domain)

```python
# app/Domain/HelloWorld/HelloWorldRepositoryInterface.py
class HelloWorldRepositoryInterface(ABC):
    @abstractmethod
    def save(self, hello_world: HelloWorld) -> HelloWorld:
        pass
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        pass

# app/Domain/HelloWorld/HelloWorldReadRepositoryInterface.py
class HelloWorldReadRepositoryInterface(ABC):
    @abstractmethod
    def find_by_id(self, id: int) -> Optional[any]:
        pass
    
    @abstractmethod
    def find_all(self, limit, offset, sort_by, sort_order) -> List[any]:
        pass
    
    @abstractmethod
    def search(self, search_text, limit, offset) -> List[any]:
        pass
    
    @abstractmethod
    def count(self) -> int:
        pass
```

---

## 📁 Estructura de Carpetas

```
app/
├── Admin/                          # 🆕 Módulo Admin (Hexagonal/DDD/CQRS)
│   ├── Application/
│   │   ├── Commands/
│   │   │   ├── CreateUserCommand.py
│   │   │   ├── UpdateUserCommand.py
│   │   │   └── DeleteUserCommand.py
│   │   ├── CommandHandlers/
│   │   │   ├── CreateUserHandler.py
│   │   │   ├── UpdateUserHandler.py
│   │   │   └── DeleteUserHandler.py
│   │   ├── Queries/
│   │   │   ├── GetUserByIdQuery.py
│   │   │   └── GetAllUsersQuery.py
│   │   ├── QueryHandlers/
│   │   │   ├── GetUserByIdHandler.py
│   │   │   └── GetAllUsersHandler.py
│   │   └── ReadModels/
│   │       └── UserReadModel.py
│   ├── Domain/
│   │   ├── User.py                 # Aggregate Root
│   │   ├── Entities/
│   │   │   └── UserAddress.py      # Entidad hija del agregado
│   │   ├── Repository/
│   │   │   ├── UserWriteRepositoryInterface.py
│   │   │   └── UserReadRepositoryInterface.py
│   │   ├── Events/
│   │   │   ├── UserCreated.py
│   │   │   ├── UserAddressAdded.py
│   │   │   └── UserAddressRemoved.py
│   │   ├── Exceptions/
│   │   │   ├── IncorrectUsernameException.py
│   │   │   └── IncorrectEmailException.py
│   │   └── ValueObjects/
│   │       ├── UsernameValueObject.py
│   │       └── EmailValueObject.py
│   └── Infrastructure/
│       ├── Controller/
│       │   └── AdminUserController.py  # CRUD completo
│       ├── Repository/
│       │   ├── UserWriteRepository.py
│       │   └── UserReadRepository.py
│       ├── Validators/
│       │   └── RequestValidators.py    # CreateUserValidator, UpdateUserValidator
│       └── Persistence/
│           ├── SQLAlchemy/
│           │   ├── UserModel.py
│           │   └── UserAddressModel.py
│           └── Mappers/
│               ├── UserMapper.py
│               └── UserAddressMapper.py
│
├── Admin2/                         # 🆕 Módulo Admin2 (Arquitectura Simple)
│   ├── models.py                   # Modelo SQLAlchemy
│   ├── services.py                 # Lógica de negocio
│   └── controller.py               # Endpoints REST
│
├── Application/                    # Capa de Aplicación (HelloWorld)
│   ├── Commands/                   # Comandos inmutables (dataclass frozen)
│   │   ├── CreateHelloWorldCommand.py
│   │   ├── UpdateHelloWorldCommand.py
│   │   └── DeleteHelloWorldCommand.py
│   ├── CommandHandlers/            # Handlers que implementan CommandHandler
│   │   ├── CreateHelloWorldHandler.py
│   │   ├── UpdateHelloWorldHandler.py
│   │   └── DeleteHelloWorldHandler.py
│   ├── Queries/                    # Queries inmutables (dataclass frozen)
│   │   ├── GetAllHelloWorldQuery.py
│   │   ├── GetHelloWorldByIdQuery.py
│   │   └── SearchHelloWorldQuery.py
│   ├── QueryHandlers/              # Handlers que implementan QueryHandler
│   │   ├── GetAllHelloWorldHandler.py
│   │   ├── GetHelloWorldByIdHandler.py
│   │   └── SearchHelloWorldHandler.py
│   ├── ReadModels/                 # DTOs para lecturas
│   │   ├── HelloWorldReadModel.py
│   │   └── HelloWorldListReadModel.py
│   ├── EventHandlers/              # Manejadores de eventos de dominio
│   │   ├── HelloWorldCreatedLogger.py
│   │   ├── HelloWorldUpdatedLogger.py
│   │   └── HelloWorldDeletedLogger.py
│   └── UseCases/                   # Use Cases (solo para módulos sin CQRS)
│       └── Shows/                  # Shows aún usa Use Cases tradicionales
│           ├── SearchShowsUseCase.py
│           └── GetShowByIdUseCase.py
│
├── Domain/                         # Capa de Dominio (HelloWorld)
│   ├── HelloWorld/
│   │   ├── HelloWorld.py           # Aggregate Root
│   │   ├── HelloWorldRepositoryInterface.py    # Puerto Write
│   │   ├── HelloWorldReadRepositoryInterface.py # Puerto Read
│   │   ├── Events/
│   │   │   ├── HelloWorldCreated.py
│   │   │   ├── HelloWorldUpdated.py
│   │   │   └── HelloWorldDeleted.py
│   │   ├── Exceptions/
│   │   │   └── IncorrectGreetingException.py
│   │   └── ValueObjects/
│   │       └── GreetingValueObject.py
│   └── Show/
│       ├── Show.py                 # Aggregate Root
│       └── ValueObjects/
│
├── Infrastructure/                 # Capa de Infraestructura
│   ├── Controller/                 # Adaptadores HTTP
│   │   └── HelloWorldController.py
│   ├── Repository/                 # Implementaciones de repositorios
│   │   ├── HelloWorldWriteRepository.py  # Impl. Write
│   │   └── HelloWorldReadRepository.py   # Impl. Read
│   ├── Persistence/
│   │   ├── SQLAlchemy/
│   │   │   └── HelloWorldModel.py
│   │   ├── Mappers/
│   │   │   └── HelloWorldMapper.py
│   │   └── database.py
│   └── Projections/                # Proyecciones CQRS
│       └── HelloWorldProjection.py
│
├── Shared/                         # Código compartido
│   ├── Application/
│   │   ├── CommandBus.py           # Bus de comandos
│   │   ├── QueryBus.py             # Bus de queries
│   │   ├── CommandHandler.py       # Interface ABC
│   │   └── QueryHandler.py         # Interface ABC
│   ├── Domain/
│   │   ├── Entities/
│   │   │   └── EntityBase.py       # AggregateRootBase
│   │   ├── Events/
│   │   │   ├── DomainEvent.py
│   │   │   └── EventDispatcherInterface.py
│   │   ├── Exceptions/
│   │   │   └── ExceptionBase.py
│   │   └── ValueObjects/
│   │       ├── StringValueObject.py
│   │       └── UuidValueObject.py
│   └── Infrastructure/
│       ├── Events/
│       │   └── EventDispatcher.py
│       ├── Exceptions/
│       │   └── DatabaseException.py
│       ├── Repository/
│       │   └── BaseWriteRepository.py  # 🆕 Manejo centralizado de errores BD
│       └── Validators/
│           └── RequestValidator.py     # 🆕 Clase base para validadores
│
└── config/
    └── container.py                # DI Container (dependency-injector)
```

---

## ✅ Principios SOLID Cumplidos

| Principio | Implementación |
|-----------|----------------|
| **S** - Single Responsibility | Cada handler tiene una única responsabilidad |
| **O** - Open/Closed | Nuevos handlers sin modificar buses existentes |
| **L** - Liskov Substitution | Interfaces permiten intercambiar implementaciones |
| **I** - Interface Segregation | Interfaces separadas Read/Write |
| **D** - Dependency Inversion | Application depende de interfaces, no de implementaciones |

---

## 🧪 Testing

```bash
# Ejecutar todos los tests unitarios
pytest tests/unit/ -v

# Tests del módulo Admin
pytest tests/unit/Admin/ -v

# Con cobertura
pytest tests/unit/ --cov=app --cov-report=html

# Tests específicos
pytest tests/unit/Application/test_command_handlers.py -v
pytest tests/unit/Application/test_query_handlers.py -v
pytest tests/unit/Admin/Application/test_command_handlers.py -v
```

**Resultado actual:** 281+ tests pasando, 90%+ cobertura

---

## 🚀 Cómo Agregar un Nuevo Módulo

### Opción A: Módulo Autocontenido (Recomendado)

Crear estructura completa bajo `app/NuevoModulo/`:

```
app/NuevoModulo/
├── Application/
│   ├── Commands/
│   │   └── CreateEntityCommand.py
│   ├── CommandHandlers/
│   │   └── CreateEntityHandler.py
│   ├── Queries/
│   │   └── GetEntityByIdQuery.py
│   ├── QueryHandlers/
│   │   └── GetEntityByIdHandler.py
│   └── ReadModels/
│       └── EntityReadModel.py
├── Domain/
│   ├── Entity.py                   # Aggregate Root
│   ├── EntityWriteRepositoryInterface.py
│   ├── EntityReadRepositoryInterface.py
│   ├── Events/
│   │   └── EntityCreated.py
│   ├── Exceptions/
│   │   └── IncorrectFieldException.py
│   └── ValueObjects/
│       └── FieldValueObject.py
└── Infrastructure/
    ├── Controller/
    │   └── EntityController.py
    ├── Repository/
    │   ├── EntityWriteRepository.py
    │   └── EntityReadRepository.py
    └── Persistence/
        ├── SQLAlchemy/
        │   └── EntityModel.py
        └── Mappers/
            └── EntityMapper.py
```

### Opción B: Módulo en estructura existente (Legacy)

```python
# Domain/NewModule/NewEntity.py
class NewEntity(AggregateRootBase):
    pass

# Domain/NewModule/NewRepositoryInterface.py
class NewRepositoryInterface(ABC):
    @abstractmethod
    def save(self, entity: NewEntity) -> NewEntity:
        pass
```

### Registrar en Container

```python
# config/container.py

# Importar handlers del nuevo módulo
from NuevoModulo.Application.CommandHandlers.CreateEntityHandler import CreateEntityHandler

# Registrar en el container
new_entity_write_repository = providers.Factory(EntityWriteRepository)
create_entity_handler = providers.Factory(
    CreateEntityHandler,
    write_repository=new_entity_write_repository,
    event_dispatcher=event_dispatcher
)

# Registrar en buses
command_bus.register(CreateEntityCommand, container.create_entity_handler())
query_bus.register(GetEntityByIdQuery, container.get_entity_by_id_handler())
```

---

## 📚 Documentación Adicional

- [CQRS_MIGRATION.md](./CQRS_MIGRATION.md) - Detalles de la migración a CQRS
- [USE_CASES_IMPLEMENTATION.md](./USE_CASES_IMPLEMENTATION.md) - Implementación de Use Cases
- [ARCHITECTURE_DIAGRAM.md](./ARCHITECTURE_DIAGRAM.md) - Diagramas detallados

---

**Última actualización: 04 de diciembre de 2025**
