# Casos de Uso y CQRS - Implementación

## ✅ Arquitectura Actual (CQRS Puro)

El módulo **HelloWorld** usa CQRS puro sin capa de Use Cases intermedia.
El módulo **Shows** mantiene Use Cases tradicionales (pendiente de migrar).

```
Application/
├── Commands/                   # Comandos CQRS (HelloWorld)
├── CommandHandlers/            # Handlers de comandos
├── Queries/                    # Queries CQRS (HelloWorld)
├── QueryHandlers/              # Handlers de queries
├── ReadModels/                 # DTOs de lectura
├── EventHandlers/              # Handlers de eventos de dominio
├── Serializers/                # Serializadores
├── DTO/                        # DTOs de entrada
├── MoviesService.py            # Servicio de orquestación (Shows)
└── UseCases/
    └── Shows/                  # Use Cases tradicionales (pendiente migrar)
        ├── SearchShowsUseCase.py
        └── GetShowByIdUseCase.py
```

---

## 🎯 Patrón CQRS Puro (HelloWorld)

### Flujo de Escritura (Commands)

```
HTTP Request (POST/PUT/DELETE)
     ↓
Controller
     ↓ [crea Command inmutable]
CreateHelloWorldCommand
     ↓
CommandBus.dispatch(command)
     ↓ [busca handler por tipo]
CreateHelloWorldHandler
     ↓
     ├─→ Value Object validation
     ├─→ Domain Entity creation
     ├─→ Repository.save()
     └─→ EventDispatcher.publish()
     ↓
return entity_id (int)
```

### Flujo de Lectura (Queries)

```
HTTP Request (GET)
     ↓
Controller
     ↓ [crea Query inmutable]
GetAllHelloWorldQuery
     ↓
QueryBus.dispatch(query)
     ↓ [busca handler por tipo]
GetAllHelloWorldHandler
     ↓
     └─→ ReadRepository.find_all()
     ↓
return List[ReadModel]
```

---

## 📋 Componentes CQRS - HelloWorld

### Commands (4 comandos)

| Command | Propósito | Entrada | Handler |
|---------|-----------|---------|---------|
| `CreateHelloWorldCommand` | Crear HelloWorld | `greeting_text: str` | `CreateHelloWorldHandler` |
| `UpdateHelloWorldCommand` | Actualizar HelloWorld | `id: int, greeting_text: str` | `UpdateHelloWorldHandler` |
| `DeleteHelloWorldCommand` | Eliminar HelloWorld | `id: int` | `DeleteHelloWorldHandler` |

### Queries (3 queries)

| Query | Propósito | Entrada | Handler |
|-------|-----------|---------|---------|
| `GetAllHelloWorldQuery` | Listar todos | `limit?, offset?, sort_by?, sort_order?` | `GetAllHelloWorldHandler` |
| `GetHelloWorldByIdQuery` | Obtener por ID | `id: int` | `GetHelloWorldByIdHandler` |
| `SearchHelloWorldQuery` | Buscar por texto | `search_text: str, limit?, offset?` | `SearchHelloWorldHandler` |

---

## 🔄 Ejemplo de Controller (CQRS Puro)

```python
# Infrastructure/Controller/HelloWorldController.py

@hello_world_controller.route('/', methods=['GET'])
def get_all_hello_world():
    """GET /api/v1/hello-world/ - Lista todos"""
    # Crear Query con parámetros opcionales
    query = GetAllHelloWorldQuery(
        limit=request.args.get('limit', type=int),
        offset=request.args.get('offset', type=int),
        sort_by=request.args.get('sort_by', default='id'),
        sort_order=request.args.get('sort_order', default='asc')
    )
    
    # Despachar al QueryBus
    query_bus = current_app.container.query_bus()
    result = query_bus.dispatch(query)
    
    return ControllerBase.format_response(result, 200)


@hello_world_controller.route('/', methods=['POST'])
def create_hello_world():
    """POST /api/v1/hello-world/ - Crear nuevo"""
    data = request.get_json()
    
    # Crear Command
    command = CreateHelloWorldCommand(greeting_text=data['greeting'])
    
    # Despachar al CommandBus
    command_bus = current_app.container.command_bus()
    entity_id = command_bus.dispatch(command)
    
    # Obtener entidad creada via QueryBus
    query = GetHelloWorldByIdQuery(id=entity_id)
    query_bus = current_app.container.query_bus()
    created_entity = query_bus.dispatch(query)
    
    return ControllerBase.format_response(created_entity, 201)


@hello_world_controller.route('/<int:id>', methods=['DELETE'])
def delete_hello_world(id: int):
    """DELETE /api/v1/hello-world/{id} - Eliminar"""
    # Verificar existencia
    query = GetHelloWorldByIdQuery(id=id)
    query_bus = current_app.container.query_bus()
    existing = query_bus.dispatch(query)
    
    if existing is None:
        return ControllerBase.format_response({"error": "Not found"}, 404)
    
    # Despachar comando de eliminación
    command = DeleteHelloWorldCommand(id=id)
    command_bus = current_app.container.command_bus()
    command_bus.dispatch(command)
    
    return ControllerBase.format_response({"message": "Deleted"}, 200)
```

---

## 📊 Comparación: CQRS vs Use Cases

| Aspecto | Use Cases (Shows) | CQRS Puro (HelloWorld) |
|---------|-------------------|------------------------|
| **Capas** | Controller → UseCase → Repository | Controller → Bus → Handler → Repository |
| **Acoplamiento** | Medio (UseCase específico) | Bajo (Bus genérico) |
| **Extensibilidad** | Nueva clase UseCase | Nuevo Command/Query + Handler |
| **Middleware** | Difícil | Fácil (en el Bus) |
| **Testing** | Mock UseCase | Mock Bus o Handler |
| **Separación R/W** | No explícita | ✅ Explícita |

---

## 🏗️ DI Container

```python
# config/container.py

class Container(containers.DeclarativeContainer):
    
    # ========== CQRS - BUSES ==========
    command_bus = providers.Singleton(CommandBus)
    query_bus = providers.Singleton(QueryBus)
    
    # ========== COMMAND HANDLERS ==========
    create_hello_world_command_handler = providers.Factory(
        CreateHelloWorldHandler,
        write_repository=hello_world_write_repository,
        event_dispatcher=event_dispatcher
    )
    
    # ========== QUERY HANDLERS ==========
    get_all_hello_world_query_handler = providers.Factory(
        GetAllHelloWorldHandler,
        read_repository=hello_world_read_repository
    )
    
    # ========== USE CASES - SHOWS (legacy) ==========
    search_shows_use_case = providers.Factory(
        SearchShowsUseCase,
        repository=shows_repository
    )


def _register_command_handlers(container: Container) -> None:
    """Registra handlers de comandos en el bus."""
    command_bus = container.command_bus()
    command_bus.register(CreateHelloWorldCommand, container.create_hello_world_command_handler())
    command_bus.register(DeleteHelloWorldCommand, container.delete_hello_world_command_handler())


def _register_query_handlers(container: Container) -> None:
    """Registra handlers de queries en el bus."""
    query_bus = container.query_bus()
    query_bus.register(GetAllHelloWorldQuery, container.get_all_hello_world_query_handler())
    query_bus.register(GetHelloWorldByIdQuery, container.get_hello_world_by_id_query_handler())
```

---

## 🚀 Cómo Agregar una Nueva Operación CQRS

### 1. Crear el Command/Query

```python
# Application/Commands/UpdateHelloWorldCommand.py
@dataclass(frozen=True)
class UpdateHelloWorldCommand:
    id: int
    greeting_text: str
```

### 2. Crear el Handler

```python
# Application/CommandHandlers/UpdateHelloWorldHandler.py
class UpdateHelloWorldHandler(CommandHandler):
    def __init__(self, write_repository, read_repository, event_dispatcher):
        self.write_repository = write_repository
        self.read_repository = read_repository
        self.event_dispatcher = event_dispatcher
    
    def handle(self, command: UpdateHelloWorldCommand) -> int:
        # Lógica de actualización
        pass
```

### 3. Registrar en Container

```python
# config/container.py
update_hello_world_handler = providers.Factory(
    UpdateHelloWorldHandler,
    write_repository=hello_world_write_repository,
    ...
)

# En _register_command_handlers:
command_bus.register(UpdateHelloWorldCommand, container.update_hello_world_handler())
```

### 4. Usar en Controller

```python
@hello_world_controller.route('/<int:id>', methods=['PUT'])
def update_hello_world(id: int):
    data = request.get_json()
    command = UpdateHelloWorldCommand(id=id, greeting_text=data['greeting'])
    command_bus = current_app.container.command_bus()
    command_bus.dispatch(command)
    return ControllerBase.format_response({"message": "Updated"}, 200)
```

---

## ✅ Beneficios de CQRS Puro

| Beneficio | Descripción |
|-----------|-------------|
| **Separación clara** | Escritura y lectura en flujos independientes |
| **Escalabilidad** | Read y Write pueden escalar por separado |
| **Testabilidad** | Handlers pequeños y fáciles de testear |
| **Extensibilidad** | Middleware en los buses (logging, validación, auth) |
| **Single Responsibility** | Cada handler hace una sola cosa |
| **Inmutabilidad** | Commands/Queries son frozen dataclasses |

---

## 📝 Resumen de Estado

| Módulo | Patrón | Estado |
|--------|--------|--------|
| **HelloWorld** | CQRS Puro | ✅ Completo |
| **Shows** | Use Cases | ⚠️ Legacy (funcional) |

**Recomendación:** Migrar Shows a CQRS cuando sea necesario escalar o agregar funcionalidad compleja.

---

**Última actualización: 26 de noviembre de 2025**
