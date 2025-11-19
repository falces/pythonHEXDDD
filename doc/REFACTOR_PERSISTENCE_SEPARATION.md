# Separación de Modelo de Persistencia del Dominio

## Cambios Realizados

### ✅ **Problema Resuelto**
El modelo de persistencia SQLAlchemy (`HelloWorldModel`) estaba mezclado con la entidad de dominio, violando los principios de la arquitectura hexagonal donde el dominio debe ser independiente de frameworks y detalles de persistencia.

---

## Estructura Nueva

### **1. Domain (Capa de Dominio - Pura)**

```
Domain/HelloWorld/
├── HelloWorld.py                         # ✨ Entidad pura (sin SQLAlchemy)
├── HelloWorldRepositoryInterface.py      # 🆕 Interface/Puerto del repositorio
├── ValueObjects/
│   └── Greeting.py
└── Exceptions/
    └── IncorrectGreetingException.py
```

**`HelloWorld.py`** - Entidad de Dominio Pura:
```python
class HelloWorld(AggregateRootBase):
    def __init__(self, greeting: Greeting):
        self.greeting = greeting
    # ✅ Sin dependencias de Flask, SQLAlchemy o persistencia
```

**`HelloWorldRepositoryInterface.py`** - Puerto/Interface:
```python
class HelloWorldRepositoryInterface(ABC):
    @abstractmethod
    def save(self, hello_world: HelloWorld) -> HelloWorld:
        pass
    
    @abstractmethod
    def find_all(self) -> List[HelloWorld]:
        pass
```

---

### **2. Infrastructure (Capa de Infraestructura)**

```
Infrastructure/
├── Persistence/
│   ├── SQLAlchemy/
│   │   └── HelloWorldModel.py           # 🆕 Modelo SQLAlchemy (movido aquí)
│   └── Mappers/
│       └── HelloWorldMapper.py          # 🆕 Mapper Domain ↔ Persistencia
└── Repository/
    └── HelloWorldRepository.py          # 🆕 Implementación del repositorio
```

**`HelloWorldModel.py`** - Modelo de Persistencia:
```python
class HelloWorldModel(db.Model):
    __tablename__ = 'hello_world'
    id = Column(Integer, Sequence('hello_world_id_seq'), primary_key=True)
    greeting = Column(String(250), nullable=False)
    # ✅ SQLAlchemy solo en Infrastructure
```

**`HelloWorldMapper.py`** - Traductor entre capas:
```python
class HelloWorldMapper:
    @staticmethod
    def toDomain(model: HelloWorldModel) -> HelloWorld:
        """Convierte modelo SQLAlchemy → Entidad Dominio"""
        
    @staticmethod
    def toModel(entity: HelloWorld) -> HelloWorldModel:
        """Convierte Entidad Dominio → modelo SQLAlchemy"""
        
    @staticmethod
    def toDict(entity: HelloWorld) -> dict:
        """Serializa entidad para API"""
```

**`HelloWorldRepository.py`** - Implementación:
```python
class HelloWorldRepository(HelloWorldRepositoryInterface):
    def save(self, hello_world: HelloWorld) -> HelloWorld:
        model = HelloWorldMapper.toModel(hello_world)
        db.session.add(model)
        db.session.commit()
        return HelloWorldMapper.toDomain(model)
    
    def find_all(self) -> List[HelloWorld]:
        models = HelloWorldModel.query.all()
        return [HelloWorldMapper.toDomain(m) for m in models]
```

---

### **3. Application (Capa de Aplicación)**

**`HelloWorldService.py`** - Servicio actualizado:
```python
class HelloWorldService:
    def __init__(self, repository: HelloWorldRepositoryInterface):
        self.repository = repository  # ✅ Recibe INSTANCIA (no clase)
    
    def get_all_hello_world(self) -> list:
        entities = self.repository.find_all()
        # Serializar con el serializer de Application
        from Application.Serializers.HelloWorldSerializer import HelloWorldSerializer
        return [HelloWorldSerializer.to_dict(e) for e in entities]
    
    def addHelloWorld(self, greetingDTO: GreetingDTO) -> dict:
        greeting = Greeting.create(greetingDTO.name)
        entity = HelloWorld(greeting=greeting)
        saved = self.repository.save(hello_world)
        # Serializar con el serializer de Application
        from Application.Serializers.HelloWorldSerializer import HelloWorldSerializer
        return HelloWorldSerializer.to_dict(saved)
```

---

### **4. Controllers (Punto de entrada HTTP)**

**`HelloWorldController.py`** - Controlador con DI correcta:
```python
@helloWorldController.route('/', methods=['GET'])
def get_all_hello_world():
    container = current_app.container
    service = container.hello_world_service()     # 2. Obtener servicio
    result = service.get_all_hello_world()           # 3. Ejecutar caso de uso
    return ControllerBase.format_response(result, 200)
```

---

## Beneficios Obtenidos

### ✅ **Independencia del Dominio**
- `HelloWorld` es una entidad pura sin conocer SQLAlchemy, Flask o bases de datos
- El dominio puede ser testeado sin frameworks
- Puedes cambiar de SQLAlchemy a MongoDB sin tocar el dominio

### ✅ **Separación de Responsabilidades**
- **Domain**: Reglas de negocio puras
- **Infrastructure**: Detalles técnicos (BD, APIs, frameworks)
- **Application**: Orquestación de casos de uso

### ✅ **Inversión de Dependencias**
- El dominio define la interface (`HelloWorldRepositoryInterface`)
- La infraestructura implementa la interface (`HelloWorldRepository`)
- Domain → no depende de Infrastructure ✅
- Infrastructure → depende de Domain ✅

### ✅ **Testabilidad**
```python
# Test unitario del dominio (sin BD)
def test_create_hello_world():
    greeting = Greeting.create("Hola")
    entity = HelloWorld(greeting)
    assert entity.greeting.getValue() == "Hola"

# Test del servicio (con mock)
def test_service_with_mock():
    mock_repo = Mock(spec=HelloWorldRepositoryInterface)
    service = HelloWorldService(mock_repo)
    # ...
```

---

## Archivos Eliminados

- ❌ `Domain/HelloWorld/HelloWorldModel.py` (movido a Infrastructure)

## Archivos Creados

- 🆕 `Infrastructure/Persistence/SQLAlchemy/HelloWorldModel.py`
- 🆕 `Infrastructure/Persistence/Mappers/HelloWorldMapper.py`
- 🆕 `Domain/HelloWorld/HelloWorldRepositoryInterface.py`
- 🆕 `Infrastructure/Repository/HelloWorldRepository.py`
- 🆕 `Infrastructure/Controller/HelloWorldController.py`

## Archivos Modificados

- ✏️ `Domain/HelloWorld/HelloWorld.py` - Entidad pura
- ✏️ `Application/HelloWorldService.py` - Inyección de dependencias correcta
- ✏️ `Shared/Infrastructure/Controller/Controller.py` - Registro del nuevo controlador
- ✏️ `Infrastructure/Controller/SignalListener/HelloWorldSignalListener.py` - DI corregida

---

## Próximos Pasos Sugeridos

1. **Implementar DI Container** (dependency-injector) para no instanciar manualmente
2. **Crear Casos de Uso** separados en Application/UseCases/
3. **Implementar Eventos de Dominio** correctamente
4. **Aplicar el mismo patrón** a `MoviesService` y `ShowsRepository`
5. **Agregar tests unitarios** para el dominio
6. **Agregar tests de integración** para repositorios

---

## Endpoints Disponibles

```http
GET    /api/v1/hello-world/          # Listar todos
POST   /api/v1/hello-world/          # Crear nuevo
GET    /api/v1/hello-world/{id}      # Obtener por ID
DELETE /api/v1/hello-world/{id}      # Eliminar
```

**Ejemplo POST:**
```json
{
  "name": "Hello from Madrid"
}
```

---

## Diagrama de Flujo

```
HTTP Request
     ↓
Controller (Infrastructure)
     ↓ [crea repositorio]
     ↓ [inyecta en servicio]
Service (Application)
     ↓ [crea entidad de dominio]
     ↓ [llama al repositorio]
Repository (Infrastructure)
     ↓ [usa Mapper]
Mapper → toDomain() / toModel()
     ↓
HelloWorldModel (SQLAlchemy) ↔ HelloWorld (Domain)
     ↓
Database
```
