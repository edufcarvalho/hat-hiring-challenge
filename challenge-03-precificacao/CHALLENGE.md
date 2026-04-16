# Challenge 03 — Motor de Precificação de Propostas
### Tema: Eficiência de Negócio · Professional Services

---

## O Contexto

Empresas de consultoria de tecnologia perdem horas por semana montando propostas comerciais no Excel — sem validação automática de margem, sem controle de desconto por senioridade, sem consistência entre vendedores. O resultado é previsível: propostas fora da realidade chegam ao cliente e geram renegociações que corroem a relação comercial antes mesmo do projeto começar.

**Por que isso importa:** Em Professional Services, a proposta é o produto. Um motor de regras que valida rentabilidade em tempo real transforma o trabalho do executivo de vendas de "copiar fórmula do Excel" para "focar na negociação".

---

## User Story (Briefing)

> **Como** executivo de vendas de uma consultoria de TI,
> **quero** submeter uma lista de profissionais alocados em uma proposta com suas respectivas horas e senioridades,
> **para que** o sistema valide automaticamente se a proposta é rentável, aplique os descontos permitidos por nível hierárquico, e me alerte quando a margem bruta estiver abaixo do threshold mínimo aceitável.

---

## Requisitos Técnicos

### Funcionais

- [ ] Endpoint `POST /propostas` para criar e validar uma nova proposta
- [ ] Endpoint `GET /propostas/{id}` para consultar o detalhe de uma proposta com o breakdown por profissional
- [ ] Endpoint `GET /propostas` com filtros: `status` (aprovada/reprovada/pendente), `cliente`, `data_inicio`, `data_fim`
- [ ] Endpoint `POST /propostas/{id}/aplicar-desconto` para aplicar um desconto adicional, respeitando as regras de aprovação por nível hierárquico
- [ ] Endpoint `GET /tabela-precos` retornando a tabela de preços por senioridade vigente

### Regras de Negócio (Motor de Precificação)

**Tabela de preços base (configurável via variável de ambiente ou seed):**

| Senioridade | Custo/hora (R$) | Preço de venda/hora (R$) | Margem alvo |
|-------------|-----------------|--------------------------|-------------|
| `JUNIOR` | 45,00 | 95,00 | 52,6% |
| `PLENO` | 75,00 | 155,00 | 51,6% |
| `SENIOR` | 120,00 | 245,00 | 51,0% |
| `ESPECIALISTA` | 180,00 | 380,00 | 52,6% |
| `GERENTE` | 250,00 | 520,00 | 51,9% |

**Regras de desconto por nível hierárquico:**

| Nível de aprovador | Desconto máximo permitido |
|--------------------|--------------------------|
| `EXECUTIVO_VENDAS` | até 5% sobre o valor total |
| `GERENTE_COMERCIAL` | até 15% sobre o valor total |
| `DIRETOR` | até 25% sobre o valor total |
| `CEO` | até 40% sobre o valor total |

**Regras de validação automática:**
- Margem bruta mínima aceitável: **40%** (configurável)
- Se a margem calculada estiver entre 40% e 45%: status `PENDENTE` (requer aprovação manual)
- Se a margem calculada estiver acima de 45%: status `APROVADA` automaticamente
- Se a margem calculada estiver abaixo de 40%: status `REPROVADA` automaticamente
- Uma proposta `REPROVADA` pode ser reeditada, mas não pode ser enviada ao cliente

### Não-Funcionais
- [ ] Testes unitários com cobertura mínima de **75%**
- [ ] Testes obrigatórios: proposta com margem exatamente em 40%, desconto que excede o limite do aprovador, proposta com zero horas alocadas
- [ ] Todos os valores monetários devem usar `Decimal` (não `float`) para evitar erros de arredondamento
- [ ] `README_CANDIDATO.md` com explicação do fluxo de estados da proposta e as decisões de design

---

## Payload de Exemplo

**Request — criar proposta:**
```json
{
  "cliente": "Empresa XYZ",
  "descricao": "Modernização de sistema legado",
  "data_inicio": "2025-02-01",
  "data_fim": "2025-05-31",
  "profissionais": [
    {
      "nome": "Ana Souza",
      "senioridade": "SENIOR",
      "horas_estimadas": 320
    },
    {
      "nome": "Bruno Lima",
      "senioridade": "PLENO",
      "horas_estimadas": 480
    },
    {
      "nome": "Carla Mendes",
      "senioridade": "JUNIOR",
      "horas_estimadas": 200
    }
  ]
}
```

**Response esperada:**
```json
{
  "id": "uuid",
  "cliente": "Empresa XYZ",
  "status": "APROVADA",
  "custo_total": 88400.00,
  "valor_venda": 181200.00,
  "margem_bruta_pct": 51.2,
  "breakdown": [
    {
      "nome": "Ana Souza",
      "senioridade": "SENIOR",
      "horas": 320,
      "custo": 38400.00,
      "valor_venda": 78400.00
    }
  ],
  "alertas": []
}
```

---

## O "Pulo do Gato" — Desconto em Cascata

Implemente o seguinte cenário de desconto em cascata:

Um `EXECUTIVO_VENDAS` aplica 5% de desconto. A proposta vai a `PENDENTE`. Um `GERENTE_COMERCIAL` precisa aprovar e quer aplicar mais 8% de desconto adicional. A regra é:

- O desconto total acumulado **não pode ultrapassar o limite do aprovador atual**
- Ou seja: 5% (executivo) + 8% (gerente) = 13%, que está dentro do limite de 15% do gerente — **permitido**
- Mas: 5% (executivo) + 12% (gerente) = 17%, que ultrapassa 15% — **bloqueado**
- O sistema deve registrar um **histórico de aprovações** com: quem aprovou, qual desconto foi aplicado, e o timestamp

> **Por que esse edge case existe:** Processos de aprovação multi-nível são um dos principais vetores de bugs em sistemas de vendas. A lógica parece simples, mas a implementação correta exige rastrear estado acumulado imutável. Queremos ver como você modela esse histórico.

---

## Estrutura de Pastas Sugerida

```
challenge-03-precificacao/
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       └── propostas.py
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── models.py           # SQLModel: Proposta, Profissional, Aprovacao
│   │   ├── schemas.py          # Pydantic schemas
│   │   ├── enums.py            # Senioridade, StatusProposta, NivelAprovador
│   │   └── services/
│   │       ├── precificacao.py  # Cálculo de custo, venda, margem
│   │       ├── validacao.py     # Regras de status e aprovação
│   │       └── desconto.py      # Lógica de desconto em cascata
│   ├── infra/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── seed.py             # Tabela de preços e propostas exemplo
│   └── tests/
│       ├── conftest.py
│       ├── test_precificacao.py
│       ├── test_desconto.py
│       └── test_validacao.py
├── main.py
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
└── README_CANDIDATO.md
```

---

## Defesa Técnica — Roteiro de 5 Perguntas

### P1 — Complexidade Algorítmica
> "Seu endpoint `GET /propostas` lista propostas com filtros. Qual a complexidade da query com todos os filtros aplicados simultaneamente? Se tivermos 1 milhão de propostas no banco, quais índices você criaria?"

**O que avaliamos:** Conhecimento de índices compostos, query planning, explain analyze.

### P2 — Precisão Numérica
> "Por que você usou `Decimal` em vez de `float` para valores monetários? Me dê um exemplo concreto de bug que `float` causaria nesse sistema."

**O que avaliamos:** Conhecimento de representação de ponto flutuante, maturidade com dinheiro em software.

### P3 — Modelagem de Estado
> "Uma proposta passa por múltiplos estados: PENDENTE → APROVADA → (cancelada?). Como você garantiria que uma proposta nunca voltasse de APROVADA para PENDENTE sem um evento explícito de rejeição? Onde essa regra viveria no código?"

**O que avaliamos:** Máquina de estados, invariantes de domínio, onde colocar lógica de negócio.

### P4 — Extensibilidade
> "O CEO pediu: quero que descontos acima de 30% enviem automaticamente um email de alerta para o CFO. Onde você adicionaria essa lógica? Criaria um novo serviço? Usaria eventos? Por quê?"

**O que avaliamos:** Event-driven thinking, separação de responsabilidades, efeitos colaterais.

### P5 — Testing Mindset
> "Mostre o teste mais importante que você escreveu nesse desafio. Por que ele é o mais importante?"

**O que avaliamos:** Capacidade de priorizar risco, maturidade de engenharia.

---

*Boa sorte. Build things that matter.*
