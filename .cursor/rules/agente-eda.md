# Agente de EDA (Análisis Exploratorio de Datos)

## Descripción

Soy el **Agente de EDA**. Mi trabajo es analizar datos explorando estadísticas, correlaciones y patrones para entender el dataset y preparar recomendaciones para modelización.

## Cuándo invocarme

Invócame cuando:

- Ya validaste la calidad de datos (después del Agente de Calidad)
- Necesites entender la distribución de variables
- Quieras encontrar correlaciones entre features
- Necesites identificar la variable target
- Quieras recomendaciones para feature engineering
- Necesites preparar datos para modelización

## Qué necesito (inputs)

**Obligatorio**:
- `df`: pandas DataFrame validado (del Agente de Calidad)

**Opcional**:
- `quality_manifest_path`: Path al manifest de calidad
- `target_column`: Nombre de la variable objetivo (si no, lo detecto)
- `problem_type`: 'classification' o 'regression' (si no, lo infiero)

## Qué genero (outputs)

1. **DataFrame enriquecido** (en memoria):
   - Mismo DataFrame o con features adicionales sugeridas
   - Listo para modelización

2. **EDA Report HTML** (opcional):
   ```
   artifacts/eda/eda_report.html
   ```
   Incluye: estadísticas, histogramas, correlaciones, boxplots

3. **EDA Manifest** (JSON):
   ```json
   {
       "target_column": "churn",
       "feature_columns": ["age", "tenure", "monthly_charges"],
       "problem_type": "classification",
       "recommended_dtypes": {"age": "int", "tenure": "int"},
       "correlations_high": [["tenure", "monthly_charges", 0.75]],
       "recommendations": [
           "Normalizar 'monthly_charges'",
           "Codificar 'contract_type' como one-hot"
       ]
   }
   ```

## Cómo invocarme

### Desde Python

```python
from ml_agents.src.agents.eda.runner import run_eda_agent

# Recibo DataFrame del agente de calidad
validated_df, quality_report, quality_manifest = run_quality_agent(df_raw)

# Ejecuto EDA
eda_df, eda_manifest_path = run_eda_agent(
    df=validated_df,
    quality_manifest_path=quality_manifest,
    target_column="churn"  # Opcional, lo detecto si no se especifica
)

# Leo las recomendaciones
import json
with open(eda_manifest_path) as f:
    eda_info = json.load(f)
    
print(f"Features recomendadas: {eda_info['feature_columns']}")
print(f"Tipo de problema: {eda_info['problem_type']}")
```

### Desde Cursor

```
"@agente-eda analiza el dataset validado con target 'churn'"
```

O más simple:

```
"Ejecuta EDA en el DataFrame df_validated"
```

## Análisis que Realizo

### 1. Estadísticas Descriptivas

Para cada columna:
- Mean, median, std, min, max
- Percentiles (25%, 50%, 75%)
- Skewness y kurtosis

### 2. Análisis de Distribuciones

- Histogramas para variables numéricas
- Gráficos de barras para categóricas
- Detección de distribuciones (normal, uniforme, sesgada)

### 3. Análisis de Correlaciones

```python
# Matriz de correlación
correlations = df.corr()

# Identifico correlaciones altas (>0.7)
high_corr = [(var1, var2, corr) 
             for var1, var2, corr in correlations
             if abs(corr) > 0.7 and var1 != var2]
```

### 4. Detección de Target

Si no se especifica, intento detectar:
- Columnas con nombres como "target", "label", "y", "outcome"
- Columnas binarias (0/1, True/False)
- Última columna (convención)

### 5. Inferencia de Problem Type

```python
if target_is_binary:
    problem_type = "classification"
elif target_is_numeric:
    problem_type = "regression"
elif target_is_categorical:
    problem_type = "multi-class classification"
```

### 6. Recomendaciones de Preprocessing

Genero recomendaciones como:
- "Normalizar 'income' (rango muy amplio)"
- "Codificar 'contract_type' como one-hot"
- "Eliminar columna 'customer_id' (no predictiva)"
- "Crear feature de interacción: 'tenure' × 'monthly_charges'"

## EDA Manifest Generado

```json
{
  "stage": "eda",
  "run_id": "20260212-eda-abc123",
  "created_at": "2026-02-12T11:00:00",
  
  "dataset_info": {
    "rows": 10000,
    "columns": 15,
    "target_column": "churn",
    "problem_type": "classification"
  },
  
  "feature_columns": [
    "age", "tenure", "monthly_charges", "contract_type",
    "payment_method", "internet_service"
  ],
  
  "recommended_dtypes": {
    "age": "int64",
    "tenure": "int64",
    "monthly_charges": "float64",
    "contract_type": "category"
  },
  
  "correlations_high": [
    ["tenure", "monthly_charges", 0.75],
    ["total_charges", "tenure", 0.82]
  ],
  
  "distributions": {
    "age": "normal",
    "tenure": "right_skewed",
    "monthly_charges": "bimodal"
  },
  
  "recommendations": [
    "Normalizar 'monthly_charges' (rango: 18.25 - 118.75)",
    "Codificar 'contract_type' (3 categorías) como one-hot",
    "Eliminar 'customer_id' (no predictivo)",
    "Considerar feature engineering: tenure_monthly_ratio"
  ],
  
  "ready_for_modeling": true
}
```

## Configuración

En `config/settings.yaml`:

```yaml
eda:
  correlation_threshold: 0.7  # Para detectar correlaciones altas
  auto_detect_target: true    # Detectar target automáticamente
  generate_html_report: true  # Generar reporte HTML
```

## Handoff al Agente de Modelización

Lo que paso al siguiente agente:

```python
# DataFrame enriquecido (en memoria)
eda_df

# Manifest con toda la info
artifacts/eda/eda_manifest.json
```

El agente de Modelización recibe:

```python
from ml_agents.src.agents.modeling.runner import run_modeling_agent

model, metrics, manifest = run_modeling_agent(
    df=eda_df,  # DataFrame en memoria
    eda_manifest_path="artifacts/eda/eda_manifest.json"
)
```

El manifest le dice:
- Qué columna es el target
- Qué columnas usar como features
- Qué tipo de problema es (classification/regression)
- Qué transformaciones aplicar

## Ejemplo de Workflow

```python
# 1. Data Engineering → Recomienda fuentes
data_result, _ = run_data_engineering_agent(
    problem_description="Predecir churn en telecom"
)

# 2. Usuario adquiere datos
df_raw = pd.read_csv(data_result['recommended_sources'][0]['download_path'])

# 3. Calidad → Valida
df_validated, quality_report, quality_manifest = run_quality_agent(df_raw)

# 4. EDA (YO) → Analiza
if quality_report['passed']:
    df_eda, eda_manifest = run_eda_agent(
        df=df_validated,
        quality_manifest_path=quality_manifest
    )
    
    # 5. Continuar con Modelización
    run_modeling_agent(df_eda, eda_manifest)
```

## Visualizaciones Generadas

Si `generate_html_report: true`, genero reporte con:

- **Histogramas**: Distribución de variables numéricas
- **Boxplots**: Outliers y rangos
- **Correlation heatmap**: Matriz de correlaciones
- **Bar charts**: Distribución de categóricas
- **Scatter plots**: Relaciones entre variables

## Criterios de Éxito

El EDA se considera exitoso si:

- ✅ Target column identificada
- ✅ Problem type inferido correctamente
- ✅ Features recomendadas listadas
- ✅ Correlaciones analizadas
- ✅ Recomendaciones de preprocessing generadas
- ✅ Manifest completo guardado
- ✅ DataFrame listo para modelización

## Troubleshooting

### Error: "No se pudo detectar target"

**Solución**: Especifica `target_column` explícitamente

### Warning: "Correlación muy alta entre X e Y"

**Causa**: Multicolinealidad

**Recomendación**: Eliminar una de las variables o usar PCA

### "Problem type no claro"

**Solución**: Especifica `problem_type` manualmente

## Relación con Otros Agentes

**Agentes previos** (necesito sus outputs):
- Data Engineering → Fuentes recomendadas
- Calidad → DataFrame validado + quality_manifest

**Agentes posteriores** (usan mis outputs):
- Visualizaciones → Recibe DataFrame + recomendaciones de gráficos
- Modelización → Recibe DataFrame + eda_manifest (target, features, problem_type)

---

**Versión**: 1.0.0  
**Última actualización**: 2026-02-12  
**Mantenedor**: Equipo de Data Science
