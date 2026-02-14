# Agente de Deployment

## Descripción

Soy el **Agente de Deployment**. Mi trabajo es convertir un modelo ML entrenado en un servicio REST listo para producción con FastAPI y Docker.

## Cuándo invocarme

Invócame cuando:

- Ya tengas un modelo entrenado (del Agente de Modelización)
- Quieras crear una API REST para servir predicciones
- Necesites deployar el modelo a producción
- Quieras generar un contenedor Docker con el servicio completo

## Qué necesito (inputs)

1. **Manifest del experimento** (obligatorio):
   - Path: `artifacts/modeling/experiment_manifest.json`
   - Contiene: info del modelo, schema de entrada/salida, métricas

2. **Configuración de la API** (opcional):
   - Título de la API (ej: "Customer Churn API")
   - Versión (ej: "1.0.0")
   - Habilitar CORS (sí/no)
   - Habilitar monitoreo (sí/no)

## Qué genero (outputs)

Creo una estructura completa en `artifacts/deployment/`:

```
artifacts/deployment/
├── api/                        # Código de la API FastAPI
│   ├── main.py                # App principal (endpoints)
│   ├── schemas.py             # Modelos Pydantic (validación)
│   ├── model_loader.py        # Cargador del modelo
│   └── health.py              # Health checks
├── Dockerfile                  # Multi-stage, optimizado
├── docker-compose.yml          # Para testing local
├── requirements.txt            # Dependencias Python
├── runbook.md                 # Documentación operativa completa
├── .dockerignore              # Optimización del build
└── deployment_manifest.json   # Metadata del deployment
```

## Características del deployment

### API FastAPI

- **GET /health**: Liveness check (¿está vivo el proceso?)
- **GET /health/ready**: Readiness check (¿listo para tráfico?)
- **POST /predict**: Predicción individual
- **POST /predict/batch**: Predicción por lotes
- **GET /docs**: Documentación interactiva Swagger
- **GET /metrics**: Métricas Prometheus (placeholder)

### Dockerfile

- Multi-stage build (builder + runtime)
- Usuario no-root (seguridad)
- Health check integrado
- Variables de entorno configurables
- Imagen optimizada (~250MB)

### Runbook

Documentación operativa completa con:
- Instrucciones de arranque
- Health checks y cómo interpretarlos
- Métricas clave y umbrales
- Troubleshooting paso a paso
- Procedimientos de rollback
- Contactos y referencias

### Código comentado

Todo el código está comentado en primera persona explicando:
- Qué hace cada función
- Por qué se hace de esa manera
- Qué validaciones se realizan
- Cómo manejar errores

## Cómo invocarme

### Opción 1: Desde Python

```python
from ml_agents.src.agents.deployment.runner import run_deployment_agent

artifacts_path, manifest = run_deployment_agent(
    experiment_manifest_path="artifacts/modeling/experiment_manifest.json",
    api_title="Customer Churn Prediction API",
    api_version="1.0.0"
)
```

### Opción 2: Desde Cursor (conversación)

Simplemente di en el chat:

```
"Ejecuta el agente de deployment para el modelo en 
artifacts/modeling/experiment_manifest.json con el título 
'Customer Churn API' versión 1.0.0"
```

O más simple:

```
"@agente-deployment para el último modelo entrenado"
```

## Después de ejecutarme

Una vez que genero todos los artefactos, puedes:

### 1. Probar localmente

```bash
cd artifacts/deployment
docker-compose up
```

Abre http://localhost:8000/docs para ver la API interactiva.

### 2. Hacer una predicción de prueba

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 35,
    "income": 50000.0,
    "tenure_months": 24,
    "num_products": 2,
    "is_active": true,
    "credit_score": 720.0
  }'
```

### 3. Verificar salud del servicio

```bash
# Liveness
curl http://localhost:8000/health

# Readiness
curl http://localhost:8000/health/ready
```

## Validaciones que hago

Antes de terminar, verifico que:

- ✅ El manifest del experimento existe y es válido
- ✅ Tiene `model_path`, `model_type`, `input_schema`
- ✅ Todos los archivos se generaron correctamente
- ✅ El Dockerfile tiene la estructura correcta
- ✅ El runbook está completo
- ✅ Los schemas Pydantic son válidos

## Configuración

Mi configuración está en `config/settings.yaml`:

```yaml
deployment:
  api:
    host: "0.0.0.0"
    port: 8000
    workers: 4
  docker:
    base_image: "python:3.11-slim"
    registry: ""
  monitoring:
    enable_drift_detection: true
    drift_threshold: 0.1
```

## Seguridad

El deployment que genero incluye:

- ⚠️ Usuario no-root en el contenedor
- ⚠️ Validación estricta de inputs (Pydantic)
- ⚠️ Manejo de errores robusto
- ⚠️ Logging estructurado
- ⚠️ Health checks para orquestadores
- ⚠️ CORS restrictivo (configurable)

**IMPORTANTE**: En producción, debes agregar:
- Autenticación (API keys, OAuth)
- Rate limiting
- HTTPS/TLS
- Secrets management (no variables de entorno)

## Próximos pasos

Después de usar este agente:

1. **Probar localmente**: `docker-compose up`
2. **Revisar el código**: Leer los comentarios en primera persona
3. **Documentar**: Usar el Agente de Documentación para agregar más docs
4. **Versionar**: Usar el Agente de Versionado para hacer commit
5. **Pushear imagen**: Subir a Docker Hub, ECR, GCR, etc.
6. **Deployar**: Kubernetes, ECS, Cloud Run, etc.

## Troubleshooting

### Error: "Manifest no encontrado"

**Solución**: Asegúrate de haber ejecutado el Agente de Modelización primero. El manifest debe estar en `artifacts/modeling/experiment_manifest.json`.

### Error: "Input schema vacío"

**Solución**: El manifest del experimento debe incluir el campo `input_schema` con los tipos de las features.

### Quiero cambiar el puerto

**Solución**: Modifica `config/settings.yaml` o usa la variable de entorno `PORT` al ejecutar el contenedor.

## Ejemplos de uso

### Ejemplo 1: API de predicción de churn

```python
run_deployment_agent(
    experiment_manifest_path="artifacts/modeling/churn_experiment.json",
    api_title="Customer Churn Prediction API",
    api_version="2.1.0"
)
```

### Ejemplo 2: API de recomendaciones

```python
run_deployment_agent(
    experiment_manifest_path="artifacts/modeling/recommender.json",
    api_title="Product Recommender API",
    api_version="1.0.0"
)
```

## Documentación adicional

- **README del agente**: `ml_agents/src/agents/deployment/README.md`
- **Runbook generado**: `artifacts/deployment/runbook.md`
- **Documentación de código**: Los archivos Python tienen comentarios extensos

## Relación con otros agentes

**Agentes previos** (necesito sus outputs):
- Agente de Modelización → Me da el `experiment_manifest.json`

**Agentes posteriores** (pueden usar mis outputs):
- Agente de Documentación → Puede documentar el código de la API
- Agente de Versionado → Puede versionar el deployment

## Criterios de éxito

El deployment se considera exitoso si:

- ✅ Docker build completa sin errores
- ✅ Contenedor arranca en <60 segundos
- ✅ `/health` responde 200 en <100ms
- ✅ `/health/ready` responde 200 después de cargar modelo
- ✅ `/predict` devuelve predicción válida
- ✅ `/predict` devuelve 422 con input inválido
- ✅ Documentación OpenAPI generada
- ✅ Runbook completo y actualizado

---

**Versión**: 1.0.0  
**Última actualización**: 2026-02-12  
**Mantenedor**: Equipo de Data Science
