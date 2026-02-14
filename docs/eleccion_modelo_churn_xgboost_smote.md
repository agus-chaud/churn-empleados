# Elección del modelo óptimo para predicción de churn de empleados

## Resumen ejecutivo

Tras evaluar los modelos entrenados con **SMOTE** (Random Forest, XGBoost y LightGBM) sobre el conjunto de test, se recomienda **XGBoost (SMOTE)** como modelo de referencia para la detección de churn. La decisión se fundamenta en la **métrica AUPR**, en el **balance entre verdaderos positivos y falsos positivos** y en un criterio de **costo operativo** asociado a los falsos positivos.

---

## 1. Métrica principal: AUPR

En problemas con **clase minoritaria** (pocos empleados que se van frente a muchos que se quedan), el **área bajo la curva Precision-Recall (AUPR)** es más informativa que el AUC-ROC porque no depende del desbalance de clases y penaliza adecuadamente los errores sobre la clase positiva (churn).

| Modelo           | AUPR (con SMOTE) |
|------------------|-------------------|
| Random Forest    | 0,4262            |
| **XGBoost**      | **0,4202**        |
| LightGBM         | 0,4118            |

XGBoost (SMOTE) presenta el **segundo mejor AUPR** entre los tres y se sitúa muy cerca del Random Forest, con una diferencia marginal. En cambio, LightGBM (SMOTE) queda claramente por debajo en esta métrica, lo que indica un peor rendimiento global en el ranking de probabilidades para la clase positiva.

---

## 2. Análisis de la matriz de confusión: TP y FP

La matriz de confusión permite cuantificar no solo cuántos casos de churn se detectan bien (TP), sino también cuántas alertas incorrectas se generan (FP), que en un contexto de RR. HH. suelen traducirse en costos (reuniones, planes de retención, seguimiento) sobre empleados que en realidad no se iban a ir.

### XGBoost (SMOTE)

|                | Predicho: No churn | Predicho: Churn |
|----------------|--------------------|-----------------|
| **Real: No churn** | 323 (TN)           | **57 (FP)**     |
| **Real: Churn**    | 28 (FN)            | **33 (TP)**     |

- **Verdaderos positivos (TP):** 33 empleados con churn correctamente identificados.  
- **Falsos positivos (FP):** 57 empleados clasificados como churn que no abandonaron.

### LightGBM (SMOTE)

|                | Predicho: No churn | Predicho: Churn |
|----------------|--------------------|-----------------|
| **Real: No churn** | 290 (TN)           | **90 (FP)**     |
| **Real: Churn**    | 22 (FN)            | **39 (TP)**     |

- **Verdaderos positivos (TP):** 39 (6 más que XGBoost).  
- **Falsos positivos (FP):** 90 (33 más que XGBoost).

LightGBM (SMOTE) acierta en **6 casos de churn más** que XGBoost (39 frente a 33), pero a cambio genera **33 falsos positivos adicionales**. Es decir, por cada TP extra que aporta LightGBM se producen aproximadamente **5,5 FP extra**, lo que degrada la precisión y aumenta el coste operativo de las intervenciones.

---

## 3. Criterio de costo y decisión

En un escenario típico de prevención de churn:

- Cada **TP** representa un empleado que sí se iba y sobre el que tiene sentido actuar (retención, ofertas, etc.).
- Cada **FP** representa un empleado que no iba a ir y sobre el que se activan acciones innecesarias: tiempo de managers, reuniones, posibles incentivos mal asignados y desgaste de confianza si las alertas se perciben como erróneas.

Asumir que **el costo de un FP es relevante** (en tiempo, recursos y credibilidad del modelo) implica que:

- Las **6 detecciones adicionales de churn** que aporta LightGBM no compensan las **33 alertas falsas extra**.
- XGBoost (SMOTE) ofrece un **mejor equilibrio**: menos FP (57 frente a 90) manteniendo un número alto de TP (33) y el **mejor AUPR entre los dos** (0,4202 frente a 0,4118).

Por tanto, desde un enfoque **técnico y de costo operativo**, se considera **XGBoost (SMOTE)** el modelo recomendado para desplegar en producción o para priorizar en análisis de churn.

---

## 4. Conclusión

La elección de **XGBoost (SMOTE)** como mejor modelo se basa en:

1. **AUPR superior** al de LightGBM (SMOTE), reflejando mejor capacidad de ranking y de discriminación de la clase positiva en contextos desbalanceados.  
2. **Mayor número de churns correctamente predichos (TP)** en relación con el número de falsas alarmas (FP) respecto a LightGBM (SMOTE).  
3. **Menor número de falsos positivos** (57 vs 90), lo que reduce el costo operativo y mejora la precisión de las intervenciones de retención.

Si en el futuro se cuantifica de forma explícita el costo de un FP y el beneficio de un TP (por ejemplo, en horas o dinero), puede aplicarse un umbral óptimo que maximice el valor esperado; con la información actual, el balance TP/FP y el AUPR apoyan la recomendación de **XGBoost (SMOTE)** como modelo de referencia para predicción de churn de empleados.
