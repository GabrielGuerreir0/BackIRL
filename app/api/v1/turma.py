from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import SessionLocal
from schemas.turma import TurmaCreate, TurmaOut
from crud import turma as crud_turma
from crud import educador as crud_educador
from typing import List
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.security import decode_access_token

router = APIRouter()

# Agora usando HTTPBearer
bearer_scheme = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def coordenador_required(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials  # pega só o JWT do header Authorization
    payload = decode_access_token(token)
    if not payload or payload.get("role") != "coordenador":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Apenas coordenadores podem cadastrar turmas."
        )
    return payload  # retorna payload caso precise na rota

@router.post("/", response_model=TurmaOut)
def criar_turma(
    turma: TurmaCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(coordenador_required)
):
    # Verifica se o educador existe apenas se educador_id for fornecido
    if turma.educador_id:
        educador = db.query(crud_educador.Educador).filter_by(id=turma.educador_id).first()
        if not educador:
            raise HTTPException(status_code=404, detail="Educador responsável não encontrado")
    return crud_turma.criar_turma(db, turma)

@router.get("/", response_model=List[TurmaOut])
def listar_turmas(db: Session = Depends(get_db)):
    return crud_turma.listar_turmas(db)

@router.put("/{turma_id}", response_model=TurmaOut)
def atualizar_turma(
    turma_id: int,
    turma_update: dict,
    db: Session = Depends(get_db),
    _: dict = Depends(coordenador_required)
):
    return crud_turma.atualizar_turma(db, turma_id, turma_update)

@router.delete("/{turma_id}")
def excluir_turma(
    turma_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(coordenador_required)
):
    return crud_turma.excluir_turma(db, turma_id)
