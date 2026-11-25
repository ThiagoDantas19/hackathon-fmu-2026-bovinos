# Achados da palestra (Bovinos Grill & Beer — Augusta)

> Fonte: `transcricoes/palestra-hackathon-fmu.txt` (abertura + ~1h de Q&A com Luísa e Gabriel, diretoria do Grupo Bovinos).
> Objetivo: separar **fato dito pelo cliente** de **suposição nossa**. O que está aqui é o que vale para o pitch.

---

## 1. Números confirmados na fala deles

| Dimensão | Valor dito | Observação |
|---|---|---|
| Unidade | Rua Augusta, SP (próximo ao Center 3) | "Beer" = happy hour de sexta + eventos fechados |
| Funcionamento | 11h30 – 15h30 | Só almoço; jantar não faz sentido para a loja |
| Pico | **12h10 – 13h20** | Concentração pós-pandemia (antes era mais espalhado) |
| Clientes | **~600/dia útil**, ~250/dia fim de semana | Pré-pandemia eram 800–850 com a mesma equipe |
| Salão | **90 mesas**, ~**450 lugares**, 2 níveis | Salão inferior + principal (4 garçons) e superior (4 garçons) |
| Equipe de salão | **7–8 garçons**, 1 gerente geral, 1 gerente de atendimento, 2–3 metres | Sem "comin" (quem leva só bebida) |
| Churrasqueira | **4 pessoas** no pico (3 atendendo + 1 operando/repondo) | 10 preparos diferentes — principal diferencial |
| Fila da churrasqueira | **4 min medidos** no pico; meta **2,5 min** | "Para a gente é ruim" |
| Fila de saída/caixa | **≤ 1,5–2 min** | Não é a dor |
| Balanças | **3**, com 1–2 operadores no pico | Testando balança automática com leitura do código de barras |
| Caixas | 2 baias + **2 totens** no principal, +1 totem no auxiliar | Caixa auxiliar abre 12h30–13h30/14h |
| Preço | **R$ 119,00/kg**; "à vontade" **R$ 90,00** | "Somos um quilo caro" |
| Cardápio | ~30 saladas, ~30 quentes, ~10 grelhados, ~20 sobremesas | Cardápio **diário variável**, não fixo |
| Desconto | **10%** antes das 12h e depois das 13h30 | Tentativa de espalhar o fluxo |
| Unidades do grupo | 13 | Sem franquia (capital próprio) |
| Grupos no hackathon | ~83 inscritos | 20 finalistas apresentam quinta 19h |

### Temas por dia (útil para "Pergunta do Dia")

| Dia | Tema |
|---|---|
| Segunda | Virado paulista |
| Terça | Comida árabe (dia mais forte de público) |
| Quarta | Feijoada |
| Quinta | Italiano (massas/risotos) |
| Sexta | Frutos do mar + happy hour |
| Sábado | Feijoada |
| Domingo | Variado, ilha de massas, mexicano |

---

## 2. Como a operação funciona hoje (fluxo real)

1. Cliente entra → **recepção humanizada** entrega o cartão-comanda (4 dígitos, 1–9999, com código de barras no verso). Eles **não querem** catraca/autoatendimento na entrada.
2. Pega o prato (**não usa bandeja** — bebida é levada na mesa), passa por 4 estações: saladas → quentes → sobremesas → churrasqueira.
3. **Pesa em uma das 3 balanças** (operador bipa a comanda, peso cai no sistema).
4. Senta; garçom anota a bebida no celular.
5. Sai pelo caixa principal (ou auxiliar no pico) / totem, paga e a comanda é zerada.

**Ponto crítico de desistência:** a fila é visível da rua. Se ela chega na **escadinha de 5–6 degraus** da entrada, o cliente olha e desce a rua — a Augusta tem muita concorrência. Isso é a métrica de "cliente perdido" que eles não têm.

---

## 3. O que eles já têm de dado (e o que não têm)

**Tem:**
- Peso e valor por comanda, por vários dias (o SaaS calcula peso × R$119).
- Ticket médio e peso médio (usados de forma agregada, dia inteiro).
- Horário de **fechamento** da comanda (passou o cartão).
- Câmeras Intelbras em salão, cozinha e financeiro — gravam local + cloud, **sem nenhuma métrica**; ninguém olha no dia a dia. Existe uma câmera ampla que "por acaso" pega a balança, mas nenhuma focada nela.
- Cartõezinhos de elogio no fim de semana + Google (como NPS informal).
- 1h30 de vídeo da casa operando, que será disponibilizado (com blur nas pessoas).

**Não tem (dito explicitamente):**
- Mix do prato servido (peso sem composição) → **a dor nº 1 na visão deles**.
- Tempo de espera em nenhuma estação (só "feeling" do gerente).
- Tempo de limpeza/desocupação de mesa.
- Resto-ingesto, aceitação por item, reposições de cuba.
- Início do processo de pagamento (só o fim).
- CRM, fidelidade, cadastro, NPS estruturado.
- Ficha técnica em uso no dia a dia (existe, mas não é seguida na produção).

Frase deles: *"a gente ainda opera um pouco como era nos anos 2000… existe muita informação ali de como o cliente navega, a gente não guarda nenhuma dessas métricas."*

---

## 4. Escopo: dentro e fora (dito na apresentação)

**Dentro:** jornada do cliente no almoço por quilo da unidade Augusta; mix do prato/CMV; filas e tempo; limpeza de salão; qualidade/desperdício/giro de cubas.

**Fora (explicitamente):**
- Cozinha, compras e estoque.
- Pagamentos, caixa, pagamento online.
- Mudar o modelo de operação (nada de à la carte, nada de catraca, nada que remova o acolhimento humano).
- Marketing/redes sociais (não é foco, "eles acreditam no boca a boca").

**Sobre hardware:** aceitam investimento pequeno; "investimento muito grande não faz sentido". Câmera dedicada na balança foi classificada como **"compra bastante razoável / plausível"**. Reforçaram reuso do parque Intelbras.

**Sobre integração:** o sistema é o **JS Softcom** (caixa + atendimento), roda em **servidor local** com Wi-Fi para celulares dos garçons, balanças e caixas. **Não há API documentada** e eles não souberam responder se existe. A chave de tudo é o **número da comanda** (o código de barras evita fraude no totem).

---

## 5. Métricas que eles próprios pediram (usar como KPI do pitch)

1. **Mix do prato** (% de proteína premium vs. acompanhamento) e **CMV por prato/comanda**.
2. **Tempo de espera** por estação (churrasqueira p50/p95), fila na escada e **estimativa de cliente perdido**.
3. **Latência de higienização** (mesa livre → mesa limpa) e mesas sujas simultâneas.
4. **Aceitação por item** (nota do item) e **resto estimado**.
5. **Reposições de cuba por dia** — dito como *"a métrica que fica mais interessante… se o arroz foi reposto cinco vezes, já é um dado bastante relevante"*.

> Esse último item é um presente: é a métrica mais barata de implementar (1 toque do cozinheiro) e a que eles valorizam mais. **Não pode ficar de fora.**

---

## 6. Frases que valem um slide

- "A gente sabe o peso que o cliente se serviu, mas não sabe o que ele pegou."
- "Se 600 gramas é arroz e feijão ou é picanha, isso impacta diretamente o nosso lucro."
- "O cliente executivo tem 30, 40 minutos no máximo — ele é muito sensível ao tempo."
- "Se a fila chega na escada, o cliente espia e segue descendo a rua."
- "É muito no olhômetro."
- "O que a gente demonstra mas não conta."

---

## 7. Perguntas que ficaram em aberto (validar com a Luísa/Gabriel)

| # | Pergunta | Por que importa |
|---|---|---|
| 1 | O JS Softcom expõe alguma API, webhook ou acesso somente-leitura ao banco local? | Define se a integração é real ou via conector de borda |
| 2 | A balança automática em teste permite acoplar câmera/trigger de pesagem? | Define o hardware do MVP |
| 3 | Qual o diâmetro/padrão do prato usado no buffet? | Calibração px→cm² e estimativa de peso |
| 4 | A comanda tem QR impresso ou só código de barras 1D? | Define o caminho do feedback na saída |
| 5 | Capacidade (kg) de uma cuba cheia, por item? | Converte "nº de reposições" em kg |
| 6 | Existe planta/altura das câmeras Intelbras atuais? | Planta de posicionamento dos novos pontos |
| 7 | O vídeo de 1h30 será disponibilizado para treino/demo? | Ativo de CV e de demonstração |
| 8 | Orçamento-teto aproximado para hardware (3 câmeras + suportes)? | Fecha o BOM |

---

## 8. O que a banca provavelmente vai cobrar

1. **Adesão ao escopo** (não entregar ERP de cozinha nem app de delivery).
2. **Não invasividade** — a solução não pode quebrar a recepção humanizada nem exigir mudança no caixa.
3. **Viabilidade econômica** com números ligados ao R$119/kg e aos 600 clientes/dia.
4. **Honestidade sobre o dado** — eles sabem que não existe histórico; assumir premissas é melhor que inventar.
5. **Demo funcionando** + vídeo de 3 min + README executável.
