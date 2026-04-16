# HAT Thinking — Scorecard de Avaliação
## Software Engineer I

> Uso interno — não compartilhar com candidatos.

---

## Candidato

| Campo | Valor |
|-------|-------|
| Nome | |
| Desafio escolhido | Challenge 0_ |
| Link do PR | |
| Avaliador | |
| Data da defesa técnica | |

---

## 1. Avaliação do Código (Take-home)

### Code Quality — /25 pontos

| Sub-critério | Peso | Nota (0–5) | Pontos |
|--------------|------|-----------|--------|
| Nomes semânticos de variáveis, funções e classes | 5 | | |
| Organização de pastas respeitando separação de responsabilidades | 5 | | |
| Ausência de código morto, comentários óbvios e TODOs não resolvidos | 5 | | |
| Consistência de estilo (linting passa sem erros) | 5 | | |
| Legibilidade geral — outro engenheiro entende sem explicação | 5 | | |

**Subtotal Code Quality:** ___ / 25

---

### Testing Mindset — /25 pontos

| Sub-critério | Peso | Nota (0–5) | Pontos |
|--------------|------|-----------|--------|
| Cobertura mínima atingida (≥70%) | 5 | | |
| Testes de edge case obrigatório implementados | 5 | | |
| Testes cobrem cenários de erro (não só caminho feliz) | 5 | | |
| `conftest.py` bem estruturado com fixtures reutilizáveis | 5 | | |
| Asserções significativas (não apenas `assert response.status_code == 200`) | 5 | | |

**Subtotal Testing Mindset:** ___ / 25

---

### SOLID & Arquitetura — /25 pontos

| Sub-critério | Peso | Nota (0–5) | Pontos |
|--------------|------|-----------|--------|
| Lógica de negócio separada da camada de API | 5 | | |
| Injeção de dependência ou abstrações para facilitar testes | 5 | | |
| Single Responsibility: cada módulo tem uma razão clara para existir | 5 | | |
| O "Pulo do Gato" foi implementado corretamente | 5 | | |
| Decisões de design justificadas no `README_CANDIDATO.md` | 5 | | |

**Subtotal Arquitetura:** ___ / 25

---

### Product Thinking — /25 pontos

| Sub-critério | Peso | Nota (0–5) | Pontos |
|--------------|------|-----------|--------|
| A API resolve o problema do usuário descrito na User Story | 5 | | |
| Mensagens de erro são informativas (não apenas status HTTP) | 5 | | |
| Documentação OpenAPI (`/docs`) está completa e com exemplos | 5 | | |
| O `seed.py` gera dados realistas (não apenas "test1", "test2") | 5 | | |
| O PR inclui seção "Decisões de Arquitetura" com raciocínio claro | 5 | | |

**Subtotal Product Thinking:** ___ / 25

---

## 2. Defesa Técnica (System Design & Code Review)

Cada resposta é avaliada de 0 a 4:
- **0** — Não soube responder
- **1** — Resposta superficial, sem embasamento técnico
- **2** — Entendeu o conceito mas não aplicou ao próprio código
- **3** — Explicou bem e conectou ao código entregue
- **4** — Explicação clara, mostrou trade-offs e alternativas

| Pergunta | Nota (0–4) | Observações |
|----------|-----------|-------------|
| P1 — Complexidade Algorítmica | | |
| P2 — Trade-off / Consistência | | |
| P3 — Escalabilidade | | |
| P4 — Extensibilidade | | |
| P5 — Testing Mindset | | |

**Subtotal Defesa Técnica:** ___ / 20

**Bônus (+5):** Candidato identificou um problema no próprio código durante a defesa e propôs solução: ☐ Sim ☐ Não

---

## Resultado Final

| Seção | Pontos | Máximo |
|-------|--------|--------|
| Code Quality | | 25 |
| Testing Mindset | | 25 |
| SOLID & Arquitetura | | 25 |
| Product Thinking | | 25 |
| Defesa Técnica | | 20 |
| Bônus | | 5 |
| **TOTAL** | | **125** |

---

## Decisão

| Faixa | Classificação |
|-------|--------------|
| 105–125 | ⭐ Forte recomendação de contratação |
| 85–104 | ✅ Recomendação de contratação |
| 65–84 | 🔄 Segunda entrevista recomendada (gaps específicos) |
| < 65 | ❌ Não recomendado para esta vaga |

**Decisão do avaliador:**

**Pontos fortes observados:**

**Gaps ou pontos de desenvolvimento:**

**Próximos passos:**

---

*HAT Thinking · Processo Seletivo Confidencial*
