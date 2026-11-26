"""Painel gerencial: o cruzamento que hoje não existe."""

from __future__ import annotations

import pathlib
import sys

_RAIZ = pathlib.Path(__file__).resolve().parents[2]
for _caminho in (_RAIZ, _RAIZ / "app"):
    if str(_caminho) not in sys.path:
        sys.path.insert(0, str(_caminho))

import pandas as pd  # noqa: E402
import plotly.express as px  # noqa: E402
import streamlit as st  # noqa: E402
from sqlalchemy import select  # noqa: E402

from ui import (  # noqa: E402
    PALETA,
    alerta_card,
    brl,
    cabecalho,
    garantir_dados,
    grade_kpis,
    grafico,
    num,
    pct,
    rodape_dados_sinteticos,
    secao,
    seletor_dia,
    setup,
    vazio,
)

setup("Painel")

from core import servico  # noqa: E402
from core.db import sessao  # noqa: E402
from core.models import CategoriaCusto  # noqa: E402

garantir_dados()

dia = seletor_dia()

with sessao() as s:
    ind = servico.indicadores(s, dia)
    pontos = servico.mix_satisfacao(s, dia)
    por_hora = servico.cmv_por_hora(s, dia)
    ranking = servico.ranking_itens(s, dias=3)
    cubas = servico.reposicoes_do_dia(s, dia)
    fila = servico.fila_do_dia(s, dia)
    sujas = servico.ranking_higienizacao(s, limite=6)
    alertas = servico.alertas_atuais(s, dia)

cabecalho(
    "Painel gerencial",
    f"Operação de {dia.strftime('%d/%m/%Y')}",
    "Dados sintéticos calibrados com a operação real. O objetivo é provar o cruzamento, "
    "não prever o faturamento.",
    [f"{ind['comandas']} comandas", "pico 12h10–13h20", "meta de espera 2,5 min"],
)

grade_kpis(
    [
        (str(ind["comandas"]), "Comandas", f"{ind['comandas_abertas']} abertas"),
        (pct(ind["cmv_pct"]), "CMV médio", "prato, sem bebida", "ok" if 20 <= ind["cmv_pct"] <= 35 else "warn"),
        (brl(ind["margem"]), "Margem do dia", "prato + bebida", "ok"),
        (brl(ind["ticket_medio"]), "Ticket médio", "por comanda"),
        (pct(ind["mix_premium_pct"]), "Mix premium", "área do prato"),
        (f"{num(ind['csat'], 1)}/4", "Satisfação", f"{ind['feedbacks']} respostas", "ok" if ind["csat"] >= 3 else "warn"),
        (pct(ind["taxa_feedback_pct"]), "Taxa de resposta", "do total de comandas"),
        (
            f"{num(ind['espera_p95_min'], 1)} min",
            "Espera p95",
            "churrasqueira",
            "bad" if ind["espera_p95_min"] > 3.5 else ("warn" if ind["espera_p95_min"] > 2.5 else "ok"),
        ),
    ]
)

st.write("")
secao("CMV ao longo do serviço", "Onde a margem escorrega dentro do próprio almoço.")

col_esq, col_dir = st.columns(2, gap="large")

with col_esq:
    if por_hora:
        df = pd.DataFrame(por_hora)
        fig = px.bar(
            df,
            x="hora",
            y="cmv_pct",
            text="pratos",
            labels={"cmv_pct": "CMV (%)", "hora": "", "pratos": "pratos"},
            color_discrete_sequence=[PALETA["vinho"]],
        )
        fig.add_hrect(y0=28, y1=32, fillcolor=PALETA["verde"], opacity=0.10, line_width=0)
        fig.update_traces(texttemplate="%{text}", textposition="outside", cliponaxis=False)
        grafico(fig, altura=320)
        st.caption("Faixa verde: 28–32%, referência de food cost para self-service.")
    else:
        vazio("Sem pesagens neste dia", "Escolha outro dia na barra lateral.")

with col_dir:
    if por_hora:
        df = pd.DataFrame(por_hora)
        fig = px.area(
            df,
            x="hora",
            y="mix_premium_pct",
            labels={"mix_premium_pct": "Mix premium (%)", "hora": ""},
            color_discrete_sequence=[PALETA["ambar"]],
        )
        grafico(fig, altura=320)
        st.caption("Quando o mix premium sobe, o CMV sobe junto — e a margem cai.")
    else:
        vazio("Sem dados de mix", "As pesagens do dia alimentam este gráfico.")

st.write("")
secao("Mix × satisfação", "A pergunta que a operação nunca conseguiu responder.")

col_a, col_b = st.columns([1.2, 1], gap="large")

with col_a:
    if pontos:
        df = pd.DataFrame(pontos)
        fig = px.scatter(
            df,
            x="mix_premium_pct",
            y="nota",
            size="peso_g",
            color="cmv_pct",
            color_continuous_scale=["#E8D5A8", PALETA["ambar"], PALETA["vinho"]],
            hover_data=["comanda", "peso_g"],
            labels={
                "mix_premium_pct": "Mix premium (%)",
                "nota": "Nota (1–4)",
                "cmv_pct": "CMV (%)",
                "peso_g": "peso (g)",
            },
        )
        fig.update_yaxes(dtick=1, range=[0.5, 4.5])
        grafico(fig, altura=360)
        st.caption(
            "Cada ponto é uma comanda com feedback e prato fotografado. "
            "Prato caro deixa o cliente mais feliz? Agora dá para responder."
        )
    else:
        vazio("Sem comandas com prato + feedback", "O cruzamento precisa dos dois lados.")

with col_b:
    if ranking:
        df = pd.DataFrame(ranking[:8])
        fig = px.bar(
            df,
            x="nota_media",
            y="item",
            orientation="h",
            text="avaliacoes",
            color="nota_media",
            color_continuous_scale=[PALETA["vermelho"], PALETA["ambar"], PALETA["verde"]],
            range_color=[1, 4],
        )
        fig.update_traces(texttemplate="%{text} aval.", textposition="outside", cliponaxis=False)
        fig.update_layout(coloraxis_showscale=False, xaxis_title="Nota média (1–4)", yaxis_title="")
        grafico(fig, altura=360)
        st.caption("Itens com pior aceitação: candidatos a sair do buffet.")
    else:
        vazio("Sem feedback de item ainda", "A pergunta do dia alimenta este ranking.")

st.write("")
secao("Fila e reposições", "Duas métricas que hoje só existem no 'olhômetro'.")

col_c, col_d = st.columns(2, gap="large")

with col_c:
    if fila:
        df = pd.DataFrame(fila)
        df["hora"] = pd.to_datetime(df["hora"])
        fig = px.line(
            df,
            x="hora",
            y="espera_min",
            color="zona",
            color_discrete_map={
                "entrada": PALETA["vinho"],
                "churrasqueira": PALETA["ambar"],
                "caixa": PALETA["verde"],
            },
            labels={"espera_min": "Espera estimada (min)", "hora": "", "zona": "Zona"},
        )
        fig.update_xaxes(tickformat="%H:%M")
        fig.add_hline(
            y=2.5,
            line_dash="dot",
            line_color=PALETA["carvao"],
            annotation_text="meta 2,5 min",
            annotation_position="top left",
        )
        grafico(fig, altura=340, legenda=True)
        st.caption("Lei de Little: espera = pessoas ÷ chegadas por minuto.")
    else:
        vazio("Sem eventos de fila", "A câmera da linha do buffet gera estes eventos.")

with col_d:
    if cubas:
        df = pd.DataFrame(cubas)
        fig = px.bar(
            df,
            x="reposicoes",
            y="item",
            orientation="h",
            text="reposicoes",
            color="reposicoes",
            color_continuous_scale=["#EFE6DA", PALETA["ambar"], PALETA["vinho"]],
        )
        fig.update_traces(textposition="outside", cliponaxis=False)
        fig.update_layout(coloraxis_showscale=False, xaxis_title="Reposições no dia", yaxis_title="")
        grafico(fig, altura=340)
        st.caption(
            "A métrica que o cliente chamou de mais valiosa: \"se o arroz foi reposto cinco "
            "vezes, já é um dado bastante relevante\"."
        )
    else:
        vazio("Nenhuma reposição registrada", "Um toque por cuba reposta já alimenta a série.")

st.write("")
col_e, col_f = st.columns([1.05, 1], gap="large")

with col_e:
    secao("Alertas ativos")
    if not alertas:
        vazio("Operação dentro das metas", "Nenhum alerta no momento.")
    for alerta in alertas:
        alerta_card(alerta)
    st.write("")
    if st.button("Registrar alertas no histórico", width="stretch"):
        with sessao() as s:
            novos = servico.registrar_alertas(s, alertas)
        st.success(f"{novos} alerta(s) registrado(s). Cooldown de 15 min por tipo.")

with col_f:
    secao("Mesas aguardando higienização")
    if sujas:
        tabela = pd.DataFrame(sujas).rename(
            columns={
                "id": "mesa",
                "nivel": "nível",
                "lugares": "lugares",
                "minutos_livre": "min livre",
                "prioridade": "prioridade",
            }
        )[["mesa", "nível", "lugares", "min livre", "prioridade"]]
        st.dataframe(
            tabela,
            hide_index=True,
            width="stretch",
            column_config={
                "min livre": st.column_config.NumberColumn("min livre", format="%.0f min"),
                "prioridade": st.column_config.ProgressColumn(
                    "prioridade", min_value=0, max_value=100, format="%.0f"
                ),
            },
        )
        st.caption("Prioridade = tempo livre × (lugares/4) × peso do nível da mesa.")
    else:
        vazio("Nenhuma mesa pendente", "Todas as mesas livres já foram higienizadas.")

st.write("")
secao(
    "Simulador de cenário",
    "Move o mix premium e mostra o efeito na margem — a conversa que o dado permite ter com a cozinha.",
)

with sessao() as s:
    casos = {c.categoria: c.custo_kg for c in s.scalars(select(CategoriaCusto))}
custo_premium = casos.get("carne_premium", 79.0)
custo_base = casos.get("acompanhamento", 12.0)

deslocamento = st.slider(
    "Deslocamento do mix: sai de acompanhamento, entra em carne premium (p.p.)",
    min_value=-10,
    max_value=10,
    value=0,
    step=1,
)
peso_medio_kg = (ind["peso_medio_g"] or 550) / 1000
delta_por_prato = (deslocamento / 100) * (custo_premium - custo_base) * peso_medio_kg
impacto_dia = -delta_por_prato * ind["comandas"]

with st.container(border=True):
    c1, c2, c3 = st.columns(3)
    c1.metric("Impacto por prato", brl(-delta_por_prato))
    c2.metric("Impacto no dia", brl(impacto_dia), f"{ind['comandas']} comandas")
    c3.metric("Projeção mensal (22 dias)", brl(impacto_dia * 22))
    st.caption(
        f"Premissa: prato médio de {peso_medio_kg * 1000:.0f} g; diferença de custo de "
        f"{brl(custo_premium)} para {brl(custo_base)} por kg. "
        "Oportunidade estimada, não retorno garantido."
    )

rodape_dados_sinteticos()
