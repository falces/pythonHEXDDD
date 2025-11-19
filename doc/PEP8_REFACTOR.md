# Refactorización PEP 8 - Nomenclatura Snake Case

## 📋 Resumen

Este documento describe la refactorización completa de nomenclatura para cumplir con PEP 8 (Python Enhancement Proposal 8), el estándar de estilo oficial de Python.

**Fecha de refactorización:** 19 de noviembre de 2025  
**Estado:** ✅ Completado  
**Tests:** ✅ 8/8 pasando (67.35% cobertura)

---

## 🎯 Objetivo

Transformar todo el código del proyecto para seguir la convención **snake_case** en variables, métodos y funciones, según lo establecido en PEP 8.

### Estándar PEP 8 Aplicado

| Elemento | Convención | Ejemplo |
|----------|-----------|---------|
| **Variables** | `snake_case` | `hello_world_controller` |
| **Funciones/Métodos** | `snake_case` | `get_all_hello_world()` |
| **Clases** | `PascalCase` | `HelloWorldController` |
| **Constantes** | `UPPER_SNAKE_CASE` | `MAX_CONNECTIONS` |

---

## 📝 Cambios Realizados

### 1. Variables Blueprint (Flask) - snake_case

**Antes:**
```python
helloWorldController = Blueprint('helloWorldController', __name__)
moviesController = Blueprint('moviesController', __name__)
helloWorldSignalListener = Blueprint('helloWorldSignalListener', __name__)
toolsController = Blueprint('toolsController', __name__)
v1ControllerBase = Blueprint('v1', __name__)
```

**Después:**
```python
hello_world_controller = Blueprint('helloWorldController', __name__)
movies_controller = Blueprint('moviesController', __name__)
hello_world_signal_listener = Blueprint('helloWorldSignalListener', __name__)
tools_controller = Blueprint('toolsController', __name__)
v1_controller_base = Blueprint('v1', __name__)
```

**Archivos afectados:**
- `Infrastructure/Controller/HelloWorldController.py`
- `Infrastructure/Controller/MoviesController.py`
- `Infrastructure/Controller/SignalListener/HelloWorldSignalListener.py`
- `Shared/Infrastructure/Controller/ToolsController.py`
- `Shared/Infrastructure/Controller/Controller.py`
- `config/controllers.py`

---

### 2. Métodos de Controladores - snake_case

**Antes:**
```python
@helloWorldController.route('/', methods=['GET'])
def getAllHelloWorld():
    ...

@helloWorldController.route('/', methods=['POST'])
def createHelloWorld():
    ...

@helloWorldController.route('/<int:id>', methods=['GET'])
def getHelloWorldById(id: int):
    ...

@helloWorldController.route('/<int:id>', methods=['DELETE'])
def deleteHelloWorld(id: int):
    ...
```

**Después:**
```python
@hello_world_controller.route('/', methods=['GET'])
def get_all_hello_world():
    ...

@hello_world_controller.route('/', methods=['POST'])
def create_hello_world():
    ...

@hello_world_controller.route('/<int:id>', methods=['GET'])
def get_hello_world_by_id(id: int):
    ...

@hello_world_controller.route('/<int:id>', methods=['DELETE'])
def delete_hello_world(id: int):
    ...
```

**Archivos afectados:**
- `Infrastructure/Controller/HelloWorldController.py`
- `Infrastructure/Controller/MoviesController.py`

---

### 3. Métodos de Entidades de Dominio - snake_case

#### 3.1 Entidad Show

**Antes:**
```python
class Show(AggregateRootBase):
    def getId(self) -> str:
        return self.show_id.value
    
    def getTitle(self) -> str:
        return self.title.value
    
    def getType(self) -> str:
        return self.show_type.value
    
    def getStreamingOption(self) -> Optional[StreamingOption]:
        return self.streaming_option
    
    def isMovie(self) -> bool:
        return self.show_type.isMovie()
    
    def isSeries(self) -> bool:
        return self.show_type.isSeries()
    
    def hasStreamingOption(self) -> bool:
        return self.streaming_option is not None
```

**Después:**
```python
class Show(AggregateRootBase):
    def get_id(self) -> str:
        return self.show_id.value
    
    def get_title(self) -> str:
        return self.title.value
    
    def get_type(self) -> str:
        return self.show_type.value
    
    def get_streaming_option(self) -> Optional[StreamingOption]:
        return self.streaming_option
    
    def is_movie(self) -> bool:
        return self.show_type.is_movie()
    
    def is_series(self) -> bool:
        return self.show_type.is_series()
    
    def has_streaming_option(self) -> bool:
        return self.streaming_option is not None
```

**Archivos afectados:**
- `Domain/Show/Show.py`
- `Domain/Show/ValueObjects/ShowType.py`
- `Domain/Show/ValueObjects/StreamingOption.py`
- `Infrastructure/ExternalAPI/Mappers/ShowMapper.py` (referencias actualizadas)

---

### 4. Métodos de Repositorios - snake_case

**Antes:**
```python
class AbstractRepository(ABC):
    @abstractmethod
    def findById(self):
        pass

    @abstractmethod
    def findAll(self):
        pass
    
    @abstractmethod
    def findByCriteria(self):
        pass
```

**Después:**
```python
class AbstractRepository(ABC):
    @abstractmethod
    def find_by_id(self):
        pass

    @abstractmethod
    def find_all(self):
        pass
    
    @abstractmethod
    def find_by_criteria(self):
        pass
```

**Implementaciones actualizadas:**
- `Shared/Domain/Repositories/AbstractRepository.py`
- `Domain/Show/ShowRepositoryInterface.py`
- `Infrastructure/Repository/ShowsAPIRepository.py`
- `Infrastructure/Repository/HelloWorldReadRepository.py`
- `Application/UseCases/Shows/GetShowByIdUseCase.py`
- `Application/UseCases/Shows/SearchShowsUseCase.py`
- `Application/HelloWorldService.py`
- `Application/CommandHandlers/UpdateHelloWorldHandler.py`
- `Application/CommandHandlers/DeleteHelloWorldHandler.py`

---

### 5. Métodos de Clases Base - snake_case

#### 5.1 ControllerBase

**Antes:**
```python
class ControllerBase():
    @staticmethod
    def formatResponse(data: list, code: int) -> list:
        return {"status": "ok", "data": data}, code
```

**Después:**
```python
class ControllerBase():
    @staticmethod
    def format_response(data: list, code: int) -> list:
        return {"status": "ok", "data": data}, code
```

**Referencias actualizadas en:**
- Todos los controladores (HelloWorldController, MoviesController)

#### 5.2 ModelBase y EntityBase

**Antes:**
```python
class ModelBase():
    def getModel(self) -> Self:
        return self.model

class EntityBase():
    def getModel(self):
        return self.model
```

**Después:**
```python
class ModelBase():
    def get_model(self) -> Self:
        return self.model

class EntityBase():
    def get_model(self):
        return self.model
```

---

### 6. CreateExcelService - snake_case

**Antes:**
```python
class CreateExcelService:
    @staticmethod
    def createExcelFromAPIResponse(data: dict, fileName: str) -> None:
        df = pd.DataFrame(data)
        df.to_excel('.' + '/output/' + fileName, index=False)
```

**Después:**
```python
class CreateExcelService:
    @staticmethod
    def create_excel_from_api_response(data: dict, file_name: str) -> None:
        df = pd.DataFrame(data)
        df.to_excel('.' + '/output/' + file_name, index=False)
```

---

### 7. Corrección de Nombre de Clase

**Antes:**
```python
class IdValueobject(IntValueObject):  # ❌ 'o' minúscula
    ...
```

**Después:**
```python
class IdValueObject(IntValueObject):  # ✅ PascalCase correcto
    ...
```

**Archivo:** `Shared/Domain/ValueObjects/IdValueObject.py`

---

### 8. Listeners de Señales - snake_case

**Antes:**
```python
class HelloWorldSignalListener():
    @signals['new_hello_world'].connect
    def newCountryListener(self, sender: str, message: dict):
        ...
```

**Después:**
```python
class HelloWorldSignalListener():
    @signals['new_hello_world'].connect
    def new_country_listener(self, sender: str, message: dict):
        ...
```

---

## 🧪 Tests Actualizados

Los tests unitarios fueron actualizados para reflejar los cambios de nomenclatura:

**Antes:**
```python
mock_read_repository.findById = Mock(return_value=None)
```

**Después:**
```python
mock_read_repository.find_by_id = Mock(return_value=None)
```

**Archivo:** `tests/unit/Application/test_command_handlers.py`

**Resultado:**
```
✅ 8/8 tests PASSED
Coverage: 67.35%
```

---

## 📊 Estadísticas de Cambios

| Categoría | Archivos Modificados | Métodos/Variables Renombrados |
|-----------|---------------------|------------------------------|
| **Controllers** | 6 | 15+ métodos |
| **Domain Entities** | 4 | 10+ métodos |
| **Repositories** | 6 | 9+ métodos |
| **Base Classes** | 3 | 4 métodos |
| **Tests** | 1 | 6 mocks |
| **Documentación** | 5 | Actualizada completa |
| **TOTAL** | **25** | **50+** |

---

## ✅ Verificación de Cumplimiento

### Convenciones Aplicadas

- ✅ **Variables globales**: snake_case
- ✅ **Métodos de instancia**: snake_case
- ✅ **Métodos estáticos**: snake_case
- ✅ **Parámetros de función**: snake_case
- ✅ **Nombres de clases**: PascalCase (corregido `IdValueobject`)
- ✅ **Constantes**: No aplica (no hay constantes UPPER_CASE en este refactor)

### Archivos sin Cambios Requeridos

Los siguientes tipos de archivos ya cumplían con PEP 8:
- ✅ Comandos y Queries (ya usaban snake_case en parámetros)
- ✅ Eventos de Dominio (propiedades ya en snake_case)
- ✅ Value Objects (métodos `create()` son factory methods válidos)
- ✅ Configuración (config/*.py ya conforme)

---

## 🔍 Herramientas de Validación

Para verificar el cumplimiento de PEP 8 en el futuro, se pueden usar:

```bash
# Instalar flake8
pip install flake8

# Verificar PEP 8
flake8 app/ --max-line-length=120

# Instalar black (formateador automático)
pip install black

# Formatear automáticamente
black app/
```

---

## 📚 Documentación Actualizada

Los siguientes documentos fueron actualizados para reflejar la nueva nomenclatura:

1. ✅ **README.md** - Flujos y ejemplos de código
2. ✅ **doc/USE_CASES_IMPLEMENTATION.md** - Implementación de casos de uso
3. ✅ **doc/REFACTOR_PERSISTENCE_SEPARATION.md** - Separación de persistencia
4. ✅ **doc/REFACTOR_SHOWS_MOVIES.md** - Refactorización de Shows
5. ✅ **doc/PEP8_REFACTOR.md** (este documento)

---

## 🎓 Beneficios

1. **Conformidad con el estándar oficial de Python** (PEP 8)
2. **Mejora de legibilidad** - Convenciones consistentes en todo el proyecto
3. **Facilita colaboración** - Código más familiar para desarrolladores Python
4. **Integración con herramientas** - Linters y formateadores funcionan mejor
5. **Profesionalismo** - Código que sigue las mejores prácticas de la industria

---

## 🚀 Próximos Pasos (Opcional)

- [ ] Configurar pre-commit hooks con flake8 y black
- [ ] Agregar pylint para análisis estático adicional
- [ ] Documentar convenciones de código en CONTRIBUTING.md
- [ ] Configurar CI/CD para verificar PEP 8 automáticamente

---

**Refactorización completada con éxito ✨**
