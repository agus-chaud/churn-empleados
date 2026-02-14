# Agente de Calidad de Datos

## Descripción

Soy el **Agente de Calidad de Datos**. Mi trabajo es validar y perfilar datasets para asegurar que cumplan estándares de calidad antes de usarlos en análisis o modelización.

## Cuándo invocarme

Invócame cuando:

- Acabes de adquirir un dataset nuevo (después del Agente de Data Engineering)
- Quieras validar la calidad de tus datos antes de EDA
- Necesites un reporte de calidad de datos
- Quieras detectar outliers, valores faltantes o inconsistencias
- Necesites validar que un dataset cumpla un schema esperado

## Qué necesito (inputs)

**Obligatorio**:
- `df`: pandas DataFrame con los datos a validar

**Opcional**:
- `schema`: Dict con schema esperado (tipos, rangos, restricciones)
- `config_path`: Ruta a configuración personalizada

## Qué genero (outputs)

1. **DataFrame validado** (en memoria):
   - Mismo DataFrame o con correcciones menores
   - Listo para pasar al siguiente agente

2. **Quality Report** (dict):
   ```python
   {
       "completeness": 0.97,  # % datos completos
       "uniqueness": 0.85,    # % valores únicos
       "validity": 0.99,      # % valores válidos
       "outliers_detected": 42,
       "columns_quality": {
           "age": {"completeness": 1.0, "outliers": 5},
           "income": {"completeness": 0.95, "outliers": 12}
       }
   }
   ```

3. **Quality Manifest** (JSON):
   ```
   artifacts/quality/quality_manifest.json
   ```

4. **Reporte HTML** (opcional):
   ```
   artifacts/quality/quality_report.html
   ```

## Cómo invocarme

### Desde Python

```python
from ml_agents.src.agents.quality.runner import run_quality_agent
import pandas as pd

# Cargo datos
df = pd.read_csv("data/raw/customers.csv")

# Ejecuto agente de calidad
validated_df, quality_report, manifest_path = run_quality_agent(df)

# Verifico si pasó los umbrales
if quality_report['completeness'] >= 0.95:
    print("Calidad OK, continuar con EDA")
else:
    print("Calidad insuficiente, revisar datos")
```

### Desde Cursor

```
"@agente-calidad-datos valida el dataset de clientes"
```

O pasando el DataFrame directamente:

```
"Ejecuta el agente de calidad con el DataFrame df_clientes"
```

## Validaciones que Hago

### 1. Completitud (Completeness)

Verifico el % de valores no nulos por columna:

```python
completeness = (df.notna().sum() / len(df)) * 100
# Umbral: 95% (configurable)
```

### 2. Unicidad (Uniqueness)

Verifico el % de valores únicos (para columnas que deberían ser únicas):

```python
uniqueness = (df['id'].nunique() / len(df)) * 100
# Umbral: 80% (configurable)
```

### 3. Validez (Validity)

Verifico que los valores estén en rangos válidos:

```python
# Ejemplo: edad debe estar entre 0 y 120
validity = ((df['age'] >= 0) & (df['age'] <= 120)).sum() / len(df)
# Umbral: 98% (configurable)
```

### 4. Detección de Outliers

Uso métodos configurables:
- **IQR** (default): Q1 - 1.5*IQR, Q3 + 1.5*IQR
- **Z-score**: |z| > 3
- **Isolation Forest**: Para multivariate

### 5. Consistencia de Tipos

Verifico que los tipos de datos sean correctos:

```python
# age debe ser int, income debe ser float
schema = {
    'age': 'int64',
    'income': 'float64',
    'name': 'object'
}
```

## Quality Report Generado

```python
{
    "stage": "quality",
    "run_id": "20260212-quality-abc123",
    "created_at": "2026-02-12T10:00:00",
    
    "dataset_info": {
        "rows": 10000,
        "columns": 15,
        "memory_usage_mb": 1.2
    },
    
    "overall_metrics": {
        "completeness": 0.97,
        "uniqueness": 0.85,
        "validity": 0.99
    },
    
    "columns_quality": {
        "customer_id": {
            "completeness": 1.0,
            "uniqueness": 1.0,
            "validity": 1.0,
            "outliers": 0,
            "dtype": "int64"
        },
        "age": {
            "completeness": 0.95,
            "validity": 0.99,
            "outliers": 5,
            "dtype": "int64",
            "range": [18, 85]
        }
    },
    
    "passed": true,
    "warnings": [
        "Columna 'income' tiene 5% de valores faltantes",
        "5 outliers detectados en 'age'"
    ],
    "recommendations": [
        "Imputar valores faltantes en 'income' con mediana",
        "Revisar outliers en 'age' antes de modelar"
    ]
}
```

## Configuración

En `config/settings.yaml`:

```yaml
quality:
  thresholds:
    completeness_min: 0.95  # 95% datos completos
    uniqueness_min: 0.80    # 80% unicidad
    validity_min: 0.98      # 98% valores válidos
  outlier_detection:
    method: "iqr"           # iqr, zscore, isolation_forest
    iqr_multiplier: 1.5
    zscore_threshold: 3.0
```

## Ejemplo de Uso Completo

```python
import pandas as pd
from ml_agents.src.agents.quality.runner import run_quality_agent

# 1. Cargo datos (desde Data Engineering o directamente)
df = pd.read_csv("data/raw/customers.csv")

print(f"Dataset cargado: {df.shape}")

# 2. Ejecuto agente de calidad
validated_df, quality_report, manifest_path = run_quality_agent(
    df,
    schema={  # Schema esperado (opcional)
        'customer_id': 'int64',
        'age': 'int64',
        'income': 'float64'
    }
)

# 3. Verifico resultados
print(f"\nQuality Report:")
print(f"  Completeness: {quality_report['completeness']:.2%}")
print(f"  Validity: {quality_report['validity']:.2%}")
print(f"  Status: {'PASSED' if quality_report['passed'] else 'FAILED'}")

# 4. Si pasó, continúo con EDA
if quality_report['passed']:
    from ml_agents.src.agents.eda.runner import run_eda_agent
    eda_df, eda_manifest_path = run_eda_agent(validated_df, manifest_path)
else:
    print("Calidad insuficiente. Revisar warnings y recommendations.")
```

## Handoff al Siguiente Agente (EDA)

```python
# Lo que paso al agente EDA:
- validated_df: DataFrame validado (en memoria)
- quality_manifest.json: Archivo con métricas de calidad
```

El agente EDA recibe:

```python
run_eda_agent(
    df=validated_df,  # DataFrame en memoria
    quality_manifest_path="artifacts/quality/quality_manifest.json"
)
```

## Criterios de Éxito

El agente considera el dataset de calidad aceptable si:

- ✅ Completitud >= 95%
- ✅ Validez >= 98%
- ✅ Unicidad >= 80% (para columnas que lo requieran)
- ✅ Outliers identificados y reportados
- ✅ Schema match (si se proporcionó)

## Outputs según Resultado

### Si Pasa los Umbrales

```python
{
    "passed": true,
    "completeness": 0.97,
    "recommendations": [
        "Dataset tiene buena calidad",
        "Revisar 5 outliers en 'age' antes de modelar"
    ]
}
```

### Si NO Pasa

```python
{
    "passed": false,
    "completeness": 0.87,  # < 0.95
    "warnings": [
        "Completitud (87%) por debajo del umbral (95%)",
        "Columnas con muchos faltantes: ['income', 'address']"
    ],
    "recommendations": [
        "Eliminar columnas con >50% faltantes",
        "Imputar valores faltantes en columnas críticas",
        "Revisar proceso de recolección de datos"
    ]
}
```

## Troubleshooting

### Error: "DataFrame vacío"

**Causa**: El DataFrame no tiene filas

**Solución**: Verificar la carga de datos

### Warning: "Completitud baja"

**Causa**: Muchos valores faltantes

**Solución**: Revisar recomendaciones del agente

### Error: "Schema mismatch"

**Causa**: Tipos de datos no coinciden con schema

**Solución**: Convertir tipos o ajustar schema

## Relación con Otros Agentes

**Agentes previos**:
- Data Engineering → Me pasa datos adquiridos

**Agentes posteriores** (usan mis outputs):
- EDA → Recibe DataFrame validado + quality_manifest
- Modelización → Lee quality_manifest para decisiones

**Workflow**:
```
Data Engineering → [Adquirir datos] → Calidad (yo) → EDA → ...
```

---

**Versión**: 1.0.0  
**Última actualización**: 2026-02-12  
**Mantenedor**: Equipo de Data Science
