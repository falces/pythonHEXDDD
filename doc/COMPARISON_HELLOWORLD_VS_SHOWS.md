# Comparación: HelloWorld vs Shows/Movies

## Tabla Comparativa

| Aspecto | HelloWorld | Shows/Movies |
|---------|-----------|--------------|
| **Origen de Datos** | Base de Datos (MySQL) | API Externa (HTTP) |
| **Framework de Persistencia** | SQLAlchemy | requests + APITools |
| **Modelo de Infrastructure** | `HelloWorldModel` (db.Model) | `ShowAPIModel` (POJO) |
| **Operaciones Soportadas** | CRUD completo (Create, Read, Delete) | Solo lectura (Read) |
| **Configuración** | Database URI, conexión | API Host, API Key |
| **Tabla/Endpoint** | `hello_world` table | `/shows` endpoint |

---

## Arquitectura Compartida

Ambos módulos siguen **exactamente el mismo patrón** de arquitectura hexagonal:

### ✅ **1. Domain Layer (idéntica estructura)**

```
Domain/
├── {Module}/
│   ├── {Module}.py                    # Entidad agregada
│   ├── {Module}RepositoryInterface.py # Interface/Puerto
│   └── ValueObjects/                  # Value objects específicos
```

**HelloWorld:**
```python
class HelloWorld(AggregateRootBase):
    def __init__(self, greeting: Greeting):
        self.greeting = greeting
```

**Show:**
```python
class Show(AggregateRootBase):
    def __init__(self, show_id: ShowId, title: ShowTitle, 
                 show_type: ShowType, streaming_option: StreamingOption):
        self.show_id = show_id
        self.title = title
        # ...
```

**Características comunes:**
- ✅ Sin dependencias de frameworks
- ✅ Value Objects con validaciones
- ✅ Lógica de negocio pura
- ✅ Testeable sin infraestructura

---

### ✅ **2. Application Layer (mismo patrón)**

**HelloWorldService:**
```python
class HelloWorldService:
    def __init__(self, repository: HelloWorldRepositoryInterface):
        self.repository = repository  # ✅ Inyección de dependencias
    
    def getAllHelloWorld(self) -> list:
        entities = self.repository.findAll()
        return [HelloWorldMapper.to_dict(e) for e in entities]
```

**MoviesService:**
```python
class MoviesService:
    def __init__(self, repository: ShowRepositoryInterface):
        self.repository = repository  # ✅ Inyección de dependencias
    
    def getMoviesByCriteria(self, criteria: Dict) -> List[dict]:
        entities = self.repository.findByCriteria(criteria)
        return ShowMapper.toDictList(entities)
```

**Patrón común:**
1. Recibe interface del repositorio (DI)
2. Orquesta operaciones de dominio
3. Usa Mapper para serialización
4. Retorna diccionarios para HTTP

---

### ✅ **3. Infrastructure Layer (adaptadores diferentes)**

#### **3.1 Modelos de Persistencia/API**

**HelloWorldModel (SQLAlchemy):**
```python
class HelloWorldModel(db.Model):
    __tablename__ = 'hello_world'
    id = Column(Integer, Sequence('hello_world_id_seq'), primary_key=True)
    greeting = Column(String(250), nullable=False)
```

**ShowAPIModel (POJO):**
```python
class ShowAPIModel:
    def __init__(self, show_id, original_title, show_type, streaming_options):
        self.show_id = show_id
        self.original_title = original_title
        # ...
    
    @staticmethod
    def fromAPIResponse(api_data: dict) -> 'ShowAPIModel':
        # Parsea respuesta de API externa
```

**Diferencias:**
- HelloWorld: Clase de SQLAlchemy con metadatos de tabla
- Show: POJO simple que parsea JSON de API

---

#### **3.2 Mappers (mismo propósito, diferente origen)**

**HelloWorldMapper:**
```python
class HelloWorldMapper:
    @staticmethod
    def toDomain(model: HelloWorldModel) -> HelloWorld:
        # SQLAlchemy Model → Domain Entity
        greeting = Greeting.create(model.greeting)
        entity = HelloWorld(greeting=greeting)
        entity._id = model.id
        return entity
    
    @staticmethod
    def toModel(entity: HelloWorld) -> HelloWorldModel:
        # Domain Entity → SQLAlchemy Model
        return HelloWorldModel(
            greeting=entity.greeting.getValue(),
            id=getattr(entity, '_id', None)
        )
```

**ShowMapper:**
```python
class ShowMapper:
    @staticmethod
    def toDomain(api_model: ShowAPIModel) -> Show:
        # API Model → Domain Entity
        show_id = ShowId.create(api_model.show_id)
        title = ShowTitle.create(api_model.original_title)
        # ...
        return Show(show_id, title, show_type, streaming_option)
    
    # No necesita toModel() porque solo lee de API
```

**Patrón común:**
- `toDomain()`: Fuente externa → Entidad de dominio
- `toDict()`: Entidad de dominio → JSON para HTTP
- Diferencia: HelloWorld necesita `toModel()` para escritura

---

#### **3.3 Repositorios (implementaciones diferentes)**

**HelloWorldRepository (SQLAlchemy):**
```python
class HelloWorldRepository(HelloWorldRepositoryInterface):
    def save(self, hello_world: HelloWorld) -> HelloWorld:
        model = HelloWorldMapper.toModel(hello_world)
        db.session.add(model)
        db.session.commit()
        return HelloWorldMapper.toDomain(model)
    
    def findAll(self) -> List[HelloWorld]:
        models = db.session.query(HelloWorldModel).all()
        return [HelloWorldMapper.toDomain(m) for m in models]
```

**ShowsRepository (API externa):**
```python
class ShowsRepository(ShowRepositoryInterface):
    def __init__(self):
        self.api_tools = APITools(url, headers)
    
    def findByCriteria(self, criteria: Dict) -> List[Show]:
        response = self.api_tools.get('/search/filters', params=criteria)
        
        shows = []
        for show_data in response.get("shows", []):
            api_model = ShowAPIModel.fromAPIResponse(show_data)
            domain_entity = ShowMapper.toDomain(api_model)
            shows.append(domain_entity)
        
        return shows
```

**Diferencias:**
- HelloWorld: Operaciones con `db.session` (SQLAlchemy)
- Shows: Llamadas HTTP con `api_tools.get()` (requests)
- HelloWorld: Escritura y lectura
- Shows: Solo lectura

---

### ✅ **4. Controllers (mismo patrón de DI)**

**HelloWorldController:**
```python
@helloWorldController.route('/', methods=['GET'])
def getAllHelloWorld():
    repository = HelloWorldRepository()        # 1. Instanciar
    service = HelloWorldService(repository)    # 2. Inyectar
    result = service.getAllHelloWorld()        # 3. Ejecutar
    return ControllerBase.formatResponse(result, 200)
```

**MoviesController:**
```python
@moviesController.route('/', methods=['GET'])
def getMoviesBy():
    repository = ShowsRepository()             # 1. Instanciar
    service = MoviesService(repository)        # 2. Inyectar
    result = service.getMoviesByCriteria(...)  # 3. Ejecutar
    return ControllerBase.formatResponse(result, 200)
```

**Patrón idéntico:**
1. Instanciar repositorio concreto
2. Inyectar en servicio
3. Ejecutar caso de uso
4. Formatear respuesta

---

## Flujos de Datos Comparados

### **HelloWorld - CREATE (POST)**

```
HTTP POST /api/v1/hello-world/
     ↓
Controller → instancia Repository + Service
     ↓
Service → crea Greeting (VO) + HelloWorld (Entity)
     ↓
Repository.save(entity)
     ↓
Mapper.toModel(entity) → HelloWorldModel
     ↓
SQLAlchemy: db.session.add() + commit()
     ↓
Mapper.toDomain(model) → HelloWorld
     ↓
Service → Mapper.toDict(entity)
     ↓
JSON Response
```

### **Shows - READ (GET)**

```
HTTP GET /api/v1/movies/?country=us
     ↓
Controller → instancia Repository + Service
     ↓
Service.getMoviesByCriteria(criteria)
     ↓
Repository.findByCriteria(criteria)
     ↓
APITools.get('/search/filters', params)
     ↓
API Externa: JSON Response
     ↓
ShowAPIModel.fromAPIResponse(json)
     ↓
Mapper.toDomain(api_model) → Show
     ↓
Service → Mapper.toDictList(entities)
     ↓
JSON Response
```

---

## Value Objects Comparados

### **HelloWorld**
- `Greeting` (StringValueObject)
  - Valida longitud (1-255 caracteres)

### **Shows**
- `ShowId` (StringValueObject)
  - Valida que no esté vacío
- `ShowTitle` (StringValueObject)
  - Valida longitud (1-500 caracteres)
- `ShowType` (StringValueObject con enum)
  - Valida valores permitidos: 'movie', 'series'
  - Métodos: `isMovie()`, `isSeries()`
- `StreamingOption` (Value Object complejo)
  - service_name, url
  - Métodos: `hasUrl()`, `toDict()`

**Patrón común:**
- Heredan de base común o implementan validaciones
- Encapsulan reglas de negocio
- Inmutables

---

## Configuración Necesaria

### **HelloWorld**
```python
# config/database.py
SQLALCHEMY_DATABASE_URI = 'mysql://user:pass@localhost/pythonhexddd'
```

### **Shows/Movies**
```python
# config/environment.py
STREAM_AVAILABILITY_HOST = 'streaming-availability.p.rapidapi.com'
STREAM_AVAILABILITY_KEY = 'your_api_key_here'
```

---

## Endpoints Comparados

### **HelloWorld**
```http
GET    /api/v1/hello-world/          # Listar todos
POST   /api/v1/hello-world/          # Crear nuevo
       Body: { "name": "Hello World" }
GET    /api/v1/hello-world/{id}      # Obtener por ID
DELETE /api/v1/hello-world/{id}      # Eliminar
```

### **Shows/Movies**
```http
GET /api/v1/movies/?country=us&showType=movie  # Buscar por criterios
GET /api/v1/movies/{show_id}                   # Obtener por ID
```

---

## Testing Comparado

### **Test Unitario del Dominio**

**HelloWorld:**
```python
def test_hello_world_creation():
    greeting = Greeting.create("Hello")
    entity = HelloWorld(greeting=greeting)
    assert entity.greeting.getValue() == "Hello"
```

**Show:**
```python
def test_show_creation():
    show = Show(
        ShowId.create("tt123"),
        ShowTitle.create("Movie"),
        ShowType.create("movie")
    )
    assert show.getId() == "tt123"
    assert show.isMovie() == True
```

### **Test del Servicio con Mock**

**HelloWorld:**
```python
def test_service():
    mock_repo = Mock(spec=HelloWorldRepositoryInterface)
    mock_repo.findAll.return_value = [HelloWorld(...)]
    
    service = HelloWorldService(mock_repo)
    result = service.getAllHelloWorld()
    assert len(result) == 1
```

**Shows:**
```python
def test_service():
    mock_repo = Mock(spec=ShowRepositoryInterface)
    mock_repo.findByCriteria.return_value = [Show(...)]
    
    service = MoviesService(mock_repo)
    result = service.getMoviesByCriteria({"country": "us"})
    assert len(result) == 1
```

**Patrón idéntico:**
- Mock de la interface del repositorio
- Inyección en servicio
- Assertions sobre el resultado

---

## Resumen: Misma Arquitectura, Diferentes Adaptadores

| Capa | HelloWorld | Shows | Patrón Común |
|------|-----------|-------|--------------|
| **Domain** | ✅ Entidad pura | ✅ Entidad pura | Mismo patrón |
| **Application** | ✅ Servicio con DI | ✅ Servicio con DI | Mismo patrón |
| **Infrastructure (Modelo)** | SQLAlchemy Model | API Model (POJO) | **Diferente** |
| **Infrastructure (Repo)** | db.session operations | HTTP requests | **Diferente** |
| **Infrastructure (Mapper)** | DB ↔ Domain | API ↔ Domain | Mismo patrón |
| **Controller** | ✅ DI pattern | ✅ DI pattern | Mismo patrón |

---

## Conclusión

Ambos módulos demuestran que **la arquitectura hexagonal es consistente independientemente de la fuente de datos**:

- ✅ **Domain** siempre puro e independiente
- ✅ **Application** siempre orquesta casos de uso
- ✅ **Infrastructure** se adapta a la tecnología (SQLAlchemy vs HTTP API)
- ✅ **Mappers** traducen entre capas
- ✅ **Controllers** siguen el mismo patrón de DI

**La diferencia está solo en los adaptadores (Infrastructure), el core de la arquitectura es idéntico.**
