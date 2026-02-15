"""
Resumen del modelo: métricas del manifest, umbral, paths y gráfico de importancia de variables.
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
)

ensure_authenticated()
manifest = get_manifest()
df_raw = get_df_scoring()
render_sidebar_filters(df_raw)
get_df_filtrado(df_raw)

st.title("Resumen del modelo")
if not manifest:
    st.warning("No se encontró el manifest en `artifacts/modeling/experiment_manifest.json`.")
    st.stop()

best = manifest.get("best_model", {})
metrics = best.get("metrics", {})
st.subheader("Modelo y métricas")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Modelo", best.get("model_type", "N/A"))
with col2:
    st.metric("AUPR", f"{metrics.get('aupr', 'N/A')}" if metrics.get('aupr') is not None else "N/A")
with col3:
    st.metric("Umbral", best.get("threshold_optimized", "N/A") or "—")
st.caption(f"Run ID: {manifest.get('run_id', 'N/A')} | Creado: {manifest.get('created_at', 'N/A')}")

st.markdown("**Paths de artefactos** (informativo)")
st.code(f"Modelo: {best.get('path', 'N/A')}\nPipeline: {best.get('pipeline_path', 'N/A')}\nPreprocessor: {best.get('preprocessor_path', 'N/A')}", language="text")

# Comparativa de modelos (AUPR por modelo)
st.subheader("Comparativa de modelos")
models_tested = manifest.get("models_tested", [])
best_model_type = best.get("model_type")
df_comp = pd.DataFrame(models_tested) if models_tested else pd.DataFrame()
if not df_comp.empty and "aupr" in df_comp.columns:
    df_comp = df_comp.sort_values("aupr", ascending=True)
    df_comp["es_mejor"] = df_comp["model_type"] == best_model_type
    fig_comp = px.bar(
        df_comp,
        x="aupr",
        y="model_type",
        orientation="h",
        color="es_mejor",
        color_discrete_map={True: "#2e7d32", False: "#78909c"},
        title="AUPR por modelo (verde = modelo elegido)",
    )
    fig_comp.update_layout(showlegend=False)
    st.plotly_chart(fig_comp, use_container_width=True)
    if best_model_type:
        st.caption(f"Modelo elegido: **{best_model_type}**")
else:
    st.caption("El manifest no incluye `models_tested` con AUPR.")

# Gráfico de importancia de variables (desde pipeline o desde manifest)
st.subheader("Importancia de variables")
df_imp = None
# 1) Intentar desde manifest (feature_importances guardados)
imp_list = (best.get("feature_importances") or manifest.get("feature_importances") or [])
if isinstance(imp_list, list) and len(imp_list) > 0:
    if isinstance(imp_list[0], dict):
        df_imp = pd.DataFrame(imp_list)
        if "variable" in df_imp.columns and "importancia" in df_imp.columns:
            df_imp = df_imp.nlargest(15, "importancia").sort_values("importancia", ascending=True)
        else:
            df_imp = None
    elif isinstance(imp_list[0], (int, float)):
        names = manifest.get("feature_columns", [])
        if len(names) != len(imp_list):
            names = [f"X{i}" for i in range(len(imp_list))]
        df_imp = pd.DataFrame({"variable": names, "importancia": imp_list}).nlargest(15, "importancia").sort_values("importancia", ascending=True)
# 2) Si no hay en manifest, intentar desde pipeline/preprocessor
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
                    feature_names = manifest.get("feature_columns", [])
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
    fig = px.bar(df_imp, x="importancia", y="variable", orientation="h", title="Top variables (importancia)")
    fig.update_layout(yaxis={"categoryorder": "total ascending"}, margin=dict(l=80))
    st.plotly_chart(fig, use_container_width=True)
else:
    st.caption(
        "Para ver este gráfico ejecute una vez el script: "
        "**python scripts/export_model_artifacts.py** (desde la raíz del proyecto, con AbandonoEmpleados.csv disponible). "
        "O guarde pipeline.pkl y preprocessor.pkl en artifacts/modeling/ desde el notebook."
    )
