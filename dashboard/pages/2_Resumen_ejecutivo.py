"""
Resumen Ejecutivo: KPIs, gráfico de bandas y costos de intervención.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from common import (
    ensure_authenticated,
    get_manifest,
    get_df_scoring,
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

# KPIs
st.subheader("KPIs")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total empleados", total)
c2.metric("Alto riesgo (≥0.5)", alto)
c3.metric("Riesgo medio (0.3–0.5)", medio)
c4.metric("% en alto riesgo", f"{pct_alto:.1f}%")

# Gráfico de bandas
st.subheader("Distribución por banda de riesgo")
df_bandas = pd.DataFrame({
    "Banda": ["Bajo (<0.3)", "Riesgo medio (0.3–0.5)", "Alto (≥0.5)"],
    "Empleados": [bajo, medio, alto],
})
fig = px.bar(df_bandas, x="Banda", y="Empleados", color="Empleados", color_continuous_scale="Blues")
st.plotly_chart(fig, use_container_width=True)

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
