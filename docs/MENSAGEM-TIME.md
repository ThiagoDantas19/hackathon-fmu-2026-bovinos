# Mensagem para o time

Pessoal, subi o esqueleto do projeto inteiro e ele **já roda de ponta a ponta** com dados de demonstração. Não é mockup: é código rodando.

## Como ver

```powershell
.\run.ps1
```

Abre em `http://localhost:8501`. Cria a venv, instala tudo, gera os dados de exemplo e sobe o painel. Não precisa de chave de API nem de internet.

## O que está pronto

- **Balança (foto → peso por alimento → CMV)**: sobe a foto do prato, o sistema identifica os alimentos, divide o peso por densidade (churrasco pesa mais que salada) e calcula o custo real daquela comanda. Se tiver chave de IA, usa visão de modelo; sem chave, cai num classificador OpenCV offline — a demo nunca trava.
- **Painel do gestor**: CMV e margem por dia, espera p95 na fila, mesas sujas, nota por prato, alertas priorizados (ex.: lasanha com 2,05/4 e churrasqueira com 4,7 min de espera).
- **Fila e mesas**: contagem de pessoas por câmera (YOLO pré-treinado, sem treinar modelo próprio) → tempo de espera e ocupação.
- **API em FastAPI** com `POST /webhooks/comanda`, pronta para o conector da balança.
- **Dados**: SQLite no demo, Postgres/Supabase só trocando `DATABASE_URL`. Mesmo `core/` usado pelo painel e pela API.
- **31 testes passando**, verificação de ambiente (`scripts/verificar.py`) e dados de 3 dias já semeados (540 comandas).

## O que falta (e está dividido)

- **Balança/Vision**: trocar os 3 pratos sintéticos por 8–10 fotos reais e rodar o protocolo de 20 pratos para publicar o MAPE medido.
- **Painel/Front**: polir as telas e gravar o vídeo de 3 min.
- **Infra/Integração**: vídeo anotado da fila e deploy (Render/Streamlit Cloud).

## Decisões travadas (para não retrabalhar)

1. Não mexemos no PDV nem no caixa. O número da comanda é a chave única.
2. Nada de treinar modelo de comida em 48h — IA genérica + heurística + fallback manual.
3. Escopo é só os 4 problemas: mix/CMV, fila, mesa, qualidade/desperdício. Cardápio, compras, estoque e fidelidade estão fora.

Documentação completa em `docs/` — comecem por `PLANO-TECNICO.md` e `README-MVP.md`.
