import random
from datetime import date, timedelta
from typing import List

from sqlmodel import Session

from src.domain.enums import TipoPessoa
from src.domain.models import Categoria, Favorecido, Gasto, Orgao
from src.infra.database import create_db_and_tables, engine

# dados para o seed
orgaos = [
    Orgao(nome="Ministério da Saúde", sigla="MS"),
    Orgao(nome="Ministério da Educação", sigla="MEC"),
    Orgao(nome="Ministério da Justiça e Segurança Pública", sigla="MJSP"),
    Orgao(nome="Ministério da Fazenda", sigla="MF"),
    Orgao(nome="Ministério da Defesa", sigla="MD"),
    Orgao(nome="Ministério do Meio Ambiente", sigla="MMA"),
    Orgao(nome="Ministério dos Transportes", sigla="MT"),
    Orgao(nome="Ministério da Infraestrutura", sigla="MInfra"),
    Orgao(nome="Ministério da Ciência, Tecnologia e Inovação", sigla="MCTI"),
    Orgao(nome="Ministério do Desenvolvimento Social", sigla="MDS"),
    Orgao(nome="Ministério da Agricultura, Pecuária e Abastecimento", sigla="MAPA"),
    Orgao(nome="Ministério das Relações Exteriores", sigla="MRE"),
    Orgao(nome="Ministério do Turismo", sigla="MTur"),
    Orgao(nome="Ministério da Mulher, Família e Direitos Humanos", sigla="MMFDH"),
    Orgao(nome="Ministério da Cidadania", sigla="MC"),
]

categorias = [
    Categoria(nome="Pessoal e Encargos Sociais"),
    Categoria(nome="Juros e Encargos da Dívida"),
    Categoria(nome="Outras Despesas Correntes"),
    Categoria(nome="Investimentos"),
    Categoria(nome="Inversões Financeiras"),
]

descricoes = {
    "Pessoal e Encargos Sociais": [
        "Pagamento de servidores ativos",
        "Pagamento de aposentadorias",
        "Pagamento de pensões",
        "Encargos sociais sobre salários",
        "Férias e licenças",
        "Auxílio alimentação",
        "Auxílio transporte",
        "Gratificações",
    ],
    "Juros e Encargos da Dívida": [
        "Juros da dívida interna",
        "Juros da dívida externa",
        "Encargos da dívida mobiliária",
        "Comissões bancárias",
    ],
    "Outras Despesas Correntes": [
        "Material de consumo",
        "Serviços de terceiros",
        "Diárias e passagens",
        "Manutenção e conservação",
        "Comunicações",
        "Energia elétrica",
        "Água e esgoto",
    ],
    "Investimentos": [
        "Obras",
        "Aquisição de equipamentos",
        "Desenvolvimento de sistemas",
        "Pesquisa tecnológica",
    ],
    "Inversões Financeiras": [
        "Aquisição de imóveis já em utilização",
        "Aquisição de bens imóveis para fins administrativos já existentes",
        "Compra de participações acionárias em empresas estatais",
        "Subscrição de ações em sociedades de economia mista",
        "Integralização de capital em empresas públicas",
        "Aporte de capital em instituições financeiras públicas",
        "Aquisição de títulos e valores mobiliários",
    ],
}


def generate_dados(records_number: int = 1000) -> List[Gasto]:
    gastos = []
    start_date = date(2025, 1, 1)
    end_date = date(2026, 4, 16)

    for _ in range(records_number):
        orgao = random.choice(orgaos)
        categoria = random.choice(categorias)
        descricao = random.choice(descricoes[categoria.nome])
        valor = round(random.uniform(100, 10000), 2)
        data_lancamento = start_date + timedelta(
            days=random.randint(0, (end_date - start_date).days)
        )
        favorecido = Favorecido(
            nome=f"Favorecido {random.randint(1, 100)}",
            tipo=random.choice(list(TipoPessoa)),
        )

        gasto = Gasto(
            orgao=orgao,
            categoria=categoria,
            favorecido=favorecido,
            descricao=descricao,
            valor=valor,
            data_lancamento=data_lancamento,
        )
        gastos.append(gasto)

    return gastos


def seed_database(records_number: int = 1000):
    create_db_and_tables()
    gastos = generate_dados(records_number)

    with Session(engine) as session:
        session.add_all(gastos)

        session.commit()
