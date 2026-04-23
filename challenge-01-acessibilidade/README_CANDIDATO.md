# Challenge 01 — Painel de Transparência Pública
### Tema: Impacto Social · Acessibilidade de Dados

# Como usar
## Dependências
```
python
pip
uv
```

## Como executar

### Localmente
Para executar localmente:
```sh
make run
```

### Containerizado

#### Dependências
```
docker
docker-compose
```

#### Execução
```sh
docker compose up
```

## Testes
### Execução de testes por aquivo
```sh
TEST_FILE=/file/to/run make test
```

### Para executar todos os testes
```sh
make test
```

## Decisões de Design

### Params(`pydantic.BaseModel`) para receber `URLQueryParams`
Optei por utilizar uma classe derivada do `pydantic.BaseModel` para guarar os URLQueryParams passados pelo usuário, isso além de faciltiar a distruição de parâmetros para classes dependentes da API (é só dar `params.key`), garante type checking em todos os campos recebidos do usuário

### Pattern Repository para conexão ao banco
Criei uma classe `BaseRepository` que tem as operações comuns a todos os repositórios (listagem de todos os elementos da classe, count do número de elementos na tabela, listagem por id, filtros e paginação)

Ao adicionar essa camada intermediária entre o `database` e a `api`, eu evito que regras ligadas a manipulação de banco sejam tratadas diretamente na camada da `api`

Se tivessemos rotas de `post`, `put`, `patch` e `delete` eu poderia ainda criar uma camada de use-cases para guardar regras de negócio, mas como só temos listagem, não foi necessário

### Biblioteca de paginação própria
Como a bibliteca de paginação da FastAPI (`fastapi-pagination`) não se dá bem com caching, criei um sistema simples de paginação no `BaseRepository._paginate()`, mas acabou não sendo de grande ajuda porque a biblioteca de caching também não funcionou com ele e tive que fazer a minha própria

### Bibliteca de caching própria (`@cachetools.cached()` wrapper)
Estava tendo problemas com `X-Cache` não refletindo se houve ou não colisão ao usar `fastapi-cache`, então desenvolvi um wrapper direto para a biblioteca `cachetools` que soluciona o problema de maneira elegante, `cachetools.cached` age como função de ordem mais baixa em relação ao wrapper `src.infra.cache` (como em todo wrapping) e eu extendo suas funcionalidades adicionando o header `X-Cache`, que ele não define

### Uso de UUIDv8 como chave primária de todas as tabelas
Com as acelerações de insersão que `UUIDv8` trouxe, adicionei `uuid6` como dependência, trazendo esses ids mais modernos para a aplicaçãos sem perder tanta velocidade de escrita, além disso, se eu quiser ordenar uma tabela por tempo, usar o `UUIDv8` tem complexidade de tempo menor que usar uma coluna `datetime`

### Indexação de campos usados em busca
Adicionei indexação nos campos de nome de todos os modelos já que eles seriam usados nas buscas por correlações (poderia ser no `id`, mas optei por usar os nomes para ser mais mnemonico na hora de consumir a API).

### Diagramas

#### Diagrama de Classes
```mermaid
---
title: Diagrama de Classes da Arquitetura
---
classDiagram

    class Gasto {
      +UUID id
      +UUID orgao_id
      +UUID categoria_id
      +str descricao
      +Decimal valor
      +date data_lancamento
      +UUID favorecido_id
    }

    class Orgao {
        +UUID id
        +str nome
        +str sigla
    }

    class Categoria {
        +UUID id
        +str nome
    }

    class Favorecido {
        +UUID id
        +str nome
    }

    Gasto --> Orgao : belongs_to
    Gasto --> Categoria : belongs_to
    Gasto --> Favorecido : belongs_to

    Orgao --> Gasto : has_many
    Categoria --> Gasto : has_many
    Favorecido --> Gasto : has_many

    class GastoResumo {
      +nome_categoria: str
      +gasto_total: Decimal
    }

    class PaginatedResponse~T~ {
      +items: list[T]
      +total: int
      +page: int
      +size: int
    }

    class RespostaResumo {
      +gastos_por_categoria: list[GastoResumo]
      +top_gastos: list[Gasto]
    }

    class PaginatedParams {
      +page: int
      +page_size: int
    }

    class OrgaoParams {
      +orgao: Optional[str]
    }

    class GastoParams {
      +ano: Optional[int]
      +mes: Optional[int]
      +categoria: Optional[str]
      +valor_min: Decimal
      +valor_max: Decimal
      +validate_min_max()
    }

    PaginatedParams <|-- OrgaoParams
    OrgaoParams <|-- GastoParams

    class BaseRepository {
        <<abstract>>
        -model
        +list_all(params)
        +list_by_id(id)
        +count(params)
        -_paginate(query, params)
        -_apply_filters(query, params)
        -_apply_filters_and_paginate(query, params)
    }

    class GastoRepository {
        +get_summary(params): RespostaResumo
        -_apply_filters(query, params)
    }

    class OrgaoRepository {
        -_apply_filters(query, params)
    }

    BaseRepository <|-- GastoRepository
    BaseRepository <|-- OrgaoRepository

    BaseRepository --> PaginatedParams
    BaseRepository --> PaginatedResponse

    GastoRepository --> Gasto
    GastoRepository --> Categoria
    GastoRepository --> Orgao
    GastoRepository --> GastoResumo
    GastoRepository --> RespostaResumo
    GastoRepository --> GastoParams

    OrgaoRepository --> Orgao
    OrgaoRepository --> OrgaoParams
```

#### Flowchart da API
```mermaid
---
title: Estado atual da arquitetura da API e suas interaçõews com o restante do sistema
---
flowchart LR
    subgraph API
        M["main.py"]
        A["gastos.py"]
        B["orgaos.py"]
    end

    subgraph Domain
      G["models.py"]
      Z["schemas.py"]
    end

    subgraph Infra
      subgraph Repositories
        D["BaseRepository (abstract)"]
        E["GastoRepository"]
        F["OrgaoRepository"]
      end

      J["Session (database.py)"]
    end
    DB[("SQLite Database")]

    A --> E
    B --> F

    E -.->|implements| D
    F -.->|implements| D

    E --> J
    F --> J

    M -->A
    M -->B
    J -->DB
    D -.->|depends| G
    D -.->|depends| Z
    G -.->|depends| Z
```
