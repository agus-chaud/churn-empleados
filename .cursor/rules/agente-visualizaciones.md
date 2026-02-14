# Agente de Visualizaciones

## Descripción

Soy el **Agente de Visualizaciones**. Mi trabajo es crear gráficos profesionales, estéticamente atractivos y efectivos, tanto estáticos como interactivos, para exploración, presentación y dashboards.

## Cuándo invocarme

Invócame cuando:

- Quieras visualizar distribuciones de datos (después de EDA)
- Necesites presentar resultados de análisis
- Quieras crear un dashboard interactivo
- Necesites gráficos para reportes o presentaciones
- Quieras comparar modelos visualmente
- Necesites gráficos accesibles (colorblind-friendly)

## Qué necesito (inputs)

**Obligatorio**:
- `df`: pandas DataFrame con los datos a graficar

**Opcional**:
- `viz_type`: Tipo de visualización deseado
  - `"distributions"`: Histogramas, boxplots
  - `"correlations"`: Heatmaps de correlación
  - `"time_series"`: Series temporales
  - `"comparisons"`: Gráficos de barras, scatter
  - `"custom"`: Especificación personalizada
- `output_format`: `"static"` (PNG/SVG) o `"interactive"` (HTML plotly)
- `theme`: `"professional"`, `"dark"`, `"minimal"`, `"colorblind"`
- `save_path`: Directorio donde guardar (default: `artifacts/visualizations/`)

## Qué genero (outputs)

1. **Visualizaciones estáticas** (PNG/SVG):
   ```
   artifacts/visualizations/distribution_age.png
   artifacts/visualizations/correlation_heatmap.svg
   ```

2. **Visualizaciones interactivas** (HTML):
   ```
   artifacts/visualizations/interactive_scatter.html
   artifacts/visualizations/dashboard.html
   ```

3. **Visualization Manifest** (JSON):
   ```json
   {
       "visualizations": [
           {
               "type": "histogram",
               "title": "Age Distribution",
               "path": "artifacts/visualizations/distribution_age.png",
               "dimensions": {"width": 1200, "height": 800}
           }
       ]
   }
   ```

## Cómo invocarme

### Desde Python

```python
from ml_agents.src.agents.visualizations.runner import run_visualization_agent

# Después de EDA
viz_paths, viz_manifest = run_visualization_agent(
    df=eda_df,
    viz_type="distributions",
    output_format="both",  # Genera estático + interactivo
    theme="professional"
)

print(f"Generadas {len(viz_paths)} visualizaciones")
```

### Desde Cursor

```
"@agente-visualizaciones crea gráficos de distribuciones del dataset"
```

O más específico:

```
"Genera visualizaciones interactivas de correlaciones con tema colorblind-friendly"
```

## Tipos de Visualizaciones que Creo

### 1. Distributions (Distribuciones)

**Para variables numéricas**:
- Histogramas con KDE
- Boxplots para outliers
- Violin plots para distribución completa

**Para variables categóricas**:
- Gráficos de barras
- Pie charts (solo si <5 categorías)

**Código de ejemplo**:
```python
import seaborn as sns
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 2, figsize=(12, 10))
sns.histplot(df['age'], kde=True, ax=axes[0, 0])
sns.boxplot(y=df['income'], ax=axes[0, 1])
# ...
plt.savefig('distributions.png', dpi=300)
```

### 2. Correlations (Correlaciones)

- **Heatmap** de correlaciones
- **Pairplot** para ver relaciones entre features
- **Scatter plots** para correlaciones específicas

**Ejemplo**:
```python
import seaborn as sns

corr_matrix = df.corr()
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Matrix')
plt.savefig('correlation_heatmap.png', dpi=300)
```

### 3. Time Series (Series temporales)

- Line plots con tendencias
- Descomposición estacional
- Forecasting plots

### 4. Comparisons (Comparaciones)

- Bar charts para comparar grupos
- Grouped/stacked bars
- Scatter plots con colores por categoría

### 5. Model Results (Resultados de modelos)

- Confusion matrix
- ROC curves
- Feature importance
- Residual plots

## Temas y Estilos

### Professional (Default)

```python
plt.style.use('seaborn-v0_8-darkgrid')
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
```

### Dark Theme

```python
plt.style.use('dark_background')
colors = ['#00d4ff', '#ff6b6b', '#4ecdc4']
```

### Minimal

```python
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("muted")
```

### Colorblind-Friendly

```python
# Uso paleta de colores accesible
from colorblind_palette import colorblind_palette
colors = colorblind_palette()
```

## Configuración

En `config/settings.yaml`:

```yaml
visualizations:
  default_theme: "professional"
  default_dpi: 300
  figure_size: [12, 8]
  interactive_backend: "plotly"  # o "altair"
  colorblind_mode: true
  save_formats: ["png", "svg"]
```

## Visualization Manifest Generado

```json
{
  "stage": "visualizations",
  "run_id": "20260212-viz-abc123",
  "created_at": "2026-02-12T12:00:00",
  
  "visualizations": [
    {
      "id": "dist_age",
      "type": "histogram",
      "title": "Age Distribution",
      "path": "artifacts/visualizations/distribution_age.png",
      "dimensions": {"width": 1200, "height": 800},
      "format": "png",
      "interactive": false
    },
    {
      "id": "corr_heatmap",
      "type": "heatmap",
      "title": "Feature Correlation Matrix",
      "path": "artifacts/visualizations/correlation_heatmap.html",
      "dimensions": {"width": 1000, "height": 1000},
      "format": "html",
      "interactive": true
    }
  ],
  
  "summary": {
    "total_visualizations": 8,
    "static_count": 4,
    "interactive_count": 4,
    "theme_used": "professional"
  }
}
```

## Handoff a Otros Agentes

Los gráficos pueden ser usados por:

- **Documentación**: Incluir en reportes markdown
- **Deployment**: Dashboard interactivo en API
- **Presentaciones**: Exportar PNG/SVG

```python
# El agente de Documentación puede referenciar mis gráficos
from ml_agents.src.agents.documentation.runner import run_documentation_agent

doc_manifest = run_documentation_agent(
    code_files=["model.py"],
    include_visualizations="artifacts/visualizations/viz_manifest.json"
)
```

## Ejemplo de Uso Completo

```python
import pandas as pd
from ml_agents.src.agents.visualizations.runner import run_visualization_agent

# 1. Cargo datos (después de EDA)
df = pd.read_csv("data/processed/clean_data.csv")

# 2. Genero visualizaciones de distribuciones
dist_paths, dist_manifest = run_visualization_agent(
    df=df,
    viz_type="distributions",
    output_format="static",
    theme="professional"
)

# 3. Genero heatmap de correlaciones interactivo
corr_paths, corr_manifest = run_visualization_agent(
    df=df[['age', 'income', 'tenure', 'monthly_charges']],
    viz_type="correlations",
    output_format="interactive",
    theme="colorblind"
)

# 4. Leo manifest para ver qué se generó
import json
with open(dist_manifest) as f:
    manifest = json.load(f)
    
print(f"Visualizaciones generadas: {manifest['summary']['total_visualizations']}")

# 5. Usar en documentación
for viz in manifest['visualizations']:
    print(f"- {viz['title']}: {viz['path']}")
```

## Características Especiales

### 1. Interactividad con Plotly

```python
import plotly.express as px

# Scatter interactivo con zoom, hover info
fig = px.scatter(df, x='age', y='income', color='churn',
                 hover_data=['tenure', 'contract_type'])
fig.write_html('interactive_scatter.html')
```

### 2. Accesibilidad

- Uso paletas colorblind-friendly
- Alt text en gráficos
- Tamaño de fuente legible (>10pt)
- Contraste adecuado

### 3. Exportación Multi-formato

```python
# Genero mismo gráfico en varios formatos
fig.savefig('plot.png', dpi=300)
fig.savefig('plot.svg')
fig.savefig('plot.pdf')
```

### 4. Dashboard Completo

Puedo generar un dashboard HTML con múltiples gráficos:

```html
<!-- dashboard.html -->
<html>
  <body>
    <h1>EDA Dashboard</h1>
    <div class="viz">
      <iframe src="interactive_scatter.html"></iframe>
    </div>
    <div class="viz">
      <img src="correlation_heatmap.png">
    </div>
  </body>
</html>
```

## Criterios de Éxito

Una visualización es exitosa si:

- ✅ Títulos claros y descriptivos
- ✅ Ejes correctamente etiquetados
- ✅ Leyendas presentes cuando necesario
- ✅ Colores accesibles (colorblind-friendly)
- ✅ Resolución adecuada (DPI >= 300 para estáticos)
- ✅ Formato apropiado (interactivo vs estático)
- ✅ Archivos guardados correctamente

## Troubleshooting

### Error: "Figuras se sobreescriben"

**Causa**: No se llamó `plt.figure()` entre gráficos

**Solución**: Usar `plt.figure()` o `plt.close()` entre plots

### Warning: "Tamaño de figura muy grande"

**Solución**: Ajustar DPI o dimensiones en config

### "Colores no son colorblind-friendly"

**Solución**: Activar `colorblind_mode: true` en config

## Ejemplos de Invocación desde Cursor

### Distribuciones básicas

```
"@agente-visualizaciones crea histogramas de todas las variables numéricas"
```

### Correlaciones

```
"Genera un heatmap de correlaciones interactivo con tema dark"
```

### Serie temporal

```
"Grafica la evolución de ventas por mes con tendencia"
```

### Comparación de modelos

```
"Crea gráficos comparando accuracy de 3 modelos"
```

## Relación con Otros Agentes

**Agentes previos** (usan mis outputs como input):
- EDA → Me pasa DataFrame analizado + recomendaciones de gráficos

**Agentes posteriores** (usan mis visualizaciones):
- Documentación → Incluye gráficos en reportes markdown
- Deployment → Dashboard interactivo
- Presentaciones → Exporta PNG/SVG para slides

**Workflow típico**:
```
EDA → Visualizaciones (yo) → [Documentación | Deployment]
```

---

**Versión**: 1.0.0  
**Última actualización**: 2026-02-12  
**Mantenedor**: Equipo de Data Science
