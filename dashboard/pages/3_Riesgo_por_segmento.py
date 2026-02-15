"""
Riesgo por segmento: departamento, antigüedad, satisfacción.
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

st.title("Riesgo por segmento")
if df is None or df.empty or SCORING_COL not in df.columns:
    st.warning("Cargue `df_con_scoring.pkl` con columna de scoring para ver los gráficos.")
    st.stop()

# Riesgo por departamento
st.subheader("Riesgo por departamento (% alto riesgo)")
if "departamento" not in df.columns:
    st.caption("No hay columna departamento en los datos.")
else:
    deps = df.groupby("departamento", dropna=False)[SCORING_COL].apply(lambda s: (s >= 0.5).mean() * 100).sort_values(ascending=True)
    dep_df = deps.reset_index(name="% alto riesgo")
    if len(dep_df) == 0:
        st.caption("Sin datos para mostrar (filtros muy restrictivos).")
    elif len(dep_df) == 1:
        st.caption("Seleccione más de un departamento en los filtros para comparar.")
        st.metric(dep_df["departamento"].iloc[0], f"{dep_df['% alto riesgo'].iloc[0]:.1f}%")
    else:
        fig = px.bar(dep_df, y="departamento", x="% alto riesgo", orientation="h", title="% empleados con scoring ≥ 0.5")
        st.plotly_chart(fig, use_container_width=True)

# Riesgo por antigüedad (bins)
st.subheader("Riesgo por antigüedad en la compañía")
if "anos_compania" not in df.columns:
    st.caption("No hay columna anos_compania.")
else:
    bins = [0, 2, 5, 10, 15, 100]
    labels = ["0-2", "2-5", "5-10", "10-15", "15+"]
    df_bin = df.copy()
    df_bin["rango_anos"] = pd.cut(df_bin["anos_compania"], bins=bins, labels=labels, include_lowest=True)
    agg = df_bin.groupby("rango_anos", observed=True)[SCORING_COL].agg([("total", "count"), ("alto_riesgo", lambda x: (x >= 0.5).sum())])
    agg["pct_alto"] = (agg["alto_riesgo"] / agg["total"] * 100).round(1)
    agg = agg.reset_index()
    fig2 = px.bar(agg, x="rango_anos", y="pct_alto", labels={"pct_alto": "% alto riesgo", "rango_anos": "Años en compañía"})
    st.plotly_chart(fig2, use_container_width=True)

# Riesgo por satisfacción
st.subheader("Riesgo por satisfacción entorno")
if "satisfaccion_entorno" not in df.columns:
    st.caption("No hay columna satisfaccion_entorno.")
else:
    orden = ["Baja", "Media", "Alta"]
    sat_vals = df["satisfaccion_entorno"].astype(str).unique().tolist()
    orden = [o for o in orden if o in sat_vals] + [x for x in sorted(sat_vals) if x not in orden]
    sat_agg = df.groupby("satisfaccion_entorno", dropna=False)[SCORING_COL].apply(lambda s: (s >= 0.5).mean() * 100).reindex(orden).reset_index(name="% alto riesgo")
    sat_agg = sat_agg.dropna(subset=["% alto riesgo"])
    if len(sat_agg):
        fig3 = px.bar(sat_agg, x="satisfaccion_entorno", y="% alto riesgo", title="% alto riesgo por nivel de satisfacción")
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.caption("Sin datos para este segmento.")
