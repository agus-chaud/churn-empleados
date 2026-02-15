"""
Distribución del scoring: histograma y boxplot por departamento.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from common import (
    ensure_authenticated,
    get_df_scoring,
    render_sidebar_filters,
    get_df_filtrado,
    SCORING_COL,
)

ensure_authenticated()
df_raw = get_df_scoring()
render_sidebar_filters(df_raw)
df = get_df_filtrado(df_raw)

st.title("Distribución del scoring")
if df is None or df.empty or SCORING_COL not in df.columns:
    st.warning("Cargue `df_con_scoring.pkl` con columna de scoring.")
    st.stop()

# Histograma
st.subheader("Distribución de probabilidad de abandono")
fig = px.histogram(df, x=SCORING_COL, nbins=20, labels={SCORING_COL: "Scoring abandono"})
fig.add_vline(x=0.5, line_dash="dash", line_color="orange", annotation_text="Umbral 0.5")
st.plotly_chart(fig, use_container_width=True)

# Boxplot por departamento
st.subheader("Scoring por departamento")
if "departamento" not in df.columns:
    st.caption("No hay columna departamento.")
else:
    orden_med = df.groupby("departamento")[SCORING_COL].median().sort_values(ascending=False).index.tolist()
    df_ord = df.copy()
    df_ord["departamento"] = pd.Categorical(df_ord["departamento"], categories=orden_med, ordered=True)
    fig2 = px.box(df_ord, x="departamento", y=SCORING_COL, points="outliers", title="Boxplot por departamento")
    st.plotly_chart(fig2, use_container_width=True)
