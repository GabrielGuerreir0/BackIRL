# Arquivo: /app/api/v1/turma.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from db.session import SessionLocal
from schemas.turma import TurmaCreate, TurmaOut, TurmaUpdate
from crud import turma as crud_turma
from crud import educador as crud_educador
from typing import List
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.security import decode_access_token
from models.turma import Turma
from models.aluno import Aluno

router = APIRouter()

bearer_scheme = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def coordenador_required(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload or payload.get("role") != "coordenador":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Apenas coordenadores podem realizar esta ação."
        )
    return payload

@router.post("/", response_model=TurmaOut, status_code=status.HTTP_201_CREATED)
def criar_turma_route(
    turma: TurmaCreate,
    db: Session = Depends(get_db),
    _ = Depends(coordenador_required)
):
    # Verifica se o educador existe apenas se educador_id for fornecido
    if turma.educador_id:
        educador = crud_educador.get_educador(db, turma.educador_id)
        if not educador:
            raise HTTPException(status_code=404, detail="Educador responsável não encontrado")
    
    db_turma = crud_turma.criar_turma(db, turma)
    return db_turma



@router.get("/", response_model=List[TurmaOut])
def listar_turmas_route(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100)
):
    """
    Retorna uma lista de todas as turmas, com paginação.
    """
    turmas = crud_turma.listar_turmas(db, skip=skip, limit=limit)
    return turmas



@router.get("/{turma_id}", response_model=TurmaOut)
def get_turma_route(
    turma_id: int,
    db: Session = Depends(get_db)
):
    """
    Retorna as informações de uma turma específica pelo seu ID.
    """
    turma = crud_turma.get_turma(db, turma_id)
    if turma is None:
        raise HTTPException(status_code=404, detail="Turma não encontrada")
    return turma



@router.put("/{turma_id}", response_model=TurmaOut)
def atualizar_turma_route(
    turma_id: int,
    turma_update: TurmaUpdate,
    db: Session = Depends(get_db),
    _ = Depends(coordenador_required)
):
    """
    Atualiza as informações de uma turma existente.
    """
    db_turma = crud_turma.atualizar_turma(db, turma_id, turma_update)
    if db_turma is None:
        raise HTTPException(status_code=404, detail="Turma não encontrada")
    return db_turma


@router.delete("/{turma_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_turma_route(
    turma_id: int,
    db: Session = Depends(get_db),
    _ = Depends(coordenador_required)
):
    """
    Exclui uma turma do banco de dados pelo seu ID.
    """
    result = crud_turma.excluir_turma(db, turma_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Turma não encontrada")
    # Retorna None para um status 204
    return None


@router.post("/{turma_id}/alunos/{aluno_id}", response_model=TurmaOut, status_code=status.HTTP_200_OK)
def adicionar_aluno_a_turma_route(
    turma_id: int,
    aluno_id: int,
    db: Session = Depends(get_db),
    _ = Depends(coordenador_required)
):
    """
    Adiciona um aluno a uma turma.
    """
    turma_com_aluno = crud_turma.adicionar_aluno_a_turma(db, turma_id, aluno_id)
    if "error" in turma_com_aluno:
        raise HTTPException(status_code=turma_com_aluno[1], detail=turma_com_aluno[0])
    return turma_com_aluno



@router.delete("/{turma_id}/alunos/{aluno_id}", status_code=status.HTTP_200_OK)
def remover_aluno_da_turma_route(
    turma_id: int,
    aluno_id: int,
    db: Session = Depends(get_db),
    _ = Depends(coordenador_required)
):
    """
    Remove um aluno de uma turma.
    """
    turma = crud_turma.get_turma(db, turma_id)
    if not turma:
        raise HTTPException(status_code=404, detail="Turma não encontrada")
    
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    if aluno.turma_id != turma_id:
        raise HTTPException(status_code=400, detail="Aluno não pertence a esta turma.")
        
    result = crud_turma.remover_aluno_da_turma(db, aluno_id)
    
    return {"message": f"Aluno com ID {aluno_id} removido da turma {turma_id} com sucesso."}