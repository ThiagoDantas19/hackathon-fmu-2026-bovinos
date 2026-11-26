"""Retenção LGPD: fotos de prato mais antigas que o prazo configurado são apagadas."""

from __future__ import annotations

import os
import time

from core.vision.pipeline import limpar_fotos_antigas


def _criar_foto(pasta, nome: str, idade_dias: float) -> "os.PathLike":
    caminho = pasta / nome
    caminho.write_bytes(b"fake-webp")
    antigo = time.time() - idade_dias * 86400
    os.utime(caminho, (antigo, antigo))
    return caminho


def test_remove_antiga_e_preserva_recente(tmp_path, monkeypatch):
    monkeypatch.setattr("core.vision.pipeline.FOTOS_DIR", tmp_path)

    antiga = _criar_foto(tmp_path, "antiga.webp", 10)
    recente = _criar_foto(tmp_path, "recente.webp", 1)

    removidas = limpar_fotos_antigas(7)

    assert removidas == 1
    assert not antiga.exists()
    assert recente.exists()


def test_prazo_zero_limpa_quase_tudo(tmp_path, monkeypatch):
    monkeypatch.setattr("core.vision.pipeline.FOTOS_DIR", tmp_path)
    antiga = _criar_foto(tmp_path, "velha.webp", 2)

    assert limpar_fotos_antigas(0) == 1
    assert not antiga.exists()


def test_pasta_sem_fotos_nao_quebra(tmp_path, monkeypatch):
    monkeypatch.setattr("core.vision.pipeline.FOTOS_DIR", tmp_path / "inexistente")
    assert limpar_fotos_antigas(7) == 0
