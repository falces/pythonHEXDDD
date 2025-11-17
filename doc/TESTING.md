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

---

**Última actualización**: Noviembre 2025
