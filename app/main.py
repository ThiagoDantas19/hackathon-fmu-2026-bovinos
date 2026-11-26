"""Roteador do app: uma navegação com nome de gente, não de arquivo."""

from __future__ import annotations

import pathlib
import sys

_RAIZ = pathlib.Path(__file__).resolve().parents[1]
for _caminho in (_RAIZ, _RAIZ / "app"):
    if str(_caminho) not in sys.path:
        sys.path.insert(0, str(_caminho))

import streamlit as st  # noqa: E402

from ui import marca_sidebar, setup  # noqa: E402

setup("Visão geral")
marca_sidebar()

paginas = [
    st.Page(
        "visao_geral.py",
        title="Visão geral",
        icon=":material/space_dashboard:",
        url_path="visao-geral",
        default=True,
    ),
    st.Page(
        "pages/1_Balanca.py", title="Balança", icon=":material/scale:", url_path="balanca"
    ),
    st.Page(
        "pages/2_Feedback.py",
        title="Feedback",
        icon=":material/sentiment_satisfied:",
        url_path="feedback",
    ),
    st.Page(
        "pages/3_Painel.py", title="Painel", icon=":material/monitoring:", url_path="painel"
    ),
    st.Page(
        "pages/4_Mesas.py", title="Mesas", icon=":material/table_restaurant:", url_path="mesas"
    ),
    st.Page(
        "pages/5_Comandas.py",
        title="Comandas",
        icon=":material/receipt_long:",
        url_path="comandas",
    ),
]

st.navigation(paginas).run()
