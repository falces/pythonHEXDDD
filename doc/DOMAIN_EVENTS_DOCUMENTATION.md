# Sistema de Eventos de Dominio (Domain Events)

## 📋 Índice

1. [¿Qué son los Eventos de Dominio?](#qué-son-los-eventos-de-dominio)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Componentes Principales](#componentes-principales)
4. [Flujo de Eventos](#flujo-de-eventos)
5. [Implementación](#implementación)
6. [Ejemplos de Uso](#ejemplos-de-uso)
7. [Cómo Agregar Nuevos Eventos](#cómo-agregar-nuevos-eventos)
8. [Testing de Eventos](#testing-de-eventos)
9. [Best Practices](#best-practices)

---

## ¿Qué son los Eventos de Dominio?

Los **Eventos de Dominio** son objetos que representan algo importante que ha ocurrido en el dominio del negocio. Son parte fundamental de Domain-Driven Design (DDD) y permiten:

- ✅ **Desacoplar** comportamientos relacionados
- ✅ **Auditoría** y trazabilidad de cambios
- ✅ **Integración** con otros sistemas
- ✅ **Eventual Consistency** entre agregados
- ✅ **Event Sourcing** (opcional)

### Características Clave

| Característica | Descripción |
|---------------|-------------|
| **Inmutables** | Una vez creados, no se modifican |
| **Pasado** | Nombrados en pasado (Created, Deleted, Updated) |
| **Información completa** | Contienen todos los datos necesarios |
| **Momento exacto** | Registran timestamp de ocurrencia |
| **Identificador único** | UUID para trazabilidad |

---

## Arquitectura del Sistema

### Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────────┐
│                     DOMAIN LAYER                            │
│                                                             │
│  ┌─────────────────┐         ┌──────────────────────────┐  │
│  │ AggregateRoot   │─────────│ DomainEvent              │  │
│  │                 │         │ - event_id               │  │
│  │ - record_event()│         │ - occurred_on            │  │
│  │ - pull_events() │         │ - event_name             │  │
│  └─────────────────┘         │ - to_dict()              │  │
│         │                    └──────────────────────────┘  │
│         │ emite                      ▲                     │
│         ▼                            │ hereda              │
│  ┌──────────────────┐         ┌──────────────────┐        │
│  │ HelloWorld       │         │ HelloWorldCreated│        │
│  │ - mark_created() │         │ HelloWorldDeleted│        │
│  └──────────────────┘         └──────────────────┘        │
└─────────────────────────────────────────────────────────────┘
                               │
                               │ publica eventos
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                  APPLICATION LAYER                          │
│                                                             │
│  ┌──────────────────────┐        ┌──────────────────────┐  │
│  │ Use Case             │───────▶│ EventDispatcher      │  │
│  │                      │        │                      │  │
│  │ 1. Ejecutar lógica   │        │ - subscribe()        │  │
│  │ 2. Obtener eventos   │        │ - publish()          │  │
│  │ 3. Publicar eventos  │        │ - publish_multiple() │  │
│  └──────────────────────┘        └──────────────────────┘  │
│                                            │                │
│                                            │ notifica       │
│                                            ▼                │
│                                   ┌──────────────────┐      │
│                                   │ Event Handlers   │      │
│                                   │                  │      │
│                                   │ - Logger         │      │
│                                   │ - Email Sender   │      │
│                                   │ - Analytics      │      │
│                                   └──────────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

---

## Componentes Principales

### 1. **DomainEvent** (Base Class)

```python
# Shared/Domain/Events/DomainEvent.py

class DomainEvent(ABC):
    """
    Clase base para todos los eventos de dominio.
    """
    def __init__(self):
        self._event_id: str = str(uuid.uuid4())
        self._occurred_on: datetime = datetime.now()
    
    @property
    def event_name(self) -> str:
        return self.__class__.__name__
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'event_id': self.event_id,
            'event_name': self.event_name,
            'occurred_on': self.occurred_on.isoformat(),
        }
```

**Responsabilidades:**
- Proveer estructura común para todos los eventos
- Generar ID único y timestamp automáticamente
- Permitir serialización

---

### 2. **DomainEventSubscriber** (Interface)

```python
# Shared/Domain/Events/DomainEventSubscriber.py

class DomainEventSubscriber(ABC):
    """
    Interfaz para los handlers de eventos.
    """
    @abstractmethod
    def subscribed_to(self) -> Type[DomainEvent]:
        """Retorna el tipo de evento al que está suscrito."""
        pass
    
    @abstractmethod
    def handle(self, event: DomainEvent) -> None:
        """Maneja el evento de dominio."""
        pass
```

**Responsabilidades:**
- Definir contrato para handlers
- Declarar a qué evento está suscrito
- Implementar lógica de manejo

---

### 3. **EventDispatcher**

```python
# Shared/Infrastructure/Events/EventDispatcher.py

class EventDispatcher:
    """
    Despachador de eventos - Patrón Observer/Pub-Sub.
    """
    def subscribe(self, subscriber: DomainEventSubscriber) -> None:
        """Registra un handler para un tipo de evento."""
        
    def publish(self, event: DomainEvent) -> None:
        """Publica un evento a todos los handlers suscritos."""
        
    def publish_multiple(self, events: List[DomainEvent]) -> None:
        """Publica múltiples eventos en orden."""
```

**Responsabilidades:**
- Gestionar suscripciones (registro de handlers)
- Despachar eventos a handlers correspondientes
- Manejar errores sin interrumpir flujo

---

### 4. **AggregateRootBase**

```python
# Shared/Domain/Entities/EntityBase.py

class AggregateRootBase(EntityBase):
    """
    Base para Aggregate Roots con soporte de eventos.
    """
    def __init__(self):
        self._domain_events: List[DomainEvent] = []
    
    def record_event(self, event: DomainEvent) -> None:
        """Registra un evento en el agregado."""
        self._domain_events.append(event)
    
    def pull_domain_events(self) -> List[DomainEvent]:
        """Extrae y limpia eventos acumulados."""
        events = self._domain_events.copy()
        self._domain_events.clear()
        return events
```

**Responsabilidades:**
- Acumular eventos durante operaciones de dominio
- Proveer método para extraer eventos
- Mantener agregado limpio después de publicación

---

## Flujo de Eventos

### Flujo Completo (Crear HelloWorld)

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. HTTP REQUEST                                                 │
│    POST /helloworld { "name": "World" }                         │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. CONTROLLER                                                   │
│    use_case = container.create_hello_world_use_case()           │
│    result = use_case.execute("World")                           │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. USE CASE - CreateHelloWorldUseCase                           │
│                                                                 │
│    a) Crear entidad:                                            │
│       hello_world = HelloWorld.create(greeting)                 │
│                                                                 │
│    b) Persistir:                                                │
│       saved = repository.save(hello_world)                      │
│                                                                 │
│    c) Marcar como creado (registra evento):                     │
│       saved.mark_as_created(saved._id)                          │
│       # Internamente: self.record_event(HelloWorldCreated(...)) │
│                                                                 │
│    d) Extraer eventos:                                          │
│       events = saved.pull_domain_events()                       │
│       # events = [HelloWorldCreated(id=1, greeting="World")]    │
│                                                                 │
│    e) Publicar eventos:                                         │
│       event_dispatcher.publish_multiple(events)                 │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. EVENT DISPATCHER                                             │
│                                                                 │
│    Para cada evento en la lista:                                │
│      - Buscar handlers suscritos a HelloWorldCreated            │
│      - Llamar handler.handle(event) para cada uno               │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. EVENT HANDLERS (en paralelo)                                 │
│                                                                 │
│    ┌──────────────────────────────────────┐                    │
│    │ HelloWorldCreatedLogger              │                    │
│    │ logger.info("HelloWorld creado...")  │                    │
│    └──────────────────────────────────────┘                    │
│                                                                 │
│    ┌──────────────────────────────────────┐                    │
│    │ (Futuro) SendEmailOnHelloWorldCreated│                    │
│    │ email_service.send(...)              │                    │
│    └──────────────────────────────────────┘                    │
└─────────────────────────────────────────────────────────────────┘
```

### Código Real del Flujo

```python
# 3. USE CASE
class CreateHelloWorldUseCase:
    def execute(self, greeting_text: str) -> dict:
        # a) Crear entidad
        greeting = Greeting.create(greeting_text)
        hello_world = HelloWorld.create(greeting=greeting)
        
        # b) Persistir
        saved_entity = self.repository.save(hello_world)
        
        # c) Marcar como creado (registra evento internamente)
        saved_entity.mark_as_created(saved_entity._id)
        
        # d) Extraer eventos del agregado
        events = saved_entity.pull_domain_events()
        
        # e) Publicar eventos
        self.event_dispatcher.publish_multiple(events)
        
        return HelloWorldMapper.toDict(saved_entity)
```

```python
# HelloWorld entity
class HelloWorld(AggregateRootBase):
    def mark_as_created(self, id: int) -> None:
        self._id = id
        # Registrar evento en el agregado
        event = HelloWorldCreated(
            hello_world_id=id,
            greeting=self.greeting.value
        )
        self.record_event(event)  # Se acumula en self._domain_events
```

---

## Implementación

### Estructura de Archivos

```
app/
├── Shared/
│   ├── Domain/
│   │   ├── Events/
│   │   │   ├── __init__.py
│   │   │   ├── DomainEvent.py              # Clase base
│   │   │   └── DomainEventSubscriber.py    # Interface handler
│   │   └── Entities/
│   │       └── EntityBase.py               # AggregateRootBase
│   └── Infrastructure/
│       └── Events/
│           ├── __init__.py
│           └── EventDispatcher.py          # Dispatcher
│
├── Domain/
│   └── HelloWorld/
│       ├── Events/
│       │   ├── __init__.py
│       │   ├── HelloWorldCreated.py        # Evento específico
│       │   └── HelloWorldDeleted.py        # Evento específico
│       └── HelloWorld.py                   # Aggregate Root
│
├── Application/
│   ├── EventHandlers/
│   │   ├── __init__.py
│   │   ├── HelloWorldCreatedLogger.py      # Handler
│   │   └── HelloWorldDeletedLogger.py      # Handler
│   └── UseCases/
│       └── HelloWorld/
│           ├── CreateHelloWorldUseCase.py  # Publica eventos
│           └── DeleteHelloWorldUseCase.py  # Publica eventos
│
└── config/
    └── container.py                        # Registra handlers
```

---

## Ejemplos de Uso

### Ejemplo 1: Evento HelloWorldCreated

```python
# Domain/HelloWorld/Events/HelloWorldCreated.py

class HelloWorldCreated(DomainEvent):
    """
    Evento: Se ha creado un nuevo HelloWorld.
    """
    def __init__(self, hello_world_id: int, greeting: str):
        super().__init__()
        self._hello_world_id = hello_world_id
        self._greeting = greeting
    
    @property
    def hello_world_id(self) -> int:
        return self._hello_world_id
    
    @property
    def greeting(self) -> str:
        return self._greeting
    
    def to_dict(self) -> Dict[str, Any]:
        base_dict = super().to_dict()
        base_dict.update({
            'hello_world_id': self.hello_world_id,
            'greeting': self.greeting,
        })
        return base_dict
```

### Ejemplo 2: Handler Logger

```python
# Application/EventHandlers/HelloWorldCreatedLogger.py

class HelloWorldCreatedLogger(DomainEventSubscriber):
    """
    Handler que registra en el log la creación.
    """
    def subscribed_to(self):
        return HelloWorldCreated
    
    def handle(self, event: HelloWorldCreated) -> None:
        logger.info(
            f"[DOMAIN EVENT] HelloWorld creado - "
            f"ID: {event.hello_world_id}, "
            f"Greeting: '{event.greeting}', "
            f"Timestamp: {event.occurred_on}"
        )
```

### Ejemplo 3: Handler Email (Futuro)

```python
# Application/EventHandlers/SendEmailOnHelloWorldCreated.py

class SendEmailOnHelloWorldCreated(DomainEventSubscriber):
    """
    Handler que envía email cuando se crea un HelloWorld.
    """
    def __init__(self, email_service: EmailService):
        self.email_service = email_service
    
    def subscribed_to(self):
        return HelloWorldCreated
    
    def handle(self, event: HelloWorldCreated) -> None:
        self.email_service.send(
            to="admin@example.com",
            subject="Nuevo HelloWorld Creado",
            body=f"Se creó HelloWorld con ID {event.hello_world_id}"
        )
```

---

## Cómo Agregar Nuevos Eventos

### Paso 1: Crear el Evento

```python
# Domain/HelloWorld/Events/HelloWorldUpdated.py

from Shared.Domain.Events.DomainEvent import DomainEvent

class HelloWorldUpdated(DomainEvent):
    """
    Evento: Se actualizó un HelloWorld.
    """
    def __init__(self, hello_world_id: int, old_greeting: str, new_greeting: str):
        super().__init__()
        self._hello_world_id = hello_world_id
        self._old_greeting = old_greeting
        self._new_greeting = new_greeting
    
    @property
    def hello_world_id(self) -> int:
        return self._hello_world_id
    
    @property
    def old_greeting(self) -> str:
        return self._old_greeting
    
    @property
    def new_greeting(self) -> str:
        return self._new_greeting
    
    def to_dict(self) -> Dict[str, Any]:
        base_dict = super().to_dict()
        base_dict.update({
            'hello_world_id': self.hello_world_id,
            'old_greeting': self.old_greeting,
            'new_greeting': self.new_greeting,
        })
        return base_dict
```

### Paso 2: Registrar el Evento en la Entidad

```python
# Domain/HelloWorld/HelloWorld.py

class HelloWorld(AggregateRootBase):
    def update_greeting(self, new_greeting: Greeting) -> None:
        """
        Actualiza el greeting y registra evento.
        """
        old_greeting_value = self.greeting.value
        self.greeting = new_greeting
        
        # Registrar evento
        event = HelloWorldUpdated(
            hello_world_id=self._id,
            old_greeting=old_greeting_value,
            new_greeting=new_greeting.value
        )
        self.record_event(event)
```

### Paso 3: Crear Handler(s)

```python
# Application/EventHandlers/HelloWorldUpdatedLogger.py

class HelloWorldUpdatedLogger(DomainEventSubscriber):
    def subscribed_to(self):
        return HelloWorldUpdated
    
    def handle(self, event: HelloWorldUpdated) -> None:
        logger.info(
            f"[DOMAIN EVENT] HelloWorld actualizado - "
            f"ID: {event.hello_world_id}, "
            f"Antes: '{event.old_greeting}', "
            f"Después: '{event.new_greeting}'"
        )
```

### Paso 4: Publicar en Use Case

```python
# Application/UseCases/HelloWorld/UpdateHelloWorldUseCase.py

class UpdateHelloWorldUseCase:
    def __init__(self, repository, event_dispatcher):
        self.repository = repository
        self.event_dispatcher = event_dispatcher
    
    def execute(self, id: int, new_greeting_text: str) -> dict:
        # Obtener entidad
        entity = self.repository.findById(id)
        
        # Actualizar (registra evento internamente)
        new_greeting = Greeting.create(new_greeting_text)
        entity.update_greeting(new_greeting)
        
        # Persistir
        updated = self.repository.save(entity)
        
        # Publicar eventos
        events = updated.pull_domain_events()
        self.event_dispatcher.publish_multiple(events)
        
        return HelloWorldMapper.toDict(updated)
```

### Paso 5: Registrar Handler en Container

```python
# config/container.py

class Container(containers.DeclarativeContainer):
    # Event Handlers
    hello_world_updated_logger = providers.Factory(
        HelloWorldUpdatedLogger
    )

def _register_event_handlers(container: Container) -> None:
    dispatcher = container.event_dispatcher()
    
    # Registrar nuevo handler
    dispatcher.subscribe(container.hello_world_updated_logger())
```

---

## Testing de Eventos

### Test 1: Verificar que el Evento se Registra

```python
def test_hello_world_records_created_event():
    # Arrange
    greeting = Greeting.create("Test")
    hello_world = HelloWorld.create(greeting=greeting)
    
    # Act
    hello_world.mark_as_created(id=123)
    
    # Assert
    assert hello_world.has_events is True
    events = hello_world.pull_domain_events()
    assert len(events) == 1
    assert isinstance(events[0], HelloWorldCreated)
    assert events[0].hello_world_id == 123
    assert events[0].greeting == "Test"
```

### Test 2: Verificar que el Dispatcher Llama al Handler

```python
from unittest.mock import Mock

def test_event_dispatcher_calls_handler():
    # Arrange
    dispatcher = EventDispatcher()
    mock_handler = Mock(spec=DomainEventSubscriber)
    mock_handler.subscribed_to.return_value = HelloWorldCreated
    
    dispatcher.subscribe(mock_handler)
    
    event = HelloWorldCreated(hello_world_id=1, greeting="Test")
    
    # Act
    dispatcher.publish(event)
    
    # Assert
    mock_handler.handle.assert_called_once_with(event)
```

### Test 3: Verificar Integración Completa

```python
def test_create_hello_world_use_case_publishes_event(caplog):
    # Arrange
    mock_repo = Mock(spec=HelloWorldRepositoryInterface)
    dispatcher = EventDispatcher()
    
    # Registrar handler real
    logger_handler = HelloWorldCreatedLogger()
    dispatcher.subscribe(logger_handler)
    
    use_case = CreateHelloWorldUseCase(
        repository=mock_repo,
        event_dispatcher=dispatcher
    )
    
    # Configurar mock para retornar entidad con ID
    def save_side_effect(entity):
        entity._id = 999
        return entity
    mock_repo.save.side_effect = save_side_effect
    
    # Act
    with caplog.at_level(logging.INFO):
        result = use_case.execute("Test Greeting")
    
    # Assert
    assert "DOMAIN EVENT" in caplog.text
    assert "HelloWorld creado" in caplog.text
    assert "ID: 999" in caplog.text
```

---

## Best Practices

### ✅ DO - Buenas Prácticas

1. **Nombrar eventos en pasado**
   ```python
   # ✅ Correcto
   class OrderPlaced(DomainEvent): pass
   class UserRegistered(DomainEvent): pass
   
   # ❌ Incorrecto
   class PlaceOrder(DomainEvent): pass
   class RegisterUser(DomainEvent): pass
   ```

2. **Eventos inmutables**
   ```python
   # ✅ Correcto - Solo propiedades read-only
   @property
   def hello_world_id(self) -> int:
       return self._hello_world_id
   
   # ❌ Incorrecto - Setters o atributos públicos
   self.hello_world_id = new_id
   ```

3. **Incluir toda la información necesaria**
   ```python
   # ✅ Correcto - Contiene todo lo necesario
   class OrderPlaced(DomainEvent):
       def __init__(self, order_id, customer_id, total, items):
           ...
   
   # ❌ Incorrecto - Handlers tendrían que consultar BD
   class OrderPlaced(DomainEvent):
       def __init__(self, order_id):
           ...
   ```

4. **Handlers independientes entre sí**
   ```python
   # ✅ Correcto - Cada handler es independiente
   class LoggerHandler(DomainEventSubscriber): ...
   class EmailHandler(DomainEventSubscriber): ...
   
   # ❌ Incorrecto - Un handler llama a otro
   class EmailHandler(DomainEventSubscriber):
       def handle(self, event):
           self.logger_handler.handle(event)  # ❌
   ```

5. **No lanzar excepciones en handlers**
   ```python
   # ✅ Correcto - Manejo de errores dentro del handler
   class EmailHandler(DomainEventSubscriber):
       def handle(self, event):
           try:
               self.email_service.send(...)
           except Exception as e:
               logger.error(f"Error enviando email: {e}")
   
   # ❌ Incorrecto - Excepción sin manejar
   class EmailHandler(DomainEventSubscriber):
       def handle(self, event):
           self.email_service.send(...)  # ❌ Puede fallar
   ```

6. **Publicar eventos DESPUÉS de persistir**
   ```python
   # ✅ Correcto
   saved_entity = self.repository.save(hello_world)
   events = saved_entity.pull_domain_events()
   self.event_dispatcher.publish_multiple(events)
   
   # ❌ Incorrecto - Publicar antes de persistir
   events = hello_world.pull_domain_events()
   self.event_dispatcher.publish_multiple(events)
   saved_entity = self.repository.save(hello_world)  # ❌ Puede fallar
   ```

7. **Usar Singleton para EventDispatcher**
   ```python
   # config/container.py
   
   # ✅ Correcto - Singleton
   event_dispatcher = providers.Singleton(EventDispatcher)
   
   # ❌ Incorrecto - Factory (nueva instancia cada vez)
   event_dispatcher = providers.Factory(EventDispatcher)
   ```

### ❌ DON'T - Anti-patrones

1. **No usar eventos para lógica de negocio crítica**
   ```python
   # ❌ INCORRECTO - La validación debe estar ANTES del evento
   class ValidateOrderHandler(DomainEventSubscriber):
       def handle(self, event: OrderPlaced):
           if event.total < 0:
               raise ValueError("Total inválido")
   
   # ✅ CORRECTO - Validar ANTES de crear el agregado
   def execute(self, order_data):
       if order_data['total'] < 0:
           raise ValueError("Total inválido")
       order = Order.create(...)
   ```

2. **No modificar estado en handlers**
   ```python
   # ❌ INCORRECTO - Handler modifica BD directamente
   class UpdateStatsHandler(DomainEventSubscriber):
       def handle(self, event: OrderPlaced):
           stats = self.stats_repository.get()
           stats.total_orders += 1  # ❌ Modifica estado
           self.stats_repository.save(stats)
   
   # ✅ CORRECTO - Usar eventos como notificación, no comando
   # Si necesitas actualizar stats, usa un Use Case separado
   ```

3. **No crear dependencias circulares**
   ```python
   # ❌ INCORRECTO
   # Domain → depends on → Infrastructure
   from Infrastructure.Email.EmailService import EmailService
   
   class OrderPlaced(DomainEvent):
       def send_email(self):  # ❌ Dominio con dependencia de infra
           EmailService().send(...)
   ```

---

## Ventajas del Sistema Implementado

| Ventaja | Descripción | Ejemplo |
|---------|-------------|---------|
| **Desacoplamiento** | Los handlers no conocen la existencia de otros | Logger y Email son independientes |
| **Extensibilidad** | Agregar nuevos handlers sin modificar código existente | Agregar Analytics handler sin tocar Use Cases |
| **Trazabilidad** | Todos los eventos tienen timestamp e ID | Auditoría completa de cambios |
| **Testing** | Fácil mockear dispatcher y verificar eventos | Tests unitarios simples |
| **Async Ready** | Fácil convertir a async/await en el futuro | Cambiar a EventQueue + Workers |
| **Event Sourcing** | Base para implementar ES si es necesario | Guardar eventos en EventStore |

---

## Próximos Pasos Posibles

1. **Event Store** - Persistir eventos en BD para auditoría
2. **Async Handlers** - Ejecutar handlers en background (Celery, RQ)
3. **Event Bus** - Integración con RabbitMQ, Kafka para microservicios
4. **Retry Logic** - Reintentar handlers que fallen
5. **Event Versioning** - Versionado de eventos para compatibilidad
6. **Snapshots** - Optimización para Event Sourcing

---

## Resumen

✅ **Sistema implementado:**
- `DomainEvent` base class
- `DomainEventSubscriber` interface
- `EventDispatcher` (Pub-Sub pattern)
- `AggregateRootBase` con soporte de eventos
- 2 eventos: `HelloWorldCreated`, `HelloWorldDeleted`
- 2 handlers: Loggers para ambos eventos
- Integración completa en Use Cases
- Registro automático en DI Container

**El sistema está listo para producción y es fácilmente extensible!** 🚀
