"""Demonstração ponta a ponta: comanda → prato → CMV → feedback."""

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
    brl,
    cabecalho,
    garantir_dados,
    grade_kpis,
    link_pagina,
    num,
    pct,
    rodape_dados_sinteticos,
    secao,
    seletor_dia,
    setup,
    vazio,
)

setup("Comandas")

from core import servico  # noqa: E402
from core.config import RAIZ  # noqa: E402
from core.db import sessao  # noqa: E402

garantir_dados()

dia = seletor_dia("dia_comandas")

with sessao() as s:
    lista = servico.listar_comandas(s, dia, limite=250)
    ind = servico.indicadores(s, dia)
    proxima = servico.proximo_numero(s)

cabecalho(
    "Demonstração",
    "Comandas ponta a ponta",
    "O número da comanda é a chave única: abertura → pesagem com foto → bebida → feedback → fechamento.",
    [f"{ind['comandas']} comandas no dia", "recepção humanizada", "caixa intocado"],
)

grade_kpis(
    [
        (str(ind["comandas"]), "Comandas no dia", f"{ind['comandas_abertas']} abertas"),
        (brl(ind["receita_total"]), "Receita", "prato + bebida", "ok"),
        (pct(ind["cmv_pct"]), "CMV médio", "prato"),
        (brl(ind["ticket_medio"]), "Ticket médio", "por comanda"),
    ]
)

st.write("")
col_esq, col_dir = st.columns([1.7, 1], gap="large")

with col_esq:
    secao("Comandas do dia", "Clique em uma linha para inspecionar na coluna ao lado.")
    if lista:
        df = pd.DataFrame(lista).rename(
            columns={
                "comanda": "comanda",
                "hora": "hora",
                "pessoas": "pessoas",
                "pratos": "pratos",
                "peso_g": "peso (g)",
                "receita": "receita",
                "cmv_pct": "CMV",
                "nota": "nota",
                "status": "status",
            }
        )
        df["nota"] = df["nota"].map(
            lambda v: "—" if v is None or pd.isna(v) else f"{float(v):.1f} ★"
        )
        st.dataframe(
            df,
            hide_index=True,
            width="stretch",
            height=420,
            column_config={
                "peso (g)": st.column_config.NumberColumn("peso", format="%.0f g"),
                "receita": st.column_config.NumberColumn("receita", format="R$ %.2f"),
                "CMV": st.column_config.NumberColumn("CMV", format="%.1f%%"),
                "nota": st.column_config.TextColumn("nota"),
            },
        )
    else:
        vazio("Nenhuma comanda neste dia", "Escolha outro dia na barra lateral.")

with col_dir:
    secao("Abrir uma comanda")
    with st.container(border=True):
        opcoes = [c["comanda"] for c in lista]
        if opcoes:
            numero = st.selectbox(
                "Número",
                opcoes,
                format_func=lambda n: (
                    f"{n} · {next(c['hora'] for c in lista if c['comanda'] == n)}"
                ),
            )
        else:
            numero = st.text_input("Número", value=proxima)

        if st.button("Nova comanda (simular abertura)", width="stretch"):
            with sessao() as s:
                nova = servico.criar_comanda(s)
            st.success(f"Comanda {nova} aberta na recepção humanizada.")
            link_pagina("pages/1_Balanca.py", label="Pesar o prato desta comanda →")
            st.stop()

with sessao() as s:
    resumo = servico.resumo_comanda(s, numero) if numero else None

if not resumo:
    vazio("Comanda não encontrada", "Escolha outro número na lista.")
    st.stop()

st.write("")
secao(
    f"Comanda {resumo['numero']}",
    "Tudo o que o sistema sabe sobre uma mesa — e por que isso só é possível com a comanda como chave.",
)

grade_kpis(
    [
        (str(resumo["pessoas"]), "Pessoas", "na mesa"),
        (resumo["aberta_em"].strftime("%H:%M"), "Aberta", "na recepção"),
        (brl(resumo["bebidas"]), "Bebidas", "lançadas no caixa"),
        ("fechada" if resumo["fechada_em"] else "aberta", "Status", "comanda"),
    ],
    colunas=4,
)

st.write("")
grade_kpis(
    [
        (brl(resumo["totais"]["receita"]), "Receita da comanda", "prato + bebida", "ok"),
        (brl(resumo["totais"]["custo"]), "Custo estimado", "tabela de custo/kg"),
        (brl(resumo["totais"]["margem"]), "Margem", "receita − custo", "ok"),
        (pct(resumo["totais"]["cmv_pct"]), "CMV da comanda", "inclui bebida a 30%"),
    ],
    colunas=4,
)

st.write("")

if not resumo["pratos"]:
    vazio("Esta comanda ainda não tem prato pesado", "Vá em Balança para registrar a pesagem.")

for prato in resumo["pratos"]:
    with st.expander(
        f"Prato das {prato['hora']} · {prato['peso_g']} g · CMV {num(prato['cmv_pct'], 1)}%",
        expanded=True,
    ):
        esq, dir_ = st.columns([1, 1.3], gap="large")
        with esq:
            caminho = RAIZ / prato["foto_path"] if prato["foto_path"] else None
            if caminho and caminho.exists():
                st.image(str(caminho), caption="Foto da balança", width="stretch")
            else:
                vazio("Foto não disponível", "Dados sintéticos do dia não guardam imagem.")
            st.caption(f"Modelo: `{prato['modelo']}`")
        with dir_:
            grade_kpis(
                [
                    (brl(prato["receita"]), "Receita", f"{prato['peso_g']} g"),
                    (brl(prato["custo"]), "Custo", "composição estimada"),
                    (brl(prato["margem"]), "Margem", "bruta"),
                    (pct(prato["mix_premium_pct"]), "Mix premium", "área do prato"),
                ],
                colunas=2,
            )

        st.write("")
        st.dataframe(
            pd.DataFrame(prato["itens"])
            .assign(percentual=lambda d: d["percentual"] * 100)
            [["rotulo", "categoria", "percentual", "peso_g", "custo"]]
            .rename(
                columns={
                    "rotulo": "item",
                    "categoria": "categoria",
                    "percentual": "área",
                    "peso_g": "peso",
                    "custo": "custo",
                }
            ),
            hide_index=True,
            width="stretch",
            column_config={
                "área": st.column_config.ProgressColumn(
                    "área", min_value=0, max_value=100, format="%.1f%%"
                ),
                "peso": st.column_config.NumberColumn("peso", format="%.0f g"),
                "custo": st.column_config.NumberColumn("custo", format="R$ %.2f"),
            },
        )

st.write("")
col_fb, col_vazio = st.columns([1.4, 1], gap="large")
with col_fb:
    secao("Feedback vinculado")
    if resumo["feedbacks"]:
        st.dataframe(
            pd.DataFrame(resumo["feedbacks"]).rename(
                columns={
                    "hora": "hora",
                    "nota_geral": "nota geral",
                    "item": "item",
                    "nota_item": "nota do item",
                    "resto": "resto",
                    "canal": "canal",
                }
            ),
            hide_index=True,
            width="stretch",
        )
    else:
        vazio("Sem avaliação ainda", "O totem/QR grava direto nesta comanda.")
    link_pagina("pages/2_Feedback.py", label="Abrir o totem de feedback →")

with col_vazio:
    secao("Por que isso importa")
    st.markdown(
        """
- A comanda liga **quanto o cliente pagou** ao **que ele comeu**.
- Com o feedback, liga também **o que ele achou**.
- É o único lugar em que mix, CMV, margem e satisfação aparecem juntos.
        """
    )

rodape_dados_sinteticos()
