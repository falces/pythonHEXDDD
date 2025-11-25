# Arquitectura Hexagonal - HelloWorld Module

## Antes de la Refactorización ❌

```
┌─────────────────────────────────────────────────┐
│  Controllers (Infrastructure)                   │
│  ┌─────────────────────────────┐               │
│  │ HelloWorldController        │               │
│  │ - Instancia repositorio     │               │
│  │ - Instancia servicio        │               │
│  └──────────────┬──────────────┘               │
└─────────────────┼───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│  Application Layer                              │
│  ┌─────────────────────────────┐               │
│  │ HelloWorldService           │               │
│  │ - repository()  ❌          │               │
│  │   (instancia en constructor)│               │
│  └──────────────┬──────────────┘               │
└─────────────────┼───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│  Domain Layer  ❌ VIOLACIÓN                     │
│  ┌─────────────────────────────┐               │
│  │ HelloWorld (Entity)         │               │
│  │ - self.model = HelloWorld-  │               │
│  │   Model() ❌ SQLAlchemy!    │               │
│  │                             │               │
│  │ HelloWorldModel ❌          │               │
│  │ - db.Model (SQLAlchemy)     │               │
│  │ - Columns, Table            │               │
│  └─────────────────────────────┘               │
└─────────────────────────────────────────────────┘
```

**Problemas:**
- ❌ Dominio depende de SQLAlchemy (db.Model)
- ❌ Entidad conoce modelo de persistencia
- ❌ No hay separación entre Domain e Infrastructure
- ❌ Imposible testear el dominio sin base de datos
- ❌ Servicios instancian repositorios (no DI)

---

## Después de la Refactorización ✅

```
┌──────────────────────────────────────────────────────────────────┐
│                    HTTP Layer (Entry Point)                      │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ HelloWorldController                                   │     │
│  │  GET  /api/v1/hello-world/                             │     │
│  │  POST /api/v1/hello-world/                             │     │
│  │  GET  /api/v1/hello-world/{id}                         │     │
│  └───────────────────────┬────────────────────────────────┘     │
└────────────────────────────┼─────────────────────────────────────┘
                             │
          ┌──────────────────▼──────────────────┐
          │   CQRS Pattern                      │
          │   1. Command/Query = Data()         │
          │   2. Bus = container.bus()          │
          │   3. result = bus.dispatch(msg)     │
          └──────────────────┬──────────────────┘
                             │
┌────────────────────────────▼─────────────────────────────────────┐
│                      Application Layer                           │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ Command/Query Handlers                                 │     │
│  │  handle(command/query)                                 │     │
│  │                                                         │     │
│  │  Orquesta:                                             │     │
│  │  - Crea Value Objects (Greeting)                       │     │
│  │  - Crea Entidades (HelloWorld)                         │     │
│  │  - Llama Repository (Interface)                        │     │
│  │  - Publica Eventos de Dominio                          │     │
│  └───────────────┬────────────────┬───────────────────────┘     │
└──────────────────┼────────────────┼─────────────────────────────┘
                   │                │
        ┌──────────▼────────┐       │
        │ GreetingDTO       │       │
        └───────────────────┘       │
                                    │
┌───────────────────────────────────▼──────────────────────────────┐
│                        Domain Layer (Core)                       │
│                    ✅ INDEPENDIENTE DE TODO                      │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ HelloWorld (Aggregate Root)                             │   │
│  │  - greeting: Greeting                                   │   │
│  │  ✅ Sin conocimiento de persistencia                    │   │
│  │  ✅ Sin imports de Flask/SQLAlchemy                     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            │                                    │
│  ┌─────────────────────────▼───────────────────────────────┐   │
│  │ Greeting (Value Object)                                 │   │
│  │  - value: str                                           │   │
│  │  - Validaciones de dominio                              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            │                                    │
│  ┌─────────────────────────▼───────────────────────────────┐   │
│  │ HelloWorldRepositoryInterface (Port/Interface)          │   │
│  │  + save(entity: HelloWorld) → HelloWorld                │   │
│  │  + findById(id: int) → Optional[HelloWorld]             │   │
│  │  + findAll() → List[HelloWorld]                         │   │
│  │  + delete(id: int) → bool                               │   │
│  │  ✅ Define el contrato (no implementación)              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
                             ▲
                             │ implements
┌────────────────────────────┼─────────────────────────────────────┐
│              Infrastructure Layer (Adapters)                     │
│                            │                                     │
│  ┌─────────────────────────▼───────────────────────────────┐   │
│  │ HelloWorldRepository                                    │   │
│  │  implements HelloWorldRepositoryInterface               │   │
│  │                                                          │   │
│  │  save():                                                │   │
│  │    1. entity → Mapper.toModel() → model                 │   │
│  │    2. db.session.add(model)                             │   │
│  │    3. model → Mapper.toDomain() → entity                │   │
│  │                                                          │   │
│  │  findAll():                                             │   │
│  │    1. query(HelloWorldModel).all()                      │   │
│  │    2. [Mapper.toDomain(m) for m in models]              │   │
│  └──────────────┬───────────────────┬──────────────────────┘   │
│                 │                   │                           │
│  ┌──────────────▼──────────┐  ┌────▼────────────────────────┐  │
│  │ HelloWorldMapper        │  │ HelloWorldModel             │  │
│  │                         │  │  (SQLAlchemy Model)         │  │
│  │ + toDomain(model)       │  │                             │  │
│  │   → HelloWorld          │  │  __tablename__ = '...'      │  │
│  │                         │  │  id = Column(Integer)       │  │
│  │ + toModel(entity)       │  │  greeting = Column(String)  │  │
│  │   → HelloWorldModel     │  │                             │  │
│  │                         │  │  ✅ Solo en Infrastructure   │  │
│  │ + toDict(entity)        │  │  ✅ Domain no lo conoce     │  │
│  │   → dict                │  │                             │  │
│  └─────────────────────────┘  └─────────────┬───────────────┘  │
│                                              │                  │
└──────────────────────────────────────────────┼──────────────────┘
                                               │
                                    ┌──────────▼──────────┐
                                    │   Database (MySQL)  │
                                    │   hello_world table │
                                    └─────────────────────┘
```

---

## Flujo de Datos Completo

### **1. Crear un HelloWorld (POST) - CQRS**

```
HTTP POST /api/v1/hello-world/
{ "greeting": "Hola Mundo" }
         │
         ▼
┌────────────────────────────────────┐
│ HelloWorldController               │
│  1. data = request.get_json()      │
│  2. cmd = CreateHelloWorldCommand( │
│       greeting_text=data['greeting']│
│     )                              │
│  3. bus = container.command_bus()  │
│  4. id = bus.dispatch(cmd)         │
└────────┬───────────────────────────┘
         │
         ▼
┌────────────────────────────────────┐
│ CommandBus                         │
│  1. handler = handlers[type(cmd)]  │
│  2. return handler.handle(cmd)     │
└────────┬───────────────────────────┘
         │
         ▼
┌────────────────────────────────────┐
│ CreateHelloWorldHandler            │
│  1. greeting = Greeting.create()   │ ← Value Object (Domain)
│  2. entity = HelloWorld(greeting)  │ ← Entity (Domain)
│  3. saved = repo.save(entity)      │ → Llama a Infrastructure
│  4. events.publish(saved.events)   │
│  5. return saved.id                │
└────────┬───────────────────────────┘
         │
         ▼
┌────────────────────────────────────┐
│ HelloWorldWriteRepository          │
│  1. model = Mapper.toModel(entity) │ ← Domain → Persistence
│  2. db.session.merge(model)        │
│  3. db.session.commit()            │
│  4. return Mapper.toDomain(model)  │ ← Persistence → Domain
└────────┬───────────────────────────┘
         │
         ▼
┌────────────────────────────────────┐
│ HelloWorldMapper                   │
│                                    │
│ toModel(entity):                   │
│   HelloWorldModel(                 │
│     greeting=entity.greeting.value │
│   )                                │
│                                    │
│ toDomain(model):                   │
│   greeting = Greeting(model.greeting)
│   entity = HelloWorld(greeting)    │
│   entity._id = model.id            │
│   return entity                    │
└────────┬───────────────────────────┘
         │
         ▼
    ┌────────────┐
    │  Database  │
    │  INSERT    │
    └────────────┘
```

---

## Principios SOLID Aplicados

### ✅ **Single Responsibility Principle (SRP)**
- `HelloWorld`: Solo lógica de dominio
- `HelloWorldModel`: Solo mapeo con BD
- `HelloWorldMapper`: Solo traducción entre capas
- `HelloWorldRepository`: Solo persistencia

### ✅ **Open/Closed Principle (OCP)**
- Puedes cambiar la implementación del repositorio sin tocar el dominio
- Ejemplo: `HelloWorldMongoRepository` implementando la misma interface

### ✅ **Liskov Substitution Principle (LSP)**
- Cualquier implementación de `HelloWorldRepositoryInterface` es intercambiable

### ✅ **Interface Segregation Principle (ISP)**
- Interface específica para HelloWorld (no genérica sobrecargada)

### ✅ **Dependency Inversion Principle (DIP)**
- Domain define la interface (`HelloWorldRepositoryInterface`)
- Infrastructure implementa la interface (`HelloWorldRepository`)
- Application depende de la abstracción (interface), no de la implementación

---

## Testing

### **Test Unitario del Dominio** (sin BD)
```python
def test_hello_world_creation():
    greeting = Greeting.create("Hello")
    entity = HelloWorld(greeting=greeting)
    assert entity.greeting.getValue() == "Hello"
```

### **Test del Servicio con Mock**
```python
def test_service_get_all():
    mock_repo = Mock(spec=HelloWorldRepositoryInterface)
    mock_repo.findAll.return_value = [
        HelloWorld(Greeting.create("Hello"))
    ]
    
    service = HelloWorldService(mock_repo)
    result = service.getAllHelloWorld()
    
    assert len(result) == 1
    assert result[0]["greeting"] == "Hello"
```

### **Test de Integración del Repositorio**
```python
def test_repository_save_and_find(db_session):
    repo = HelloWorldRepository()
    entity = HelloWorld(Greeting.create("Test"))
    
    saved = repo.save(entity)
    found = repo.findById(saved._id)
    
    assert found.greeting.getValue() == "Test"
```

---

## Comparación

| Aspecto | Antes ❌ | Después ✅ |
|---------|---------|-----------|
| **Dominio** | Depende de SQLAlchemy | Independiente total |
| **Testabilidad** | Requiere BD | Tests unitarios puros |
| **Acoplamiento** | Alto (Entity ↔ Model) | Bajo (separado por Mapper) |
| **DI** | `repository()` instancia | Recibe instancia inyectada |
| **Cambiar BD** | Toca el dominio | Solo cambia Infrastructure |
| **Principio DIP** | Violado | Cumplido |
| **Arquitectura** | Capas acopladas | Hexagonal correcta |

---

## Conclusión

✅ **Domain es puro**: No conoce Flask, SQLAlchemy ni detalles técnicos  
✅ **Infrastructure adaptable**: Puedes cambiar de BD sin tocar Domain  
✅ **Application orquesta**: Coordina Domain e Infrastructure  
✅ **Dependency Inversion**: Domain define contratos, Infrastructure los cumple  
✅ **Testeable**: Domain e Application se testean sin BD  
✅ **Arquitectura Hexagonal**: Correctamente implementada
