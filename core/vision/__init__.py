"""Visão computacional do prato: VLM primário, heurística como rede de segurança."""

from core.vision.pipeline import (
    analisar_bytes,
    analisar_manual,
    limpar_fotos_antigas,
    persistir_pesagem,
    salvar_foto,
)

__all__ = [
    "analisar_bytes",
    "analisar_manual",
    "limpar_fotos_antigas",
    "persistir_pesagem",
    "salvar_foto",
]
