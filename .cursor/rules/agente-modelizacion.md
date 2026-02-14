# Agente de Modelización

## Descripción

Soy el **Agente de Modelización**. Mi trabajo es entrenar modelos de Machine Learning, optimizar hiperparámetros, evaluar métricas y registrar experimentos para problemas de clasificación y regresión.

## Cuándo invocarme

Invócame cuando:

- Ya tengas datos limpios y analizados (después de EDA)
- Necesites entrenar un modelo de ML
- Quieras optimizar hiperparámetros automáticamente
- Necesites comparar múltiples modelos
- Quieras registrar experimentos en MLflow
- Necesites un pipeline completo (preprocessing + modelo)

## Qué necesito (inputs)

**Obligatorio**:
- `df`: pandas DataFrame procesado (del Agente de EDA)
- `eda_manifest_path`: Path al manifest de EDA (con target, features, problem_type)

**Opcional**:
- `model_types`: Lista de modelos a probar (default: auto-detecta según problem_type)
  - Classification: `['logistic', 'random_forest', 'xgboost', 'lightgbm']`
  - Regression: `['linear', 'random_forest', 'xgboost', 'lightgbm']`
- `optimization`: `"grid"`, `"random"`, `"optuna"` (default: `"optuna"`)
- `n_trials`: Número de trials para optimización (default: 50)
- `cv_folds`: Folds para cross-validation (default: 5)
- `metric_threshold`: Umbral mínimo de métrica para aceptar modelo

## Qué genero (outputs)

1. **Modelo entrenado + Pipeline** (en memoria y guardado):
   ```
   artifacts/modeling/best_model.pkl
   artifacts/modeling/pipeline.pkl
   ```

2. **Métricas del experimento** (JSON):
   ```json
   {
       "model_type": "random_forest",
       "accuracy": 0.87,
       "f1_score": 0.85,
       "roc_auc": 0.91
   }
   ```

3. **Experiment Manifest** (JSON):
   ```
   artifacts/modeling/experiment_manifest.json
   ```

4. **Registro en MLflow** (opcional):
   - Run ID
   - Parámetros
   - Métricas
   - Artifacts

## Cómo invocarme

### Desde Python

```python
from ml_agents.src.agents.modeling.runner import run_modeling_agent

# Después de EDA
model, pipeline, metrics, manifest_path = run_modeling_agent(
    df=eda_df,
    eda_manifest_path="artifacts/eda/eda_manifest.json",
    model_types=['random_forest', 'xgboost'],
    optimization="optuna",
    n_trials=100
)

print(f"Mejor modelo: {metrics['model_type']}")
print(f"Accuracy: {metrics['accuracy']:.3f}")

# Usar modelo para predicción
predictions = pipeline.predict(X_test)
```

### Desde Cursor

```
"@agente-modelizacion entrena modelos con optimización automática"
```

O más específico:

```
"Entrena Random Forest y XGBoost con 100 trials de Optuna, umbral de accuracy 0.85"
```

## Proceso de Modelización

### 1. Lectura del EDA Manifest

```python
# Leo el manifest para saber:
- target_column: "churn"
- feature_columns: ["age", "tenure", "monthly_charges", ...]
- problem_type: "classification"
- recommended_dtypes: {...}
- recommendations: [...]
```

### 2. Preparación de Datos

```python
# Separo features y target
X = df[eda_manifest['feature_columns']]
y = df[eda_manifest['target_column']]

# Split train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

### 3. Construcción de Pipeline

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer

# Pipeline de preprocessing
preprocessor = ColumnTransformer([
    ('num', StandardScaler(), numeric_features),
    ('cat', OneHotEncoder(), categorical_features)
])

# Pipeline completo
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('model', RandomForestClassifier())
])
```

### 4. Optimización de Hiperparámetros

#### Con Optuna (Recomendado)

```python
import optuna

def objective(trial):
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 100, 500),
        'max_depth': trial.suggest_int('max_depth', 3, 15),
        'min_samples_split': trial.suggest_int('min_samples_split', 2, 10)
    }
    
    model = RandomForestClassifier(**params)
    score = cross_val_score(model, X_train, y_train, cv=5).mean()
    return score

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=50)
```

#### Con Grid Search

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [5, 10, 15]
}

grid_search = GridSearchCV(
    RandomForestClassifier(),
    param_grid,
    cv=5,
    scoring='accuracy'
)
grid_search.fit(X_train, y_train)
```

### 5. Evaluación de Métricas

#### Para Clasificación

```python
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

metrics = {
    'accuracy': accuracy_score(y_test, y_pred),
    'f1_score': f1_score(y_test, y_pred),
    'precision': precision_score(y_test, y_pred),
    'recall': recall_score(y_test, y_pred),
    'roc_auc': roc_auc_score(y_test, y_pred_proba)
}
```

#### Para Regresión

```python
from sklearn.metrics import mean_squared_error, r2_score

metrics = {
    'mse': mean_squared_error(y_test, y_pred),
    'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
    'mae': mean_absolute_error(y_test, y_pred),
    'r2_score': r2_score(y_test, y_pred)
}
```

### 6. Registro en MLflow

```python
import mlflow

with mlflow.start_run():
    mlflow.log_params(best_params)
    mlflow.log_metrics(metrics)
    mlflow.sklearn.log_model(pipeline, "model")
```

## Experiment Manifest Generado

```json
{
  "stage": "modeling",
  "run_id": "20260212-model-abc123",
  "created_at": "2026-02-12T13:00:00",
  
  "problem_type": "classification",
  "target_column": "churn",
  "feature_columns": ["age", "tenure", "monthly_charges", "contract_type"],
  
  "models_tested": [
    {
      "model_type": "random_forest",
      "accuracy": 0.87,
      "f1_score": 0.85,
      "training_time_seconds": 12.5,
      "best_params": {
        "n_estimators": 300,
        "max_depth": 10,
        "min_samples_split": 5
      }
    },
    {
      "model_type": "xgboost",
      "accuracy": 0.89,
      "f1_score": 0.87,
      "training_time_seconds": 8.2,
      "best_params": {
        "n_estimators": 200,
        "max_depth": 6,
        "learning_rate": 0.1
      }
    }
  ],
  
  "best_model": {
    "model_type": "xgboost",
    "path": "artifacts/modeling/best_model.pkl",
    "pipeline_path": "artifacts/modeling/pipeline.pkl",
    "metrics": {
      "accuracy": 0.89,
      "f1_score": 0.87,
      "precision": 0.88,
      "recall": 0.86,
      "roc_auc": 0.93
    }
  },
  
  "optimization": {
    "method": "optuna",
    "n_trials": 100,
    "best_trial": 73
  },
  
  "mlflow": {
    "run_id": "abc123def456",
    "experiment_name": "churn_prediction",
    "tracking_uri": "http://localhost:5000"
  },
  
  "passed_threshold": true,
  "threshold_metric": "accuracy",
  "threshold_value": 0.85
}
```

## Configuración

En `config/settings.yaml`:

```yaml
modeling:
  default_test_size: 0.2
  random_state: 42
  cv_folds: 5
  
  classification:
    default_models: ['logistic', 'random_forest', 'xgboost']
    default_metric: 'f1_score'
    threshold_metric: 0.80
  
  regression:
    default_models: ['linear', 'random_forest', 'xgboost']
    default_metric: 'r2_score'
    threshold_metric: 0.70
  
  optimization:
    method: "optuna"  # grid, random, optuna
    n_trials: 50
    timeout_seconds: 3600
  
  mlflow:
    enabled: true
    tracking_uri: "http://localhost:5000"
    experiment_name: "ml_experiments"
```

## Modelos Disponibles

### Clasificación

- **Logistic Regression**: Baseline rápido
- **Random Forest**: Robusto, feature importance
- **XGBoost**: Alto rendimiento
- **LightGBM**: Rápido en grandes datasets
- **SVM**: Para datasets pequeños con buen tuning

### Regresión

- **Linear Regression**: Baseline interpretable
- **Random Forest Regressor**: Robusto
- **XGBoost Regressor**: Alto rendimiento
- **LightGBM Regressor**: Rápido
- **Ridge/Lasso**: Regularización

## Handoff al Agente de Deployment

Lo que paso al siguiente agente:

```python
# Modelo guardado
artifacts/modeling/best_model.pkl

# Pipeline completo
artifacts/modeling/pipeline.pkl

# Manifest con info
artifacts/modeling/experiment_manifest.json
```

El agente de Deployment recibe:

```python
from ml_agents.src.agents.deployment.runner import run_deployment_agent

deploy_result = run_deployment_agent(
    model_path="artifacts/modeling/best_model.pkl",
    manifest_path="artifacts/modeling/experiment_manifest.json"
)
```

## Ejemplo de Uso Completo

```python
import pandas as pd
from ml_agents.src.agents.modeling.runner import run_modeling_agent

# 1. Cargar datos (después de EDA)
df = pd.read_csv("data/processed/clean_data.csv")

# 2. Entrenar modelos con optimización
model, pipeline, metrics, manifest_path = run_modeling_agent(
    df=df,
    eda_manifest_path="artifacts/eda/eda_manifest.json",
    model_types=['random_forest', 'xgboost', 'lightgbm'],
    optimization="optuna",
    n_trials=100,
    metric_threshold=0.85  # Accuracy mínima requerida
)

# 3. Verificar si cumple umbral
if metrics['accuracy'] >= 0.85:
    print(f"[OK] Modelo aceptado: {metrics['model_type']}")
    print(f"Accuracy: {metrics['accuracy']:.3f}")
    
    # 4. Continuar con Deployment
    from ml_agents.src.agents.deployment.runner import run_deployment_agent
    run_deployment_agent(
        model_path="artifacts/modeling/best_model.pkl",
        manifest_path=manifest_path
    )
else:
    print(f"[FAIL] Modelo no cumple umbral: {metrics['accuracy']:.3f} < 0.85")
    print("Recomendaciones:")
    print("- Revisar feature engineering")
    print("- Aumentar n_trials de optimización")
    print("- Probar más tipos de modelos")
```

## Feature Importance

Genero análisis de importancia de features:

```python
# Para Random Forest, XGBoost, LightGBM
importances = model.feature_importances_
feature_importance_df = pd.DataFrame({
    'feature': feature_names,
    'importance': importances
}).sort_values('importance', ascending=False)

# Guardo en manifest
manifest['feature_importance'] = feature_importance_df.to_dict('records')
```

## Criterios de Éxito

El modelo se considera exitoso si:

- ✅ Métrica principal >= threshold configurado
- ✅ Pipeline completo guardado correctamente
- ✅ Manifest con todos los metadatos generado
- ✅ Registro en MLflow exitoso (si habilitado)
- ✅ Modelo serializable (puede cargarse con joblib)

## Troubleshooting

### Error: "Modelo no converge"

**Causa**: Hiperparámetros inadecuados o datos no normalizados

**Solución**: Normalizar features, aumentar iterations/epochs

### Warning: "Accuracy bajo umbral"

**Causa**: Datos insuficientes o features poco predictivas

**Solución**: Revisar feature engineering en EDA, aumentar n_trials

### Error: "MLflow no disponible"

**Solución**: Iniciar servidor MLflow o deshabilitar en config

```bash
mlflow server --host 0.0.0.0 --port 5000
```

## Relación con Otros Agentes

**Agentes previos** (necesito sus outputs):
- EDA → DataFrame procesado + eda_manifest (target, features, problem_type)

**Agentes posteriores** (usan mis outputs):
- Deployment → Modelo + pipeline + manifest para API
- Documentación → Métricas y feature importance para reportes
- Versionado → Taggear modelo exitoso (ej. `v1.0.0` si accuracy > 0.90)

**Workflow típico**:
```
EDA → Modelización (yo) → [Deployment | Versionado]
```

---

**Versión**: 1.0.0  
**Última actualización**: 2026-02-12  
**Mantenedor**: Equipo de Data Science
