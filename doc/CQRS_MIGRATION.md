# CQRS - Implementación Completa

## 📋 Resumen

El módulo **HelloWorld** implementa CQRS puro donde el Controller interactúa directamente con `CommandBus` y `QueryBus`, sin capas intermedias de Use Cases.

---

## ✅ Arquitectura CQRS Pura

### Flujo de Escritura (Commands)

```
HTTP POST/PUT/DELETE /api/v1/hello-world/
     ↓
HelloWorldController
     ↓
CreateHelloWorldCommand (frozen dataclass)
     ↓
CommandBus.dispatch(command)
     ↓ [busca handler por tipo de comando]
CreateHelloWorldHandler
     ├─→ GreetingValueObject.create()  [Domain validation]
     ├─→ HelloWorld.create()           [Entity creation]
     ├─→ WriteRepository.save()        [Persistence]
     ├─→ entity.mark_as_created()      [Record event]
     └─→ EventDispatcher.publish()     [Publish events]
     ↓
return entity_id (int)
     ↓
Controller usa QueryBus para obtener datos completos (opcional)
     ↓
HTTP Response 201 { "id": 1, "greeting": "Hello" }
```

### Flujo de Lectura (Queries)

```
HTTP GET /api/v1/hello-world/
     ↓
HelloWorldController
     ↓
GetAllHelloWorldQuery (frozen dataclass)
     ↓
QueryBus.dispatch(query)
     ↓ [busca handler por tipo de query]
GetAllHelloWorldHandler
     └─→ ReadRepository.find_all()  [Optimized for reads]
     ↓
return List[HelloWorldReadModel]
     ↓
HTTP Response 200 [{ "id": 1, "greeting": "Hello" }, ...]
```

---

## 🏗️ Implementación en Controller

### GET - Listar todos (Query)

```python
@hello_world_controller.route('/', methods=['GET'])
def get_all_hello_world():
    # Parámetros de paginación opcionales
    limit = request.args.get('limit', type=int)
    offset = request.args.get('offset', type=int)
    sort_by = request.args.get('sort_by', default='id')
    sort_order = request.args.get('sort_order', default='asc')

    # Crear Query inmutable
    query = GetAllHelloWorldQuery(
        limit=limit,
        offset=offset,
        sort_by=sort_by,
        sort_order=sort_order
    )

    # Despachar al QueryBus
    query_bus = current_app.container.query_bus()
    result = query_bus.dispatch(query)

    return ControllerBase.format_response(result, 200)
```

### POST - Crear (Command)

```python
@hello_world_controller.route('/', methods=['POST'])
def create_hello_world():
    data = request.get_json()

    if not data or 'greeting' not in data:
        return ControllerBase.format_response(
            {"error": "Field 'greeting' is required"}, 400
        )

    # Crear Command inmutable
    command = CreateHelloWorldCommand(greeting_text=data['greeting'])

    # Despachar al CommandBus
    command_bus = current_app.container.command_bus()
    entity_id = command_bus.dispatch(command)

    # Obtener entidad creada via QueryBus
    query = GetHelloWorldByIdQuery(id=entity_id)
    query_bus = current_app.container.query_bus()
    created_entity = query_bus.dispatch(query)

    return ControllerBase.format_response(created_entity, 201)
```

### DELETE - Eliminar (Command)

```python
@hello_world_controller.route('/<int:id>', methods=['DELETE'])
def delete_hello_world(id: int):
    # Verificar existencia via Query
    query = GetHelloWorldByIdQuery(id=id)
    query_bus = current_app.container.query_bus()
    existing = query_bus.dispatch(query)

    if existing is None:
        return ControllerBase.format_response(
            {"error": "HelloWorld not found"}, 404
        )

    # Despachar comando de eliminación
    command = DeleteHelloWorldCommand(id=id)
    command_bus = current_app.container.command_bus()
    command_bus.dispatch(command)

    return ControllerBase.format_response(
        {"message": "HelloWorld deleted successfully"}, 200
    )
```

---

## 🔷 Componentes CQRS

### Commands (Inmutables)

```python
# Application/Commands/CreateHelloWorldCommand.py
@dataclass(frozen=True)
class CreateHelloWorldCommand:
    """Comando inmutable para crear HelloWorld."""
    greeting_text: str
    
    def __post_init__(self):
        if not isinstance(self.greeting_text, str):
            raise TypeError("greeting_text must be a string")
```

### Command Handlers

```python
# Application/CommandHandlers/CreateHelloWorldHandler.py
class CreateHelloWorldHandler(CommandHandler):
    """Implementa CommandHandler ABC."""
    
    def __init__(
        self,
        write_repository: HelloWorldRepositoryInterface,
        event_dispatcher: EventDispatcherInterface
    ):
        self.write_repository = write_repository
        self.event_dispatcher = event_dispatcher

    def handle(self, command: CreateHelloWorldCommand) -> int:
        # 1. Value Object con validación de dominio
        greeting = GreetingValueObject.create(command.greeting_text)
        
        # 2. Crear entidad de dominio
        hello_world = HelloWorld.create(greeting=greeting)
        
        # 3. Persistir
        saved_entity = self.write_repository.save(hello_world)
        
        # 4. Registrar evento
        saved_entity.mark_as_created(saved_entity.id)
        
        # 5. Publicar eventos
        self.event_dispatcher.publish_multiple(
            saved_entity.pull_domain_events()
        )
        
        # 6. Retornar solo ID
        return saved_entity.id
```

### Queries (Inmutables)

```python
# Application/Queries/GetAllHelloWorldQuery.py
@dataclass(frozen=True)
class GetAllHelloWorldQuery:
    """Query inmutable para obtener todos."""
    limit: Optional[int] = None
    offset: Optional[int] = None
    sort_by: Optional[str] = 'id'
    sort_order: Optional[str] = 'asc'
```

### Query Handlers

```python
# Application/QueryHandlers/GetAllHelloWorldHandler.py
class GetAllHelloWorldHandler(QueryHandler):
    """Implementa QueryHandler ABC."""
    
    def __init__(self, read_repository: HelloWorldReadRepositoryInterface):
        self.read_repository = read_repository

    def handle(self, query: GetAllHelloWorldQuery) -> List[HelloWorldReadModel]:
        return self.read_repository.find_all(
            limit=query.limit,
            offset=query.offset,
            sort_by=query.sort_by,
            sort_order=query.sort_order
        )
```

---

## 📊 Separación Write/Read

### Write Repository (Commands)

```python
# Domain/HelloWorld/HelloWorldRepositoryInterface.py
class HelloWorldRepositoryInterface(ABC):
    @abstractmethod
    def save(self, hello_world: HelloWorld) -> HelloWorld:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass
```

### Read Repository (Queries)

```python
# Domain/HelloWorld/HelloWorldReadRepositoryInterface.py
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

## 🔧 Registro en DI Container

```python
# config/container.py

def _register_command_handlers(container: Container) -> None:
    """Registra handlers de comandos."""
    command_bus = container.command_bus()
    
    command_bus.register(
        CreateHelloWorldCommand,
        container.create_hello_world_command_handler()
    )
    command_bus.register(
        UpdateHelloWorldCommand,
        container.update_hello_world_command_handler()
    )
    command_bus.register(
        DeleteHelloWorldCommand,
        container.delete_hello_world_command_handler()
    )


def _register_query_handlers(container: Container) -> None:
    """Registra handlers de queries."""
    query_bus = container.query_bus()
    
    query_bus.register(
        GetAllHelloWorldQuery,
        container.get_all_hello_world_query_handler()
    )
    query_bus.register(
        GetHelloWorldByIdQuery,
        container.get_hello_world_by_id_query_handler()
    )
    query_bus.register(
        SearchHelloWorldQuery,
        container.search_hello_world_query_handler()
    )
```

---

## ✅ Beneficios de CQRS Puro

| Beneficio | Descripción |
|-----------|-------------|
| **Sin capa intermedia** | Controller → Bus → Handler (sin Use Cases) |
| **Menor acoplamiento** | Controller solo conoce Commands/Queries y Buses |
| **Extensibilidad** | Fácil agregar middleware al Bus |
| **Testabilidad** | Mock del Bus o Handler directamente |
| **Separación clara** | Escritura (Commands) vs Lectura (Queries) |
| **Escalabilidad** | Read y Write pueden escalar independientemente |

---

## 🧪 Testing

### Test de Handler

```python
def test_create_hello_world_handler():
    mock_repository = Mock(spec=HelloWorldRepositoryInterface)
    mock_dispatcher = Mock(spec=EventDispatcherInterface)
    
    def save_side_effect(entity):
        entity._id = 123
        return entity
    mock_repository.save = Mock(side_effect=save_side_effect)
    
    handler = CreateHelloWorldHandler(mock_repository, mock_dispatcher)
    command = CreateHelloWorldCommand(greeting_text="Test")
    
    result_id = handler.handle(command)
    
    assert result_id == 123
    mock_repository.save.assert_called_once()
    mock_dispatcher.publish_multiple.assert_called_once()
```

### Test de Controller (con mock de Bus)

```python
def test_get_all_hello_world_endpoint(client, app):
    with app.container.query_bus.override(Mock()):
        mock_bus = app.container.query_bus()
        mock_bus.dispatch.return_value = [{"id": 1, "greeting": "Test"}]
        
        response = client.get('/api/v1/hello-world/')
        
        assert response.status_code == 200
        mock_bus.dispatch.assert_called_once()
```

---

**Última actualización: 26 de noviembre de 2025**
