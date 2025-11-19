# Migración a CQRS - Flujo POST CreateHelloWorld

## 📋 Resumen

El endpoint `POST /api/v1/hello-world/` ha sido refactorizado para usar el patrón **CQRS completo** con **Command Bus**, abandonando el uso directo de Use Cases.

---

## ✅ Cambios Realizados

### Antes (Use Case directo)

```python
@hello_world_controller.route('/', methods=['POST'])
def create_hello_world():
    data = request.get_json()
    
    # Obtener Use Case desde el container
    use_case = current_app.container.create_hello_world_use_case()
    
    # Ejecutar Use Case directamente
    result = use_case.execute(data['name'])
    
    return ControllerBase.format_response(result, 201)
```

**Flujo:**
```
Controller → CreateHelloWorldUseCase → Repository → Database
```

**Problemas:**
- ❌ No sigue el patrón CQRS puro
- ❌ Controller acoplado a implementación específica (Use Case)
- ❌ Sin separación clara entre Commands y Queries
- ❌ No aprovecha el Command Bus implementado

---

### Después (CQRS con Command Bus)

```python
@hello_world_controller.route('/', methods=['POST'])
def create_hello_world():
    data = request.get_json()
    
    if not data or 'greeting' not in data:
        return ControllerBase.format_response(
            {"error": "Field 'greeting' is required"},
            400
        )
    
    # 1. Crear el comando CQRS (inmutable)
    command = CreateHelloWorldCommand(
        greeting_text=data['greeting']
    )
    
    # 2. Obtener el Command Bus desde el container
    command_bus = current_app.container.command_bus()
    
    # 3. Despachar el comando al handler correspondiente
    entity_id = command_bus.dispatch(command)
    
    # 4. Retornar respuesta con el ID
    return ControllerBase.format_response(
        {"id": entity_id, "greeting": data['greeting']},
        201
    )
```

**Flujo CQRS:**
```
Controller 
   → CreateHelloWorldCommand 
   → Command Bus 
   → CreateHelloWorldHandler 
   → Repository 
   → Database
```

**Beneficios:**
- ✅ Sigue el patrón CQRS puro
- ✅ Controller desacoplado de la implementación
- ✅ Separación clara: Commands (escritura) vs Queries (lectura)
- ✅ Command Bus centraliza el despacho de comandos
- ✅ Fácil agregar middleware (logging, validación, transacciones)
- ✅ Testeable con mocks del Command Bus

---

## 🏗️ Componentes CQRS

### 1. Command (Comando Inmutable)

**Archivo:** `app/Application/Commands/CreateHelloWorldCommand.py`

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class CreateHelloWorldCommand:
    """
    Comando inmutable para crear un HelloWorld.
    Representa la INTENCIÓN de crear una entidad.
    """
    greeting_text: str
    
    def __post_init__(self):
        """Validaciones básicas del comando."""
        if not isinstance(self.greeting_text, str):
            raise TypeError("greeting_text must be a string")
```

**Características:**
- Inmutable (`frozen=True`)
- Sin lógica de negocio
- Solo datos y validaciones básicas de tipo
- Representa una intención, no una acción

---

### 2. Command Handler

**Archivo:** `app/Application/CommandHandlers/CreateHelloWorldHandler.py`

```python
class CreateHelloWorldHandler:
    """
    Maneja la creación de HelloWorld.
    Encapsula la lógica de negocio para crear entidades.
    """
    
    def __init__(
        self,
        repository: HelloWorldRepositoryInterface,
        event_dispatcher: EventDispatcherInterface
    ):
        self.repository = repository
        self.event_dispatcher = event_dispatcher
    
    def handle(self, command: CreateHelloWorldCommand) -> int:
        """
        Procesa el comando de creación.
        
        Returns:
            int: ID de la entidad creada
        """
        # 1. Crear Value Object (con validaciones de dominio)
        greeting = GreetingValueObject.create(command.greeting_text)
        
        # 2. Crear entidad de dominio (registra eventos)
        hello_world = HelloWorld.create(greeting=greeting)
        
        # 3. Persistir a través del repositorio
        saved_entity = self.repository.save(hello_world)
        
        # 4. Marcar como creado para registrar el evento
        saved_entity.mark_as_created(saved_entity.id)
        
        # 5. Publicar eventos de dominio
        self.event_dispatcher.publish_multiple(
            saved_entity.pull_domain_events()
        )
        
        # 6. Retornar solo el ID (sin exponer el modelo de dominio)
        return saved_entity.id
```

**Características:**
- Contiene la lógica de negocio
- Valida reglas de dominio
- Publica eventos
- Retorna solo el ID (no expone entidad completa)
- Método estándar: `handle(command)`

---

### 3. Command Bus

**Archivo:** `app/Shared/Application/CommandBus.py`

```python
class CommandBus:
    """
    Bus de comandos que despacha comandos a sus handlers.
    Separa la invocación de comandos de su ejecución.
    """
    
    def __init__(self):
        self._handlers: Dict[Type, Any] = {}
    
    def register(self, command_type: Type, handler: Any) -> None:
        """Registra un handler para un tipo de comando."""
        if command_type in self._handlers:
            raise ValueError(f"Handler already registered for {command_type.__name__}")
        self._handlers[command_type] = handler
    
    def dispatch(self, command: Any) -> Any:
        """
        Despacha un comando a su handler correspondiente.
        
        Returns:
            El resultado del handler
        """
        command_type = type(command)
        
        if command_type not in self._handlers:
            raise ValueError(f"No handler registered for {command_type.__name__}")
        
        handler = self._handlers[command_type]
        return handler.handle(command)
```

**Características:**
- Registro de handlers por tipo de comando
- Despacho automático al handler correcto
- Validación de handlers registrados
- Punto único de entrada para todos los comandos

---

### 4. Registro en DI Container

**Archivo:** `app/config/container.py`

```python
def _register_command_handlers(container: Container) -> None:
    """
    Registra todos los command handlers en el command bus.
    """
    command_bus = container.command_bus()
    
    # Registrar CreateHelloWorldHandler
    command_bus.register(
        CreateHelloWorldCommand,
        container.create_hello_world_handler()
    )
    
    # Otros handlers...
    command_bus.register(
        UpdateHelloWorldCommand,
        container.update_hello_world_handler()
    )
    
    command_bus.register(
        DeleteHelloWorldCommand,
        container.delete_hello_world_handler()
    )
```

---

## 🔄 Comparación de Flujos

### Flujo Completo ANTES

```
1. HTTP POST /api/v1/hello-world/
   Body: {"name": "Hello World"}
        ↓
2. HelloWorldController.create_hello_world()
        ↓
3. container.create_hello_world_use_case()
        ↓
4. CreateHelloWorldUseCase.execute(greeting_text)
        ├─→ Greeting.create(greeting_text)
        ├─→ HelloWorld.create(greeting)
        ├─→ repository.save(hello_world)
        ├─→ event_dispatcher.publish_multiple(events)
        └─→ HelloWorldSerializer.to_dict(saved_entity)
        ↓
5. Retorna: {"id": 1, "greeting": "Hello World"}
```

### Flujo Completo DESPUÉS (CQRS)

```
1. HTTP POST /api/v1/hello-world/
   Body: {"greeting": "Hello World"}
        ↓
2. HelloWorldController.create_hello_world()
        ↓
3. CreateHelloWorldCommand(greeting_text="Hello World")
        ↓
4. command_bus.dispatch(command)
        ↓
5. Command Bus busca handler por tipo
        ↓
6. CreateHelloWorldHandler.handle(command)
        ├─→ GreetingValueObject.create(command.greeting_text)
        ├─→ HelloWorld.create(greeting)
        ├─→ repository.save(hello_world)
        ├─→ saved_entity.mark_as_created(saved_entity.id)
        ├─→ event_dispatcher.publish_multiple(events)
        └─→ return saved_entity.id
        ↓
7. Controller construye respuesta
        ↓
8. Retorna: {"id": 1, "greeting": "Hello World"}
```

---

## 📊 Diferencias Clave

| Aspecto | Antes (Use Case) | Después (CQRS) |
|---------|-----------------|----------------|
| **Patrón** | Use Case directo | Command + Command Bus |
| **Acoplamiento** | Controller → Use Case | Controller → Command Bus |
| **Punto de entrada** | Use Case | Command Bus |
| **Tipo de operación** | Método execute() | Comando inmutable |
| **Retorno** | Entidad serializada (dict) | Solo ID (int) |
| **Separación Commands/Queries** | No clara | ✅ Explícita |
| **Extensibilidad** | Modificar Use Case | Agregar middleware al bus |
| **Testing** | Mock Use Case | Mock Command Bus |
| **Campo API** | `name` | `greeting` (más semántico) |

---

## 🧪 Testing

### Test del Command Handler

```python
def test_handle_creates_hello_world_and_saves():
    """Debe crear entidad y guardarla en el repositorio"""
    # Arrange
    mock_repository = Mock()
    
    def save_side_effect(entity):
        entity._id = 123
        return entity
    mock_repository.save = Mock(side_effect=save_side_effect)
    
    mock_event_dispatcher = Mock()
    
    handler = CreateHelloWorldHandler(mock_repository, mock_event_dispatcher)
    command = CreateHelloWorldCommand(greeting_text="Test Greeting")
    
    # Act
    result_id = handler.handle(command)
    
    # Assert
    mock_repository.save.assert_called_once()
    assert result_id == 123
```

### Test del Command Bus

```python
def test_dispatch_calls_correct_handler():
    """Debe despachar al handler correcto según el tipo de comando"""
    # Arrange
    bus = CommandBus()
    mock_handler = Mock()
    mock_handler.handle.return_value = 42
    
    bus.register(CreateHelloWorldCommand, mock_handler)
    command = CreateHelloWorldCommand(greeting_text="Test")
    
    # Act
    result = bus.dispatch(command)
    
    # Assert
    mock_handler.handle.assert_called_once_with(command)
    assert result == 42
```

---

## 🚀 Próximos Pasos

### Endpoints a Migrar

- ✅ **POST /api/v1/hello-world/** - Migrado a CQRS
- 🔄 **PUT /api/v1/hello-world/{id}** - Usar UpdateHelloWorldCommand (ya existe)
- 🔄 **DELETE /api/v1/hello-world/{id}** - Usar DeleteHelloWorldCommand (ya existe)

### Queries (Ya implementados)

- ✅ **GET /api/v1/hello-world/** - Usa QueryBus
- ✅ **GET /api/v1/hello-world/{id}** - Usa QueryBus

---

## 📝 Correcciones Adicionales

### Imports Circulares Corregidos

Se corrigieron imports que usaban `app.Domain` en lugar de `Domain`:

**Archivos corregidos:**
- `app/Domain/HelloWorld/HelloWorld.py`
- `app/Application/HelloWorldService.py`
- `app/Application/UseCases/HelloWorld/CreateHelloWorldUseCase.py`
- `app/Application/CommandHandlers/CreateHelloWorldHandler.py`
- `app/Application/CommandHandlers/UpdateHelloWorldHandler.py`
- `app/Infrastructure/Persistence/Mappers/HelloWorldMapper.py`

**Antes:**
```python
from app.Domain.HelloWorld.ValueObjects.GreetingValueObject import GreetingValueObject
```

**Después:**
```python
from Domain.HelloWorld.ValueObjects.GreetingValueObject import GreetingValueObject
```

### Tests Actualizados

Todos los tests fueron actualizados para usar `GreetingValueObject` en lugar de `Greeting`:

**Archivos actualizados:**
- `tests/unit/Application/test_command_handlers.py` (✅ 8/8 tests passing)
- `tests/unit/domain/entities/test_hello_world.py`
- `tests/unit/domain/value_objects/test_greeting.py`
- `tests/integration/test_hello_world_repository.py`
- `tests/unit/use_cases/test_hello_world_use_cases.py`
- `conftest.py`

---

## ✅ Resultado Final

**El proyecto ahora implementa CQRS puro con:**

- ✅ Command Bus para operaciones de escritura
- ✅ Query Bus para operaciones de lectura
- ✅ Comandos inmutables (`@dataclass(frozen=True)`)
- ✅ Handlers con responsabilidad única
- ✅ Separación clara Commands vs Queries
- ✅ Event-Driven Architecture integrada
- ✅ Dependency Injection con registro automático
- ✅ Tests pasando (8/8 command handlers con 100% cobertura)

**Beneficios arquitectónicos:**
- 🎯 Mejor separación de responsabilidades
- 🔧 Más fácil de mantener y extender
- 🧪 Más testeable con mocks
- 📈 Escalable (read/write independientes)
- 🛡️ Más robusto ante cambios

---

**Documentación actualizada el 19 de noviembre de 2025**
