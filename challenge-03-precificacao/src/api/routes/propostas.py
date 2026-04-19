"""Rotas para propostas comerciais — implemente aqui."""

from fastapi import APIRouter

router = APIRouter()


@router.post("")
def criar_proposta():
    # TODO: Cálculo de margem + validação de status (APROVADA/PENDENTE/REPROVADA)
    raise NotImplementedError


@router.get("")
def listar_propostas():
    # TODO: Filtros: status, cliente, data_inicio, data_fim
    raise NotImplementedError


@router.get("/{proposta_id}")
def detalhar_proposta(proposta_id: str):
    # TODO: Retornar breakdown por profissional
    raise NotImplementedError


@router.post("/{proposta_id}/aplicar-desconto")
def aplicar_desconto(proposta_id: str):
    # TODO: Validação de nível hierárquico + histórico de aprovações (desconto em cascata)
    raise NotImplementedError
