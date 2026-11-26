"""O seed é sempre relativo a hoje: a demo não pode abrir vazia no dia seguinte."""

from __future__ import annotations

from datetime import date, datetime, time, timedelta

from sqlalchemy import func, select

from core import seed
from core.db import sessao
from core.models import Comanda, Mesa


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


def test_reancorar_mesas_nao_deixa_tempo_negativo() -> None:
    """Demo aberta por horas não pode mostrar 'suja há 400 min' nem tempo negativo."""
    seed.popular(force=True)

    # Envelhece os carimbos das mesas como se o processo estivesse aberto há 6 h.
    with sessao() as s:
        for mesa in s.scalars(select(Mesa)):
            if mesa.livre_desde:
                mesa.livre_desde -= timedelta(hours=6)
            if mesa.ocupada_desde:
                mesa.ocupada_desde -= timedelta(hours=6)
        s.commit()

    with sessao() as s:
        assert seed.reancorar_mesas(s) is True

    agora = datetime.now()
    with sessao() as s:
        tempos = [
            (agora - carimbo).total_seconds() / 60
            for mesa in s.scalars(select(Mesa))
            if (carimbo := (mesa.livre_desde or mesa.ocupada_desde)) is not None
        ]
    assert tempos, "o seed precisa de mesas com carimbo"
    assert all(tempo >= 0 for tempo in tempos), "nenhum tempo pode ficar no futuro"
    assert max(tempos) <= 25, "o 'ao vivo' precisa voltar para a faixa plausível"
