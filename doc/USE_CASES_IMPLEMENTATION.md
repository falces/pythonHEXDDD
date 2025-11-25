# Casos de Uso - Implementación

## ✅ Estructura Creada

```
Application/
├── UseCases/
│   ├── HelloWorld/
│   │   ├── __init__.py
│   │   ├── CreateHelloWorldUseCase.py
│   │   ├── GetAllHelloWorldUseCase.py
│   │   ├── GetHelloWorldByIdUseCase.py
│   │   └── DeleteHelloWorldUseCase.py
│   └── Shows/
│       ├── __init__.py
│       ├── SearchShowsUseCase.py
│       └── GetShowByIdUseCase.py
├── HelloWorldService.py (mantiene lógica de eventos)
└── MoviesService.py (mantiene lógica de orquestación compleja)
```

---

## ⚠️ Migración a CQRS

**El flujo POST (CREATE) ahora usa CQRS con Command Bus:**

- ✅ **CreateHelloWorldHandler** + **CommandBus** (nuevo patrón CQRS)
- ⚠️ **CreateHelloWorldUseCase** (legacy, mantenido por compatibilidad)

**Flujo actual (CQRS):**
```python
# Controller
command = CreateHelloWorldCommand(greeting_text=data['greeting'])
command_bus = current_app.container.command_bus()
entity_id = command_bus.dispatch(command)  # Retorna solo el ID
```

**Ver README.md sección "Flujo de Escritura (Commands)" para detalles completos.**

---

## 🎯 Patrón Use Case

### **Antes - Servicios con múltiples responsabilidades**

```python
# HelloWorldService.py
class HelloWorldService:
    def __init__(self, repository):
        self.repository = repository
    
    def get_all_hello_world():
    use_case = current_app.container.get_all_hello_world_use_case()
    result = use_case.execute()
    return format_response(result, 200)
    
    def addHelloWorld(self, dto):
        # Lógica de crear
        # + Emitir eventos
        # + Validaciones
        ...
    
    def getById(self, id):
        # Lógica de obtener uno
        ...
    
    def delete(self, id):
        # Lógica de eliminar
        ...
```

**Problemas:**
- ❌ Clase con múltiples responsabilidades (viola SRP)
- ❌ Difícil de testear casos específicos
- ❌ No es claro qué hace cada método sin leer todo
- ❌ Mezcla orquestación con casos de uso específicos

---

### **Después - Casos de Uso específicos**

```python
# CreateHelloWorldUseCase.py
class CreateHelloWorldUseCase:
    """
    Responsabilidad única: Crear un HelloWorld
    """
    def __init__(self, command_bus):
        self.command_bus = command_bus
    
    def execute(self, greeting_text: str) -> dict:
        command = CreateHelloWorldCommand(greeting_text=greeting_text)
        entity_id = self.command_bus.dispatch(command)
        return {"id": entity_id, "greeting": greeting_text}


# GetAllHelloWorldUseCase.py
class GetAllHelloWorldUseCase:
    """
    Responsabilidad única: Obtener todos los HelloWorld
    """
    def __init__(self, repository):
        self.repository = repository
    
    def execute(self) -> List[dict]:
        entities = self.repository.findAll()
        return [HelloWorldSerializer.to_dict(e) for e in entities]


# GetHelloWorldByIdUseCase.py
class GetHelloWorldByIdUseCase:
    """
    Responsabilidad única: Obtener un HelloWorld por ID
    """
    def __init__(self, query_bus):
        self.query_bus = query_bus
    
    def execute(self, id: int) -> Optional[dict]:
        query = GetHelloWorldByIdQuery(id=id)
        result = self.query_bus.dispatch(query)
        return result.to_dict() if result else None


# DeleteHelloWorldUseCase.py
class DeleteHelloWorldUseCase:
    """
    Responsabilidad única: Eliminar un HelloWorld
    """
    def __init__(self, command_bus):
        self.command_bus = command_bus
    
    def execute(self, id: int) -> bool:
        command = DeleteHelloWorldCommand(id=id)
        return self.command_bus.dispatch(command)
```

**Beneficios:**
- ✅ Una clase = Una responsabilidad (SRP)
- ✅ Fácil de testear individualmente
- ✅ Nombre descriptivo del propósito
- ✅ Código más pequeño y enfocado
- ✅ Fácil de extender (agregar nuevos casos de uso)

---

## 🔄 Flujo Comparado

### **Antes (con Servicios)**

```
HTTP Request
     ↓
Controller
     ↓ [obtiene Service desde Container]
HelloWorldService
     ↓ [método específico: getAllHelloWorld()]
     ↓ [método específico: addHelloWorld()]
     ↓ [método específico: delete()]
Repository
     ↓
Database
```

**Controller:**
```python
@helloWorldController.route('/', methods=['GET'])
def getAllHelloWorld():
    service = container.hello_world_service()
    result = service.getAllHelloWorld()  # Método del servicio
    return formatResponse(result, 200)
```

---

### **Después (con Use Cases)**

```
HTTP Request
     ↓
Controller
     ↓ [obtiene Use Case específico desde Container]
GetAllHelloWorldUseCase
     ↓ [execute()]
Repository
     ↓
Database
```

**Controller:**
```python
@helloWorldController.route('/', methods=['GET'])
def get_all_hello_world():
    use_case = current_app.container.get_all_hello_world_use_case()
    result = service.get_all_hello_world()  # Método del servicio
    return format_response(result, 200)
```

---

## 📋 Casos de Uso Creados

### **HelloWorld (4 casos de uso)**

| Use Case | Responsabilidad | Entrada | Salida | Estado |
|----------|----------------|---------|--------|--------|
| `CreateHelloWorldUseCase` | Crear nuevo HelloWorld (usa CommandBus) | `greeting_text: str` | `dict` | ✅ Activo |
| `GetAllHelloWorldUseCase` | Listar todos (usa QueryBus) | - | `List[dict]` | ✅ Activo |
| `GetHelloWorldByIdUseCase` | Obtener por ID (usa QueryBus) | `id: int` | `Optional[dict]` | ✅ Activo |
| `DeleteHelloWorldUseCase` | Eliminar por ID (usa CommandBus) | `id: int` | `bool` | ✅ Activo |

### **Shows/Movies (2 casos de uso)**

| Use Case | Responsabilidad | Entrada | Salida |
|----------|----------------|---------|--------|
| `SearchShowsUseCase` | Buscar shows por criterios | `criteria: Dict` | `List[dict]` |
| `GetShowByIdUseCase` | Obtener show por ID | `show_id: str` | `Optional[dict]` |

---

## 🏗️ DI Container Actualizado

```python
# config/container.py
class Container(containers.DeclarativeContainer):
    # Repositories
    hello_world_repository = providers.Factory(HelloWorldRepository)
    shows_repository = providers.Factory(ShowsRepository, ...)
    
    # ========== USE CASES - HELLO WORLD ==========
    
    create_hello_world_use_case = providers.Factory(
        CreateHelloWorldUseCase,
        command_bus=command_bus
    )
    
    get_all_hello_world_use_case = providers.Factory(
        GetAllHelloWorldUseCase,
        query_bus=query_bus
    )
    
    get_hello_world_by_id_use_case = providers.Factory(
        GetHelloWorldByIdUseCase,
        query_bus=query_bus
    )
    
    delete_hello_world_use_case = providers.Factory(
        DeleteHelloWorldUseCase,
        command_bus=command_bus
    )
    
    # ========== USE CASES - SHOWS ==========
    
    search_shows_use_case = providers.Factory(
        SearchShowsUseCase,
        repository=shows_repository
    )
    
    get_show_by_id_use_case = providers.Factory(
        GetShowByIdUseCase,
        repository=shows_repository
    )
```

---

## 🎯 Controladores Actualizados

### **Antes**

```python
@helloWorldController.route('/', methods=['POST'])
def createHelloWorld():
    data = request.get_json()
    
    # Crear DTO
    dto = GreetingDTO(name=data['name'])
    
    # Obtener servicio
    service = container.hello_world_service()
    
    # Llamar método específico del servicio
    result = service.addHelloWorld(dto)
    
    return formatResponse(result, 201)
```

### **Después**

```python
@helloWorldController.route('/', methods=['POST'])
def createHelloWorld():
    data = request.get_json()
    
    # Obtener caso de uso específico
    use_case = container.create_hello_world_use_case()
    
    # Ejecutar caso de uso (siempre es .execute())
    result = use_case.execute(data['name'])
    
    return formatResponse(result, 201)
```

**Mejoras:**
- ✅ No necesita DTO (simplificado)
- ✅ Obtiene el caso de uso específico del container
- ✅ Método `execute()` consistente en todos los casos de uso
- ✅ Más declarativo y claro

---

## 🧪 Testing

### **Test de Use Case (simple)**

```python
def test_create_hello_world_use_case():
    # Arrange
    mock_repo = Mock(spec=HelloWorldRepositoryInterface)
    mock_repo.save.return_value = HelloWorld(Greeting.create("Test"))
    
    use_case = CreateHelloWorldUseCase(repository=mock_repo)
    
    # Act
    result = use_case.execute("Test")
    
    # Assert
    assert result["greeting"] == "Test"
    mock_repo.save.assert_called_once()


def test_delete_hello_world_use_case():
    # Arrange
    mock_repo = Mock(spec=HelloWorldRepositoryInterface)
    mock_repo.delete.return_value = True
    mock_event_dispatcher = Mock()
    
    use_case = DeleteHelloWorldUseCase(
        repository=mock_repo,
        event_dispatcher=mock_event_dispatcher
    )
    
    # Act
    result = use_case.execute(1)
    
    # Assert
    assert result is True
    mock_repo.delete.assert_called_once_with(1)
    mock_event_dispatcher.publish.assert_called_once()
```

**Ventajas del testing:**
- ✅ Test más pequeños y enfocados
- ✅ Cada caso de uso se testea independientemente
- ✅ Fácil de hacer mocks específicos
- ✅ Cobertura más granular

---

## 📊 Comparación de Responsabilidades

### **Servicios (mantienen)**
- Orquestación compleja de múltiples casos de uso
- Emisión de eventos de dominio
- Lógica transversal a varios casos de uso
- Coordinación entre múltiples agregados

**Ejemplo (mantener):**
```python
class HelloWorldService:
    def processComplexOperation(self, data):
        # 1. Crear HelloWorld
        create_use_case = CreateHelloWorldUseCase(...)
        created = create_use_case.execute(data)
        
        # 2. Emitir evento
        signals['new_hello_world'].send(...)
        
        # 3. Realizar otra operación
        # ...
        
        return result
```

### **Use Cases (nuevos)**
- Una responsabilidad específica
- Operación CRUD simple
- Caso de uso de negocio aislado
- No dependen entre sí

**Ejemplo:**
```python
class GetAllHelloWorldUseCase:
    def execute(self):
        # Solo obtener y serializar
        entities = self.repository.findAll()
        return [HelloWorldSerializer.to_dict(e) for e in entities]
```

---

## ✅ Beneficios Obtenidos

| Aspecto | Antes (Servicios) | Después (Use Cases) |
|---------|------------------|---------------------|
| **Responsabilidad** | Múltiple (varios métodos) | Única (un caso de uso) |
| **Tamaño de clase** | Grande (muchos métodos) | Pequeña (solo execute) |
| **Testing** | Tests grandes para toda la clase | Tests pequeños por caso de uso |
| **Claridad** | "¿Qué hace este servicio?" | "Crea un HelloWorld" |
| **Extensibilidad** | Agregar métodos al servicio | Agregar nueva clase |
| **Reusabilidad** | Limitada (acoplado al servicio) | Alta (independiente) |
| **SRP** | Violado | Cumplido |

---

## 🚀 Cómo Agregar un Nuevo Caso de Uso

### **1. Crear el caso de uso**

```python
# Application/UseCases/HelloWorld/UpdateHelloWorldUseCase.py
class UpdateHelloWorldUseCase:
    def __init__(self, repository: HelloWorldRepositoryInterface):
        self.repository = repository
    
    def execute(self, id: int, new_greeting: str) -> Optional[dict]:
        # 1. Buscar entidad existente
        entity = self.repository.findById(id)
        if not entity:
            return None
        
        # 2. Actualizar (crear nuevo con nuevo greeting)
        greeting = Greeting.create(new_greeting)
        updated_entity = HelloWorld(greeting=greeting)
        updated_entity._id = entity._id
        
        # 3. Guardar
        saved = self.repository.save(updated_entity)
        
        # 4. Serializar
        return HelloWorldSerializer.to_dict(saved)
```

### **2. Registrar en el Container**

```python
# config/container.py
update_hello_world_use_case = providers.Factory(
    UpdateHelloWorldUseCase,
    repository=hello_world_repository
)
```

### **3. Usar en el Controller**

```python
@helloWorldController.route('/<int:id>', methods=['PUT'])
def updateHelloWorld(id: int):
    data = request.get_json()
    use_case = container.update_hello_world_use_case()
    result = use_case.execute(id, data['name'])
    
    if result is None:
        return format_response({"error": "Not found"}, 404)
    
    return format_response(result, 200)
```

---

## 📝 Resumen

✅ **6 casos de uso creados** (4 HelloWorld + 2 Shows)  
✅ **Controladores refactorizados** para usar casos de uso  
✅ **DI Container actualizado** con todos los casos de uso  
✅ **Single Responsibility Principle** aplicado correctamente  
✅ **Testing simplificado** con casos de uso pequeños  
✅ **Código más mantenible** y extensible  
✅ **Patrón consistente** en toda la aplicación

**Los servicios antiguos se mantienen para lógica de orquestación compleja, pero los casos de uso simples ahora están separados.**
