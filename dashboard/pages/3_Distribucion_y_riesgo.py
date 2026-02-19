"""
Distribución y riesgo por segmento: histograma, boxplot y % alto riesgo por departamento, antigüedad y satisfacción.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from common import (
    ensure_authenticated,
    get_df_scoring,
    render_sidebar_filters,
    get_df_filtrado,
    get_umbrales_riesgo,
    SCORING_COL,
)

ensure_authenticated()
df_raw = get_df_scoring()
render_sidebar_filters(df_raw)
df = get_df_filtrado(df_raw)

st.title("Distribución y riesgo por segmento")
if df is None or df.empty or SCORING_COL not in df.columns:
    st.warning("Cargue `df_con_scoring.pkl` con columna de scoring.")
    st.stop()

th_low, th_high = get_umbrales_riesgo()
st.caption("Los umbrales de riesgo se configuran en el panel izquierdo y aplican a todos los gráficos.")

# 1. Distribución de probabilidad
st.subheader("Distribución de probabilidad de abandono")
fig = px.histogram(df, x=SCORING_COL, nbins=20, labels={SCORING_COL: "Scoring abandono"})
fig.add_vline(x=th_low, line_dash="dash", line_color="gray", annotation_text=f"Medio {th_low}")
fig.add_vline(x=th_high, line_dash="dash", line_color="orange", annotation_text=f"Alto {th_high}")
st.plotly_chart(fig, use_container_width=True)

# 2. Scoring por departamento (boxplot)
st.subheader("Scoring por departamento")
if "departamento" not in df.columns:
    st.caption("No hay columna departamento.")
else:
    orden_med = df.groupby("departamento")[SCORING_COL].median().sort_values(ascending=False).index.tolist()
    df_ord = df.copy()
    df_ord["departamento"] = pd.Categorical(df_ord["departamento"], categories=orden_med, ordered=True)
    fig2 = px.box(df_ord, x="departamento", y=SCORING_COL, points="outliers", title="Boxplot por departamento")
    st.plotly_chart(fig2, use_container_width=True)

# 3. Riesgo por departamento (% alto riesgo)
st.subheader("Riesgo por departamento (% alto riesgo)")
if "departamento" not in df.columns:
    st.caption("No hay columna departamento en los datos.")
else:
    deps = df.groupby("departamento", dropna=False)[SCORING_COL].apply(lambda s: (s >= th_high).mean() * 100).sort_values(ascending=True)
    dep_df = deps.reset_index(name="% alto riesgo")
    if len(dep_df) == 0:
        st.caption("Sin datos para mostrar (filtros muy restrictivos).")
    elif len(dep_df) == 1:
        st.caption("Seleccione más de un departamento en los filtros para comparar.")
        st.metric(dep_df["departamento"].iloc[0], f"{dep_df['% alto riesgo'].iloc[0]:.1f}%")
    else:
        fig3 = px.bar(dep_df, y="departamento", x="% alto riesgo", orientation="h", title=f"% empleados con scoring ≥ {th_high}")
        st.plotly_chart(fig3, use_container_width=True)

# 4. Riesgo por antigüedad
st.subheader("Riesgo por antigüedad en la compañía")
if "anos_compania" not in df.columns:
    st.caption("No hay columna anos_compania.")
else:
    bins = [0, 2, 5, 10, 15, 100]
    labels = ["0-2", "2-5", "5-10", "10-15", "15+"]
    df_bin = df.copy()
    df_bin["rango_anos"] = pd.cut(df_bin["anos_compania"], bins=bins, labels=labels, include_lowest=True)
    agg = df_bin.groupby("rango_anos", observed=True)[SCORING_COL].agg([("total", "count"), ("alto_riesgo", lambda x: (x >= th_high).sum())])
    agg["pct_alto"] = (agg["alto_riesgo"] / agg["total"] * 100).round(1)
    agg = agg.reset_index()
    fig4 = px.bar(agg, x="rango_anos", y="pct_alto", labels={"pct_alto": "% alto riesgo", "rango_anos": "Años en compañía"})
    st.plotly_chart(fig4, use_container_width=True)

# 5. Riesgo por satisfacción entorno
st.subheader("Riesgo por satisfacción entorno")
if "satisfaccion_entorno" not in df.columns:
    st.caption("No hay columna satisfaccion_entorno.")
else:
    orden = ["Baja", "Media", "Alta"]
    sat_vals = df["satisfaccion_entorno"].astype(str).unique().tolist()
    orden = [o for o in orden if o in sat_vals] + [x for x in sorted(sat_vals) if x not in orden]
    sat_agg = df.groupby("satisfaccion_entorno", dropna=False)[SCORING_COL].apply(lambda s: (s >= th_high).mean() * 100).reindex(orden).reset_index(name="% alto riesgo")
    sat_agg = sat_agg.dropna(subset=["% alto riesgo"])
    if len(sat_agg):
        fig5 = px.bar(sat_agg, x="satisfaccion_entorno", y="% alto riesgo", title=f"% alto riesgo por nivel de satisfacción (umbral ≥{th_high})")
        st.plotly_chart(fig5, use_container_width=True)
    else:
        st.caption("Sin datos para este segmento.")
