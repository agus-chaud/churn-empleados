# Churn de empleados – Predicción y dashboard

Proyecto de **detección y priorización del riesgo de abandono (churn)** de los empleados. Incluye un notebook con un modelo predictivo y un dashboard Streamlit con login para explorar scoring, KPIs y candidatos a retención.

**Ver el dashboard en vivo:** [https://churn-empleados.streamlit.app/Resumen_ejecutivo](https://churn-empleados.streamlit.app/Resumen_ejecutivo) (user: agus , password: streamlit).

---

## Contexto del negocio

**Problema:** Identificar qué empleados tienen mayor probabilidad de abandonar la empresa para poder actuar con tiempo (retención, ofertas, seguimiento) y priorizar recursos.

**Objetivo:** Entregar un modelo de predicción de churn con probabilidad (scoring) por empleado, métricas de evaluación adecuadas a clase desbalanceada (AUPR), y un dashboard que permita  filtrar por departamento, antigüedad y satisfacción, ver KPIs y bandas de riesgo.

---

## Enfoque y decisiones técnicas

- **Metodología:** Análisis exploratorio y feature engineering en notebook; entrenamiento con **SMOTE** para balancear la clase minoritaria (abandono); evaluación con **AUPR** y matriz de confusión (TP/FP) por el coste operativo de los falsos positivos.
- **Modelo elegido:** **XGBoost (SMOTE)** como modelo de referencia (ver `docs/eleccion_modelo_churn_xgboost_smote.md`): mejor equilibrio TP/FP y AUPR frente a Random Forest y LightGBM con SMOTE.
- **Pipeline:** Datos en CSV (`AbandonoEmpleados.csv`) → preprocesado (numéricas + categóricas con OneHotEncoder) → SMOTE en entrenamiento → XGBoost → probabilidad de abandono por empleado. Artefactos (modelo, preprocessor, manifest, DataFrame con scoring) se guardan en `artifacts/modeling/` para el dashboard.
- **Dashboard:** Streamlit multipágina con autenticación (usuario/contraseña vía secrets o variables de entorno), filtros globales en sidebar (departamento, umbral alto/medio de riesgo, banda de scoring, años en compañía, satisfacción entorno) y estado persistente entre páginas (`st.session_state`). Los umbrales de riesgo son configurables y aplican a todas las solapas.
- **Convenciones:** Columna de scoring `scoring_abandono`; bandas Bajo / Riesgo medio / Alto según umbrales configurables (por defecto 0,3 y 0,5).

---

## Resultados e impacto

**Funcionalidades entregadas:**

- **Resumen ejecutivo:** KPIs (total empleados, alto riesgo, riesgo medio, % en alto riesgo), impacto abandono (solo alto riesgo), riesgo promedio, departamento con más riesgo; gráfico de distribución por banda de riesgo y gráfico de importancia de variables (mitad y mitad).
- **Distribución y riesgo por segmento:** Histograma del scoring con líneas de umbral; boxplot por departamento; barras de % alto riesgo por departamento, por antigüedad (bins) y por satisfacción entorno. Umbral configurable desde el sidebar.
- **Scoring y datos:** Tabla de candidatos a retención (solo empleados que no han abandonado y con scoring mayor al umbral de riesgo medio), ordenada por scoring descendente, con bandas coloreadas (rojo claro = alto riesgo, amarillo claro = riesgo medio) y descarga CSV.

**Visualizaciones:** Gráficos de barras (Plotly) para bandas, importancia de variables y riesgo por segmento; histograma y boxplot para distribución del scoring; tabla con estilo condicional por banda. Exportación CSV de la tabla de scoring.

---

## Principales desafíos y cómo se solucionaron

- **Clase desbalanceada:** Uso de SMOTE en el pipeline de entrenamiento y métrica AUPR para evaluar el modelo sin que el desbalance predomine.
- **Coste de falsos positivos:** Elección de XGBoost (SMOTE) frente a LightGBM por menor número de FP (57 vs 90) manteniendo TP razonables, reduciendo coste operativo de intervenciones innecesarias.
- **Rendimiento del dashboard:** Caché de la tabla preparada en “Scoring y datos” (`@st.cache_data`) y cálculo de bandas/estilos vectorizado con NumPy para acelerar la carga.

---

## Futuras mejoras

- Cuantificar de forma explícita el coste de un FP y el beneficio de un TP (en horas o dinero) para definir un umbral óptimo que maximice el valor esperado.

---

## Estructura del proyecto

```
Primera Semana/
├── Churn-empleados.ipynb     # Análisis, feature engineering, entrenamiento y evaluación del modelo
├── AbandonoEmpleados.csv     # Dataset de entrada (empleados y abandono; no versionado si es sensible)
├── README.md                 # Este archivo
├── docs/
│   ├── eleccion_modelo_churn_xgboost_smote.md   # Justificación del modelo elegido
│   └── plans/
│       └── 2026-02-15-dashboard-churn-design.md # Especificación del dashboard
├── dashboard/
│   ├── app.py                # Entrada: login y redirección; sidebar con filtros
│   ├── common.py             # Carga de manifest, df scoring, pipeline, filtros y get_df_filtrado
│   ├── pages/
│   │   ├── 2_Resumen_ejecutivo.py      # KPIs, bandas, importancia de variables
│   │   ├── 3_Distribucion_y_riesgo.py  # Histograma, boxplot, riesgo por segmento
│   │   └── 5_Scoring_y_datos.py        # Tabla priorizada y descarga CSV
│   ├── .streamlit/
│   │   ├── config.toml
│   │   └── secrets.example.toml       # Ejemplo de credenciales (no subir secrets.toml)
│   ├── requirements.txt
│   ├── README_DEPLOY.md      # Instrucciones de despliegue local y en nube
│   └── dashboard_manifest.json
├── artifacts/
│   └── modeling/             # experiment_manifest.json, df_con_scoring.pkl, pipeline.pkl, best_model.pkl, preprocessor.pkl
└── scripts/
    └── export_model_artifacts.py       # Entrena pipeline y genera artefactos para el dashboard
```

---

## Requisitos

- **Python:** 3.8+ (recomendado 3.10+).
- **Dashboard:** `dashboard/requirements.txt` incluye `streamlit>=1.28.0`, `pandas>=1.5.0`, `joblib>=1.2.0`, `plotly>=5.14.0`, `scikit-learn>=1.2.0`, `imbalanced-learn>=0.10.0`, `xgboost>=1.7.0`.
- **Notebook:** Además, las librerías típicas de análisis (pandas, numpy, matplotlib, seaborn, scikit-learn) según el notebook.

---

## Dataset

- **Origen:** Archivo CSV `AbandonoEmpleados.csv` (separador `;`, índice `id`, valores faltantes `#N/D`).
- **Columnas clave:** `edad`, `abandono` (Yes/No o 0/1), `viajes`, `departamento`, `distancia_casa`, `educacion`, `carrera`, `empleados`, `satisfaccion_entorno`, `sexo`, `satisfaccion_companeros`, `horas_quincena`, y otras de experiencia, promociones, formación, etc. El notebook deriva variables adicionales (p. ej. `impacto_abandono`, `ratio_estancamiento`).
- **Formato esperado para el dashboard:** Tras el notebook (o el script de exportación), se esperan en `artifacts/modeling/`: `experiment_manifest.json`, `df_con_scoring.pkl` (DataFrame con columna `scoring_abandono` y columnas como `departamento`, `anos_compania`, `satisfaccion_entorno`, `impacto_abandono`), y opcionalmente `pipeline.pkl` o `best_model.pkl` y `preprocessor.pkl` para el gráfico de importancia.

---

## Cómo ejecutarlo y usarlo

1. **Entorno:** Crear y activar un entorno virtual (opcional pero recomendado).
2. **Instalar dependencias del dashboard:**
   ```bash
   pip install -r dashboard/requirements.txt
   ```
3. **Credenciales:** Crear `dashboard/.streamlit/secrets.toml` (o `.streamlit/secrets.toml` en la raíz si se ejecuta desde la raíz) con:
   ```toml
   [passwords]
   usuario = "su_contraseña"
   ```
   No versionar este archivo.
4. **Artefactos:** Para que el dashboard muestre datos y gráficos, colocar en `artifacts/modeling/` al menos `experiment_manifest.json` y, recomendado, `df_con_scoring.pkl`. Si no existen, se pueden generar desde el notebook (guardando el DataFrame con scoring y el manifest) o ejecutando:
   ```bash
   python scripts/export_model_artifacts.py
   ```
   (requiere `AbandonoEmpleados.csv` en la raíz o indicar `--csv ruta/al/archivo.csv`).
5. **Arrancar el dashboard:** Desde la raíz del proyecto:
   ```bash
   streamlit run dashboard/app.py
   ```
   O desde `dashboard/`: `streamlit run app.py`.
6. **Uso:** Iniciar sesión con el usuario y contraseña configurados; usar el sidebar para filtrar por departamento, umbrales de riesgo, banda, años en compañía y satisfacción. Las tres solapas (Resumen ejecutivo, Distribución y riesgo, Scoring y datos) usan los mismos filtros. En “Scoring y datos” se puede descargar la tabla en CSV.

Para más detalle sobre despliegue local y en la nube (Streamlit Cloud), ver `dashboard/README_DEPLOY.md`.
