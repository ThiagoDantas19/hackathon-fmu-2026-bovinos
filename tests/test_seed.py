"""O seed é sempre relativo a hoje: a demo não pode abrir vazia no dia seguinte."""

from __future__ import annotations

from datetime import date, datetime, time, timedelta

from sqlalchemy import func, select

from core import seed
from core.db import sessao
from core.models import Comanda


def _comandas_do_dia(dia: date) -> int:
    with sessao() as s:
        inicio = datetime.combine(dia, time(0))
        consulta = select(func.count()).select_from(Comanda).where(Comanda.aberta_em >= inicio)
        return s.scalar(consulta) or 0


def test_seed_cria_dados_de_hoje() -> None:
    seed.popular(force=True)
    assert _comandas_do_dia(date.today()) > 0


def test_seed_refaz_janela_quando_hoje_esta_vazio() -> None:
    seed.popular(force=True)

    # Simula um banco deixado aberto de um dia para o outro: tudo cai no passado.
    with sessao() as s:
        s.query(Comanda).update({Comanda.aberta_em: Comanda.aberta_em - timedelta(days=5)})
        s.commit()

    assert _comandas_do_dia(date.today()) == 0
    assert seed.popular() is True
    assert _comandas_do_dia(date.today()) > 0
