# Challenge 01 — Painel de Transparência Pública
### Tema: Impacto Social · Acessibilidade de Dados

---

## O Contexto

O Brasil publica bilhões de registros de dados governamentais — licitações, gastos, beneficiários de programas sociais — mas a grande maioria da população não consegue consumi-los. As APIs do governo são lentas, sem paginação eficiente, e os formatos variam de CSV arcaico a JSON mal estruturado. Organizações do terceiro setor perdem semanas apenas para preparar dados antes de conseguir qualquer análise.

**Por que isso importa:** Transparência sem acessibilidade não é transparência. Um cidadão de baixa renda, uma ONG com um estagiário de TI ou um jornalista investigativo não têm equipe de dados. Sua API pode mudar isso.

---

## User Story (Briefing)

> **Como** analista de uma ONG de controle social,
> **quero** consultar e filtrar os gastos federais por órgão, período e categoria de despesa via uma API REST simples,
> **para que** eu possa gerar relatórios mensais sem precisar baixar arquivos CSV de 2 GB do Portal da Transparência.

---

## Requisitos Técnicos

### Funcionais
- [x] Endpoint `GET /gastos` com filtros opcionais: `orgao`, `ano`, `mes`, `categoria`, `valor_min`, `valor_max`
- [x] Endpoint `GET /gastos/{id}` retornando o detalhe de um registro
- [x] Endpoint `GET /orgaos` listando os órgãos disponíveis
- [x] Paginação obrigatória em todos os endpoints de listagem (`page`, `page_size`, máximo 100 registros/página)
- [x] Endpoint `GET /resumo` retornando agregações: total gasto por categoria e top 5 maiores despesas do período filtrado

### Não-Funcionais
- [x] Testes unitários com cobertura mínima de **70%** (medido via `pytest-cov`)
- [x] Testes devem cobrir: filtro vazio, filtro combinado, página inexistente, e valor_min > valor_max
- [x] Documentação OpenAPI acessível em `/docs`
- [x] Um arquivo `seed.py` que popula o banco com ao menos **500 registros** de dados fictícios, mas realistas
- [X] `README_CANDIDATO.md` explicando como rodar o projeto e suas decisões de design

### Stack
Utilize a stack base do repositório (FastAPI + SQLModel + SQLite). Se preferir outra, justifique.

---

## Dataset de Referência

Para popular o banco, utilize dados fictícios inspirados na estrutura do Portal da Transparência:

```json
{
  "id": "uuid",
  "orgao": "Ministério da Saúde",
  "categoria": "Pessoal e Encargos Sociais",
  "descricao": "Pagamento de servidores ativos",
  "valor": 1250000.00,
  "data_lancamento": "2024-03-15",
  "favorecido": "Folha Consolidada MS"
}
```

---

## O "Pulo do Gato" — Edge Case Obrigatório

Implemente um mecanismo de **cache em memória** (pode ser simples, ex.: `functools.lru_cache` ou `cachetools`) para o endpoint `/resumo`. A regra é:

- O resumo deve ser recalculado **no máximo uma vez a cada 60 segundos** por combinação de filtros
- Se o usuário chamar `/resumo?orgao=saude&ano=2024` 100 vezes em 30 segundos, o banco deve ser consultado apenas **uma vez**
- O header da resposta deve indicar se veio do cache: `X-Cache: HIT` ou `X-Cache: MISS`

> **Por que esse edge case existe:** Endpoints de agregação em bases grandes são caros. Qualquer API de transparência real enfrentará esse problema com tráfego mínimo. Queremos ver se você pensa em custo computacional, não só em funcionalidade.

---

## Estrutura de Pastas Sugerida

```
challenge-01-acessibilidade/
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── gastos.py
│   │   │   └── orgaos.py
│   │   └── dependencies.py
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── models.py        # SQLModel models
│   │   ├── schemas.py       # Pydantic schemas (request/response)
│   │   └── services.py      # Business logic
│   ├── infra/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── cache.py         # Cache implementation
│   │   └── seed.py
│   └── tests/
│       ├── conftest.py
│       ├── test_gastos.py
│       └── test_resumo.py
├── main.py
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
└── README_CANDIDATO.md
```

---

## Defesa Técnica — Roteiro de 5 Perguntas

As perguntas abaixo serão feitas na entrevista após a entrega. Não há resposta certa ou errada — o objetivo é entender seu raciocínio.

### P1 — Complexidade Algorítmica
> "Seu endpoint `/resumo` faz uma agregação no banco. Qual a complexidade de tempo da query que você escreveu? Se a tabela tiver 50 milhões de registros e você não puder usar cache, o que você faria diferente?"
Como em big O sempre devemos considerar o pior caso, a complexidade de tempo é `O(n log(n))` e no caso médio `O(n)`

Sem cache, eu talvez adicionasse um particionamento (não adicionei porque `SQLModel` não suporta), assim filtrando as *rows* antes delas carregarem, reduzindo o peso da busca, além disso, já adiconei, mas vvale comentar que os campos usados em buscas estão todos indexados
**O que avaliamos:** Consciência de índices, particionamento, materialização de views.

### P2 — Trade-off de Consistência
> "Você implementou cache de 60 segundos. Um gestor público acabou de cancelar uma despesa no sistema de origem. Um usuário que chama `/resumo` nesse intervalo verá dados desatualizados. Você aceitaria esse trade-off? Como comunicaria isso ao usuário da API?"

*Não, não aceitaria.*

Eu implementaria um header `Cache-Control` onde, quando eu recebesse `no-cache`, eu bateria no banco novamente independente de cache e guardaria a nova resposta
Assim, caso o usuário precise de dados consistentes, ele pode abrir mão de performance em favor da consistência.

**O que avaliamos:** Consciência de consistência eventual vs. performance; design de contrato de API.

### P3 — Escalabilidade
> "Hoje você usa SQLite. Se amanhã precisarmos servir 10 mil requisições por segundo, quais 3 mudanças você faria na arquitetura, em ordem de prioridade?"
Passos:
1. Trocaria o SQLite por PostgreSQL com pooling do PgBouncer. Motivo: Postgres tem uma grande quantidade de extensões é um banco extremamente escalável e confiável;
2. Criaria réplicas de leitura pro banco, usando asyncronous replication (performance > consistência) ou syncronous replication (consitencia > performance), dependendo do que a nível de caso de uso fizer mais sentido, eu acredito que seja melhor sincrono, com um custo de 1-10ms por write, eu consigo ter consistência para entregar sempre a resposta mais atualizada na API;
3. Adicionaria um cache distribuído (1 servidor de Redis para n nodes da API) usando `docker` e `compose`

**O que avaliamos:** Conhecimento de connection pooling, réplicas de leitura, cache distribuído (Redis).

### P4 — Extensibilidade
> "Um novo cliente pediu para filtrar gastos por geolocalização — estado e município. Como você adicionaria esse filtro sem quebrar os contratos de API existentes?"

Eu poderia criar uma nova API usando a namespace `/v2` e adicionaria o suporte, criaria a tabela `localizacoes` com os campos `id`, `estado`,`municipio`, adicionaria na tabela `gastos` a coluna opcional `localizacao_id` para fazer a correlação entre o gasto e onde ele foi feito, e objetos próprios para a `v2`, como: Params com municipio e estado opcionais e repositório que herdasse do `BaseRepository` e faria o `__apply_filter`:
```
class GastoRepository(BaseRepository):
  def __init__(self, session: Session):
    super().__init__(session, Gasto)

  # outras funções do repository de gastos

  def _apply_filters(self, query, params: Params):
    query = super()._apply_filters(query, params)

    if params.municipio:
      query = # logic to join and filter municipio

    if params.estado:
      query = # logic join and filter municipio
    return query
```

Também é possível não versionar a API e só adicionar tudo como opcional, o código seria bem semelhante

**O que avaliamos:** Versionamento de API, design de parâmetros opcionais, backward compatibility.

### P5 — Testing Mindset
> "Mostre um teste que você escreveu que NÃO testa o caminho feliz. Por que você escolheu esse cenário?"

`TestBaseRepository::test_valor_min_greater_than_valor_max`, escolhei esse caminho porque é um erro comum preencher errado campos com nomes semelhantes, ou seja, trocar valor_min por valor_max, então era necessário testar para garantir que não houvesse erro

**O que avaliamos:** Maturidade de testes, capacidade de antecipar falhas reais de usuário.

---

*Boa sorte. Build things that matter.*
