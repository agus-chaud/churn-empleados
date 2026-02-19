"""
Módulo común del dashboard: carga de manifest y datos, filtros globales en sidebar.
"""
from pathlib import Path
import json
import streamlit as st
import pandas as pd
import joblib

# Rutas: buscar artifacts/modeling desde raíz del repo o desde cwd (por si se ejecuta desde dashboard/)
BASE_DIR = Path(__file__).resolve().parent.parent
_CANDIDATE_ARTIFACTS = [
    BASE_DIR / "artifacts" / "modeling",
    Path.cwd() / "artifacts" / "modeling",
    Path.cwd().parent / "artifacts" / "modeling",
]

def _artifacts_dir():
    for d in _CANDIDATE_ARTIFACTS:
        if (d / "experiment_manifest.json").exists():
            return d
    return _CANDIDATE_ARTIFACTS[0]

ARTIFACTS_DIR = _artifacts_dir()
MANIFEST_PATH = ARTIFACTS_DIR / "experiment_manifest.json"
DF_SCORING_PATH = ARTIFACTS_DIR / "df_con_scoring.pkl"
PIPELINE_PATH = ARTIFACTS_DIR / "pipeline.pkl"
BEST_MODEL_PATH = ARTIFACTS_DIR / "best_model.pkl"

# Nombre de la columna de scoring (según plan)
SCORING_COL = "scoring_abandono"


def _load_manifest():
    if not MANIFEST_PATH.exists():
        return None
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _load_df_scoring():
    if not DF_SCORING_PATH.exists():
        return None
    try:
        return joblib.load(DF_SCORING_PATH)
    except Exception:
        return None


def _load_pipeline():
    """Carga el pipeline para feature importance. Prueba varias rutas y pipeline.pkl o best_model.pkl."""
    candidates = [
        PIPELINE_PATH, BEST_MODEL_PATH,
        Path.cwd() / "artifacts" / "modeling" / "pipeline.pkl",
        Path.cwd() / "artifacts" / "modeling" / "best_model.pkl",
        Path.cwd().parent / "artifacts" / "modeling" / "pipeline.pkl",
        Path.cwd().parent / "artifacts" / "modeling" / "best_model.pkl",
    ]
    for path in candidates:
        if path.exists():
            try:
                return joblib.load(path)
            except Exception:
                continue
    return None


@st.cache_data(ttl=300)
def get_manifest():
    return _load_manifest()


@st.cache_data(ttl=300)
def get_df_scoring():
    return _load_df_scoring()


@st.cache_resource
def get_pipeline():
    return _load_pipeline()


def _load_preprocessor():
    """Carga el preprocessor para nombres de features (mismas rutas que pipeline)."""
    for base in [ARTIFACTS_DIR, Path.cwd() / "artifacts" / "modeling", Path.cwd().parent / "artifacts" / "modeling"]:
        path = base / "preprocessor.pkl"
        if path.exists():
            try:
                return joblib.load(path)
            except Exception:
                continue
    return None


@st.cache_resource
def get_preprocessor():
    return _load_preprocessor()


def _init_session_state():
    if "filter_departamentos" not in st.session_state:
        st.session_state.filter_departamentos = []
    if "filter_banda" not in st.session_state:
        st.session_state.filter_banda = "Todos"
    if "filter_umbral_alto" not in st.session_state:
        st.session_state.filter_umbral_alto = 0.5
    if "filter_umbral_medio" not in st.session_state:
        st.session_state.filter_umbral_medio = 0.3
    if "filter_anos_min" not in st.session_state:
        st.session_state.filter_anos_min = None
    if "filter_anos_max" not in st.session_state:
        st.session_state.filter_anos_max = None
    if "filter_satisfaccion" not in st.session_state:
        st.session_state.filter_satisfaccion = []


def get_umbrales_riesgo():
    """Devuelve (umbral_medio, umbral_alto) para bandas Bajo/Medio/Alto, con medio <= alto."""
    th_medio = st.session_state.get("filter_umbral_medio", 0.3)
    th_alto = st.session_state.get("filter_umbral_alto", 0.5)
    th_low = min(th_medio, th_alto)
    th_high = max(th_medio, th_alto)
    return th_low, th_high


def render_sidebar_filters(df: pd.DataFrame | None):
    """
    Renderiza los filtros globales en el sidebar. Debe llamarse al inicio de cada página.
    Persiste valores en st.session_state.
    """
    _init_session_state()
    st.sidebar.markdown("### Filtros")
    if df is None or df.empty:
        st.sidebar.caption("Cargue datos con scoring para activar filtros.")
        return
    # Opciones desde datos
    departamentos = sorted(df["departamento"].dropna().astype(str).unique().tolist()) if "departamento" in df.columns else []
    satisfaccion_opts = sorted(df["satisfaccion_entorno"].dropna().astype(str).unique().tolist()) if "satisfaccion_entorno" in df.columns else []
    anos_compania = df["anos_compania"].dropna() if "anos_compania" in df.columns else pd.Series(dtype=float)
    anos_min_data = int(anos_compania.min()) if len(anos_compania) else 0
    anos_max_data = int(anos_compania.max()) if len(anos_compania) else 30
    if SCORING_COL not in df.columns:
        st.sidebar.caption("No hay columna de scoring en los datos.")
        return
    # Departamento (multiselect): "Todos" = lista vacía
    sel_dep = st.sidebar.multiselect(
        "Departamento",
        options=departamentos,
        default=st.session_state.filter_departamentos if st.session_state.filter_departamentos else [],
        placeholder="Todos",
    )
    st.session_state.filter_departamentos = sel_dep
    # Umbrales de riesgo (compartidos por todas las solapas)
    th_low, th_high = get_umbrales_riesgo()
    st.sidebar.slider(
        "Umbral alto riesgo (≥)",
        0.0, 1.0,
        value=float(st.session_state.filter_umbral_alto),
        step=0.05,
        key="slider_umbral_alto",
        help="Scoring ≥ este valor = Alto riesgo. Afecta KPIs y gráficos en todas las solapas.",
    )
    st.session_state.filter_umbral_alto = st.session_state.get("slider_umbral_alto", 0.5)
    st.sidebar.slider(
        "Umbral riesgo medio (≥)",
        0.0, 1.0,
        value=float(st.session_state.filter_umbral_medio),
        step=0.05,
        key="slider_umbral_medio",
        help="Scoring ≥ este valor = al menos Riesgo medio. Por debajo = Bajo. Afecta todas las solapas.",
    )
    st.session_state.filter_umbral_medio = st.session_state.get("slider_umbral_medio", 0.3)
    th_low, th_high = get_umbrales_riesgo()
    # Banda de scoring (opciones dinámicas según umbrales)
    bandas_opts = ["Todos", f"Alto riesgo (≥{th_high})", f"Riesgo medio ({th_low}–{th_high})", f"Bajo (<{th_low})"]
    idx = bandas_opts.index(st.session_state.filter_banda) if st.session_state.filter_banda in bandas_opts else 0
    banda = st.sidebar.selectbox("Banda de scoring", options=bandas_opts, index=idx)
    st.session_state.filter_banda = banda
    # Antigüedad (slider)
    rango = st.sidebar.slider(
        "Años en la compañía",
        min_value=anos_min_data,
        max_value=anos_max_data,
        value=(st.session_state.filter_anos_min if st.session_state.filter_anos_min is not None else anos_min_data,
               st.session_state.filter_anos_max if st.session_state.filter_anos_max is not None else anos_max_data),
    )
    st.session_state.filter_anos_min, st.session_state.filter_anos_max = rango[0], rango[1]
    # Satisfacción
    sel_sat = []
    if satisfaccion_opts:
        sel_sat = st.sidebar.multiselect(
            "Satisfacción entorno",
            options=satisfaccion_opts,
            default=st.session_state.filter_satisfaccion if st.session_state.filter_satisfaccion else [],
            placeholder="Todos",
        )
        st.session_state.filter_satisfaccion = sel_sat
    # Badge filtros activos
    activos = sum([
        1 if sel_dep else 0,
        1 if banda != "Todos" else 0,
        1 if (rango[0] != anos_min_data or rango[1] != anos_max_data) else 0,
        1 if (satisfaccion_opts and sel_sat) else 0,
    ])
    if activos > 0:
        st.sidebar.caption(f"Filtros activos: {activos}")


def get_df_filtrado(df: pd.DataFrame | None) -> pd.DataFrame | None:
    """
    Aplica los filtros del sidebar al DataFrame y devuelve una copia filtrada.
    Si df es None, devuelve None.
    """
    if df is None or df.empty:
        return None
    out = df.copy()
    if st.session_state.filter_departamentos and "departamento" in out.columns:
        out = out[out["departamento"].astype(str).isin(st.session_state.filter_departamentos)]
    if SCORING_COL in out.columns:
        th_low, th_high = get_umbrales_riesgo()
        banda = st.session_state.get("filter_banda", "Todos")
        if banda == f"Alto riesgo (≥{th_high})":
            out = out[out[SCORING_COL] >= th_high]
        elif banda == f"Riesgo medio ({th_low}–{th_high})":
            out = out[out[SCORING_COL].ge(th_low) & out[SCORING_COL].lt(th_high)]
        elif banda == f"Bajo (<{th_low})":
            out = out[out[SCORING_COL] < th_low]
    if "anos_compania" in out.columns:
        a_min = st.session_state.get("filter_anos_min")
        a_max = st.session_state.get("filter_anos_max")
        if a_min is not None:
            out = out[out["anos_compania"] >= a_min]
        if a_max is not None:
            out = out[out["anos_compania"] <= a_max]
    if st.session_state.get("filter_satisfaccion") and "satisfaccion_entorno" in out.columns:
        out = out[out["satisfaccion_entorno"].astype(str).isin(st.session_state.filter_satisfaccion)]
    return out


def ensure_authenticated():
    """Comprueba sesión. Si no está autenticado, muestra mensaje y detiene ejecución."""
    if not st.session_state.get("authenticated", False):
        st.warning("Debe iniciar sesión para ver el dashboard.")
        st.page_link("app.py", label="Ir a inicio")
        st.stop()
