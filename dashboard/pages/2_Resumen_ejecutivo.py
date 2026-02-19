"""
Resumen Ejecutivo: KPIs, gráfico de bandas, importancia de variables y costos de intervención.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from common import (
    ensure_authenticated,
    get_manifest,
    get_df_scoring,
    get_pipeline,
    get_preprocessor,
    render_sidebar_filters,
    get_df_filtrado,
    SCORING_COL,
)

ensure_authenticated()
manifest = get_manifest()
df_raw = get_df_scoring()
render_sidebar_filters(df_raw)
df = get_df_filtrado(df_raw)

st.title("Resumen Ejecutivo")
if df is None or df.empty:
    st.warning("Cargue `df_con_scoring.pkl` en artifacts/modeling/ para ver KPIs y costos de intervención.")
    st.stop()

if SCORING_COL not in df.columns:
    st.error("El DataFrame no tiene la columna de scoring.")
    st.stop()

total = len(df)
alto = (df[SCORING_COL] >= 0.5).sum()
medio = ((df[SCORING_COL] >= 0.3) & (df[SCORING_COL] < 0.5)).sum()
bajo = (df[SCORING_COL] < 0.3).sum()
pct_alto = (alto / total * 100) if total else 0

# Impacto abandono solo para alto riesgo
impacto_alto_riesgo = None
if "impacto_abandono" in df.columns:
    impacto_alto_riesgo = df.loc[df[SCORING_COL] >= 0.5, "impacto_abandono"].sum()

# Riesgo promedio (scoring medio)
riesgo_promedio = df[SCORING_COL].mean()

# Departamento con más riesgo (% en alto riesgo)
depto_mas_riesgo = None
if "departamento" in df.columns and total > 0:
    pct_alto_por_dept = df.groupby("departamento", dropna=False)[SCORING_COL].apply(lambda s: (s >= 0.5).mean() * 100)
    if len(pct_alto_por_dept) > 0:
        depto_mas_riesgo = pct_alto_por_dept.idxmax()

# KPIs
st.subheader("KPIs")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total empleados", total)
c2.metric("Alto riesgo (≥0.5)", alto)
c3.metric("Riesgo medio (0.3–0.5)", medio)
c4.metric("% en alto riesgo", f"{pct_alto:.1f}%")

r1, r2, r3 = st.columns(3)
r1.metric("Impacto abandono (solo alto riesgo)", f"{impacto_alto_riesgo:,.0f}" if impacto_alto_riesgo is not None and pd.notna(impacto_alto_riesgo) else "—")
r2.metric("Riesgo promedio", f"{riesgo_promedio:.2f}")
r3.metric("Departamento con más riesgo", depto_mas_riesgo if depto_mas_riesgo is not None else "—")

# Gráfico de bandas e importancia de variables (mitad y mitad)
st.subheader("Distribución por banda de riesgo e importancia del modelo")
col_bandas, col_imp = st.columns(2)

with col_bandas:
    df_bandas = pd.DataFrame({
        "Banda": ["Bajo (<0.3)", "Riesgo medio (0.3–0.5)", "Alto (≥0.5)"],
        "Empleados": [bajo, medio, alto],
    })
    fig_bandas = px.bar(df_bandas, x="Banda", y="Empleados", color="Empleados", color_continuous_scale="Blues")
    fig_bandas.update_traces(
        hovertemplate="<b>%{x}</b><br>Empleados: %{y}<br>Representa el número de empleados en esta banda de riesgo según su scoring.<extra></extra>"
    )
    fig_bandas.update_layout(title="Distribución por banda de riesgo")
    st.plotly_chart(fig_bandas, use_container_width=True)

with col_imp:
    df_imp = None
    best = (manifest or {}).get("best_model", {})
    imp_list = (best.get("feature_importances") or (manifest or {}).get("feature_importances") or [])
    if isinstance(imp_list, list) and len(imp_list) > 0:
        if isinstance(imp_list[0], dict):
            df_imp = pd.DataFrame(imp_list)
            if "variable" in df_imp.columns and "importancia" in df_imp.columns:
                df_imp = df_imp.nlargest(15, "importancia").sort_values("importancia", ascending=True)
            else:
                df_imp = None
        elif isinstance(imp_list[0], (int, float)):
            names = (manifest or {}).get("feature_columns", [])
            if len(names) != len(imp_list):
                names = [f"X{i}" for i in range(len(imp_list))]
            df_imp = pd.DataFrame({"variable": names, "importancia": imp_list}).nlargest(15, "importancia").sort_values("importancia", ascending=True)
    if df_imp is None:
        pipeline = get_pipeline()
        if pipeline is not None:
            try:
                if hasattr(pipeline, "steps") and len(pipeline.steps):
                    clf = pipeline.steps[-1][1]
                elif hasattr(pipeline, "named_steps"):
                    clf = pipeline.named_steps.get("clf", pipeline.named_steps.get("classifier", pipeline))
                else:
                    clf = pipeline
                if hasattr(clf, "feature_importances_"):
                    imp = clf.feature_importances_
                    preprocessor = get_preprocessor()
                    if preprocessor is not None and hasattr(preprocessor, "get_feature_names_out"):
                        try:
                            feature_names = preprocessor.get_feature_names_out()
                        except Exception:
                            feature_names = []
                    else:
                        feature_names = (manifest or {}).get("feature_columns", [])
                    if len(feature_names) != len(imp):
                        feature_names = [f"X{i}" for i in range(len(imp))]
                    top_n = min(15, len(imp))
                    idx_sorted = imp.argsort()[::-1][:top_n]
                    df_imp = pd.DataFrame({
                        "variable": [feature_names[i] for i in idx_sorted],
                        "importancia": imp[idx_sorted],
                    })
            except Exception:
                pass
    if df_imp is not None and len(df_imp) > 0:
        fig_imp = px.bar(df_imp, x="importancia", y="variable", orientation="h", title="Importancia de variables")
        fig_imp.update_layout(yaxis={"categoryorder": "total ascending"}, margin=dict(l=80))
        fig_imp.update_traces(
            hovertemplate="<b>%{y}</b><br>Importancia: %{x:.4f}<br>Contribución relativa de la variable al modelo de predicción de abandono.<extra></extra>"
        )
        st.plotly_chart(fig_imp, use_container_width=True)
    else:
        st.caption(
            "Para ver el gráfico de importancia, guarde pipeline.pkl (y preprocessor.pkl) en artifacts/modeling/ desde el notebook, "
            "o ejecute **scripts/export_model_artifacts.py**."
        )

# Costos de intervención
st.subheader("Costos de intervención")
umbral_default = 0.5
if manifest and manifest.get("best_model"):
    th_opt = manifest["best_model"].get("threshold_optimized")
    if th_opt and isinstance(th_opt, (int, float)):
        umbral_default = float(th_opt)
umbral = st.slider("Umbral de intervención (scoring ≥ este valor)", 0.0, 1.0, umbral_default, 0.05)
seleccionados = (df[SCORING_COL] >= umbral).sum()
if manifest and manifest.get("best_model", {}).get("metrics", {}).get("aupr"):
    st.caption("Precisión exacta en este umbral requiere curva Precision-Recall; use AUPR del modelo como referencia.")
st.metric("Empleados que serían seleccionados (scoring ≥ umbral)", seleccionados)
if total:
    st.caption(f"Representa {seleccionados/total*100:.1f}% del total filtrado.")
