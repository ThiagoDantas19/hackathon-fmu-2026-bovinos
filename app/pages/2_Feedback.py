"""Totem/QR de feedback: 1-clique + Pergunta do Dia, vinculado à comanda."""

from __future__ import annotations

import pathlib
import sys

_RAIZ = pathlib.Path(__file__).resolve().parents[2]
for _caminho in (_RAIZ, _RAIZ / "app"):
    if str(_caminho) not in sys.path:
        sys.path.insert(0, str(_caminho))

import streamlit as st  # noqa: E402

from ui import garantir_dados, passos, pct, setup  # noqa: E402

setup("Feedback", layout="centered")

from core import servico  # noqa: E402
from core.db import sessao  # noqa: E402

garantir_dados()

# O totem é estreito de propósito: mesma tela no tablet da saída e no celular.
st.markdown(
    """
<style>
.block-container { max-width: 580px; }
div[data-testid="stButton"] > button { min-height: 84px; font-size: 1.18rem; font-weight: 650; }
div[data-testid="stButton"] > button p { font-size: 1.18rem; font-weight: 650; }
.totem-topo { text-align: center; margin-bottom: .4rem; }
.totem-topo h1 { font-size: 2rem; margin-bottom: .25rem; }
.totem-topo p { color: #7A6F66; margin: 0; }
.barra { margin: 10px 0; }
.barra span { font-size: .8rem; color: #4A413C; display: block; margin-bottom: 4px; }
.barra .trilho { background: #EFE7DC; border-radius: 999px; height: 8px; overflow: hidden; }
.barra .trilho i { display: block; height: 100%; background: #8B1E2D; border-radius: 999px; }
</style>
""",
    unsafe_allow_html=True,
)

with sessao() as s:
    sugestao = servico.proximo_numero(s)
    pergunta = servico.pergunta_do_dia(s)

st.markdown(
    '<div class="totem-topo"><h1>Como foi seu almoço?</h1>'
    "<p>Um toque. Dois segundos. Sem cadastro, sem login.</p></div>",
    unsafe_allow_html=True,
)

comanda = st.text_input(
    "Número da comanda (está impresso no cartão)",
    value=st.session_state.get("fb_comanda", sugestao),
)
st.session_state["fb_comanda"] = comanda
st.caption("No totem real este campo vem do código de barras. No QR, vem na URL.")

for chave in ("fb_nota", "fb_item_nota", "fb_resto"):
    st.session_state.setdefault(chave, None)
st.session_state.setdefault("fb_ok", None)

NOTAS = [
    (1, "😞", "Ruim"),
    (2, "🙁", "Fraco"),
    (3, "🙂", "Bom"),
    (4, "😄", "Ótimo"),
]

# --------------------------------------------------------------------------- #
# Tela de agradecimento
# --------------------------------------------------------------------------- #
if st.session_state["fb_ok"]:
    passos(3)
    st.success("Obrigado! Sua avaliação foi registrada na sua comanda.")
    st.balloons()
    with sessao() as s:
        resumo = servico.resumo_comanda(s, st.session_state["fb_ok"]["comanda"])
    if resumo and resumo["pratos"]:
        st.markdown("#### O que tinha no seu prato")
        for item in resumo["pratos"][0]["itens"]:
            largura = max(1.5, min(100.0, item["percentual"] * 100))
            rotulo = item["rotulo"] or item["categoria"]
            st.markdown(
                f'<div class="barra"><span>{rotulo} — {pct(item["percentual"] * 100, 0)}</span>'
                f'<div class="trilho"><i style="width:{largura}%"></i></div></div>',
                unsafe_allow_html=True,
            )
        st.caption(
            "Esse retorno ajuda a cozinha a decidir o que continua no buffet. "
            "Nenhum dado pessoal é coletado."
        )
    if st.button("Avaliar outra comanda", width="stretch"):
        st.session_state.update(
            {"fb_nota": None, "fb_item_nota": None, "fb_resto": None, "fb_ok": None}
        )
        st.rerun()
    st.stop()

# --------------------------------------------------------------------------- #
# Passo 1 · nota geral
# --------------------------------------------------------------------------- #
if st.session_state["fb_nota"] is None:
    passos(1)
    st.markdown("### 1 · De 0 a 4, como foi o almoço?")
    for col, (valor, emoji, rotulo) in zip(st.columns(4, gap="small"), NOTAS, strict=False):
        with col:
            if st.button(f"{emoji}\n\n{rotulo}", key=f"nota_{valor}", width="stretch"):
                st.session_state["fb_nota"] = valor
                st.rerun()
    st.caption("As carinhas bastam: nada de estrela, nada de texto obrigatório.")
    st.stop()

escolhida = next(n for n in NOTAS if n[0] == st.session_state["fb_nota"])
passos(1)
st.markdown(f"### Sua nota: {escolhida[1]} {escolhida[2]}")
st.progress(st.session_state["fb_nota"] / 4)

# --------------------------------------------------------------------------- #
# Passo 2 · pergunta do dia
# --------------------------------------------------------------------------- #
if st.session_state["fb_item_nota"] is None:
    passos(2)
    st.markdown(f"### 2 · E o **{pergunta['item']}** de hoje?")
    st.caption(f"Pergunta do dia escolhida automaticamente: {pergunta['motivo']}.")
    for col, (valor, emoji, rotulo) in zip(st.columns(4, gap="small"), NOTAS, strict=False):
        with col:
            if st.button(f"{emoji}\n\n{rotulo}", key=f"item_{valor}", width="stretch"):
                st.session_state["fb_item_nota"] = valor
                st.rerun()
    if st.button("Não comi esse item", width="stretch"):
        st.session_state["fb_item_nota"] = 0
        st.rerun()
    st.stop()

# --------------------------------------------------------------------------- #
# Passo 3 · resto
# --------------------------------------------------------------------------- #
if st.session_state["fb_resto"] is None:
    passos(3)
    st.markdown("### 3 · Sobrou comida no prato?")
    opcoes = [("nada", "Nada"), ("pouco", "Um pouco"), ("muito", "Muito")]
    for col, (valor, rotulo) in zip(st.columns(3, gap="small"), opcoes, strict=False):
        with col:
            if st.button(rotulo, key=f"resto_{valor}", width="stretch"):
                st.session_state["fb_resto"] = valor
                st.rerun()
    st.caption("O 'sobrou?' é o único jeito de estimar desperdício sem pesar o prato de volta.")
    st.stop()

# --------------------------------------------------------------------------- #
# Envio
# --------------------------------------------------------------------------- #
passos(4, total=4)
comentario = st.text_area("Quer deixar um comentário? (opcional)", max_chars=280)

if st.button("Enviar avaliação", type="primary", width="stretch"):
    nota_item = st.session_state["fb_item_nota"] or None
    with sessao() as s:
        servico.criar_comanda(s, numero=comanda)
        servico.registrar_feedback(
            s,
            comanda_numero=comanda,
            nota_geral=st.session_state["fb_nota"],
            item=pergunta["item"] if nota_item else None,
            nota_item=nota_item,
            resto=st.session_state["fb_resto"],
            comentario=comentario or None,
            canal="totem",
        )
    st.session_state["fb_ok"] = {"comanda": comanda}
    st.rerun()

with st.expander("O que acontece com esse dado"):
    st.markdown(
        """
- A nota entra no **ranking de itens** do painel gerencial.
- A pergunta do dia é escolhida sozinha: o item com **menor nota** dos últimos 3 dias.
- O "sobrou?" alimenta a estimativa de **resto ingesto** — que hoje é zero.
- O número da comanda liga o feedback ao **mix do prato** e ao **CMV**. É esse cruzamento
  que responde "esta lasanha vale a pena?".
        """
    )
