# Correções do deck e da narração

O projeto já foi ajustado. Abaixo, **só** o que muda no slide e no vídeo.
Onde há "trocar por", é texto pronto para colar.

## 1. Nome da marca (slide 1, cabeçalho e rodapé)

| Está | Trocar por |
|---|---|
| Bovinus | **Bovinu's** |
| Bovinus · Inteligência Operacional | **Bovinu's · Inteligência Operacional** |
| Bovinus Grill & Beer | **Bovinu's Grill & Beer** |

São 6 ocorrências. Atenção ao apóstrofo: `Bovinu's`, com "u".

## 2. Slide "A solução" — card Balança

| Está | Trocar por |
|---|---|
| Foto do prato, composição e CMV, com correção em 2 segundos. | **Foto automática ao estabilizar o peso: composição, CMV e vínculo com a comanda sem digitação. O operador só corrige quando a confiança fica abaixo de 0,55.** |

Motivo: na balança real a foto dispara sozinha (peso estável por 300 ms). Dizer
"operador fotografa" contradiz o produto e perde o melhor argumento de não invasividade.

## 3. Slide "O problema" — linha Qualidade e desperdício

| Está | Trocar por |
|---|---|
| nota por item, resto e reposições de cuba por dia | **nota por item, resto declarado no feedback e reposições de cuba por dia** |

Motivo: o resto hoje vem do cliente respondendo "sobrou?". Medir resto por imagem é roadmap.

## 4. Slide "Integração" — caminho A

| Está | Trocar por |
|---|---|
| A · Conector de borda — implementado | **A · Conector de borda — protótipo implementado** |

Motivo: o fluxo comanda + peso + foto existe; o gatilho físico da balança ainda não.

## 5. Slide "Filas e mesas"

| Está | Trocar por |
|---|---|
| espera estimada por estação e fila na escada | **espera estimada por zona (entrada, churrasqueira, caixa) e fila na escada** |

Motivo: o código mede três zonas. As seis estações da planta são evolução, não entrega.

## 6. Slide "Números"

| Está | Trocar por |
|---|---|
| 100 mesas × 5 lugares × 2 min ÷ 37 min | **90 mesas × 5 lugares (450 lugares) × 2 min ÷ 37 min** |
| ~27 clientes/dia | **~24 clientes/dia** |
| 3 câmeras USB, suportes e iluminação | **3 câmeras USB (uma por balança), suportes e iluminação; salão usa as Intelbras existentes** |

Conta: 450 lugares × 2 min ÷ 37 min = 24,3. O cliente informou 90 mesas e ~450 lugares,
não 100 mesas.

## 7. Slide "LGPD"

| Está | Trocar por |
|---|---|
| Fotos guardadas por 7 dias | **Fotos apagadas automaticamente após 7 dias** |

Motivo: a limpeza automática agora existe no código (`RETENCAO_DIAS`), roda no app e na API.

## 8. Slide "API"

| Está | Trocar por |
|---|---|
| GET `/api/v1/fila e /alertas` | **GET `/api/v1/fila`** e **GET `/api/v1/alertas`** (duas rotas) |
| — | **GET `/api/v1/comandas/{numero}`** (comanda ponta a ponta) |

## 9. Slide "Demonstração"

| Está | Trocar por |
|---|---|
| 3 dias de operação simulada, com 180 comandas por dia | **3 dias de operação simulada, com 180 comandas por dia (~600 clientes, mesas compartilhadas)** |

## 10. Três frases que mudam na narração do vídeo

1. **Balança:** "A câmera dispara sozinha quando o peso estabiliza. O operador não digita nada —
   só entra se a confiança ficar abaixo de 55%."
2. **Mesas:** "Dois minutos a menos de mesa suja são **24 clientes** a mais no almoço."
3. **Fecho:** "**Bovinu's**: vocês já têm os clientes, as câmeras e as balanças."

## O que já está pronto no código para gravar

- A tela **Balança** abre com **"Modo balança automática"** ligado: escolher o prato já dispara
  a análise, sem botão "Analisar". É o comportamento que o slide passa a descrever.
- Os três pratos de demonstração mostram **"CMV detectado"** sozinhos (antes exigiam clique).
- A base de demonstração se **refaz sozinha** se o banco tiver apenas dias anteriores — a demo
  não abre vazia no dia da entrega.
