---
name: ML desbalance y modelos
overview: Plan para incorporar compensación de desbalance (class_weight/scale_pos_weight), optimización de hiperparámetros con RandomizedSearchCV en todos los modelos, añadir Random Forest, XGBoost y LightGBM, y evaluar con AUPR, F1, Precision, Recall y matriz de confusión.
todos: []
isProject: false
---

# Plan: Desbalance, nuevos modelos y métricas en TPS_Dia_3_ML

## Contexto

- **Archivo:** [TPS_Dia_3_Machine_Learning.ipynb](c:\Agus\Primera Semana\TPS_Dia_3_Machine_Learning.ipynb)
- **Situación actual:** Un solo modelo `DecisionTreeClassifier(max_depth=4)`, evaluación solo con `roc_auc_score(test_y, pred)` donde `pred` son probabilidades. Variables `train_x`, `test_x`, `train_y`, `test_y` ya definidas; `x`/`y` vienen de `df_ml`.
- **Dependencias posteriores:** La variable `ac` se usa en: `plot_tree(ac,...)`, `ac.feature_importances_` y `df['scoring_abandono'] = ac.predict_proba(...)`. Hay que mantener compatibilidad con esas celdas (por ejemplo dejando `ac` como el modelo elegido o el que se use para scoring).

## 1. Reproducibilidad del split

- En la celda donde está `train_test_split(x, y, test_size=0.3)`, añadir `**random_state=42**` para que los resultados sean reproducibles al comparar modelos.

## 2. Configuración común para RandomizedSearchCV

- Importar `RandomizedSearchCV` de `sklearn.model_selection`.
- Criterios comunes para todos los modelos:
  - **scoring:** usar una métrica adecuada para desbalance (ej. `'average_precision'` o `'f1'`). Recomendación: `scoring='average_precision'` (AUPR) para que la búsqueda priorice el ranking de la clase positiva.
  - **cv:** 5 (o 3 si el entrenamiento es lento).
  - **n_iter:** número de combinaciones aleatorias (ej. 25–40 por modelo; ajustar según tiempo).
  - **random_state=42** en `RandomizedSearchCV` para reproducibilidad.
  - **refit=True** (por defecto) para que el mejor estimador quede disponible en `.best_estimator_`.
- Tras cada búsqueda: usar `busqueda.best_estimator_` para evaluar en test con la función de evaluación y para la tabla comparativa.

## 3. Función de evaluación unificada

- Añadir una **nueva celda** (o bloque de código reutilizable) que defina una función, por ejemplo `evaluar_clasificador(y_true, y_pred_proba, nombre_modelo="")`, que:
  - Reciba `y_true`, las **probabilidades** de la clase positiva `y_pred_proba`, y opcionalmente el nombre del modelo.
  - Obtenga las **clases predichas** con umbral 0.5: `y_pred = (y_pred_proba >= 0.5).astype(int)`.
  - Calcule y muestre (print o return):
    - **AUPR:** `sklearn.metrics.average_precision_score(y_true, y_pred_proba)`
    - **F1:** `sklearn.metrics.f1_score(y_true, y_pred, zero_division=0)`
    - **Precision:** `sklearn.metrics.precision_score(y_true, y_pred, zero_division=0)`
    - **Recall:** `sklearn.metrics.recall_score(y_true, y_pred, zero_division=0)`
    - **Matriz de confusión:** `sklearn.metrics.confusion_matrix(y_true, y_pred)` (mostrarla en texto o como tabla).
  - Opcional pero recomendable: usar `ConfusionMatrixDisplay.from_predictions(y_true, y_pred)` para visualizar la matriz (por modelo o en una figura con subplots).
- Importar: `average_precision_score`, `f1_score`, `precision_score`, `recall_score`, `confusion_matrix`, y opcionalmente `ConfusionMatrixDisplay`.

## 4. Decision Tree con class_weight y RandomizedSearchCV

- En la celda de modelo (o nueva celda): usar **RandomizedSearchCV** sobre `DecisionTreeClassifier(class_weight='balanced', random_state=42)`.
- **param_distributions** sugerido (usar distribuciones para muestreo aleatorio):
  - `max_depth`: lista o `np.arange`, ej. `[3, 5, 7, 10, 15, 20, None]`
  - `min_samples_split`: ej. `[2, 5, 10, 20]`
  - `min_samples_leaf`: ej. `[1, 2, 5, 10]`
  - `criterion`: `['gini', 'entropy']`
- Llamar `.fit(train_x, train_y)`. Asignar el mejor estimador: `ac = busqueda_dt.best_estimator_` (o guardar en variable intermedia y luego asignar a `ac` para compatibilidad con celdas posteriores).
- Obtener `pred = ac.predict_proba(test_x)[:, 1]` y llamar `evaluar_clasificador(test_y, pred, "Decision Tree")`.

## 5. Random Forest con RandomizedSearchCV

- **Nueva celda:** Importar `RandomForestClassifier` de `sklearn.ensemble`.
- **RandomizedSearchCV** sobre `RandomForestClassifier(class_weight='balanced', random_state=42)`.
- **param_distributions** sugerido:
  - `n_estimators`: ej. `[50, 100, 200, 300]`
  - `max_depth`: ej. `[5, 10, 15, 20, None]`
  - `min_samples_split`: ej. `[2, 5, 10]`
  - `min_samples_leaf`: ej. `[1, 2, 5]`
  - `max_features`: ej. `['sqrt', 'log2', None]`
- Tras `.fit(train_x, train_y)`: `model_rf = busqueda_rf.best_estimator_`, luego `pred_rf = model_rf.predict_proba(test_x)[:, 1]` y `evaluar_clasificador(test_y, pred_rf, "Random Forest")`.

## 6. XGBoost con RandomizedSearchCV

- **Nueva celda:** Importar `XGBClassifier` (paquete `xgboost`). Calcular `scale_pos_weight = (train_y == 0).sum() / max((train_y == 1).sum(), 1)` y fijarlo en el estimador base.
- **RandomizedSearchCV** sobre `XGBClassifier(scale_pos_weight=scale_pos_weight, random_state=42, use_label_encoder=False, eval_metric='logloss')` (parámetros según versión de XGBoost).
- **param_distributions** sugerido:
  - `n_estimators`: ej. `[50, 100, 200, 300]`
  - `max_depth`: ej. `[3, 5, 7, 9]`
  - `learning_rate`: ej. `[0.01, 0.05, 0.1, 0.2]`
  - `subsample`: ej. `[0.7, 0.8, 0.9, 1.0]`
  - `colsample_bytree`: ej. `[0.7, 0.8, 0.9, 1.0]`
  - `min_child_weight`: ej. `[1, 3, 5]`
- Tras `.fit(train_x, train_y)`: `model_xgb = busqueda_xgb.best_estimator_`, luego `pred_xgb = model_xgb.predict_proba(test_x)[:, 1]` y `evaluar_clasificador(test_y, pred_xgb, "XGBoost")`.

## 7. LightGBM con RandomizedSearchCV

- **Nueva celda:** Importar `LGBMClassifier` (paquete `lightgbm`). Calcular `scale_pos_weight` igual que para XGBoost.
- **RandomizedSearchCV** sobre `LGBMClassifier(scale_pos_weight=scale_pos_weight, random_state=42)`.
- **param_distributions** sugerido:
  - `n_estimators`: ej. `[50, 100, 200, 300]`
  - `max_depth`: ej. `[3, 5, 7, 10, -1]`
  - `learning_rate`: ej. `[0.01, 0.05, 0.1, 0.2]`
  - `num_leaves`: ej. `[31, 50, 70, 100]`
  - `min_child_samples`: ej. `[5, 10, 20, 30]`
  - `subsample`: ej. `[0.7, 0.8, 0.9, 1.0]`
  - `colsample_bytree`: ej. `[0.7, 0.8, 0.9, 1.0]`
- Tras `.fit(train_x, train_y)`: `model_lgb = busqueda_lgb.best_estimator_`, luego `pred_lgb = model_lgb.predict_proba(test_x)[:, 1]` y `evaluar_clasificador(test_y, pred_lgb, "LightGBM")`.

## 8. Tabla comparativa y modelo para scoring

- **Nueva celda:** Construir un DataFrame resumen con columnas: `Modelo`, `AUPR`, `F1`, `Precision`, `Recall` (y opcionalmente `ROC_AUC` si se guardó en la función de evaluación). Rellenar con los resultados de Decision Tree, Random Forest, XGBoost y LightGBM (usar variables guardadas o recalcular con la función).
- Definir criterio de “mejor” (por ejemplo mayor F1 o mayor AUPR). Asignar el mejor modelo a `**ac**` para no romper las celdas posteriores que usan `ac`:
  - `plot_tree(ac, ...)` solo tiene sentido si `ac` es un árbol (DecisionTree); si el mejor es RF/XGB/LGB, se puede dejar `ac` como el mejor modelo y comentar o adaptar la celda de `plot_tree` (solo para DT), o mantener `ac` como DT y usar otra variable para el scoring si se prefiere.
- Recomendación: asignar a `ac` el modelo que se vaya a usar para scoring (el elegido como mejor), de forma que `df['scoring_abandono'] = ac.predict_proba(df_ml.drop(columns='abandono'))[:, 1]` siga funcionando. La celda de `plot_tree` puede quedar condicionada a “si ac es DecisionTree” o dejarse solo para cuando el usuario elija DT como mejor.

## Orden sugerido de celdas

1. Añadir `random_state=42` al `train_test_split`.
2. Celda con imports de métricas, `RandomizedSearchCV`, y función `evaluar_clasificador`.
3. Celda Decision Tree: RandomizedSearchCV con `class_weight='balanced'` + evaluación con la función.
4. Celda Random Forest: RandomizedSearchCV + evaluación.
5. Celda XGBoost: RandomizedSearchCV con `scale_pos_weight` + evaluación.
6. Celda LightGBM: RandomizedSearchCV con `scale_pos_weight` + evaluación.
7. Celda tabla comparativa y asignación de `ac` al mejor modelo.

## Notas

- **RandomizedSearchCV:** Usar `n_iter` moderado (25–40) para equilibrar tiempo y calidad; si el entrenamiento es muy lento, reducir `cv` a 3 o `n_iter` a 15–20.
- **Scoring en la búsqueda:** Con `scoring='average_precision'` la optimización prioriza AUPR (recomendado para desbalance). Alternativa: `scoring='f1'` si se prefiere optimizar F1 directamente.
- **AUPR** (Average Precision): `average_precision_score` en sklearn; no se infla por los TN, adecuado para clases minoritarias.
- **Dependencias:** Verificar que `xgboost` y `lightgbm` estén en el entorno; si el notebook corre en Colab, incluirlos en una celda de instalación si hace falta.
- **Feature importance:** Las celdas que usan `ac.feature_importances_` funcionan con RF, XGB y LGB (todos exponen `feature_importances_`). Solo `plot_tree` es específico de un único árbol.

