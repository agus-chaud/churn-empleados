# Dashboard Churn Empleados – Despliegue

## Uso en local (ahora)

1. **Credenciales:** Cree el archivo `.streamlit/secrets.toml` en la carpeta `dashboard/` (o en la raíz del proyecto si ejecuta desde la raíz) con:

   ```toml
   [passwords]
   usuario = "su_contraseña"
   ```

   Es decir: la clave es el **nombre de usuario** y el valor es la **contraseña**. Para un solo usuario `admin` con contraseña `admin`:

   ```toml
   [passwords]
   admin = "admin"
   ```

   **No suba este archivo al repositorio.** Añada `dashboard/.streamlit/secrets.toml` y `.streamlit/secrets.toml` al `.gitignore`.

2. **Artefactos:** Para ver todas las secciones (Resumen Ejecutivo, Riesgo por segmento, etc.) necesita:
   - `artifacts/modeling/experiment_manifest.json` (obligatorio)
   - `artifacts/modeling/df_con_scoring.pkl` (recomendado; DataFrame con columna `scoring_abandono` y columnas como `departamento`, `anos_compania`, `satisfaccion_entorno`)
   - Para el **gráfico de importancia de variables** (Resumen del modelo): el dashboard puede obtener las importancias de dos formas:
     - Cargando `artifacts/modeling/best_model.pkl` (o `pipeline.pkl`) y, si existe, `artifacts/modeling/preprocessor.pkl` para los nombres de las variables.
     - O leyendo `feature_importances` desde el manifest (lista de `{variable, importancia}` dentro de `best_model` o en la raíz del JSON). Si el manifest ya incluye esa clave, el gráfico se muestra sin necesidad de los `.pkl`.

3. **Generar artefactos del modelo (gráfico de importancia):** Si no tiene `best_model.pkl` ni el manifest con `feature_importances`, puede generarlos con el script incluido en el proyecto. Desde la **raíz del proyecto**, con `AbandonoEmpleados.csv` disponible (en la raíz o en la ruta que indique):

   ```bash
   python scripts/export_model_artifacts.py
   ```

   Con otro CSV:

   ```bash
   python scripts/export_model_artifacts.py --csv ruta/al/archivo.csv
   ```

   El script entrena un pipeline XGBoost+SMOTE (estructura similar al notebook), guarda `artifacts/modeling/best_model.pkl` y `artifacts/modeling/preprocessor.pkl`, y actualiza el manifest con `best_model.feature_importances`. Tras ejecutarlo, reinicie el dashboard para ver el gráfico de importancia.

4. **Ejecución desde la raíz del proyecto:**

   ```bash
   cd "c:\Agus\Primera Semana"
   pip install -r dashboard/requirements.txt
   streamlit run dashboard/app.py
   ```

   O desde `dashboard/`:

   ```bash
   cd dashboard
   pip install -r requirements.txt
   streamlit run app.py
   ```

   Si ejecuta desde la raíz, las rutas a `artifacts/modeling/` se resuelven correctamente. Si ejecuta desde `dashboard/`, el código usa `Path(__file__).resolve().parent.parent` para apuntar a la raíz y encontrar `artifacts/`.

   (Los pasos 3 y 4 son independientes: puede ejecutar el dashboard sin haber corrido el script; en ese caso el gráfico de importancia solo aparecerá si el manifest ya trae `feature_importances`.)

---

## Despliegue en la nube (más adelante)

Cuando quiera subir el dashboard a **Streamlit Cloud** con control de credenciales:

1. **Conectar el repositorio** con Streamlit Cloud y seleccionar este proyecto.

2. **Directorio y comando:**
   - Directorio raíz del repositorio: deje el directorio raíz (donde está `dashboard/` y `artifacts/`).
   - Comando de arranque: `streamlit run dashboard/app.py`

3. **Secrets en Streamlit Cloud:** En la app → Settings → Secrets, añada el mismo formato que en local:

   ```toml
   [passwords]
   usuario = "contraseña_segura"
   ```

   **No** ponga credenciales en el código ni las suba al repo; solo en Secrets de la nube.

4. **Artefactos:** En Cloud, el repositorio se clona completo, así que `artifacts/modeling/` debe estar versionado (o generado en un paso previo de CI). Si prefiere no versionar los `.pkl`, puede configurar un job que genere los artefactos y los suba antes del deploy, o usar un directorio de trabajo que los descargue.

5. **URL pública:** Tras el deploy, Streamlit Cloud proporciona una URL. Compártala solo con quienes deban acceder; el login (usuario y contraseña) sigue siendo obligatorio.

---

## Estructura esperada

```
dashboard/
├── app.py
├── common.py
├── pages/
│   ├── 1_Resumen_modelo.py
│   ├── 2_Resumen_ejecutivo.py
│   ├── 3_Riesgo_por_segmento.py
│   ├── 4_Distribucion_scoring.py
│   └── 5_Scoring_y_datos.py
├── .streamlit/
│   └── config.toml
├── requirements.txt
├── README_DEPLOY.md
└── dashboard_manifest.json
```

Referencia de diseño: `docs/plans/2026-02-15-dashboard-churn-design.md`.
