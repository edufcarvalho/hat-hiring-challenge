# Challenge 02 — Motor de Rotas Sustentáveis
### Tema: Tech for Good · Otimização de Recursos e Emissões

---

## O Contexto

O setor de logística é responsável por cerca de **8% das emissões globais de CO₂**. Empresas de delivery e frotas urbanas frequentemente otimizam apenas para tempo ou custo — raramente para emissões. A maioria das APIs de roteirização (Google Maps, OSRM) não expõe métricas de carbono como parâmetro de otimização.

**Por que isso importa:** Uma frota de 50 veículos que reduz 15% das emissões diárias evita toneladas de CO₂ por ano. Isso não exige veículos elétricos — exige algoritmos melhores. Você pode construir esse algoritmo.

---

## User Story (Briefing)

> **Como** gerente de operações de uma empresa de entregas urbanas,
> **quero** calcular a rota de menor emissão de carbono para uma sequência de paradas,
> **para que** minha frota reduza seu impacto ambiental sem comprometer os prazos de entrega acordados com os clientes.

---

## Requisitos Técnicos

### Funcionais
- [ ] Endpoint `POST /rotas/calcular` que recebe uma lista de paradas (coordenadas lat/lng) e o perfil do veículo, e retorna a rota com menor emissão estimada
- [ ] Endpoint `POST /rotas/comparar` que recebe as mesmas paradas e retorna **duas rotas**: a de menor emissão e a de menor distância, com a diferença percentual de CO₂ entre elas
- [ ] Endpoint `GET /veiculos/perfis` listando os perfis de veículo disponíveis
- [ ] Suporte a pelo menos 3 perfis de veículo com fatores de emissão distintos

### Modelo de Emissão (simplificado)
Use a fórmula a seguir como base — você pode refiná-la:

```
emissao_kg_co2 = distancia_km × fator_emissao_veículo × (1 + peso_carga_kg / capacidade_maxima_kg)
```

**Perfis de veículo sugeridos:**

| Perfil | Combustível | Fator base (kg CO₂/km) | Capacidade máx (kg) |
|--------|------------|------------------------|---------------------|
| `VAN_DIESEL` | Diesel | 0.268 | 1200 |
| `MOTO_FLEX` | Flex | 0.089 | 30 |
| `CAMINHAO_LEVE` | Diesel | 0.512 | 3500 |

### Algoritmo de Roteamento
- Implemente um algoritmo de **permutação com poda** (nearest neighbor ou força bruta com limite) para encontrar a sequência de paradas que minimiza a emissão total
- O ponto de origem (depósito) é fixo e sempre o primeiro elemento da lista
- O retorno ao depósito ao final da rota é **opcional** (parâmetro `retornar_origem: bool`)

### Não-Funcionais
- [ ] Testes unitários com cobertura mínima de **70%**
- [ ] O endpoint deve rejeitar listas com menos de 2 paradas ou mais de 15 paradas (com mensagem de erro clara)
- [ ] Latência máxima aceitável: 500ms para listas de até 10 paradas (documente no README se exceder)
- [ ] `README_CANDIDATO.md` com instruções de execução e justificativa do algoritmo escolhido

### Stack
Utilize a stack base do repositório. O cálculo de distância entre coordenadas pode usar a fórmula de Haversine — não é necessário integrar com APIs externas de mapas.

---

## Payload de Exemplo

**Request:**
```json
{
  "veiculo": "VAN_DIESEL",
  "peso_carga_kg": 800,
  "retornar_origem": true,
  "paradas": [
    {"id": "deposito", "lat": -23.5505, "lng": -46.6333, "label": "Depósito Central SP"},
    {"id": "p1", "lat": -23.5615, "lng": -46.6560, "label": "Cliente A"},
    {"id": "p2", "lat": -23.5489, "lng": -46.6388, "label": "Cliente B"},
    {"id": "p3", "lat": -23.5701, "lng": -46.6218, "label": "Cliente C"}
  ]
}
```

**Response esperada:**
```json
{
  "rota_otimizada": ["deposito", "p2", "p1", "p3", "deposito"],
  "distancia_total_km": 12.4,
  "emissao_total_kg_co2": 4.21,
  "tempo_estimado_min": 38,
  "economia_vs_ordem_original": {
    "distancia_pct": 8.3,
    "co2_pct": 11.2
  }
}
```

---

## O "Pulo do Gato" — Restrição de Performance

Para listas com **mais de 8 paradas**, o algoritmo de força bruta (O(n!)) se torna inviável. O desafio:

- Para listas de até 8 paradas: use o algoritmo exato que preferir
- Para listas de 9 a 15 paradas: implemente uma **heurística** (nearest neighbor, 2-opt, ou similar) que entregue uma solução boa o suficiente em menos de 500ms
- A resposta deve incluir um campo `"algoritmo_usado": "exato" | "heuristico"` para que o consumidor da API saiba o nível de otimização recebido

> **Por que esse edge case existe:** Problemas reais de roteirização são NP-difíceis. Queremos ver se você conhece essa limitação e sabe quando aplicar uma heurística com trade-off explícito — uma habilidade central em engenharia de IA aplicada.

---

## Estrutura de Pastas Sugerida

```
challenge-02-sustentabilidade/
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       └── rotas.py
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── schemas.py
│   │   ├── models.py
│   │   └── services/
│   │       ├── emissao.py       # Cálculo de emissão
│   │       ├── roteamento.py    # Algoritmos de otimização
│   │       └── haversine.py     # Cálculo de distância
│   ├── infra/
│   │   └── __init__.py
│   └── tests/
│       ├── conftest.py
│       ├── test_haversine.py
│       ├── test_emissao.py
│       └── test_roteamento.py
├── main.py
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
└── README_CANDIDATO.md
```

---

## Defesa Técnica — Roteiro de 5 Perguntas

### P1 — Complexidade Algorítmica
> "Qual a complexidade de tempo do seu algoritmo para listas de até 8 paradas? E para 9 a 15? Se o cliente pedisse suporte a 50 paradas, qual algoritmo você usaria e por quê?"

**O que avaliamos:** Consciência de O(n!), O(n²), conhecimento de heurísticas (greedy, metaheurísticas).

### P2 — Confiabilidade do Modelo
> "Sua fórmula de emissão é uma simplificação. Que variáveis do mundo real ela ignora? Se um cliente da frota reclamasse que o cálculo está errado, como você investigaria e corrigiria sem quebrar os contratos existentes?"

**O que avaliamos:** Pensamento de produto, humildade técnica, versionamento de modelos.

### P3 — Trade-off Heurística vs. Ótimo
> "Seu endpoint pode retornar uma rota que não é a ótima para listas grandes. Como você comunicaria esse nível de incerteza para o usuário de negócio que não é técnico?"

**O que avaliamos:** Comunicação de limitações, UX de APIs, design de contratos claros.

### P4 — Extensibilidade
> "Amanhã o cliente quer adicionar janelas de tempo por parada — por exemplo, o Cliente A só pode receber entre 10h e 12h. Quais partes do seu código precisariam mudar? Consegue estimar o esforço em dias?"

**O que avaliamos:** Capacidade de estimativa, acoplamento da lógica de negócio.

### P5 — Testing Mindset
> "Como você testaria a corretude do seu algoritmo de roteamento? Como sabe que ele está retornando a melhor rota possível e não apenas 'uma rota'?"

**O que avaliamos:** Property-based testing, oráculos de teste, benchmarking de algoritmos.

---

*Boa sorte. Build things that matter.*
