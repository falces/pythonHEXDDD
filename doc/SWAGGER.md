# Documentación OpenAPI/Swagger

## Acceso a la Documentación

La documentación interactiva de la API está disponible en:

```
http://localhost:5000/api/docs
```

## Características

### Swagger UI
- **Interfaz interactiva** para explorar y probar la API
- **Pruebas en tiempo real** de todos los endpoints
- **Esquemas de datos** detallados
- **Ejemplos de peticiones** y respuestas
- **Validación automática** de parámetros

### Especificación OpenAPI 3.0.3

El archivo de especificación está ubicado en:
```
app/APIDocs/apidoc.yaml
```

## Endpoints Documentados

### HelloWorld API

#### `GET /api/v1/hello-world/`
Obtiene todos los HelloWorld registrados.

**Respuesta exitosa:**
```json
[
  {
    "id": 1,
    "greeting": "Hello World"
  },
  {
    "id": 2,
    "greeting": "Hola Mundo"
  }
]
```

#### `POST /api/v1/hello-world/`
Crea un nuevo HelloWorld.

**Request Body:**
```json
{
  "name": "Hello from Spain"
}
```

**Respuesta exitosa (201):**
```json
{
  "id": 3,
  "greeting": "Hello from Spain"
}
```

#### `GET /api/v1/hello-world/{id}`
Obtiene un HelloWorld específico por ID.

**Parámetros:**
- `id` (path) - ID del HelloWorld

**Respuesta exitosa (200):**
```json
{
  "id": 1,
  "greeting": "Hello World"
}
```

**Respuesta error (404):**
```json
{
  "error": "HelloWorld not found"
}
```

#### `DELETE /api/v1/hello-world/{id}`
Elimina un HelloWorld por ID.

**Parámetros:**
- `id` (path) - ID del HelloWorld

**Respuesta exitosa (200):**
```json
{
  "message": "HelloWorld deleted successfully"
}
```

### Shows/Movies API

#### `GET /api/v1/movies/`
Busca shows (películas o series) según criterios.

**Query Parameters:**
- `country` (opcional) - Código de país ISO 3166-1 alpha-2 (ej: "us", "es")
- `showType` (opcional) - Tipo: "movie" o "series"

**Ejemplo:**
```
GET /api/v1/movies/?country=us&showType=movie
```

**Respuesta exitosa:**
```json
[
  {
    "id": "ts123456",
    "title": "The Matrix",
    "showType": "movie",
    "streamingOptions": [
      {
        "service": "Netflix",
        "type": "subscription"
      }
    ]
  }
]
```

#### `GET /api/v1/movies/{show_id}`
Obtiene un show específico por ID.

**Parámetros:**
- `show_id` (path) - ID del show (formato: ts123456)

**Respuesta exitosa:**
```json
{
  "id": "ts123456",
  "title": "The Matrix",
  "showType": "movie",
  "streamingOptions": [
    {
      "service": "Netflix",
      "type": "subscription"
    },
    {
      "service": "Amazon Prime",
      "type": "rent"
    }
  ]
}
```

## Modelos de Datos

### HelloWorld
```yaml
HelloWorld:
  type: object
  properties:
    id:
      type: integer
      description: ID único
      example: 1
    greeting:
      type: string
      minLength: 1
      maxLength: 255
      description: Texto del saludo
      example: "Hello World"
```

### Show
```yaml
Show:
  type: object
  properties:
    id:
      type: string
      pattern: '^ts[0-9]+$'
      description: ID único del show
      example: "ts123456"
    title:
      type: string
      description: Título del show
      example: "The Matrix"
    showType:
      type: string
      enum: [movie, series]
      description: Tipo de contenido
      example: "movie"
    streamingOptions:
      type: array
      items:
        $ref: '#/components/schemas/StreamingOption'
```

### StreamingOption
```yaml
StreamingOption:
  type: object
  properties:
    service:
      type: string
      description: Nombre del servicio
      example: "Netflix"
    type:
      type: string
      description: Tipo de acceso
      example: "subscription"
```

## Códigos de Estado HTTP

| Código | Descripción |
|--------|-------------|
| 200 | OK - Petición exitosa |
| 201 | Created - Recurso creado exitosamente |
| 400 | Bad Request - Petición inválida |
| 404 | Not Found - Recurso no encontrado |
| 500 | Internal Server Error - Error del servidor |

## Configuración

### Instalación de Dependencias

```bash
pip install flask-swagger-ui==4.11.1
```

### Personalización de Swagger UI

Para personalizar la interfaz, edita la configuración en:
```python
app/Shared/Infrastructure/Controller/SwaggerController.py
```

Opciones disponibles:
- `app_name` - Nombre de la aplicación
- `layout` - Diseño de la UI
- `deepLinking` - Enlaces profundos a operaciones
- `displayRequestDuration` - Mostrar duración de requests
- `docExpansion` - Nivel de expansión inicial ('list', 'full', 'none')
- `filter` - Habilitar filtro de búsqueda
- `syntaxHighlight.theme` - Tema de resaltado de sintaxis

### Actualizar Especificación OpenAPI

Edita el archivo:
```bash
app/APIDocs/apidoc.yaml
```

La documentación se actualiza automáticamente al reiniciar la aplicación.

## Validación de Especificación

Para validar el archivo OpenAPI:

```bash
# Usando swagger-cli
npm install -g @apidevtools/swagger-cli
swagger-cli validate app/APIDocs/apidoc.yaml

# O usando una herramienta online
# https://editor.swagger.io/
```

## Generación de Clientes

Puedes generar clientes automáticamente usando la especificación OpenAPI:

```bash
# Instalar openapi-generator
npm install -g @openapitools/openapi-generator-cli

# Generar cliente Python
openapi-generator-cli generate \
  -i app/APIDocs/apidoc.yaml \
  -g python \
  -o ./generated-client

# Generar cliente JavaScript
openapi-generator-cli generate \
  -i app/APIDocs/apidoc.yaml \
  -g javascript \
  -o ./generated-client-js
```

## Testing con Swagger UI

1. Accede a http://localhost:5000/api/docs
2. Expande el endpoint que quieres probar
3. Haz clic en "Try it out"
4. Completa los parámetros requeridos
5. Haz clic en "Execute"
6. Revisa la respuesta

## Integración con Postman

Puedes importar la especificación OpenAPI directamente en Postman:

1. Abre Postman
2. Clic en "Import"
3. Selecciona "Link" o "File"
4. Ingresa: `http://localhost:5000/api/docs/openapi.yaml`
5. Postman generará automáticamente toda la colección

## Recursos Adicionales

- [OpenAPI Specification](https://swagger.io/specification/)
- [Swagger UI Documentation](https://swagger.io/tools/swagger-ui/)
- [Flask-RESTX](https://flask-restx.readthedocs.io/) - Alternativa con decoradores
- [OpenAPI Generator](https://openapi-generator.tech/)

---

**Última actualización**: Noviembre 2025
