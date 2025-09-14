from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.security import decode_access_token
from sqlalchemy.orm import Session
from typing import List
from datetime import date

# Importando os schemas necessários
from schemas.relatorio import (
    RelatorioCreate,
    RelatorioOut,
    RelatorioUpdate,
    EducadorWithRelatoriosOut,
    TurmaWithRelatoriosOut
)
from db.session import get_db
from crud import relatorios as crud_relatorios

# AJUSTADO: Adicionando prefixo e tags para melhor organização da API
router = APIRouter()

# --- ROTAS DE CRUD BÁSICO ---
bearer_scheme = HTTPBearer()
def educador_turma_required(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload or payload.get("role") != "educador" :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Apenas pessoas autenticadas podem acessar esta rota."
        )
    return payload

@router.post("/", response_model=RelatorioOut, summary="Cria um novo relatório",dependencies=[Depends(educador_turma_required)])
def create_relatorio(
    relatorio: RelatorioCreate,
    db: Session = Depends(get_db)
):
    """Cria um novo relatório associado a um educador e uma turma."""
    return crud_relatorios.create_relatorio(db=db, relatorio=relatorio)


@router.get("/{relatorio_id}", response_model=RelatorioOut, summary="Busca um relatório pelo ID")
def read_relatorio(relatorio_id: int, db: Session = Depends(get_db)):
    """Busca os detalhes de um relatório específico pelo seu ID."""
    db_relatorio = crud_relatorios.get_relatorio(db, relatorio_id=relatorio_id)
    if db_relatorio is None:
        raise HTTPException(status_code=404, detail="Relatório não encontrado")
    return db_relatorio


@router.put("/{relatorio_id}", response_model=RelatorioOut, summary="Atualiza um relatório")
def update_relatorio(
    relatorio_id: int,
    relatorio_update: RelatorioUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza as informações de um relatório. Aceita atualizações parciais."""
    db_relatorio = crud_relatorios.get_relatorio(db, relatorio_id=relatorio_id)
    if db_relatorio is None:
        raise HTTPException(status_code=404, detail="Relatório não encontrado")
    
    return crud_relatorios.update_relatorio(
        db=db,
        db_relatorio=db_relatorio,
        relatorio_update=relatorio_update
    )


@router.delete("/{relatorio_id}", response_model=RelatorioOut, summary="Deleta um relatório")
def delete_relatorio(relatorio_id: int, db: Session = Depends(get_db)):
    """Deleta um relatório do banco de dados."""
    db_relatorio = crud_relatorios.delete_relatorio(db, relatorio_id=relatorio_id)
    if db_relatorio is None:
        raise HTTPException(status_code=404, detail="Relatório não encontrado")
    return db_relatorio


# --- ROTAS DE LISTAGEM ANINHADA ---

@router.get(
    "/por-educador/{educador_id}",
    response_model=EducadorWithRelatoriosOut,
    summary="Lista todos os relatórios de um educador"
)
def read_relatorios_por_educador(educador_id: int, db: Session = Depends(get_db)):
    """Busca um educador e retorna uma lista de todos os seus relatórios."""
    educador = crud_relatorios.get_educador_with_relatorios(db, educador_id=educador_id)
    if educador is None:
        raise HTTPException(status_code=404, detail="Educador não encontrado")
    return educador


@router.get(
    "/por-turma/{turma_id}",
    response_model=TurmaWithRelatoriosOut,
    summary="Lista todos os relatórios de uma turma"
)
def read_relatorios_por_turma(turma_id: int, db: Session = Depends(get_db)):
    """Busca uma turma e retorna uma lista de todos os seus relatórios."""
    turma = crud_relatorios.get_turma_with_relatorios(db, turma_id=turma_id)
    if turma is None:
        raise HTTPException(status_code=404, detail="Turma não encontrada")
    return turma


# --- ROTAS DE FILTRAGEM POR DATA (ADICIONADAS) ---

@router.get(
    "/data/{data_iso}",
    response_model=List[RelatorioOut],
    summary="Busca relatórios por data"
)
def read_relatorios_por_data(data_iso: date, db: Session = Depends(get_db)):
    """
    Busca todos os relatórios de uma data específica (formato YYYY-MM-DD).
    """
    relatorios = crud_relatorios.get_relatorios_by_date(db=db, data=data_iso)
    return relatorios


@router.get(
    "/educador/{educador_id}/data/{data_iso}",
    response_model=List[RelatorioOut],
    summary="Busca relatórios de um educador por data"
)
def read_relatorios_de_educador_por_data(
    educador_id: int,
    data_iso: date,
    db: Session = Depends(get_db)
):
    """
    Busca os relatórios de um educador específico em uma data específica.
    """
    relatorios = crud_relatorios.get_relatorios_by_educador_and_date(
        db=db, educador_id=educador_id, data=data_iso
    )
    return relatorios


@router.get(
    "/turma/{turma_id}/data/{data_iso}",
    response_model=List[RelatorioOut],
    summary="Busca relatórios de uma turma por data"
)
def read_relatorios_de_turma_por_data(
    turma_id: int,
    data_iso: date,
    db: Session = Depends(get_db)
):
    """

    Busca os relatórios de uma turma específica em uma data específica.
    """
    relatorios = crud_relatorios.get_relatorios_by_turma_and_date(
        db=db, turma_id=turma_id, data=data_iso
    )
    return relatorios