# Arquivo: /app/api/v1/turma.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from db.session import SessionLocal
from schemas.turma import TurmaCreate, TurmaOut, TurmaUpdate
from schemas.aluno import AlunoOut
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
    # LÓGICA SIMPLIFICADA: O schema já exige o educador_id.
    # A verificação 'if turma.educador_id:' foi removida por ser redundante.
    educador = crud_educador.get_educador(db, turma.educador_id)
    if not educador:
        raise HTTPException(status_code=404, detail=f"Educador com ID {turma.educador_id} não encontrado.")
    
    # Adicionar verificação para nome de turma duplicado
    db_turma_existente = db.query(Turma).filter(Turma.nome == turma.nome).first()
    if db_turma_existente:
        raise HTTPException(status_code=400, detail="Já existe uma turma com este nome.")

    db_turma = crud_turma.criar_turma(db, turma)
    return db_turma




@router.get("/", response_model=List[TurmaOut])
def listar_turmas_route(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100)
):
    turmas = crud_turma.listar_turmas(db, skip=skip, limit=limit)
    return turmas



@router.get("/{turma_id}", response_model=TurmaOut)
def get_turma_route(
    turma_id: int,
    db: Session = Depends(get_db)
):
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
    result = crud_turma.excluir_turma(db, turma_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Turma não encontrada")
    return None


@router.post("/{turma_id}/alunos/{aluno_id}", response_model=AlunoOut) # MELHORIA: Retorna o aluno atualizado
def adicionar_aluno_a_turma_route(
    turma_id: int,
    aluno_id: int,
    db: Session = Depends(get_db),
    _ = Depends(coordenador_required)
):
    aluno_atualizado = crud_turma.adicionar_aluno_a_turma(db, turma_id=turma_id, aluno_id=aluno_id)
    
    if not aluno_atualizado:
         raise HTTPException(status_code=404, detail="Turma ou Aluno não encontrado.")

    return aluno_atualizado



@router.delete("/{turma_id}/alunos/{aluno_id}", status_code=status.HTTP_200_OK)
def remover_aluno_da_turma_route(
    turma_id: int,
    aluno_id: int,
    db: Session = Depends(get_db),
    _ = Depends(coordenador_required)
):
    sucesso = crud_turma.remover_aluno_da_turma(db, turma_id=turma_id, aluno_id=aluno_id)
    
    if not sucesso:
        raise HTTPException(status_code=404, detail="Aluno não encontrado ou não pertence a esta turma.")
        
    return {"message": f"Aluno removido da turma com sucesso."}