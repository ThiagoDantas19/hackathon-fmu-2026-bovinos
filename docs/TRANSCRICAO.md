# Transcrição local (faster-whisper) — Palestra FMU Tech / Hackathon

> **Apêndice.** Este documento descreve a ferramenta usada para transcrever a palestra do cliente,
> que serviu de fonte para os requisitos. O projeto em si está no [README principal](../README.md).

Transcrição 100% offline com [faster-whisper](https://github.com/SYSTRAN/faster-whisper) (CTranslate2) na GPU (CUDA).

## Estrutura

```
.
├── .venv/                     # ambiente Python com faster-whisper, yt-dlp, cublas/cudnn
├── transcrever.py             # transcreve áudio/vídeo → .txt .srt .vtt .json
├── baixar.py                  # baixa áudio de YouTube/URLs (yt-dlp)
├── bench.py                   # mede velocidade (RTF) e VRAM de um modelo
├── midia/                     # áudios baixados
├── transcricoes/              # saídas
└── logs/
```

## Uso rápido

```powershell
# 1) baixar só o áudio de um link (opcional)
.\.venv\Scripts\python.exe baixar.py "https://www.youtube.com/watch?v=XXXX"

# 2) transcrever
.\.venv\Scripts\python.exe transcrever.py "midia\arquivo.m4a" --lang pt
```

Saídas em `transcricoes\<nome>.txt|.srt|.vtt|.json` (timestamps por segmento).

### Opções do `transcrever.py`

| Flag | Padrão | Descrição |
|---|---|---|
| `--model` | `large-v3` | `tiny`, `base`, `small`, `medium`, `large-v3` |
| `--lang` | detectar | ex.: `pt` (forçar idioma melhora precisão) |
| `--device` | `cuda` | `cuda` ou `cpu` |
| `--compute-type` | `int8_float16` (GPU) / `int8` (CPU) | quantização |
| `--beam-size` | `5` | maior = mais preciso, mais lento |
| `--no-vad` | VAD ligado | desliga o filtro de silêncio |

## Notas desta máquina

- GPU: **GTX 1650, 4 GB VRAM**
  - `large-v3` int8_float16 → ~3.8 GB em uso: **não cabe** para inferência
  - `medium` int8_float16 → ~2.0 GB: **opção usada**
- Windows: os DLLs de cuBLAS/cuDNN vêm do pip (`nvidia-cublas-cu12`, `nvidia-cudnn-cu12`);
  o `transcrever.py` registra essas pastas via `os.add_dll_directory` automaticamente.
- Não é necessário instalar FFmpeg: o faster-whisper decodifica via PyAV.
- **PyAV precisa ficar em `av==13.1.0`**: a partir do av 15 o parâmetro `metadata_errors`
  foi removido e o faster-whisper 1.2.1 quebra na decodificação.
