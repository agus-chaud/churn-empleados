"""
Scoring y datos: tabla priorizada y descarga CSV/Excel.
"""
import streamlit as st
import pandas as pd
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

# Solo empleados que aún no abandonaron: objetivo de técnicas de retención
if df is not None and not df.empty and "abandono" in df.columns:
    df = df[df["abandono"].isin([0, "No"])].copy()

st.title("Scoring y datos")
if df is None or df.empty:
    st.warning("Cargue `df_con_scoring.pkl` en artifacts/modeling/.")
    st.stop()

if SCORING_COL not in df.columns:
    st.error("No hay columna de scoring en los datos.")
    st.stop()

st.caption("Solo se muestran empleados que aún no han abandonado (candidatos a retención).")

umbral = st.slider(
    "Umbral de intervención (scoring ≥ este valor = Alto riesgo)",
    0.0, 1.0, 0.5, 0.05,
    help="Empleados con scoring por encima de este valor se consideran de alto riesgo."
)
umbral_medio = 0.3  # Límite entre Bajo y Medio

def banda(s, th_alto, th_medio):
    if s >= th_alto:
        return "Alto"
    if s >= th_medio:
        return "Medio"
    return "Bajo"

df_show = df.copy()
df_show["banda"] = df_show[SCORING_COL].apply(lambda x: banda(x, umbral, umbral_medio))
columnas_relevantes = [c for c in ["departamento", "anos_compania", "satisfaccion_entorno", "anos_desde_ult_promocion"] if c in df_show.columns]
columnas_show = [SCORING_COL, "banda"] + columnas_relevantes + [c for c in df_show.columns if c not in [SCORING_COL, "banda"] + columnas_relevantes]
columnas_show = [c for c in columnas_show if c in df_show.columns]
df_show = df_show[columnas_show].sort_values(SCORING_COL, ascending=False)

st.dataframe(df_show, use_container_width=True, height=400)

st.download_button(
    "Descargar CSV",
    data=df_show.to_csv(index=True).encode("utf-8-sig"),
    file_name="scoring_empleados.csv",
    mime="text/csv",
)
