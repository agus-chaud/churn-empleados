# Diseño del dashboard de churn de empleados

**Fecha:** 2026-02-15  
**Versión:** 1.0  
**Objetivo:** Especificación única para implementar el dashboard Streamlit con login, filtros globales, Resumen Ejecutivo con costos de intervención e integración con artefactos en `artifacts/modeling/`.

---

## 1. Alcance y dependencias

- **Inputs obligatorios:** `artifacts/modeling/experiment_manifest.json`, modelo y preprocessor en las rutas del manifest.
- **Input recomendado:** `artifacts/modeling/df_con_scoring.pkl` (DataFrame con columna `scoring_abandono` o equivalente y columnas de atributos: departamento, satisfaccion_entorno, anos_compania, etc.).
- **Autenticación:** Login por usuario y contraseña (secrets o variables de entorno); sin login no se muestra contenido.
- **Filtros:** Visibles en **todas las páginas** (sidebar); estado persistente entre páginas (ej. `st.session_state`).

---

## 2. Filtros globales (sidebar)

**Ubicación:** Sidebar, misma posición y controles en todas las páginas. Los filtros aplican al subset de datos usado en KPIs, tablas y gráficos que dependan del DataFrame con scoring.

| Filtro | Tipo | Comportamiento |
|--------|------|----------------|
| **Departamento** | Multiselect | Valores únicos de `departamento`. "Todos" por defecto. |
| **Banda de scoring** | Select o 2 sliders | Opciones: "Todos", "Alto riesgo (≥0.5)", "Riesgo medio (0.3–0.5)", "Bajo (<0.3)". Alternativa: slider min y max (0–1). |
| **Antigüedad en compañía** | Slider o select | Rango de `anos_compania` (min–max según datos). Ej.: 0–5, 5–10, 10–15, 15+. |
| **Satisfacción entorno** | Multiselect | Valores de `satisfaccion_entorno` (ej. Baja, Media, Alta). "Todos" por defecto. |

**Persistencia:** Al cambiar de página, los valores del sidebar se mantienen. Todo el contenido usa el mismo `df_filtrado` resultante de aplicar estos filtros.

**Opcional (firma):** Badge o indicador de "filtros activos" (cuántos filtros están distintos del valor por defecto).

---

## 3. Estructura de páginas

| # | Página / archivo | Nombre visible | Contenido principal |
|---|------------------|----------------|---------------------|
| 1 | `1_Resumen_modelo.py` | Resumen del modelo | Métricas del manifest, umbral, paths + **gráfico de importancia de variables** |
| 2 | `2_Resumen_ejecutivo.py` | Resumen Ejecutivo | KPIs (total, alto riesgo, riesgo medio, % riesgo) + donut/barras de bandas + **Costos de intervención** (slider umbral + resumen) |
| 3 | `3_Riesgo_por_segmento.py` | Riesgo por segmento | Riesgo por departamento, por antigüedad, por satisfacción |
| 4 | `4_Distribucion_scoring.py` | Distribución del scoring | Histograma/KDE del scoring + boxplot por departamento |
| 5 | `5_Scoring_y_datos.py` | Scoring y datos | Tabla priorizada por scoring + descarga CSV/Excel |
| 6 | `6_Comparativa_modelos.py` | Comparativa modelos | AUPR (u otra métrica) por modelo; destacar best_model |

**Nota:** No se incluye la sección "Contexto plantilla" (satisfacción, formaciones, años sin promoción como página independiente).

---

## 4. Especificación por página

### 4.1 Resumen del modelo (`1_Resumen_modelo.py`)

**Contenido:**
- Nombre del modelo (ej. XGBoost con SMOTE), run_id, fecha del manifest.
- Métricas del manifest: AUPR, F1, precision, recall, ROC AUC (las que existan).
- Umbral optimizado (si está en manifest).
- Paths de artefactos (informativo, sin rutas sensibles).
- **Gráfico de importancia de variables:**
  - **Tipo:** Barras horizontales.
  - **Eje Y:** Nombre de la variable (legible: ej. "Años en compañía", "Satisfacción entorno").
  - **Eje X:** Valor de importancia (`feature_importances_` del modelo o permutation importance). Top 10–15 variables, orden descendente.
  - **Datos:** Del modelo en `artifacts/modeling/` (pipeline/modelo final). Si el manifest incluye `feature_importances` o lista de features, usarlos para etiquetas.
  - **Filtros:** Ninguno (es propiedad del modelo, no del DataFrame filtrado).

---

### 4.2 Resumen Ejecutivo (`2_Resumen_ejecutivo.py`)

**Contenido:**

1. **KPIs (fila de columnas):**
   - Total empleados (filtrado): `len(df_filtrado)`.
   - Alto riesgo: `(df_filtrado['scoring_abandono'] >= 0.5).sum()`.
   - Riesgo medio: `(scoring >= 0.3) & (scoring < 0.5)`.
   - % plantilla en alto riesgo: (Alto riesgo / Total) × 100.
   - Todos reaccionan a los filtros del sidebar.

2. **Gráfico de bandas (opcional):**
   - Donut o barras horizontales: Bajo riesgo | Riesgo medio | Alto riesgo (count o %). Mismos umbrales (0.3 y 0.5).

3. **Costos de intervención (misma página):**
   - **Slider:** Umbral de intervención (0–1). Valor por defecto: umbral del manifest si existe, si no ej. 0.5.
   - **Resumen dinámico:** Dado el umbral elegido, mostrar:
     - Número de empleados que serían seleccionados (scoring ≥ umbral).
     - Precisión estimada en ese punto (si se puede derivar de curva precision-recall o del manifest).
     - Falsos positivos aproximados (texto o fórmula según métricas disponibles).
   - Todo calculado sobre `df_filtrado`.

---

### 4.3 Riesgo por segmento (`3_Riesgo_por_segmento.py`)

**Gráficos (todos sobre `df_filtrado`):**

| Gráfico | Tipo | Eje X | Eje Y | Notas |
|--------|------|--------|--------|--------|
| Riesgo por departamento | Barras horizontales | Departamento | % empleados con scoring ≥ 0.5 en ese departamento | Ordenar por % descendente. |
| Riesgo por antigüedad | Barras | Bins de `anos_compania` (ej. 0–2, 2–5, 5–10, 10–15, 15+) | % alto riesgo o count | Bins fijos. |
| Riesgo por satisfacción | Barras | `satisfaccion_entorno` (orden: Baja → Media → Alta) | % empleados con scoring ≥ 0.5 | Opcional: mismo para `satisfaccion_companeros`. |

**Filtros:** Sidebar global. Si se filtra por un solo departamento, el gráfico por departamento puede mostrar solo ese o un mensaje tipo "Seleccione más de un departamento para comparar".

**Opcional:** Drill-down: clic en barra aplica filtro de departamento al resto del dashboard (persistiendo en sidebar).

---

### 4.4 Distribución del scoring (`4_Distribucion_scoring.py`)

| Gráfico | Tipo | Eje X | Eje Y | Notas |
|--------|------|--------|--------|--------|
| Distribución | Histograma o KDE | `scoring_abandono` (bins 0–0.1 … 0.9–1) | Frecuencia | Línea vertical opcional en umbral (ej. 0.5). Área "alto riesgo" sombreada opcional. |
| Por departamento | Boxplot | Departamento | `scoring_abandono` | Varios box; ordenar por mediana descendente. |

**Filtros:** Sidebar global.

---

### 4.5 Scoring y datos (`5_Scoring_y_datos.py`)

- **Tabla:** Columnas relevantes + `scoring_abandono` + banda (Alto/Medio/Bajo). Orden por defecto: `scoring_abandono` descendente. Paginación si hay muchos registros.
- **Filtros:** Los del sidebar; opcional filtro adicional por banda solo para esta tabla.
- **Descarga:** Botón para exportar el DataFrame filtrado a CSV o Excel (incluyendo scoring y columnas mostradas).

---

### 4.6 Comparativa modelos (`6_Comparativa_modelos.py`)

- Si `experiment_manifest.json` tiene `models_tested`: tabla o gráfico de barras con AUPR (u otra métrica) por modelo.
- Destacar el modelo elegido (`best_model`).

---

## 5. Guía de diseño de interfaz

Alineado con `.cursor/rules/interface-design.md`. Aplicar a todas las páginas y al sidebar.

### 5.1 Checkpoint antes de cada componente

Declarar para cada bloque de UI:

- **Intención:** Quién usa (RRHH/manager), qué debe lograr (ver riesgo, priorizar, exportar), cómo debe sentirse (claro, accionable, no abrumador).
- **Paleta:** Colores del dominio (oficina, datos, confianza): grises neutros, un acento para riesgo (ej. ámbar/naranja suave), uno para estable (verde apagado). No múltiples acentos sin motivo.
- **Profundidad:** Una sola estrategia en todo el dashboard: solo bordes **o** solo sombras sutiles. Bordes en rgba suave para separar secciones.
- **Superficies:** Sidebar mismo fondo que el canvas; separación por borde sutil. Tarjetas/KPIs con elevación ligera (borde o sombra muy sutil).
- **Tipografía:** Cuatro niveles (primario, secundario, terciario, atenuado). Números "héroe" para KPIs y para "N empleados" en costos de intervención.
- **Espaciado:** Unidad base (ej. 8px) y múltiplos (8, 16, 24, 32) en padding y entre secciones.

### 5.2 Decisiones por interfaz

| Interfaz | Intención | Diseño clave |
|----------|-----------|--------------|
| Sidebar | "Desde aquí filtro todo" | Mismo fondo que contenido; borde sutil; estados hover/focus en controles; opcional badge "filtros activos". |
| Resumen modelo | "Qué modelo es y por qué dice lo que dice" | Métricas con jerarquía clara + un gráfico de importancia (barras horizontales); color con significado. |
| Resumen Ejecutivo | "Cuántos en riesgo y qué pasa si actúo" | KPIs en fila + donut/bandas + bloque Costos de intervención (slider + N, precisión, FP). Número "héroe" en costos. |
| Riesgo por segmento | "Dónde se concentra el riesgo" | 2–3 gráficos homogéneos; misma paleta y profundidad. |
| Distribución scoring | "Forma y dispersión del riesgo" | Histograma/KDE + boxplot; línea de umbral opcional. |
| Scoring y datos | "Lista para actuar y exportar" | Tabla con jerarquía visual; botón descarga visible pero no dominante. |
| Comparativa modelos | "Por qué este modelo" | Barras o tabla con modelo elegido destacado. |

### 5.3 Tokens sugeridos

- `--text-primary`, `--text-secondary`, `--text-tertiary`, `--text-muted`
- `--surface-base`, `--surface-raised`
- `--border-subtle`, `--border-strong`
- `--accent-risk`, `--accent-success` (opcional)
- Unidad base de espaciado y escala (ej. 8px, 16px, 24px, 32px)

### 5.4 Evitar

- Bordes duros (hex sólidos que destaquen).
- Sidebar con color de fondo distinto al contenido (rompe unidad).
- Múltiples colores de acento sin significado.
- Estados faltantes en controles (hover, focus, disabled).

---

## 6. Estructura de archivos del dashboard

```
dashboard/
├── app.py                      # Login + redirección; sidebar con filtros globales
├── pages/
│   ├── 1_Resumen_modelo.py     # Métricas + importancia de variables
│   ├── 2_Resumen_ejecutivo.py  # KPIs + bandas + costos de intervención
│   ├── 3_Riesgo_por_segmento.py
│   ├── 4_Distribucion_scoring.py
│   ├── 5_Scoring_y_datos.py
│   └── 6_Comparativa_modelos.py
├── .streamlit/
│   └── config.toml
├── requirements.txt
├── README_DEPLOY.md
└── dashboard_manifest.json     # Metadata: páginas, fuentes de datos
```

**Implementación del sidebar en todas las páginas:** En `app.py`, si la app es multipágina, el sidebar con filtros debe renderizarse en el layout principal antes de mostrar la página seleccionada (o incluir un fragmento común que cada página llame al inicio para dibujar los mismos filtros y leer/escribir `st.session_state`).

---

## 7. Validaciones pre-implementación

- [ ] Manifest existe y tiene al menos `best_model`, `model_path` y métricas o `models_tested`.
- [ ] Si se usa `df_con_scoring.pkl`: path existe y tiene columna de scoring esperada y columnas para filtros (departamento, anos_compania, satisfaccion_entorno).
- [ ] `app.py` comprueba credenciales antes de mostrar contenido.
- [ ] Filtros definidos una sola vez y visibles en todas las páginas con estado persistente.
- [ ] Resumen Ejecutivo incluye el bloque "Costos de intervención" en la misma página.
- [ ] Resumen del modelo incluye el gráfico de importancia de variables.
- [ ] No existe la sección "Contexto plantilla" como página independiente.

---

## 8. Referencias

- Regla del dashboard: `.cursor/rules/agente-streamlit.md`
- Diseño de interfaces: `.cursor/rules/interface-design.md`
- Documentación del modelo: `docs/eleccion_modelo_churn_xgboost_smote.md`
