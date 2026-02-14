---
name: EDA y Calidad de Datos
overview: Plan para incorporar en el notebook de TPS (Día 1) un análisis de calidad de datos, EDA de variables categóricas, EDA de variables numéricas y un conjunto de preguntas semilla orientadas al target "abandono".
todos: []
isProject: false
---

# Plan: Análisis de calidad, EDA y preguntas semilla

Contexto: el dataset [AbandonoEmpleados.csv](c:\Agus\Primera Semana\AbandonoEmpleados.csv) tiene 1470 filas y 31 columnas (target: `abandono` Yes/No). Se carga en [TPS_Dia_1_Configuracion.ipynb](c:\Agus\Primera Semana\TPS_Dia_1_Configuracion.ipynb) con `sep=';'`, `index_col='id'` y `na_values='#N/D'`. Ya se observan NaN en `conciliacion`, `anos_en_puesto`, `educacion` y `sexo` (este último como float 2.0/3.0/4.0).

---

## 1. Análisis de calidad de datos

Objetivo: cuantificar y documentar problemas que afecten modelado o interpretación.

- **Estructura y tipos**
  - `df.info()`, `df.dtypes` para ver tipos inferidos.
  - Identificar columnas que deberían ser categóricas pero están como numéricas (ej. `sexo`, quizá `nivel_laboral`, `empleados`) o al revés (ej. `distancia_casa` si se usa como categoría).
- **Valores faltantes**
  - Por columna: `df.isna().sum()` y porcentaje sobre total filas.
  - Matriz o mapa de calor de faltantes (opcional: `missingno` o heatmap con `sns.heatmap(df.isna(), ...)`).
  - Decisión por variable: columnas con muchos faltantes (ej. `conciliacion`) vs pocos (ej. `educacion`, `sexo`, `anos_en_puesto`); documentar si se imputará, se eliminará o se dejará para más adelante.
- **Duplicados y unicidad**
  - `df.duplicated().sum()` (tras resetear índice si hace falta).
  - Comprobar si el índice `id` es único.
- **Valores extraños / rangos**
  - Revisión rápida de rangos numéricos (mín/máx) y categorías únicas en texto (valores inesperados, espacios, mayúsculas inconsistentes).
  - Detección de posibles códigos numéricos mal interpretados (ej. `sexo` 1,2,3,4 sin etiqueta).
- **Resumen de calidad**
  - Tabla o sección markdown: por variable, tipo recomendado, % faltantes, observaciones (duplicados, valores raros, decisiones).

---

## 2. EDA variables categóricas

Variables candidatas (según cabecera del CSV): `abandono`, `viajes`, `departamento`, `educacion`, `carrera`, `satisfaccion_entorno`, `sexo` (recodificar si es numérico), `implicacion`, `puesto`, `satisfaccion_trabajo`, `estado_civil`, `mayor_edad`, `horas_extra`, `evaluacion`, `satisfaccion_companeros`, `conciliacion`.

- **Frecuencias**
  - Conteo por categoría: `value_counts()` con y sin normalizar.
  - Gráficos: barras horizontales (para muchas categorías) o barras verticales; ordenar por frecuencia para legibilidad.
- **Relación con el target**
  - Tasas de abandono por categoría (porcentaje de `abandono == 'Yes'` en cada nivel).
  - Gráficos: barras agrupadas o apiladas (abandono Sí/No por categoría), o líneas de tasa por categoría.
  - Destacar categorías con tasa de abandono muy alta o muy baja.
- **Cardinalidad y categorías poco frecuentes**
  - Número de categorías por variable; listar variables con muchas modalidades (ej. `puesto`).
  - Decisión: agrupar categorías poco frecuentes (“Otros”) solo si se documenta y es útil para el análisis.

---

## 3. EDA variables numéricas

Variables candidatas: `edad`, `distancia_casa`, `empleados`, `salario_mes`, `num_empresas_anteriores`, `incremento_salario_porc`, `horas_quincena`, `nivel_acciones`, `anos_experiencia`, `num_formaciones_ult_ano`, `anos_compania`, `anos_en_puesto`, `anos_desde_ult_promocion`, `anos_con_manager_actual`. Considerar `nivel_laboral` según decisión de tipos en calidad.

- **Estadísticos descriptivos**
  - `df[columnas_numericas].describe()` (incluir percentiles y std).
  - Medidas de asimetría si se dispone (ej. `scipy.stats.skew` o comentario visual).
- **Distribuciones**
  - Histogramas por variable (elegir bins adecuados).
  - Boxplots por variable para ver mediana, cuartiles y outliers.
  - Identificar variables muy sesgadas o con muchos outliers y documentarlo.
- **Relación con el target**
  - Medias (o medianas) de cada numérica según `abandono` (Yes vs No).
  - Boxplots o histogramas superpuestos: variable numérica segmentada por `abandono`.
  - Variables donde la distribución cambie claramente entre quienes abandonan y quienes no.
- **Correlaciones (entre numéricas)**
  - Matriz de correlación (Pearson) y heatmap.
  - Marcar pares con correlación alta para tener en cuenta en interpretación o multicolinealidad más adelante.

---

## 4. Preguntas semilla

Definir 5–8 preguntas concretas que el EDA debe poder responder y que orienten el uso del modelo (predicción de abandono). Ejemplos adaptados al dataset:

- ¿Qué porcentaje de empleados abandona? ¿Hay desbalance de clases?
- ¿El abandono está asociado al departamento o al tipo de puesto?
- ¿La satisfacción (entorno, trabajo, compañeros) se relaciona con menor tasa de abandono?
- ¿Los que hacen horas extra o viajan con frecuencia abandonan más?
- ¿La distancia al trabajo, los años en la compañía o sin promoción se asocian al abandono?
- ¿El nivel salarial o el incremento salarial reciente se relacionan con el abandono?
- ¿Hay diferencias por edad, años de experiencia o formación reciente?

Formato sugerido: una celda markdown con la lista de preguntas y, en celdas siguientes, una respuesta breve con gráfico o tabla clave que la sustente (enlazando a los resultados del EDA de calidad, categóricas y numéricas).

---

## Orden sugerido en el notebook

1. Celdas actuales (libs + carga + `df`).
2. **Calidad**: estructura, faltantes, duplicados, valores raros, resumen.
3. **Clasificación de columnas**: listas `cat_cols` y `num_cols` (tras decisiones de tipos en calidad).
4. **EDA categóricas**: frecuencias y relación con `abandono`.
5. **EDA numéricas**: descripción, distribuciones, relación con `abandono`, correlaciones.
6. **Preguntas semilla**: lista + respuestas con evidencia.

Dependencias: además de `numpy`, `pandas` y `matplotlib`, conviene usar `seaborn` para heatmaps y boxplots más claros.