# Roteiro do vídeo (≤ 3 min) — Bovinu's · Inteligência Operacional

**Regra de ouro:** o vídeo é a única coisa que a banca vê antes de decidir os 20 finalistas. Ele precisa provar que funciona, não explicar que funcionaria.

**Formato:** gravação de tela + narração em off (voz única, masculina ou feminina, ritmo rápido). Legendas queimadas (muita gente assiste no mudo).
**Resolução:** 1080p, 30 fps. Cortes secos, sem transição.
**Música:** base instrumental baixa (-24 dB) só para não ficar seco.

---

## Estrutura por tempo

### 0:00–0:15 · O gancho (sem logo, sem "olá")
> "Este prato custou 32 reais de comida e foi vendido por 65. Só que o restaurante não sabe disso — porque a balança só registra o peso."

Tela: foto de um prato + overlay de segmentação aparecendo item por item + números surgindo (R$ 32 → R$ 65 → margem).

### 0:15–0:40 · O problema, com os números deles
> "O Bovinu's da Augusta serve 600 pessoas por dia, 119 reais o quilo, e tem 70 minutos de pico. Eles sabem o peso do prato. Não sabem se foram 600 gramas de picanha ou de arroz. Não sabem o tempo de fila na churrasqueira. Não sabem quanto tempo uma mesa fica suja. E o cliente executivo tem 40 minutos para almoçar."

Tela: 4 cards das dores com os números (4 min de fila vs. 2,5 de meta · 90 mesas · 450 lugares · R$119/kg).

### 0:40–1:30 · A solução funcionando (o coração)
**Cena 1 — Balança (25 s).** Operador bipa a comanda, prato vai na balança, foto é tirada.
> "A câmera na balança captura o prato. A IA identifica a composição e devolve JSON. Com o peso real e a tabela de custo, o CMV sai na hora."

Tela: JSON aparecendo ao lado da foto + tela do operador com os chips de correção.

**Cena 2 — Margem por prato (15 s).** Três pratos lado a lado: premium, equilibrado, carboidrato. CMV de cada um.
> "Mesmo peso, margens completamente diferentes. É esse número que eles nunca tiveram."

**Cena 3 — Feedback (12 s).** Celular: 4 carinhas → Pergunta do Dia → obrigado.
> "Na saída, um toque. Quatro carinhas e uma pergunta sobre o prato do dia."

**Cena 4 — Painel (18 s).** Abrir o painel: mix × satisfação, ranking de itens, alerta piscando.
> "E aqui o cruzamento que ninguém consegue fazer hoje: a lasanha tem nota 2,1 e custa 12% do prato. Ou conserta, ou sai do buffet."

### 1:30–2:05 · Filas e mesas (o "uau" de visão computacional)
> "Reaproveitamos as câmeras Intelbras que já existem. Nenhum treino novo: detecção de pessoas e regiões de interesse."

Tela: vídeo anotado com caixas e contagem na churrasqueira; gráfico de espera; alerta "fila na escada — risco de desistência".
> "Com a lei de Little, o tamanho da fila vira tempo de espera. A meta deles é 2,5 minutos: isso significa no máximo 21 pessoas na fila. Aos 34, vira os 4 minutos que eles mediram."

Cena mesas (12 s): planta com mesas mudando de cor, cronômetro subindo, alerta priorizando a mesa de 8 lugares.

### 2:05–2:30 · Arquitetura e não invasividade
> "Tudo isso sem tocar no sistema de comandas. O número da comanda é a chave. A recepção continua humana, o caixa continua igual. A integração é plugável: conector de borda hoje, API ou webhook quando o fornecedor abrir."

Tela: diagrama de arquitetura animado em 6 segundos, destacando "PaaS" vs. "SaaS existente".

### 2:30–2:50 · Impacto
> "Cada ponto percentual de mix premium é 200 reais por dia. Dois minutos a menos de mesa no pico são 24 clientes a mais. E o investimento em hardware é de 1.300 a 2.800 reais — três câmeras, uma por balança."

> ⚠️ Dizer "oportunidade estimada", nunca "retorno garantido".

### 2:50–3:00 · Fecho
> "Bovinu's: vocês já têm os clientes, as câmeras e as balanças. Falta só transformar o que vocês veem em número."
Tela final: nome do projeto + "github.com/…" + as 4 dores resolvidas em uma linha cada.

---

## Checklist de gravação

- [ ] Gravar a demo **em tela cheia, 1080p**, sem barra de tarefas, sem notificação
- [ ] Fonte do navegador em 110–125% (legível no celular)
- [ ] Dados de demo com nomes plausíveis (comanda 0421, picanha, lasanha) — nada de "teste1"
- [ ] Rodar o fluxo real pelo menos uma vez na gravação (não só slides)
- [ ] Cortar tempos de espera de API — acelerar 2–4× no corte
- [ ] Legendas revisadas (nomes: Bovinu's, Augusta, CMV, Little)
- [ ] Backup: se a IA falhar ao vivo, usar o prato pré-analisado **sem mencionar** que é cache
- [ ] Exportar em 1080p, ≤ 100 MB, upload como "não listado"
- [ ] Link do vídeo no README **e** no topo do repositório

## Erros que eliminam pontos
- Vídeo de 4 minutos (o limite é 3).
- Slide de "obrigado" com 20 segundos.
- Falar de tecnologia antes de falar do problema.
- Prometer retorno financeiro como certeza.
- Demo que não roda e é substituída por slides.
