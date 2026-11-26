"""Mesas e cubas: giro do salão e a métrica de reposição que o cliente pediu."""

from __future__ import annotations

import pathlib
import sys

_RAIZ = pathlib.Path(__file__).resolve().parents[2]
for _caminho in (_RAIZ, _RAIZ / "app"):
    if str(_caminho) not in sys.path:
        sys.path.insert(0, str(_caminho))

import pandas as pd  # noqa: E402
import streamlit as st  # noqa: E402

from ui import (  # noqa: E402
    CORES_STATUS,
    cabecalho,
    garantir_dados,
    grade_kpis,
    legenda,
    mesa_card,
    num,
    secao,
    setup,
    vazio,
)

setup("Mesas")

from core import servico  # noqa: E402
from core.db import sessao  # noqa: E402
from core.fluxo import META_LIMPEZA_MIN, cor_mesa  # noqa: E402

garantir_dados()

with sessao() as s:
    mesas = servico.mesas_com_tempo(s)
    ranking = servico.ranking_higienizacao(s, limite=5)
    cubas = servico.reposicoes_do_dia(s)

ocupadas = [m for m in mesas if m["status"] == "ocupada"]
livres = [m for m in mesas if m["status"] == "livre"]
sujas = [m for m in mesas if m["status"] == "suja"]
media_livre = sum(m["minutos_livre"] for m in sujas) / len(sujas) if sujas else 0.0

cabecalho(
    "Salão",
    "Mesas, higienização e giro",
    "A câmera detecta que a mesa esvaziou; o garçom confirma a higienização. "
    "O que era 'olhômetro' vira tempo em minutos e prioridade.",
    ["detecção por ROI", f"meta de limpeza: {META_LIMPEZA_MIN:.0f} min", "sem reconhecer rostos"],
)

grade_kpis(
    [
        (str(len(ocupadas)), "Ocupadas", "detecção por ROI"),
        (str(len(livres)), "Livres e limpas", "prontas para sentar", "ok"),
        (
            str(len(sujas)),
            "Aguardando limpeza",
            f"meta: até {META_LIMPEZA_MIN:.0f} min",
            "bad" if sujas and max(m["minutos_livre"] for m in sujas) > META_LIMPEZA_MIN else "",
        ),
        (f"{num(media_livre, 1)} min", "Tempo médio suja", "mesa livre sem higienizar"),
    ]
)

st.write("")
col_esq, col_dir = st.columns([1, 1.35], gap="large")

with col_esq:
    secao("Prioridade de higienização", "Quem o garçom deve atender primeiro.")
    if not ranking:
        vazio("Nenhuma mesa pendente", "Todo o salão está limpo ou ocupado.")

    for mesa in ranking:
        cor = cor_mesa(mesa["minutos_livre"])
        with st.container(border=True):
            linha1, linha2 = st.columns([2.2, 1], vertical_alignment="center")
            with linha1:
                st.markdown(
                    f'<div style="border-left:3px solid {cor};padding-left:10px">'
                    f"<strong>Mesa {mesa['id']}</strong> · {mesa['lugares']} lugares · "
                    f"{mesa['nivel']}<br>"
                    f'<span style="font-size:.78rem;color:#7A6F66">livre há '
                    f"<strong>{num(mesa['minutos_livre'], 0)} min</strong> · "
                    f"prioridade {num(mesa['prioridade'], 0)}</span></div>",
                    unsafe_allow_html=True,
                )
            with linha2:
                if st.button("Higienizada", key=f"hig_{mesa['id']}", width="stretch"):
                    with sessao() as s:
                        servico.mudar_status_mesa(s, mesa["id"], "livre")
                    st.rerun()

    st.write("")
    with st.expander("Simular movimento no salão"):
        with sessao() as s:
            mapa = {f"Mesa {m['id']}": m["id"] for m in mesas}
        escolha = st.selectbox("Mesa", list(mapa))
        b1, b2 = st.columns(2)
        if b1.button("Cliente sentou", width="stretch"):
            with sessao() as s:
                servico.mudar_status_mesa(s, mapa[escolha], "ocupada")
            st.rerun()
        if b2.button("Cliente saiu", width="stretch"):
            with sessao() as s:
                servico.mudar_status_mesa(s, mapa[escolha], "suja")
            st.rerun()

with col_dir:
    secao("Mapa do salão", "40 mesas visíveis pelas câmeras — o salão tem 90.")
    for nivel in ("principal", "superior"):
        do_nivel = [m for m in mesas if m["nivel"] == nivel]
        st.markdown(
            f'<div style="font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;'
            f'color:#7A6F66;margin:6px 0 8px">Salão {nivel} · {len(do_nivel)} mesas</div>',
            unsafe_allow_html=True,
        )
        for inicio in range(0, len(do_nivel), 8):
            bloco = do_nivel[inicio : inicio + 8]
            cols = st.columns(8, gap="small")
            for col, mesa in zip(cols, bloco, strict=False):
                with col:
                    if mesa["status"] == "ocupada":
                        cor = CORES_STATUS["ocupada"]
                    elif mesa["status"] == "livre":
                        cor = CORES_STATUS["livre"]
                    else:
                        cor = cor_mesa(mesa["minutos_livre"])
                    mesa_card(mesa, cor)

    legenda(
        [
            (CORES_STATUS["livre"], "livre e limpa"),
            (CORES_STATUS["ocupada"], "ocupada"),
            ("#B25B12", "suja há mais de 3 min"),
            ("#B42318", "suja há mais de 6 min"),
        ]
    )

st.write("")
secao(
    "Cozinha · reposições de cuba",
    "A métrica que a operação disse ser a mais valiosa (\"se o arroz foi reposto cinco vezes...\").",
)

with sessao() as s:
    registros = servico.reposicoes_do_dia(s)

col_a, col_b = st.columns([1, 1.2], gap="large")

with col_a:
    itens = [
        "arroz branco",
        "feijão",
        "picanha",
        "costela",
        "lasanha",
        "salada de grão-de-bico",
        "farofa",
        "legumes",
    ]
    item = st.selectbox("Item reposto", itens)
    capacidade = st.number_input("Capacidade da cuba (kg)", 1.0, 30.0, 10.0, step=0.5)
    if st.button("+1 reposição", type="primary", width="stretch"):
        with sessao() as s:
            servico.registrar_reposicao(s, item, capacidade)
        st.rerun()
    st.caption("Um toque por reposição. O kg estimado é a ponte para o consumo real.")

with col_b:
    if registros:
        st.dataframe(
            pd.DataFrame(registros)[["item", "reposicoes", "capacidade_kg", "kg_estimado"]].rename(
                columns={
                    "item": "item",
                    "reposicoes": "reposições",
                    "capacidade_kg": "kg/cuba",
                    "kg_estimado": "kg estimado",
                }
            ),
            hide_index=True,
            width="stretch",
            column_config={
                "reposições": st.column_config.NumberColumn("reposições", format="%d×"),
                "kg/cuba": st.column_config.NumberColumn("kg/cuba", format="%.1f kg"),
                "kg estimado": st.column_config.NumberColumn("kg estimado", format="%.1f kg"),
            },
        )
        st.caption("Kg estimado = reposições × capacidade da cuba.")
    else:
        vazio("Nenhuma reposição hoje", "Registre a primeira para abrir a série.")
