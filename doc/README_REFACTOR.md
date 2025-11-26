# Arquitectura Hexagonal - Refactorización Completa

## 📋 Resumen

Este repositorio implementa una **API REST con Flask** siguiendo los principios de **Arquitectura Hexagonal** (Ports & Adapters). Se han refactorizado dos módulos completos aplicando correctamente la separación de capas:

1. ✅ **HelloWorld** - Persistencia en base de datos (SQLAlchemy + MySQL)
2. ✅ **Shows/Movies** - Consulta a API externa (Stream Availability API)

---

## 🏗️ Estructura del Proyecto

```
app/
├── Domain/                           # ⚡ Capa de Dominio (Lógica de Negocio Pura)
│   ├── HelloWorld/
│   │   ├── HelloWorld.py            # Entidad agregada (Aggregate Root)
│   │   ├── HelloWorldRepositoryInterface.py  # Puerto Write
│   │   ├── HelloWorldReadRepositoryInterface.py  # Puerto Read (CQRS)
│   │   ├── Events/                  # Domain Events
│   │   │   ├── HelloWorldCreated.py
│   │   │   └── HelloWorldDeleted.py
│   │   └── ValueObjects/
│   │       └── GreetingValueObject.py
│   └── Show/
│       ├── Show.py                  # Entidad agregada
│       ├── ShowRepositoryInterface.py
│       └── ValueObjects/
│           ├── ShowId.py
│           ├── ShowTitle.py
│           ├── ShowType.py
│           └── StreamingOption.py
│
├── Application/                      # 🔄 Capa de Aplicación (CQRS)
│   ├── Commands/                    # Comandos inmutables
│   │   ├── CreateHelloWorldCommand.py
│   │   ├── UpdateHelloWorldCommand.py
│   │   └── DeleteHelloWorldCommand.py
│   ├── CommandHandlers/             # Handlers de comandos
│   │   ├── CreateHelloWorldHandler.py
│   │   ├── UpdateHelloWorldHandler.py
│   │   └── DeleteHelloWorldHandler.py
│   ├── Queries/                     # Queries inmutables
│   │   ├── GetAllHelloWorldQuery.py
│   │   ├── GetHelloWorldByIdQuery.py
│   │   └── SearchHelloWorldQuery.py
│   ├── QueryHandlers/               # Handlers de queries
│   │   ├── GetAllHelloWorldHandler.py
│   │   ├── GetHelloWorldByIdHandler.py
│   │   └── SearchHelloWorldHandler.py
│   ├── ReadModels/                  # DTOs de lectura
│   │   └── HelloWorldReadModel.py
│   ├── EventHandlers/               # Handlers de eventos de dominio
│   │   ├── HelloWorldCreatedLogger.py
│   │   └── HelloWorldDeletedLogger.py
│   ├── MoviesService.py             # Servicio para Shows (legacy)
│   └── UseCases/
│       └── Shows/                   # Use Cases tradicionales
│           ├── SearchShowsUseCase.py
│           └── GetShowByIdUseCase.py
│
├── Infrastructure/                   # 🔌 Capa de Infraestructura (Adaptadores)
│   ├── Persistence/
│   │   ├── SQLAlchemy/
│   │   │   └── HelloWorldModel.py   # Modelo de base de datos
│   │   └── Mappers/
│   │       └── HelloWorldMapper.py  # Domain ↔ DB
│   │
│   ├── ExternalAPI/
│   │   ├── Models/
│   │   │   └── ShowAPIModel.py      # Modelo de API externa
│   │   └── Mappers/
│   │       └── ShowMapper.py        # Domain ↔ API
│   │
│   ├── Repository/
│   │   ├── HelloWorldWriteRepository.py  # Impl. Write (CQRS)
│   │   ├── HelloWorldReadRepository.py   # Impl. Read (CQRS)
│   │   └── ShowsAPIRepository.py         # Implementación API externa
│   │
│   ├── Projections/                 # Proyecciones CQRS
│   │   └── HelloWorldProjection.py
│   │
│   └── Controller/
│       ├── HelloWorldController.py  # Usa CommandBus/QueryBus
│       └── MoviesController.py
│
├── Shared/                          # 🔧 Componentes compartidos
│   ├── Application/
│   │   ├── CommandBus.py            # Bus de comandos
│   │   ├── QueryBus.py              # Bus de queries
│   │   ├── CommandHandler.py        # Interface ABC
│   │   └── QueryHandler.py          # Interface ABC
│   ├── Domain/
│   │   ├── Entities/
│   │   │   └── EntityBase.py        # AggregateRootBase
│   │   ├── Events/
│   │   │   ├── DomainEvent.py
│   │   │   └── EventDispatcherInterface.py
│   │   └── ValueObjects/
│   └── Infrastructure/
│       ├── Events/
│       │   └── EventDispatcher.py
│       └── APITools.py
│
└── config/
    └── container.py                 # DI Container
```

---

## 🎯 Principios Aplicados

### ✅ **Separación de Capas**

| Capa | Responsabilidad | Dependencias |
|------|----------------|--------------|
| **Domain** | Lógica de negocio pura | ❌ Ninguna (independiente) |
| **Application** | Orquestar casos de uso | → Domain |
| **Infrastructure** | Detalles técnicos (BD, APIs, HTTP) | → Domain, Application |

### ✅ **Dependency Inversion Principle (DIP)**

```
┌─────────────────────┐
│   Domain Layer      │
│  ┌──────────────┐   │
│  │  Interface   │   │  ← Define el contrato
│  └──────────────┘   │
└──────────┬──────────┘
           │ implements
┌──────────▼──────────┐
│ Infrastructure      │
│  ┌──────────────┐   │
│  │Implementation│   │  ← Implementa el contrato
│  └──────────────┘   │
└─────────────────────┘
```

- Domain define las **interfaces** (puertos)
- Infrastructure **implementa** las interfaces (adaptadores)
- Application depende de las **abstracciones**, no de implementaciones concretas

### ✅ **Inyección de Dependencias**

```python
# ❌ ANTES (malo)
class MoviesService:
    def __init__(self, repository):
        self.repository = repository()  # Instancia aquí

# ✅ DESPUÉS (correcto)
class MoviesService:
    def __init__(self, repository: ShowRepositoryInterface):
        self.repository = repository  # Recibe instancia inyectada
```

### ✅ **Mappers (Traducción entre capas)**

```
External World (API/DB)
        ↓
   API Model / DB Model
        ↓
    [Mapper]
        ↓
  Domain Entity (pura)
        ↓
   Application
        ↓
    [Mapper]
        ↓
     JSON/DTO
        ↓
    HTTP Response
```

---

## 📦 Módulos Refactorizados

### 1️⃣ **HelloWorld** (Base de Datos)

**Flujo:**
```
POST /api/v1/hello-world/
  ↓
HelloWorldController
  ↓ [crea HelloWorldRepository()]
  ↓ [inyecta en HelloWorldService()]
HelloWorldService
  ↓ [crea Greeting (Value Object)]
  ↓ [crea HelloWorld (Entity)]
  ↓ [llama repository.save()]
HelloWorldRepository
  ↓ [Mapper.toModel() → HelloWorldModel]
  ↓ [SQLAlchemy: INSERT]
  ↓ [Mapper.toDomain() → HelloWorld]
  ↓ [retorna Entity]
HelloWorldService
  ↓ [Mapper.toDict()]
JSON Response
```

**Endpoints:**
```http
GET    /api/v1/hello-world/          # Listar todos
POST   /api/v1/hello-world/          # Crear nuevo
GET    /api/v1/hello-world/{id}      # Obtener por ID
DELETE /api/v1/hello-world/{id}      # Eliminar
```

---

### 2️⃣ **Shows/Movies** (API Externa)

**Flujo:**
```
GET /api/v1/movies/?country=us&showType=movie
  ↓
MoviesController
  ↓ [crea ShowsRepository()]
  ↓ [inyecta en MoviesService()]
MoviesService
  ↓ [llama repository.findByCriteria()]
ShowsRepository
  ↓ [APITools.get() → API externa]
  ↓ [recibe JSON]
  ↓ [ShowAPIModel.fromAPIResponse()]
  ↓ [ShowMapper.toDomain() → Show entities]
  ↓ [retorna List<Show>]
MoviesService
  ↓ [ShowMapper.toDictList()]
JSON Response
```

**Endpoints:**
```http
GET /api/v1/movies/?country=us&showType=movie  # Buscar shows
GET /api/v1/movies/{show_id}                   # Obtener show por ID
```

---

## 🔑 Conceptos Clave

### **Entidad de Dominio (Aggregate Root)**

```python
class Show(AggregateRootBase):
    def __init__(self, show_id: ShowId, title: ShowTitle, 
                 show_type: ShowType, streaming_option: StreamingOption):
        self.show_id = show_id
        self.title = title
        self.show_type = show_type
        self.streaming_option = streaming_option
    
    # ✅ Sin dependencias externas
    # ✅ Solo lógica de negocio
    # ✅ Testeable sin frameworks
```

### **Value Object**

```python
class ShowType(StringValueObject):
    VALID_TYPES = ['movie', 'series']
    
    def __init__(self, value: str):
        if value.lower() not in self.VALID_TYPES:
            raise IncorrectValueException(f"Invalid type: {value}")
        super().__init__(value=value.lower())
    
    def isMovie(self) -> bool:
        return self.value == 'movie'
```

### **Repository Interface (Puerto)**

```python
# Domain/Show/ShowRepositoryInterface.py
class ShowRepositoryInterface(ABC):
    @abstractmethod
    def findByCriteria(self, criteria: Dict) -> List[Show]:
        pass
```

### **Repository Implementation (Adaptador)**

```python
# Infrastructure/Repository/ShowsRepository.py
class ShowsRepository(ShowRepositoryInterface):
    def findByCriteria(self, criteria: Dict) -> List[Show]:
        # Llama API externa
        response = self.api_tools.get('/search/filters', params=criteria)
        
        # Convierte a entidades de dominio
        return [ShowMapper.toDomain(ShowAPIModel.fromAPIResponse(data)) 
                for data in response['shows']]
```

### **Mapper**

```python
class ShowMapper:
    @staticmethod
    def toDomain(api_model: ShowAPIModel) -> Show:
        """API Model → Domain Entity"""
        return Show(
            show_id=ShowId.create(api_model.show_id),
            title=ShowTitle.create(api_model.original_title),
            show_type=ShowType.create(api_model.show_type),
            streaming_option=StreamingOption.create(...)
        )
    
    @staticmethod
    def toDict(entity: Show) -> dict:
        """Domain Entity → JSON"""
        return {
            "id": entity.getId(),
            "originalTitle": entity.getTitle(),
            "showType": entity.getType(),
            ...
        }
```

---

## 🧪 Testing

### **Test Unitario del Dominio** (sin infraestructura)

```python
def test_show_creation():
    show = Show(
        show_id=ShowId.create("tt123"),
        title=ShowTitle.create("Test Movie"),
        show_type=ShowType.create("movie"),
        streaming_option=StreamingOption.create("Netflix", "https://...")
    )
    
    assert show.getId() == "tt123"
    assert show.isMovie() == True
    assert show.hasStreamingOption() == True
```

### **Test del Servicio con Mock**

```python
def test_movies_service():
    mock_repo = Mock(spec=ShowRepositoryInterface)
    mock_repo.findByCriteria.return_value = [
        Show(ShowId.create("tt1"), ShowTitle.create("Movie"), 
             ShowType.create("movie"))
    ]
    
    service = MoviesService(mock_repo)
    result = service.getMoviesByCriteria({"country": "us"})
    
    assert len(result) == 1
    assert result[0]["originalTitle"] == "Movie"
```

---

## 🚀 Instalación y Uso

### **Requisitos**
- Python 3.9+
- MySQL 8.0+
- Docker (opcional)

### **Instalación**

```bash
# Clonar repositorio
git clone https://github.com/falces/pythonHEXDDD.git
cd pythonHEXDDD

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales
```

### **Ejecutar con Docker**

```bash
cd docker
docker-compose up -d
```

### **Ejecutar local**

```bash
python app/app.py
```

La API estará disponible en `http://localhost:5000`

---

## 📚 Documentación Adicional

- 📄 [REFACTOR_PERSISTENCE_SEPARATION.md](./REFACTOR_PERSISTENCE_SEPARATION.md) - Refactorización HelloWorld
- 📄 [REFACTOR_SHOWS_MOVIES.md](./REFACTOR_SHOWS_MOVIES.md) - Refactorización Shows/Movies
- 📄 [ARCHITECTURE_DIAGRAM.md](./ARCHITECTURE_DIAGRAM.md) - Diagramas visuales de arquitectura

---

## ✅ Beneficios Obtenidos

| Antes ❌ | Después ✅ |
|---------|-----------|
| Domain depende de SQLAlchemy | Domain independiente |
| Entidades conocen persistencia | Entidades puras |
| Servicios instancian repositorios | Inyección de dependencias |
| Sin separación de capas | Capas bien definidas |
| Difícil de testear | Fácil de testear |
| Acoplamiento alto | Bajo acoplamiento |
| Cambiar BD toca Domain | Solo cambia Infrastructure |

---

## 🎯 Próximos Pasos

1. ⏳ Implementar **DI Container** (dependency-injector)
2. ⏳ Crear **Casos de Uso** separados en Application/UseCases/
3. ⏳ Implementar **Eventos de Dominio**
4. ⏳ Agregar **Tests unitarios completos**
5. ⏳ Agregar **Tests de integración**
6. ⏳ Documentación **OpenAPI/Swagger**
7. ⏳ **CI/CD** con GitHub Actions

---

## 📖 Referencias

- [Hexagonal Architecture (Alistair Cockburn)](https://alistair.cockburn.us/hexagonal-architecture/)
- [Domain-Driven Design (Eric Evans)](https://domainlanguage.com/ddd/)
- [Clean Architecture (Robert C. Martin)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

---

## 👨‍💻 Autor

**falces**
- GitHub: [@falces](https://github.com/falces)
- Repository: [pythonHEXDDD](https://github.com/falces/pythonHEXDDD)

---

## 📝 Licencia

Este proyecto es una plantilla de código abierto para APIs con arquitectura hexagonal en Python.
