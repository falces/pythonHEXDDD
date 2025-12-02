# Guía de Testing

Esta guía explica cómo ejecutar y trabajar con los tests del proyecto pythonHEXDDD.

## Tabla de Contenidos

- [Requisitos Previos](#requisitos-previos)
- [Estructura de Tests](#estructura-de-tests)
- [Ejecutar Tests](#ejecutar-tests)
- [Cobertura de Código](#cobertura-de-código)
- [Marcadores de Tests](#marcadores-de-tests)
- [Fixtures Disponibles](#fixtures-disponibles)
- [Mejores Prácticas](#mejores-prácticas)

## Requisitos Previos

### Instalar Dependencias de Testing

```bash
pip install -r requirements.txt
```

Las dependencias de testing incluyen:
- `pytest==8.3.4` - Framework de testing
- `pytest-cov==6.0.0` - Plugin de cobertura
- `pytest-flask==1.3.0` - Plugin para testing de Flask
- `pytest-mock==3.14.0` - Plugin para mocking
- `faker==33.1.0` - Generación de datos de prueba

### Crear Directorio de Logs

Antes de ejecutar tests de integración:

```bash
mkdir -p /home/falces/Code/tools/pythonHEXDDD/app/log
```

## Estructura de Tests

```
tests/
├── conftest.py                 # Fixtures globales
├── unit/                       # Tests unitarios (aislados con mocks)
│   ├── Admin/                  # 🆕 Tests del módulo Admin
│   │   ├── Application/
│   │   │   ├── test_commands.py
│   │   │   ├── test_command_handlers.py
│   │   │   ├── test_queries.py
│   │   │   ├── test_query_handlers.py
│   │   │   └── test_read_models.py
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   │   └── test_user.py
│   │   │   └── value_objects/
│   │   │       └── test_user_value_objects.py
│   │   └── events/
│   │       └── test_user_events.py
│   ├── Application/            # Tests de HelloWorld
│   │   ├── test_commands.py           # Tests de Commands (CQRS)
│   │   ├── test_command_handlers.py   # Tests de Command Handlers
│   │   ├── test_queries.py            # Tests de Queries (CQRS)
│   │   ├── test_query_handlers.py     # Tests de Query Handlers
│   │   └── test_read_models.py        # Tests de Read Models
│   ├── Shared/
│   │   ├── test_command_bus.py        # Tests de Command Bus
│   │   ├── test_query_bus.py          # Tests de Query Bus
│   │   └── test_event_dispatcher.py   # Tests de Event Dispatcher
│   ├── domain/
│   │   ├── entities/          # Tests de entidades del dominio
│   │   └── value_objects/     # Tests de value objects
│   ├── events/                # Tests de eventos de dominio
│   ├── handlers/              # Tests de event handlers
│   └── use_cases/             # Tests de casos de uso
└── integration/               # Tests de integración (con BD)
    ├── test_hello_world_api.py
    └── test_hello_world_repository.py
```

## Ejecutar Tests

### Resumen de comandos

Para ejecutar todos los tests, puedes usar:

```bash
python -m pytest tests/ -v
```

**Variantes útiles:**

```bash
# Todos los tests con resumen corto
python -m pytest tests/

# Tests solo del módulo Admin
python -m pytest tests/unit/Admin/ -v

# Solo mostrar el resumen (más rápido de leer)
python -m pytest tests/ -q

# Con coverage
python -m pytest tests/ --cov=app --cov-report=html

# Solo tests de integración
python -m pytest tests/integration/ -v

# Solo tests unitarios
python -m pytest tests/unit/ -v

# Detener en el primer fallo
python -m pytest tests/ -x

# Solo los tests que fallaron en la última ejecución
python -m pytest tests/ --lf
```

Comando más completo:

```bash
python -m pytest tests/ -v --tb=short
```

- `-v` = verbose (muestra cada test)
- `--tb=short` = tracebacks cortos (más legibles)

### Todos los Tests

```bash
cd /home/falces/Code/tools/pythonHEXDDD
PYTHONPATH=/home/falces/Code/tools/pythonHEXDDD/app:$PYTHONPATH pytest
```

### Tests con Modo Verbose

```bash
# Verbose básico
pytest -v

# Muy verbose (muestra más detalles)
pytest -vv

# Con traceback completo en caso de error
pytest --tb=long
```

### Tests por Tipo

```bash
# Solo tests unitarios
pytest -m unit

# Solo tests de integración
pytest -m integration

# Solo tests lentos
pytest -m slow
```

### Tests por Capa

```bash
# Tests del dominio
pytest -m domain

# Tests de la capa de aplicación
pytest -m application

# Tests de infraestructura
pytest -m infrastructure
```

### Tests Específicos

```bash
# Un archivo específico
pytest tests/unit/domain/entities/test_hello_world.py

# Una clase de tests específica
pytest tests/unit/domain/entities/test_hello_world.py::TestHelloWorld

# Un test individual
pytest tests/unit/domain/entities/test_hello_world.py::TestHelloWorld::test_create_hello_world_with_greeting

# Todos los tests que contienen "greeting" en el nombre
pytest -k greeting

# Tests de CQRS (Commands, Queries, Handlers, Buses)
pytest tests/unit/Application/ tests/unit/Shared/

# Solo tests de Commands
pytest tests/unit/Application/test_commands.py

# Solo tests de Query Bus
pytest tests/unit/Shared/test_query_bus.py
```

### Tests con Salida en Tiempo Real

```bash
# Mostrar prints durante la ejecución
pytest -s

# Combinado con verbose
pytest -v -s
```

## Cobertura de Código

### Generar Reporte de Cobertura

```bash
# Reporte en terminal + HTML
pytest --cov=app --cov-report=html --cov-report=term

# Solo reporte en terminal
pytest --cov=app --cov-report=term

# Reporte detallado con líneas faltantes
pytest --cov=app --cov-report=term-missing
```

### Ver Reporte HTML

Después de generar el reporte HTML:

```bash
# En Linux
xdg-open htmlcov/index.html

# En macOS
open htmlcov/index.html

# En WSL
explorer.exe htmlcov/index.html
```

### Cobertura de Archivos Específicos

```bash
# Cobertura solo de un módulo
pytest --cov=app/Domain --cov-report=term

# Múltiples módulos
pytest --cov=app/Domain --cov=app/Application --cov-report=term
```

### Configuración de Cobertura

La configuración está en `.coveragerc`:
- **Objetivo**: 95% de cobertura mínima
- **Excluidos**: tests/, migrations/, venv/, __pycache__/

## Marcadores de Tests

Los marcadores permiten categorizar y ejecutar grupos específicos de tests.

### Marcadores Disponibles

| Marcador | Descripción | Uso |
|----------|-------------|-----|
| `unit` | Tests unitarios aislados | `pytest -m unit` |
| `integration` | Tests de integración | `pytest -m integration` |
| `slow` | Tests que tardan más tiempo | `pytest -m slow` |
| `domain` | Tests de la capa de dominio | `pytest -m domain` |
| `application` | Tests de la capa de aplicación | `pytest -m application` |
| `infrastructure` | Tests de infraestructura | `pytest -m infrastructure` |

### Combinar Marcadores

```bash
# Tests unitarios del dominio
pytest -m "unit and domain"

# Tests de integración o lentos
pytest -m "integration or slow"

# Tests unitarios pero no lentos
pytest -m "unit and not slow"
```

## Fixtures Disponibles

### Fixtures Globales (conftest.py)

| Fixture | Descripción | Alcance |
|---------|-------------|---------|
| `app` | Instancia de Flask configurada para tests | function |
| `client` | Cliente de prueba de Flask | function |
| `app_context` | Contexto de aplicación activo | function |
| `db_session` | Sesión de base de datos (auto-rollback) | function |
| `mock_repository` | Mock del repositorio | function |
| `mock_event_dispatcher` | Mock del dispatcher de eventos | function |
| `sample_greeting` | Objeto Greeting de ejemplo | function |
| `sample_hello_world` | Entidad HelloWorld de ejemplo | function |

### Usar Fixtures en Tests

```python
def test_example(client, sample_hello_world):
    """Test usando fixtures."""
    response = client.get('/hello-world')
    assert response.status_code == 200
```

## Tests CQRS

El proyecto implementa el patrón CQRS (Command Query Responsibility Segregation) con una suite completa de tests.

### Cobertura de Tests CQRS

| Componente | Archivo de Test | Tests | Estado |
|------------|-----------------|-------|--------|
| **Commands** | `test_commands.py` | 10 | ✅ 100% |
| CreateHelloWorldCommand | | 3 | ✅ |
| UpdateHelloWorldCommand | | 4 | ✅ |
| DeleteHelloWorldCommand | | 3 | ✅ |
| **Command Handlers** | `test_command_handlers.py` | 9 | ✅ |
| CreateHelloWorldHandler | | 2 | ✅ |
| UpdateHelloWorldHandler | | 3 | ✅ |
| DeleteHelloWorldHandler | | 3 | ✅ |
| **Queries** | `test_queries.py` | 11 | ✅ |
| GetAllHelloWorldQuery | | 5 | ✅ |
| GetHelloWorldByIdQuery | | 3 | ✅ |
| SearchHelloWorldQuery | | 5 | ✅ |
| **Query Handlers** | `test_query_handlers.py` | 9 | ✅ |
| GetAllHelloWorldHandler | | 3 | ✅ |
| GetHelloWorldByIdHandler | | 2 | ✅ |
| SearchHelloWorldHandler | | 3 | ✅ |
| **Command Bus** | `test_command_bus.py` | 5 | ✅ |
| **Query Bus** | `test_query_bus.py` | 6 | ✅ |
| **Event Dispatcher** | `test_event_dispatcher.py` | 11 | ✅ |
| **Read Models** | `test_read_models.py` | 12 | ✅ |

### Ejecutar Tests CQRS

```bash
# Todos los tests CQRS
pytest tests/unit/Application/ tests/unit/Shared/ -v

# Solo Commands y Command Handlers
pytest tests/unit/Application/test_commands.py tests/unit/Application/test_command_handlers.py -v

# Solo Queries y Query Handlers
pytest tests/unit/Application/test_queries.py tests/unit/Application/test_query_handlers.py -v

# Solo Buses (Command Bus y Query Bus)
pytest tests/unit/Shared/test_command_bus.py tests/unit/Shared/test_query_bus.py -v

# Event Dispatcher (soporte para múltiples eventos)
pytest tests/unit/Shared/test_event_dispatcher.py -v

# Read Models (serialización y paginación)
pytest tests/unit/Application/test_read_models.py -v
```

### Características Testeadas en CQRS

#### Commands
- ✅ Inmutabilidad (frozen dataclasses)
- ✅ Validaciones de tipos
- ✅ Validaciones de valores (IDs positivos, strings no vacíos)
- ✅ Protección contra modificación

#### Command Handlers
- ✅ Creación de entidades de dominio
- ✅ Actualización con validación de existencia
- ✅ Eliminación con validación
- ✅ Publicación de eventos de dominio
- ✅ Interacción con repositorio (write)

#### Queries
- ✅ Inmutabilidad (frozen dataclasses)
- ✅ Valores por defecto (limit, offset, sort)
- ✅ Validaciones de paginación
- ✅ Criterios de búsqueda opcionales

#### Query Handlers
- ✅ Consultas optimizadas sin lógica de dominio
- ✅ Uso de Read Repository
- ✅ Retorno de Read Models
- ✅ Paginación y ordenamiento
- ✅ Búsqueda con criterios

#### Command Bus & Query Bus
- ✅ Registro de handlers por tipo
- ✅ Despacho de comandos/queries
- ✅ Manejo de errores (handlers no registrados)
- ✅ Reemplazo de handlers existentes
- ✅ Propagación de excepciones

#### Event Dispatcher
- ✅ Suscripción a evento único
- ✅ **Suscripción a múltiples eventos** (nuevo)
- ✅ Publicación a múltiples suscriptores
- ✅ Manejo de excepciones en suscriptores
- ✅ Prevención de duplicados
- ✅ Publicación múltiple de eventos

#### Read Models
- ✅ Serialización to_dict()
- ✅ Deserialización from_dict()
- ✅ Cálculo de metadatos de paginación
- ✅ Propiedades has_next / has_previous
- ✅ Total de páginas calculado

### Ejemplo: Test de Command

```python
def test_create_command_with_valid_data():
    """Debe crear comando con datos válidos"""
    command = CreateHelloWorldCommand(greeting_text="Hello World")
    
    assert command.greeting_text == "Hello World"

def test_create_command_is_immutable():
    """Debe ser inmutable (frozen dataclass)"""
    command = CreateHelloWorldCommand(greeting_text="Hello World")
    
    with pytest.raises(AttributeError):
        command.greeting_text = "New greeting"
```

### Ejemplo: Test de Command Handler

```python
def test_handle_creates_hello_world_and_saves():
    """Debe crear entidad y guardarla en el repositorio"""
    # Arrange
    mock_repository = Mock()
    mock_event_dispatcher = Mock()
    handler = CreateHelloWorldHandler(mock_repository, mock_event_dispatcher)
    command = CreateHelloWorldCommand(greeting_text="Test")
    
    # Act
    result_id = handler.handle(command)
    
    # Assert
    mock_repository.save.assert_called_once()
    assert isinstance(result_id, int)
```

### Ejemplo: Test de Query Bus

```python
def test_register_and_dispatch_query():
    """Debe registrar handler y despachar query correctamente"""
    # Arrange
    bus = QueryBus()
    mock_handler = Mock()
    read_model = HelloWorldReadModel(id=1, greeting="Test")
    mock_handler.handle = Mock(return_value=read_model)
    query = GetHelloWorldByIdQuery(id=1)
    
    # Act
    bus.register(GetHelloWorldByIdQuery, mock_handler)
    result = bus.dispatch(query)
    
    # Assert
    assert result == read_model
    mock_handler.handle.assert_called_once_with(query)
```

### Ejemplo: Test de Event Dispatcher (Múltiples Eventos)

```python
def test_subscribe_multiple_events():
    """Debe suscribir correctamente a múltiples eventos"""
    # Arrange
    dispatcher = EventDispatcher()
    
    # Mock de suscriptor que escucha múltiples eventos
    class MultiEventSubscriber:
        def subscribed_to(self):
            return [HelloWorldCreated, HelloWorldDeleted]
        
        def handle(self, event):
            pass
    
    subscriber = MultiEventSubscriber()
    
    # Act
    dispatcher.subscribe(subscriber)
    
    # Assert
    assert dispatcher.has_subscribers(HelloWorldCreated)
    assert dispatcher.has_subscribers(HelloWorldDeleted)
```

## Mejores Prácticas

### 1. Patrón AAA (Arrange-Act-Assert)

```python
def test_create_hello_world():
    # Arrange - Preparar datos
    greeting = "Test Greeting"
    
    # Act - Ejecutar acción
    result = create_hello_world(greeting)
    
    # Assert - Verificar resultado
    assert result.greeting == greeting
```

### 2. Nombres Descriptivos

```python
# ✅ Bueno
def test_create_hello_world_with_empty_string_raises_exception():
    pass

# ❌ Malo
def test_create():
    pass
```

### 3. Aislar Tests Unitarios

```python
# ✅ Bueno - Usa mocks para aislar
def test_use_case(mock_repository, mock_event_dispatcher):
    use_case = CreateHelloWorldUseCase(mock_repository, mock_event_dispatcher)
    # ...

# ✅ Bueno - Test de Command Handler con mocks
def test_command_handler():
    mock_repository = Mock()
    mock_event_dispatcher = Mock()
    handler = CreateHelloWorldHandler(mock_repository, mock_event_dispatcher)
    # ...

# ❌ Malo - Usa dependencias reales en test unitario
def test_use_case():
    repository = HelloWorldRepository()  # ❌ BD real
    # ...
```

### 4. Tests de Integración con Base de Datos

```python
@pytest.mark.integration
def test_repository_integration(app, db_session):
    """Test de integración con BD."""
    with app.app_context():
        repository = HelloWorldRepository()
        # ... test con BD real
```

### 5. Un Assert por Test (cuando sea posible)

```python
# ✅ Bueno
def test_greeting_has_correct_value():
    greeting = Greeting.create("Hello")
    assert greeting.value == "Hello"

def test_greeting_trims_whitespace():
    greeting = Greeting.create("  Hello  ")
    assert greeting.value == "Hello"

# ⚠️ Aceptable pero menos específico
def test_greeting():
    greeting = Greeting.create("Hello")
    assert greeting.value == "Hello"
    assert len(greeting.value) == 5
```

### 6. Testear Inmutabilidad en CQRS

```python
# ✅ Bueno - Validar que Commands y Queries son inmutables
def test_command_is_immutable():
    command = CreateHelloWorldCommand(greeting_text="Test")
    
    with pytest.raises(AttributeError):
        command.greeting_text = "Modified"  # Debe fallar

def test_query_is_immutable():
    query = GetAllHelloWorldQuery(limit=10)
    
    with pytest.raises(AttributeError):
        query.limit = 20  # Debe fallar
```

### 7. Testear Interacciones con Mocks

```python
# ✅ Bueno - Verificar que se llaman los métodos correctos
def test_handler_saves_to_repository():
    mock_repository = Mock()
    handler = CreateHelloWorldHandler(mock_repository, Mock())
    command = CreateHelloWorldCommand(greeting_text="Test")
    
    handler.handle(command)
    
    # Verificar que save fue llamado una vez
    mock_repository.save.assert_called_once()
    
    # Verificar que el argumento es correcto
    saved_entity = mock_repository.save.call_args[0][0]
    assert isinstance(saved_entity, HelloWorld)
```

### 8. Testear Buses (Command/Query Bus)

```python
# ✅ Bueno - Testear registro y despacho
def test_bus_dispatches_to_correct_handler():
    bus = CommandBus()
    mock_handler = Mock()
    mock_handler.handle = Mock(return_value=123)
    
    command = CreateHelloWorldCommand(greeting_text="Test")
    bus.register(CreateHelloWorldCommand, mock_handler)
    
    result = bus.dispatch(command)
    
    assert result == 123
    mock_handler.handle.assert_called_once_with(command)
```

## Comandos Útiles

### Ejecutar Tests y Generar Reporte Completo

```bash
pytest -v --cov=app --cov-report=html --cov-report=term-missing
```

### Ejecutar Solo Tests Rápidos

```bash
pytest -m "not slow"
```

### Ejecutar Tests con Rerun en Caso de Fallo

```bash
pip install pytest-rerunfailures
pytest --reruns 3
```

### Ver Tests sin Ejecutarlos

```bash
pytest --collect-only
```

### Ejecutar Tests en Paralelo

```bash
pip install pytest-xdist
pytest -n auto  # Usa todos los cores disponibles
```

### Detener en Primer Fallo

```bash
pytest -x
```

### Detener después de N fallos

```bash
pytest --maxfail=3
```

## Solución de Problemas

### Error: "No such file or directory: log/app.log"

```bash
mkdir -p /home/falces/Code/tools/pythonHEXDDD/app/log
```

### Error: "ModuleNotFoundError"

Asegúrate de configurar PYTHONPATH:

```bash
export PYTHONPATH=/home/falces/Code/tools/pythonHEXDDD/app:$PYTHONPATH
pytest
```

### Tests de Integración Fallan

Verifica que la base de datos de prueba esté configurada correctamente en `conftest.py`:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
```

### Ver Output de Prints

```bash
pytest -s  # Muestra prints durante los tests
```

## Integración Continua

Para CI/CD, usa este comando:

```bash
PYTHONPATH=/home/falces/Code/tools/pythonHEXDDD/app:$PYTHONPATH \
pytest -v \
  --cov=app \
  --cov-report=xml \
  --cov-report=term \
  --cov-fail-under=95 \
  --junitxml=junit.xml
```

## Recursos Adicionales

- [Pytest Documentation](https://docs.pytest.org/)
- [pytest-flask Documentation](https://pytest-flask.readthedocs.io/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
- [Testing Best Practices](https://docs.pytest.org/en/stable/goodpractices.html)

## Estadísticas de Cobertura

### Cobertura Global (con tests CQRS)
- **Total**: 71%+ de cobertura
- **Commands**: 100% de cobertura
- **Query Bus**: 95% de cobertura
- **Event Dispatcher**: 67% de cobertura (mejorado con soporte multi-evento)

### Componentes con 100% de Cobertura
- ✅ CreateHelloWorldCommand
- ✅ UpdateHelloWorldCommand
- ✅ DeleteHelloWorldCommand
- ✅ GetHelloWorldByIdQuery

### Tests por Módulo

| Módulo | Tests Creados | Cobertura |
|--------|---------------|-----------|
| Commands | 10 | 100% |
| Command Handlers | 9 | Parcial |
| Queries | 11 | 80%+ |
| Query Handlers | 9 | Parcial |
| Command Bus | 5 | 35% |
| Query Bus | 6 | 95% |
| Event Dispatcher | 11 | 67% |
| Read Models | 12 | 82-86% |

## Notas Importantes

### Event Dispatcher - Soporte Multi-Evento

El `EventDispatcher` ahora soporta suscriptores que escuchan múltiples eventos:

```python
# Suscriptor a un solo evento
class SingleEventSubscriber:
    def subscribed_to(self):
        return HelloWorldCreated  # Una sola clase

# Suscriptor a múltiples eventos
class MultiEventSubscriber:
    def subscribed_to(self):
        return [HelloWorldCreated, HelloWorldDeleted]  # Lista de clases
```

Este fix permite que las **Projections** (usadas en CQRS para eventual consistency) puedan escuchar múltiples eventos de dominio.

### Convenciones de Naming

- **Commands**: `*Command` (ej: `CreateHelloWorldCommand`)
- **Queries**: `*Query` (ej: `GetAllHelloWorldQuery`)
- **Handlers**: `*Handler` (ej: `CreateHelloWorldHandler`)
- **Read Models**: `*ReadModel` (ej: `HelloWorldReadModel`)
- **Events**: `*Created`, `*Updated`, `*Deleted` (ej: `HelloWorldCreated`)

---

**Última actualización**: Noviembre 2025 (Añadidos tests CQRS completos)
