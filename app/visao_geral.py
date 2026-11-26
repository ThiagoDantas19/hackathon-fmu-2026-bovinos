"""Visão geral: a porta de entrada da demonstração."""

from __future__ import annotations

import pathlib
import sys

_RAIZ = pathlib.Path(__file__).resolve().parents[1]
for _caminho in (_RAIZ, _RAIZ / "app"):
    if str(_caminho) not in sys.path:
        sys.path.insert(0, str(_caminho))

import streamlit as st  # noqa: E402

from ui import (  # noqa: E402
    alerta_card,
    atalho_pagina,
    brl,
    garantir_dados,
    grade_kpis,
    hero,
    num,
    pct,
    rodape_dados_sinteticos,
    secao,
    setup,
    vazio,
)

setup("Visão geral")

from core import servico  # noqa: E402
from core.db import sessao  # noqa: E402

garantir_dados()

with sessao() as s:
    ind = servico.indicadores(s)
    alertas = servico.alertas_atuais(s)

hero(
    "Vocês já veem o prato. Falta transformar isso em número.",
    "Uma camada não invasiva sobre o sistema de comandas: mix do prato, CMV, filas, "
    "mesas e satisfação, tudo ligado pelo número da comanda.",
    ["não invasivo", "comanda como chave única", "reuso das câmeras Intelbras", "recepção preservada"],
)

grade_kpis(
    [
        (str(ind["comandas"]), "Comandas hoje", f"{ind['comandas_abertas']} ainda abertas"),
        (pct(ind["cmv_pct"]), "CMV médio", "custo do prato ÷ receita", "ok" if 20 <= ind["cmv_pct"] <= 35 else "warn"),
        (brl(ind["margem"]), "Margem estimada", "prato + bebida", "ok"),
        (brl(ind["ticket_medio"]), "Ticket médio", "por comanda"),
        (pct(ind["mix_premium_pct"]), "Mix premium", "% da área em carne premium"),
        (f"{num(ind['csat'], 1)}/4", "Satisfação", f"{ind['feedbacks']} feedbacks", "ok" if ind["csat"] >= 3 else "warn"),
        (
            f"{num(ind['espera_p95_min'], 1)} min",
            "Espera p95",
            "churrasqueira · meta 2,5",
            "bad" if ind["espera_p95_min"] > 3.5 else ("warn" if ind["espera_p95_min"] > 2.5 else "ok"),
        ),
        (
            f"{num(ind['mesa_suja_p95_min'], 0)} min",
            "Mesa suja p95",
            f"{ind['mesas_sujas']} aguardando",
            "warn" if ind["mesas_sujas"] else "ok",
        ),
    ],
    colunas=4,
)

st.write("")

secao("As quatro dores, resolvidas na mesma chave", "Cada dor tem uma métrica que hoje não existe.")

DORES = [
    ("1", "Mix do prato e CMV", "Composição por categoria, custo/kg, CMV e margem por comanda — a dor nº 1 do cliente."),
    ("2", "Filas e tempo de espera", "Espera por zona, fila na escada e p95 contra a meta de 2,5 min."),
    ("3", "Limpeza e giro de mesa", "Cronômetro por mesa e ranking de prioridade para o garçom."),
    ("4", "Qualidade e desperdício", "Nota por item, resto declarado e reposições de cuba por dia."),
]
for col, (numero, titulo, texto) in zip(st.columns(4, gap="small"), DORES, strict=False):
    with col:
        st.markdown(
            f'<div class="painel-dor"><div class="num">{numero}</div>'
            f"<strong>{titulo}</strong><p>{texto}</p></div>",
            unsafe_allow_html=True,
        )

st.write("")

esquerda, direita = st.columns([1.25, 1], gap="large")

with esquerda:
    secao("Alertas ativos", "O que o gerente precisa ver antes de abrir o salão.")
    if not alertas:
        vazio("Nenhum alerta agora", "A operação está dentro das metas do dia.")
    for alerta in alertas[:5]:
        alerta_card(alerta)

with direita:
    secao("Comece por aqui")
    st.markdown(
        "<style>"
        'div[data-testid="stButton"] > button { justify-content: flex-start; '
        "padding: 10px 14px; min-height: 48px; }"
        'div[data-testid="stButton"] > button p { font-weight: 600; }'
        "</style>",
        unsafe_allow_html=True,
    )
    for rotulo, caminho, icone in [
        ("Balança — a foto do prato vira CMV", "pages/1_Balanca.py", ":material/scale:"),
        ("Feedback — totem de um toque", "pages/2_Feedback.py", ":material/sentiment_satisfied:"),
        ("Painel — mix × satisfação e margem", "pages/3_Painel.py", ":material/monitoring:"),
        ("Mesas — prioridade de higienização", "pages/4_Mesas.py", ":material/table_restaurant:"),
        ("Comandas — a demonstração ponta a ponta", "pages/5_Comandas.py", ":material/receipt_long:"),
    ]:
        atalho_pagina(rotulo, caminho, icone)

rodape_dados_sinteticos()
