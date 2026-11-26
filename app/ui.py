"""Design system das telas (Streamlit).

Um único lugar para cores, tipografia e componentes. As páginas não escrevem CSS:
elas chamam `cabecalho`, `secao`, `kpi`, `alerta_card`, `vazio` e `grafico`.
"""

from __future__ import annotations

import pathlib
import sys

_RAIZ = pathlib.Path(__file__).resolve().parents[1]
for _caminho in (_RAIZ, _RAIZ / "app"):
    if str(_caminho) not in sys.path:
        sys.path.insert(0, str(_caminho))

import streamlit as st  # noqa: E402

PALETA = {
    "vinho": "#8B1E2D",
    "vinho_escuro": "#6E1623",
    "carvao": "#211B18",
    "creme": "#FAF7F2",
    "borda": "#E7DED2",
    "texto": "#4A413C",
    "suave": "#7A6F66",
    "verde": "#2E6B3F",
    "ambar": "#B25B12",
    "vermelho": "#B42318",
}

# Cores usadas por status de mesa e severidade de alerta.
CORES_STATUS = {
    "livre": PALETA["verde"],
    "ocupada": "#6B6259",
    "suja": PALETA["ambar"],
    "suja_critica": PALETA["vermelho"],
}

CSS = """
<style>
:root {
  --bg: #FAF7F2;
  --surface: #FFFFFF;
  --surface-2: #F4EDE3;
  --ink: #211B18;
  --ink-2: #4A413C;
  --muted: #7A6F66;
  --line: #E7DED2;
  --brand: #8B1E2D;
  --brand-700: #6E1623;
  --brand-soft: #F7E9EA;
  --ok: #2E6B3F;
  --warn: #B25B12;
  --bad: #B42318;
  --radius: 14px;
  --sombra: 0 1px 2px rgba(33, 27, 24, .05), 0 6px 18px rgba(33, 27, 24, .04);
}

html, body, [class*="css"], .stApp {
  font-family: "Segoe UI", system-ui, -apple-system, Roboto, "Helvetica Neue", Arial, sans-serif;
  color: var(--ink);
}

.stApp { background: var(--bg); }

/* ---------- layout ---------- */
.block-container { padding-top: 2.4rem; padding-bottom: 3rem; max-width: 1180px; }
header[data-testid="stHeader"] { background: transparent; }
[data-testid="stToolbar"], [data-testid="stToolbarActions"], [data-testid="stMainMenu"],
[data-testid="stStatusWidget"], #MainMenu, [data-testid="stDecoration"] {
  display: none !important;
}
[data-testid="stToolbar"] { right: 1rem; }
div[data-testid="stVerticalBlock"] { gap: .85rem; }

h1, h2, h3, h4 { color: var(--ink); letter-spacing: -.02em; font-weight: 750; }
h1 { font-size: 2.05rem; line-height: 1.15; margin-bottom: .2rem; }
h2 { font-size: 1.5rem; }
h3 { font-size: 1.08rem; margin-bottom: .1rem; }
p, li { color: var(--ink-2); }

a { color: var(--brand); }

/* ---------- sidebar ---------- */
section[data-testid="stSidebar"] {
  background: var(--surface-2);
  border-right: 1px solid var(--line);
}
section[data-testid="stSidebar"] .block-container { padding-top: 1.2rem; }
[data-testid="stSidebarNav"] { padding-top: .2rem; }
[data-testid="stSidebarNav"] ul { gap: 2px; }
[data-testid="stSidebarNav"] a {
  border-radius: 9px; padding: .38rem .6rem; color: var(--ink-2);
  font-weight: 550; transition: background .12s ease, color .12s ease;
}
[data-testid="stSidebarNav"] a span { color: inherit; }
[data-testid="stSidebarNav"] a:hover { background: #EBE1D4; color: var(--ink); }
[data-testid="stSidebarNav"] a[aria-current="page"] {
  background: var(--brand-soft); color: var(--brand-700); font-weight: 700;
  box-shadow: inset 3px 0 0 var(--brand);
}
[data-testid="stSidebarNav"] a[aria-current="page"] span { color: var(--brand-700); }

.marca { display: flex; align-items: center; gap: 10px; padding: 14px 4px 10px; }
.marca-selo {
  width: 34px; height: 34px; border-radius: 10px; flex: 0 0 34px;
  background: linear-gradient(135deg, #8B1E2D, #5E1520); color: #fff;
  display: grid; place-items: center; font-weight: 800; font-size: .95rem;
  box-shadow: 0 2px 6px rgba(139, 30, 45, .28);
}
.marca-txt { line-height: 1.15; }
.marca-txt strong { display: block; font-size: .9rem; color: var(--ink); }
.marca-txt span { font-size: .7rem; color: var(--muted); letter-spacing: .04em; text-transform: uppercase; }

.status-demo {
  display: flex; align-items: center; gap: 7px; margin: 10px 0 4px;
  font-size: .72rem; color: var(--muted);
}
.ponto { width: 7px; height: 7px; border-radius: 50%; background: var(--ok); box-shadow: 0 0 0 3px rgba(46,107,63,.12); }
.ponto.vlm { background: var(--brand); box-shadow: 0 0 0 3px rgba(139,30,45,.12); }

/* ---------- cabeçalho de página ---------- */
.eyebrow {
  font-size: .72rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase;
  color: var(--brand); margin-bottom: .35rem;
}
.page-head { margin-bottom: .4rem; }
.page-head h1 { margin: 0 0 .35rem; }
.page-head p { margin: 0; color: var(--muted); font-size: .95rem; max-width: 78ch; }
.badges { display: flex; flex-wrap: wrap; gap: 6px; margin-top: .7rem; }

.badge {
  display: inline-flex; align-items: center; gap: 5px;
  background: var(--surface); border: 1px solid var(--line); color: var(--ink-2);
  border-radius: 999px; padding: 3px 10px; font-size: .72rem; font-weight: 600;
}
.badge.ok { border-color: #CFE3D6; background: #F1F8F3; color: #26603A; }
.badge.warn { border-color: #F0D9C2; background: #FDF4EA; color: #8A4612; }
.badge.bad { border-color: #F3D3CF; background: #FDF1EF; color: #8E1D14; }
.badge.brand { border-color: #EBCFD3; background: var(--brand-soft); color: var(--brand-700); }

/* ---------- seção ---------- */
.section {
  display: flex; align-items: baseline; justify-content: space-between; gap: 12px;
  margin: .6rem 0 .1rem; padding-bottom: .45rem; border-bottom: 1px solid var(--line);
}
.section h3 { margin: 0; font-size: 1.02rem; }
.section p { margin: 0; color: var(--muted); font-size: .8rem; max-width: 62ch; }

/* ---------- cartões de KPI ---------- */
.kpi {
  background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius);
  padding: 15px 16px 13px; height: 100%; box-shadow: var(--sombra);
  position: relative; overflow: hidden;
}
.kpi::before {
  content: ""; position: absolute; inset: 0 auto 0 0; width: 3px; background: var(--brand);
  opacity: .85;
}
.kpi.ok::before { background: var(--ok); }
.kpi.warn::before { background: var(--warn); }
.kpi.bad::before { background: var(--bad); }
.kpi-valor {
  font-size: 1.62rem; font-weight: 760; color: var(--ink); line-height: 1.1;
  font-variant-numeric: tabular-nums; letter-spacing: -.02em;
}
.kpi-rotulo {
  font-size: .7rem; text-transform: uppercase; letter-spacing: .08em;
  color: var(--muted); margin-top: 6px; font-weight: 650;
}
.kpi-ajuda { font-size: .72rem; color: #8A8078; margin-top: 2px; }

/* ---------- alertas ---------- */
.alerta {
  background: var(--surface); border: 1px solid var(--line); border-left: 3px solid var(--warn);
  border-radius: 11px; padding: 11px 13px; margin-bottom: 8px; box-shadow: var(--sombra);
}
.alerta-critica { border-left-color: var(--bad); background: #FEF7F6; }
.alerta-alta { border-left-color: var(--warn); background: #FFFBF5; }
.alerta-media { border-left-color: #8A6D1F; background: #FFFDF4; }
.alerta-titulo {
  font-weight: 700; font-size: .84rem; color: var(--ink);
  display: flex; align-items: center; gap: 6px;
}
.alerta-sev {
  font-size: .62rem; letter-spacing: .08em; text-transform: uppercase;
  color: var(--muted); font-weight: 700;
}
.alerta-msg { font-size: .82rem; color: var(--ink-2); margin-top: 2px; }
.alerta-acao {
  margin-top: 7px; padding-top: 7px; border-top: 1px dashed var(--line);
  font-size: .78rem; color: var(--brand-700); font-weight: 600;
}

/* ---------- mesas ---------- */
.mesa {
  border-radius: 11px; padding: 8px 6px; text-align: center; color: #fff;
  font-weight: 700; font-size: .76rem; margin-bottom: 6px; line-height: 1.2;
  min-height: 60px; display: flex; flex-direction: column; justify-content: center;
  box-shadow: inset 0 0 0 1px rgba(255,255,255,.14);
}
.mesa small { display: block; font-weight: 500; opacity: .9; font-size: .65rem; }

.legenda { display: flex; flex-wrap: wrap; gap: 14px; margin-top: 6px; }
.legenda span { display: inline-flex; align-items: center; gap: 6px; font-size: .74rem; color: var(--muted); }
.legenda i { width: 9px; height: 9px; border-radius: 3px; display: inline-block; }

/* ---------- estado vazio ---------- */
.vazio {
  border: 1px dashed #DCCFBF; border-radius: 12px; background: #FCFAF7;
  padding: 18px; text-align: center;
}
.vazio strong { display: block; font-size: .9rem; color: var(--ink); margin-bottom: 2px; }
.vazio span { font-size: .8rem; color: var(--muted); }

/* ---------- hero ---------- */
.hero {
  position: relative; overflow: hidden;
  background: linear-gradient(120deg, #8B1E2D 0%, #5E1520 78%);
  color: #fff; border-radius: 18px; padding: 30px 32px; margin-bottom: 6px;
  box-shadow: 0 12px 30px rgba(94, 21, 32, .18);
}
.hero::after {
  content: ""; position: absolute; right: -60px; top: -70px; width: 260px; height: 260px;
  background: radial-gradient(circle, rgba(255,255,255,.16), transparent 62%);
}
.hero .eyebrow { color: #F0C9C9; }
.hero h2 { color: #fff; margin: 0 0 8px; font-size: 1.85rem; letter-spacing: -.02em; }
.hero p { color: #F2DFDB; margin: 0; max-width: 62ch; font-size: .95rem; }
.hero .badges { margin-top: 14px; }
.hero .badge {
  background: rgba(255,255,255,.10); border-color: rgba(255,255,255,.22); color: #FBEDEA;
}

/* ---------- cartões genéricos ---------- */
.painel-dor {
  background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius);
  padding: 16px; height: 100%; box-shadow: var(--sombra);
}
.painel-dor .num {
  width: 24px; height: 24px; border-radius: 8px; background: var(--brand-soft); color: var(--brand);
  display: grid; place-items: center; font-size: .78rem; font-weight: 800; margin-bottom: 8px;
}
.painel-dor strong { display: block; font-size: .92rem; color: var(--ink); margin-bottom: 4px; }
.painel-dor p { margin: 0; font-size: .8rem; color: var(--muted); line-height: 1.45; }

.atalho {
  display: block; background: var(--surface); border: 1px solid var(--line);
  border-radius: 12px; padding: 12px 14px; margin-bottom: 8px;
  box-shadow: var(--sombra);
}
.atalho strong { display: block; font-size: .86rem; color: var(--ink); }
.atalho span { font-size: .76rem; color: var(--muted); }

/* ---------- fluxo em etapas (estado vazio da balança) ---------- */
.fluxo {
  background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius);
  padding: 6px 16px; box-shadow: var(--sombra);
}
.fluxo-item {
  display: flex; gap: 11px; padding: 11px 0; border-bottom: 1px dashed var(--line);
}
.fluxo-item:last-child { border-bottom: 0; }
.fluxo-num {
  width: 22px; height: 22px; flex: 0 0 22px; border-radius: 50%;
  background: var(--brand-soft); color: var(--brand-700);
  display: grid; place-items: center; font-size: .72rem; font-weight: 800;
}
.fluxo-item strong { display: block; font-size: .85rem; color: var(--ink); }
.fluxo-item span { font-size: .79rem; color: var(--muted); }

/* ---------- passos (feedback) ---------- */
.passos { display: flex; gap: 6px; justify-content: center; margin: 6px 0 4px; }
.passo { width: 26px; height: 4px; border-radius: 999px; background: #E3D8CA; }
.passo.on { background: var(--brand); }

/* ---------- widgets ---------- */
.stButton > button {
  border-radius: 10px; border: 1px solid var(--line); background: var(--surface);
  color: var(--ink); font-weight: 600; transition: all .12s ease; box-shadow: none;
}
.stButton > button:hover {
  border-color: var(--brand); color: var(--brand-700); background: #FFFDFC;
}
.stButton > button[kind="primary"] {
  background: var(--brand); border-color: var(--brand); color: #fff;
}
.stButton > button[kind="primary"]:hover {
  background: var(--brand-700); border-color: var(--brand-700); color: #fff;
}
/* O rótulo do botão é um <p>: sem isso o texto herda a cor escura e some no vinho. */
.stButton > button[kind="primary"] p,
.stButton > button[kind="primary"] span,
.stButton > button[data-testid="stBaseButton-primary"] p,
.stButton > button[data-testid="stBaseButton-primary"] span {
  color: #fff !important;
}

/* Atalhos de página como cartões clicáveis */
div[data-testid="stPageLink"], .stPageLink { width: 100% !important; }
a[data-testid="stPageLink-NavLink"] {
  display: flex !important; align-items: center; gap: 8px; width: 100% !important;
  background: var(--surface); border: 1px solid var(--line); border-radius: 12px;
  padding: 12px 14px; margin-bottom: 8px; box-shadow: var(--sombra);
  transition: border-color .12s ease;
}
a[data-testid="stPageLink-NavLink"]:hover { border-color: var(--brand); }
a[data-testid="stPageLink-NavLink"] p { font-weight: 650; color: var(--ink); font-size: .87rem; }
a[data-testid="stPageLink-NavLink"]:hover p { color: var(--brand-700); }

/* Botão-atalho: parece uma linha de menu, não um botão de ação. */
.stButton > button p { white-space: normal; }
[data-testid="stFormSubmitButton"] button { border-radius: 10px; }

div[data-baseweb="input"] > div, div[data-baseweb="select"] > div,
div[data-baseweb="textarea"] > div {
  border-radius: 10px; border-color: var(--line); background: var(--surface);
}
div[data-baseweb="input"] > div:focus-within,
div[data-baseweb="select"] > div:focus-within {
  border-color: var(--brand); box-shadow: 0 0 0 3px rgba(139, 30, 45, .10);
}
[data-testid="stNumberInput"] button { border-radius: 8px; }

div[data-testid="stExpander"] {
  border: 1px solid var(--line); border-radius: 12px; background: var(--surface);
  box-shadow: var(--sombra); overflow: hidden;
}
div[data-testid="stExpander"] summary { font-weight: 650; font-size: .88rem; }

div[data-testid="stDataFrame"] { border: 1px solid var(--line); border-radius: 12px; overflow: hidden; }

div[data-testid="stMetric"] {
  background: var(--surface); border: 1px solid var(--line); border-radius: 12px;
  padding: 10px 12px; box-shadow: var(--sombra);
}
div[data-testid="stMetric"] label { color: var(--muted); font-size: .72rem; }
div[data-testid="stMetricValue"] { font-size: 1.25rem; font-variant-numeric: tabular-nums; }

div[data-testid="stProgress"] > div > div { background: var(--brand); }

hr { border-color: var(--line); }

.rodape {
  color: var(--muted); font-size: .74rem; margin-top: 26px; padding-top: 12px;
  border-top: 1px solid var(--line);
}

/* ---------- celular (totem/QR) ---------- */
@media (max-width: 640px) {
  .block-container { padding-top: 1.2rem; padding-left: 1rem; padding-right: 1rem; }
  .hero { padding: 22px 20px; border-radius: 14px; }
  .hero h2 { font-size: 1.45rem; }
  h1 { font-size: 1.6rem; }
  .kpi-valor { font-size: 1.35rem; }
  .kpi { padding: 12px 13px; }
}
</style>
"""


# --------------------------------------------------------------------------- #
# Ambiente
# --------------------------------------------------------------------------- #
_CONFIGURADO = False


def setup(titulo: str, layout: str = "wide") -> None:
    """Configura a página e aplica o CSS do projeto (uma vez por processo)."""
    global _CONFIGURADO
    if not _CONFIGURADO:
        st.set_page_config(
            page_title=f"{titulo} · Bovinu's",
            page_icon="🍖",
            layout=layout,
            initial_sidebar_state="expanded",
        )
        st.markdown(CSS, unsafe_allow_html=True)
        _CONFIGURADO = True
    # O CSS entra sempre: o st.navigation limpa o corpo do roteador ao rodar a página.
    st.markdown(CSS, unsafe_allow_html=True)


def marca_sidebar() -> None:
    """Cartão do projeto no rodapé da barra lateral (chamado só pelo roteador)."""
    modo, classe = _modo_visao()
    st.sidebar.markdown(
        f'<div class="marca">'
        f'<div class="marca-selo">B</div>'
        f'<div class="marca-txt"><strong>Bovinu\'s</strong>'
        f"<span>Inteligência operacional</span></div></div>"
        f'<div class="status-demo"><i class="ponto {classe}"></i> {modo} · demo offline</div>',
        unsafe_allow_html=True,
    )


def _modo_visao() -> tuple[str, str]:
    """Texto e classe do indicador de modo, sem quebrar se o core não importar."""
    try:
        from core.config import settings

        if settings.tem_vlm and settings.vision_provider != "heuristica":
            return "VLM ativo com heurística de reserva", "vlm"
    except Exception:  # noqa: BLE001 - o setup nunca pode falhar
        pass
    return "Modo heurística (offline)", ""


@st.cache_resource(show_spinner=False)
def _preparar_ambiente() -> bool:
    """Inicializa banco, seed sintético e imagens de demo (uma vez por processo)."""
    from core.db import init_db
    from core.demo import gerar_todas
    from core.seed import popular
    from core.vision import limpar_fotos_antigas

    init_db()
    popular(force=False)
    gerar_todas()
    limpar_fotos_antigas()  # retenção LGPD: fotos de prato com mais de 7 dias
    return True


def garantir_dados() -> None:
    """Garante o ambiente e mantém o "ao vivo" das mesas fresco a cada rerun."""
    _preparar_ambiente()
    from core.seed import popular

    popular(force=False)  # idempotente: só reancora as mesas se o "ao vivo" esfriou


# --------------------------------------------------------------------------- #
# Cabeçalhos e seções
# --------------------------------------------------------------------------- #
def cabecalho(
    sobretitulo: str,
    titulo: str,
    descricao: str = "",
    meta: list[str] | None = None,
) -> None:
    """Cabeçalho padrão de página: sobretítulo, título, descrição e etiquetas."""
    etiquetas = "".join(f'<span class="badge">{m}</span>' for m in (meta or []))
    st.markdown(
        f'<div class="page-head"><div class="eyebrow">{sobretitulo}</div>'
        f"<h1>{titulo}</h1>"
        + (f"<p>{descricao}</p>" if descricao else "")
        + (f'<div class="badges">{etiquetas}</div>' if etiquetas else "")
        + "</div>",
        unsafe_allow_html=True,
    )


def secao(titulo: str, descricao: str = "") -> None:
    """Título de seção com linha de base, no lugar de `st.subheader` + `st.divider`."""
    st.markdown(
        f'<div class="section"><h3>{titulo}</h3>'
        + (f"<p>{descricao}</p>" if descricao else "")
        + "</div>",
        unsafe_allow_html=True,
    )


def hero(titulo: str, subtitulo: str, etiquetas: list[str] | None = None) -> None:
    """Bloco de destaque da home, com gradiente da marca."""
    tags = "".join(f'<span class="badge">{e}</span>' for e in (etiquetas or []))
    st.markdown(
        f'<div class="hero"><div class="eyebrow">Bovinu\'s · Rua Augusta</div>'
        f"<h2>{titulo}</h2><p>{subtitulo}</p>"
        + (f'<div class="badges">{tags}</div>' if tags else "")
        + "</div>",
        unsafe_allow_html=True,
    )


# --------------------------------------------------------------------------- #
# Números
# --------------------------------------------------------------------------- #
def brl(valor: float | None) -> str:
    if valor is None:
        return "—"
    texto = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


def num(valor: float | int | None, casas: int = 0) -> str:
    if valor is None:
        return "—"
    texto = f"{valor:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return texto


def pct(valor: float | None, casas: int = 1) -> str:
    return "—" if valor is None else f"{num(valor, casas)}%"


def kpi(valor: str, rotulo: str, ajuda: str = "", tom: str = "") -> None:
    """Cartão de indicador. `tom`: "", "ok", "warn" ou "bad"."""
    classe = f" {tom}" if tom else ""
    st.markdown(
        f'<div class="kpi{classe}"><div class="kpi-valor">{valor}</div>'
        f'<div class="kpi-rotulo">{rotulo}</div>'
        f'<div class="kpi-ajuda">{ajuda}</div></div>',
        unsafe_allow_html=True,
    )


def grade_kpis(itens: list[tuple], colunas: int = 4) -> None:
    """Grade de KPIs. Cada item é `(valor, rótulo, ajuda)` ou `(valor, rótulo, ajuda, tom)`."""
    for inicio in range(0, len(itens), colunas):
        bloco = itens[inicio : inicio + colunas]
        cols = st.columns(len(bloco), gap="small")
        for col, item in zip(cols, bloco, strict=False):
            valor, rotulo, ajuda = item[0], item[1], item[2]
            tom = item[3] if len(item) > 3 else ""
            with col:
                kpi(valor, rotulo, ajuda, tom)


# --------------------------------------------------------------------------- #
# Cartões
# --------------------------------------------------------------------------- #
def alerta_card(alerta: dict) -> None:
    """Cartão de alerta. Se o alerta trouxer `acao`, ela aparece destacada."""
    acao = alerta.get("acao")
    st.markdown(
        f'<div class="alerta alerta-{alerta["severidade"]}">'
        f'<div class="alerta-titulo">{alerta["tipo"].replace("_", " ").title()}'
        f'<span class="alerta-sev">{alerta["severidade"]}</span></div>'
        f'<div class="alerta-msg">{alerta["mensagem"]}</div>'
        + (f'<div class="alerta-acao">{acao}</div>' if acao else "")
        + "</div>",
        unsafe_allow_html=True,
    )


def mesa_card(mesa: dict, cor: str) -> None:
    """Card de mesa para o mapa do salão."""
    st.markdown(
        f'<div class="mesa" style="background:{cor}">'
        f'Mesa {mesa["id"]}<small>{mesa["lugares"]} lugares</small>'
        f'<small>{mesa["status"]}</small></div>',
        unsafe_allow_html=True,
    )


def vazio(titulo: str, texto: str = "") -> None:
    """Estado vazio, no lugar de um `st.info` solto."""
    st.markdown(
        f'<div class="vazio"><strong>{titulo}</strong>'
        + (f"<span>{texto}</span>" if texto else "")
        + "</div>",
        unsafe_allow_html=True,
    )


def legenda(itens: list[tuple[str, str]]) -> None:
    """Legenda de cores: lista de `(cor, rótulo)`."""
    partes = "".join(
        f'<span><i style="background:{cor}"></i>{rotulo}</span>' for cor, rotulo in itens
    )
    st.markdown(f'<div class="legenda">{partes}</div>', unsafe_allow_html=True)


def passos(atual: int, total: int = 3) -> None:
    """Indicador de etapas do totem de feedback."""
    barras = "".join(
        f'<span class="passo{" on" if indice <= atual else ""}"></span>'
        for indice in range(1, total + 1)
    )
    st.markdown(f'<div class="passos">{barras}</div>', unsafe_allow_html=True)


def atalho_pagina(rotulo: str, caminho: str, icone: str | None = None) -> None:
    """Botão-atalho que troca de página (largura cheia, alinhado à esquerda)."""
    if st.button(rotulo, icon=icone, width="stretch", key=f"ir_{caminho}"):
        st.switch_page(caminho)


def rodape_dados_sinteticos() -> None:
    st.markdown(
        '<div class="rodape">Dados sintéticos para demonstração, calibrados com os números '
        "informados pela operação (600 clientes/dia, pico 12h10–13h20, R$ 119/kg). "
        "Nenhum dado real de cliente foi usado.</div>",
        unsafe_allow_html=True,
    )


# --------------------------------------------------------------------------- #
# Gráficos
# --------------------------------------------------------------------------- #
def grafico(fig, altura: int | None = None, legenda: bool = False) -> None:
    """Aplica o tema visual do projeto e renderiza o gráfico Plotly."""
    if altura:
        fig.update_layout(height=altura)
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Segoe UI, system-ui, sans-serif", size=12, color="#4A413C"),
        margin=dict(l=6, r=6, t=14, b=6),
        showlegend=legenda,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0, bgcolor="rgba(0,0,0,0)"),
        hoverlabel=dict(font_family="Segoe UI, system-ui, sans-serif"),
    )
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor="#E7DED2", ticks="outside")
    fig.update_yaxes(gridcolor="#EFE7DC", zeroline=False, linecolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})


# --------------------------------------------------------------------------- #
# Navegação
# --------------------------------------------------------------------------- #
def link_pagina(caminho: str, label: str, icone: str | None = None) -> None:
    """Link interno entre páginas.

    No app normal (multipágina por pasta) o `st.page_link` resolve o caminho.
    Em contextos de teste/preview ele não encontra a página, então caímos para
    um texto simples em vez de quebrar a tela.
    """
    try:
        st.page_link(caminho, label=label, icon=icone)
    except Exception:  # noqa: BLE001 - fallback visual, nunca derrubar a página
        st.caption(f"→ {label}")


def seletor_dia(chave: str = "dia") -> "object":
    from datetime import date, timedelta

    opcoes = [date.today() - timedelta(days=d) for d in (2, 1, 0)]
    rotulos = {d: d.strftime("%d/%m/%Y") + (" (hoje)" if d == date.today() else "") for d in opcoes}
    return st.sidebar.selectbox(
        "Dia de operação",
        options=opcoes,
        index=len(opcoes) - 1,
        format_func=lambda d: rotulos[d],
        key=chave,
    )
