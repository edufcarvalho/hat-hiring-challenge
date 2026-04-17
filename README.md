# HAT Thinking — Technical Challenge
## Software Engineer I · Take-home Assignment

> **"We don't prohibit AI. We ask you to explain every line of it."**

---

## Sobre o Processo

Este repositório contém o desafio técnico para a vaga de **Software Engineer I** na [HAT Thinking](https://hatkg.com) — consultoria especializada em IA aplicada a negócios.

Nosso processo foi desenhado para avaliar **raciocínio real**, não memória de algoritmos. Ferramentas de IA são bem-vindas — o diferencial está em saber defendê-las.

---

## Como Participar

1. Faça um **fork** deste repositório
2. Crie uma branch com seu nome: `git checkout -b candidato/seu-nome`
3. Escolha **um** dos três desafios abaixo
4. Navegue até a pasta do desafio escolhido e leia o `CHALLENGE.md` dentro dela
5. Implemente sua solução dentro da pasta correspondente, respeitando a estrutura existente
6. Abra um **Pull Request** para a branch `main` com o título: `[Challenge-0X] Seu Nome`
7. No PR, inclua uma seção `## Decisões de Arquitetura` explicando suas escolhas

**Prazo:** 5 dias corridos após o recebimento deste link.

---

## Stack Base (comum aos 3 desafios)

| Camada | Tecnologia |
|--------|-----------|
| Linguagem | Python 3.11+ | React | Node | Angular | Springboot
| Framework web | FastAPI |
| ORM / Persistência | SQLModel + SQLite (dev) / PostgreSQL (prod-ready) |
| Testes | Pytest + pytest-cov |
| Containerização | Docker + docker-compose |
| Linting / Format | Ruff + Black |
| Documentação da API | OpenAPI automático (via FastAPI) |

> A stack é **sugerida**, não obrigatória. Se preferir Node.js/TypeScript ou Go, justifique a escolha no PR.

---

## Os Três Desafios

| # | Tema | Pasta |
|---|------|-------|
| 01 | Impacto Social — Acessibilidade de Dados Públicos | `challenge-01-acessibilidade/` |
| 02 | Tech for Good — Otimização de Rotas Sustentáveis | `challenge-02-sustentabilidade/` |
| 03 | Eficiência de Negócio — Motor de Precificação de Propostas | `challenge-03-precificacao/` |

---

## O que Será Avaliado

| Critério | O que observamos |
|----------|-----------------|
| **Code Quality** | Código limpo, nomes semânticos, organização de pastas, ausência de código morto |
| **Testing Mindset** | Testes que cobrem erros e edge cases, não apenas o caminho feliz |
| **Product Thinking** | A solução resolve o problema do usuário ou é apenas tecnicamente bonita? |
| **Comunicação** | Você consegue explicar o fluxo de dados de ponta a ponta? |
| **SOLID & Separação de Responsabilidades** | Cada classe/módulo tem uma razão clara para existir |
| **Big O Awareness** | Você pensou em como sua solução escala? |

---

## Defesa Técnica (após entrega)

Após a entrega do PR, você será convidado para uma sessão de **System Design & Code Review** de 45 minutos com nosso time de engenharia.

As 5 perguntas-base estão documentadas dentro de cada `CHALLENGE.md`. O objetivo não é reprovar — é entender como você pensa.

> Candidatos que não usarem IA para gerar o código serão classificados como top tier e os que utilizarem IA precisarão explicar cada decisão de arquitetura e não será a **mesma avaliação** que quem escreveu tudo do zero. O que reprovará é não saber o que o código faz.

---

## Dúvidas

Abra uma **Issue** neste repositório com o label `pergunta`. Respondemos em até 24h úteis.

---

*HAT Thinking · "Build things that matter."*
