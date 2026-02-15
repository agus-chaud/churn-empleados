"""
Churn Empleados - Dashboard
Punto de entrada: login y redirección. Filtros globales en sidebar.
Uso local: configurar .streamlit/secrets.toml con [passwords] usuario = "valor"
Para nube: configurar secrets en Streamlit Cloud (ver README_DEPLOY.md).
"""
import os
import streamlit as st
from common import (
    get_manifest,
    get_df_scoring,
    render_sidebar_filters,
    get_df_filtrado,
    SCORING_COL,
)

st.set_page_config(
    page_title="Churn Empleados - Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


def get_credentials():
    """Obtiene credenciales desde secrets (Streamlit) o variables de entorno. Sin hardcodeo."""
    try:
        if hasattr(st, "secrets") and st.secrets.get("passwords"):
            return dict(st.secrets["passwords"])
    except Exception:
        pass
    env_user = os.environ.get("DASHBOARD_USER")
    env_pass = os.environ.get("DASHBOARD_PASSWORD")
    if env_user and env_pass:
        return {env_user: env_pass}
    return None


def check_login(username: str, password: str) -> bool:
    creds = get_credentials()
    if not creds:
        return False
    return creds.get(username) == password or creds.get(username) == str(password)


def main():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "username" not in st.session_state:
        st.session_state.username = None

    if not st.session_state.authenticated:
        creds = get_credentials()
        if not creds:
            st.error(
                "No hay credenciales configuradas. Para uso local, cree `.streamlit/secrets.toml` "
                "con:\n\n[passwords]\nusuario = \"tu_password\"\n\n"
                "O defina DASHBOARD_USER y DASHBOARD_PASSWORD en el entorno."
            )
            st.stop()
        st.title("Churn Empleados - Dashboard")
        st.markdown("Inicie sesión para continuar.")
        with st.form("login"):
            user = st.text_input("Usuario")
            pwd = st.text_input("Contraseña", type="password")
            if st.form_submit_button("Entrar"):
                if check_login(user, pwd):
                    st.session_state.authenticated = True
                    st.session_state.username = user
                    st.rerun()
                else:
                    st.error("Usuario o contraseña incorrectos.")
        st.stop()

    # Autenticado: cargar datos y mostrar sidebar en todas las vistas
    manifest = get_manifest()
    df_raw = get_df_scoring()
    render_sidebar_filters(df_raw)
    df_filtrado = get_df_filtrado(df_raw) if df_raw is not None else None

    st.sidebar.markdown("---")
    st.sidebar.caption(f"Sesión: {st.session_state.username}")
    if st.sidebar.button("Cerrar sesión"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.rerun()

    # Página de inicio (Home)
    st.title("Churn Empleados - Dashboard")
    st.markdown("Utilice el menú lateral para navegar a cada sección.")
    if manifest:
        b = manifest.get("best_model", {})
        st.info(f"Modelo activo: **{b.get('model_type', 'N/A')}**. AUPR: {b.get('metrics', {}).get('aupr', 'N/A')}")
    else:
        st.warning("No se encontró `experiment_manifest.json` en `artifacts/modeling/`.")
    if df_raw is None:
        st.warning(
            "No se encontró `df_con_scoring.pkl` en `artifacts/modeling/`. "
            "Algunas páginas (Resumen Ejecutivo, Riesgo por segmento, etc.) requieren este archivo. "
            "Genérelo desde el notebook de modelización guardando el DataFrame con scoring."
        )
    else:
        n = len(df_filtrado) if df_filtrado is not None else 0
        st.success(f"Datos cargados: **{n}** empleados (tras filtros).")


if __name__ == "__main__":
    main()
