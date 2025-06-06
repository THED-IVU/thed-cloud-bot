# utils_ui.py
import streamlit as st
from config_state import sidebar_config
from runtime_config import get_runtime_config  # ✅ Correctement séparé

def init_page(titre="📊 Dashboard"):
    st.set_page_config(layout="wide")
    st.title(titre)
    sidebar_config()
    return get_runtime_config()
