# Refactorización: Shows/Movies con Arquitectura Hexagonal

## Resumen

Se ha aplicado el mismo patrón de arquitectura hexagonal al módulo de Shows/Movies, separando completamente el dominio de los detalles de infraestructura (API externa).

---

## Estructura Creada

### **1. Domain Layer (Capa de Dominio - Pura)**

```
Domain/Show/
├── Show.py                           # Entidad de dominio pura
├── ShowRepositoryInterface.py        # Puerto/Interface del repositorio
└── ValueObjects/
    ├── ShowId.py                     # Identificador del show
    ├── ShowTitle.py                  # Título con validaciones
    ├── ShowType.py                   # Tipo (movie/series) con validaciones
    └── StreamingOption.py            # Opción de streaming
```

**Características:**
- ✅ Sin dependencias de Flask, requests o APIs externas
- ✅ Validaciones de negocio en Value Objects
- ✅ Entidad pura con comportamiento de dominio
- ✅ Testeable sin infraestructura

---

### **2. Infrastructure Layer**

```
Infrastructure/
├── ExternalAPI/
│   ├── Models/
│   │   └── ShowAPIModel.py          # Modelo de respuesta API
│   └── Mappers/
│       └── ShowMapper.py            # Domain ↔ API
└── Repository/
    └── ShowsRepository.py           # Implementación del repositorio
```

**ShowAPIModel.py** - Modelo de la API externa:
```python
class ShowAPIModel:
    def __init__(self, show_id, original_title, show_type, streaming_options):
        # Representa la estructura de la API externa
        
    @staticmethod
    def fromAPIResponse(api_data: dict) -> 'ShowAPIModel':
        # Parsea la respuesta de la API externa
```

**ShowMapper.py** - Traductor entre capas:
```python
class ShowMapper:
    @staticmethod
    def toDomain(api_model: ShowAPIModel) -> Show:
        """API Model → Domain Entity"""
        
    @staticmethod
    def toDict(entity: Show) -> dict:
        """Domain Entity → JSON Response"""
        
    @staticmethod
    def toDictList(entities: List[Show]) -> List[dict]:
        """List of Entities → List of Dicts"""
```

**ShowsRepository.py** - Implementación:
```python
class ShowsRepository(ShowRepositoryInterface):
    def findByCriteria(self, criteria: Dict) -> List[Show]:
        # 1. Llama a API externa
        response = self.api_tools.get('/search/filters', params=criteria)
        
        # 2. Convierte respuesta a ShowAPIModel
        api_models = [ShowAPIModel.fromAPIResponse(d) for d in response]
        
        # 3. Convierte a entidades de dominio
        return [ShowMapper.toDomain(m) for m in api_models]
```

---

### **3. Application Layer**

**MoviesService.py** - Servicio actualizado:
```python
class MoviesService:
    def __init__(self, repository: ShowRepositoryInterface):
        self.repository = repository  # ✅ Recibe INSTANCIA
    
    def getMoviesByCriteria(self, criteria: Dict) -> List[dict]:
        shows = self.repository.findByCriteria(criteria)
        return ShowMapper.toDictList(shows)
    
    def getShowById(self, show_id: str) -> dict:
        show = self.repository.findById(show_id)
        return ShowMapper.toDict(show) if show else None
```

---

### **4. Controllers (HTTP)**

**MoviesController.py** - Controlador actualizado:
```python
@moviesController.route('/', methods=['GET'])
def getMoviesBy():
    repository = ShowsRepository()              # 1. Instanciar repositorio
    service = MoviesService(repository)         # 2. Inyectar en servicio
    result = service.getMoviesByCriteria(       # 3. Ejecutar caso de uso
        request.args.to_dict()
    )
    return ControllerBase.formatResponse(result, 200)

@moviesController.route('/<show_id>', methods=['GET'])
def getMovieById(show_id: str):
    repository = ShowsRepository()
    service = MoviesService(repository)
    result = service.getShowById(show_id)
    
    if result is None:
        return ControllerBase.formatResponse({"error": "Show not found"}, 404)
    
    return ControllerBase.formatResponse(result, 200)
```

---

## Comparación Antes vs Después

### **Antes ❌**

```python
# MoviesController.py
moviesService = MoviesService(ShowsRepository)  # Pasa clase
moviesService.getMoviesByCriteria(request.args)

# MoviesService.py
def __init__(self, repository: AbstractRepository):
    self.repository = repository()  # ❌ Instancia aquí

# ShowsRepository.py
class ShowsRepository(AbstractRepository):
    def findByCriteria(self, args: dict) -> dict:
        response = self.api_tools.get('/search/filters', params=args)
        shows = []
        for show in response["shows"]:
            # ❌ Usa servicio de traducción mezclado
            shows.append(ShowsModelTranslationService.showsTranslation(show))
        return shows
```

**Problemas:**
- ❌ No existe entidad de dominio Show
- ❌ Datos de API se pasan directamente como dict
- ❌ Sin validaciones de dominio
- ❌ Servicio instancia repositorio (viola DI)
- ❌ Acoplamiento directo a estructura de API externa

---

### **Después ✅**

```python
# MoviesController.py
repository = ShowsRepository()           # Instancia repositorio
service = MoviesService(repository)      # ✅ Inyecta instancia
result = service.getMoviesByCriteria(criteria)

# MoviesService.py
def __init__(self, repository: ShowRepositoryInterface):
    self.repository = repository  # ✅ Recibe instancia

def getMoviesByCriteria(self, criteria: Dict) -> List[dict]:
    shows = self.repository.findByCriteria(criteria)  # Entidades de dominio
    return ShowMapper.toDictList(shows)

# ShowsRepository.py
def findByCriteria(self, criteria: Dict) -> List[Show]:
    response = self.api_tools.get('/search/filters', params=criteria)
    
    shows = []
    for show_data in response.get("shows", []):
        api_model = ShowAPIModel.fromAPIResponse(show_data)  # API Model
        domain_entity = ShowMapper.toDomain(api_model)       # ✅ Domain Entity
        if domain_entity:
            shows.append(domain_entity)
    
    return shows  # ✅ Devuelve entidades de dominio
```

**Mejoras:**
- ✅ Entidad de dominio `Show` pura
- ✅ Value Objects con validaciones (`ShowType`, `ShowTitle`, etc.)
- ✅ Repositorio devuelve entidades de dominio
- ✅ Inyección de dependencias correcta
- ✅ Mapper separa API de Dominio
- ✅ Testeable sin API externa

---

## Value Objects Creados

### **ShowId**
```python
ShowId.create("tt1234567")  # Valida que no esté vacío
```

### **ShowTitle**
```python
ShowTitle.create("The Matrix")  # Valida longitud (1-500 chars)
```

### **ShowType**
```python
show_type = ShowType.create("movie")
show_type.isMovie()   # True
show_type.isSeries()  # False
# Valida que sea 'movie' o 'series'
```

### **StreamingOption**
```python
streaming = StreamingOption.create(
    service_name="Netflix",
    url="https://netflix.com/watch/123"
)
streaming.getServiceName()  # "Netflix"
streaming.hasUrl()           # True
```

---

## Flujo de Datos

### **Búsqueda de Shows (GET /api/v1/movies/?country=us)**

```
HTTP Request
     ↓
MoviesController
     ↓ [instancia ShowsRepository]
     ↓ [inyecta en MoviesService]
MoviesService
     ↓ [llama repository.findByCriteria()]
ShowsRepository (Infrastructure)
     ↓ [llama API externa con APITools]
     ↓ [recibe JSON response]
     ↓
ShowAPIModel.fromAPIResponse(json)
     ↓ [parsea respuesta API]
ShowMapper.toDomain(api_model)
     ↓ [crea Value Objects]
     ↓ [crea entidad Show]
Show (Domain Entity) ← ✅ Entidad pura
     ↓
[List<Show>] retorna a servicio
     ↓
ShowMapper.toDictList(shows)
     ↓ [serializa para HTTP]
JSON Response → Cliente
```

---

## Diferencias Clave con HelloWorld

| Aspecto | HelloWorld | Shows/Movies |
|---------|-----------|--------------|
| **Origen de datos** | Base de datos (SQLAlchemy) | API externa (HTTP) |
| **Modelo de persistencia** | `HelloWorldModel` (SQLAlchemy) | `ShowAPIModel` (POJO) |
| **Escritura** | Sí (`save()`) | No (solo lectura) |
| **Mapper origen** | SQLAlchemy Model | JSON de API |
| **Configuración** | Database connection | API keys y host |

**Ambos comparten:**
- ✅ Entidad de dominio pura
- ✅ Value Objects con validaciones
- ✅ Interface de repositorio en Domain
- ✅ Implementación en Infrastructure
- ✅ Mapper para traducir capas
- ✅ Inyección de dependencias en servicios

---

## Endpoints Disponibles

```http
GET /api/v1/movies/?country=us&showType=movie
  → Busca shows por criterios

GET /api/v1/movies/{show_id}
  → Obtiene un show específico por ID
```

**Ejemplo de respuesta:**
```json
{
  "status": "ok",
  "data": [
    {
      "id": "tt1234567",
      "originalTitle": "The Matrix",
      "showType": "movie",
      "streamingOptions": {
        "service": "Netflix",
        "url": "https://netflix.com/watch/123"
      }
    }
  ]
}
```

---

## Testing

### **Test Unitario del Dominio**
```python
def test_show_creation():
    show_id = ShowId.create("tt123")
    title = ShowTitle.create("Test Movie")
    show_type = ShowType.create("movie")
    streaming = StreamingOption.create("Netflix", "https://...")
    
    show = Show(show_id, title, show_type, streaming)
    
    assert show.getId() == "tt123"
    assert show.isMovie() == True
    assert show.hasStreamingOption() == True
```

### **Test de Value Objects**
```python
def test_show_type_validation():
    with pytest.raises(IncorrectValueException):
        ShowType.create("invalid_type")  # Solo acepta movie/series
    
    show_type = ShowType.create("movie")
    assert show_type.isMovie() == True
```

### **Test del Servicio con Mock**
```python
def test_service_get_movies():
    mock_repo = Mock(spec=ShowRepositoryInterface)
    mock_repo.findByCriteria.return_value = [
        Show(ShowId.create("tt1"), ShowTitle.create("Movie 1"), 
             ShowType.create("movie"))
    ]
    
    service = MoviesService(mock_repo)
    result = service.getMoviesByCriteria({"country": "us"})
    
    assert len(result) == 1
    assert result[0]["originalTitle"] == "Movie 1"
```

---

## Archivos Modificados

- ✏️ `Application/MoviesService.py` - Inyección de dependencias y entidades
- ✏️ `Infrastructure/Repository/ShowsRepository.py` - Implementa interface y devuelve entidades
- ✏️ `Infrastructure/Controller/MoviesController.py` - DI correcta y nuevo endpoint

## Archivos Creados

- 🆕 `Domain/Show/Show.py`
- 🆕 `Domain/Show/ShowRepositoryInterface.py`
- 🆕 `Domain/Show/ValueObjects/ShowId.py`
- 🆕 `Domain/Show/ValueObjects/ShowTitle.py`
- 🆕 `Domain/Show/ValueObjects/ShowType.py`
- 🆕 `Domain/Show/ValueObjects/StreamingOption.py`
- 🆕 `Infrastructure/ExternalAPI/Models/ShowAPIModel.py`
- 🆕 `Infrastructure/ExternalAPI/Mappers/ShowMapper.py`

## Archivos Obsoletos (pueden eliminarse)

- ❌ `Infrastructure/Service/ShowsModelTranslationService.py` (reemplazado por ShowMapper)

---

## Próximos Pasos

1. ✅ **HelloWorld separado** - Completado
2. ✅ **Shows/Movies separado** - Completado
3. ⏳ **Implementar DI Container** (dependency-injector)
4. ⏳ **Crear Casos de Uso** en Application/UseCases/
5. ⏳ **Eventos de Dominio** correctos
6. ⏳ **Tests unitarios y de integración**
7. ⏳ **Documentación OpenAPI/Swagger**

---

## Conclusión

✅ **Domain independiente**: Show no conoce APIs externas  
✅ **Infrastructure adaptable**: Puedes cambiar de API sin tocar Domain  
✅ **Mapper centralizado**: Traduce entre API y Domain  
✅ **DI correcta**: Servicios reciben instancias  
✅ **Value Objects**: Validaciones de dominio  
✅ **Testeable**: Domain y Application se testean sin API externa  
✅ **Arquitectura Hexagonal**: Correctamente implementada
