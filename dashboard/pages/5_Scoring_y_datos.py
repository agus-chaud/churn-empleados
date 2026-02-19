"""
Scoring y datos: tabla priorizada y descarga CSV/Excel.
"""
import numpy as np
import streamlit as st
import pandas as pd
from common import (
    ensure_authenticated,
    get_df_scoring,
    render_sidebar_filters,
    get_df_filtrado,
    get_umbrales_riesgo,
    SCORING_COL,
)


@st.cache_data(ttl=300)
def _prepare_scoring_table(_df: pd.DataFrame, th_low: float, th_high: float) -> pd.DataFrame:
    """Prepara la tabla filtrada y ordenada. Cacheada para evitar recálculo con mismos datos y umbrales."""
    if _df is None or _df.empty or SCORING_COL not in _df.columns:
        return pd.DataFrame()
    df = _df.copy()
    # Banda de forma vectorizada (más rápido que .apply por fila)
    df["banda"] = np.where(
        df[SCORING_COL] >= th_high, "Alto",
        np.where(df[SCORING_COL] >= th_low, "Medio", "Bajo"),
    )
    df = df[df[SCORING_COL] >= th_low].copy()
    columnas_relevantes = [c for c in ["departamento", "anos_compania", "satisfaccion_entorno", "anos_desde_ult_promocion"] if c in df.columns]
    columnas_show = [SCORING_COL, "banda"] + columnas_relevantes + [c for c in df.columns if c not in [SCORING_COL, "banda"] + columnas_relevantes]
    columnas_show = [c for c in columnas_show if c in df.columns]
    return df[columnas_show].sort_values(SCORING_COL, ascending=False)


def _estilo_riesgo_vectorized(df: pd.DataFrame) -> pd.DataFrame:
    """Estilo por fila de forma vectorizada (mismo resultado, más rápido que apply axis=1)."""
    colors = np.where(
        df["banda"] == "Alto", "background-color: #ffcccc",
        np.where(df["banda"] == "Medio", "background-color: #fffacd", ""),
    )
    return pd.DataFrame(
        np.tile(colors[:, np.newaxis], (1, len(df.columns))),
        index=df.index,
        columns=df.columns,
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

st.caption("Solo empleados que aún no han abandonado y con scoring mayor al umbral de riesgo medio. Los umbrales se configuran en el panel izquierdo.")

th_low, th_high = get_umbrales_riesgo()

df_show = _prepare_scoring_table(df, th_low, th_high)

if df_show.empty:
    st.info("No hay candidatos con scoring mayor al umbral de riesgo medio con los filtros actuales.")

df_styled = df_show.style.apply(_estilo_riesgo_vectorized, axis=None)
st.dataframe(df_styled, use_container_width=True, height=400)

st.download_button(
    "Descargar CSV",
    data=df_show.to_csv(index=True).encode("utf-8-sig"),
    file_name="scoring_empleados.csv",
    mime="text/csv",
)
