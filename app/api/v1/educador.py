from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from db.session import SessionLocal
from schemas.educador import EducadorCreate, EducadorOut, EducadorUpdate
from crud import educador as crud_educador
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from core.security import decode_access_token
from typing import List

router = APIRouter()

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
            detail="Apenas coordenadores podem cadastrar educadores."
        )
    return payload  # retorna o payload decodificado se precisar usar na rota

@router.post("/", response_model=EducadorOut, status_code=status.HTTP_201_CREATED)
def criar_educador_route(
    educador: EducadorCreate,
    db: Session = Depends(get_db),
    _ = Depends(coordenador_required)
):
    db_educador = crud_educador.get_educador_by_email(db, email=educador.email)
    if db_educador:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")
    return crud_educador.criar_educador(db, educador)


@router.get("/", response_model=List[EducadorOut])
def listar_educadores_route(
    db: Session = Depends(get_db),
    _ = Depends(coordenador_required)
):
    return crud_educador.listar_educadores(db)

@router.get("/by_email/{email}", response_model=EducadorOut)
def get_educador_by_email_route(email: str, db: Session = Depends(get_db)):
    educador = crud_educador.get_educador_by_email(db, email=email)
    if not educador:
        raise HTTPException(status_code=404, detail="Educador não encontrado")
    return educador

@router.get("/{educador_id}", response_model=EducadorOut)
def get_educador_route(
    educador_id: int, 
    db: Session = Depends(get_db)
):
    educador = crud_educador.get_educador(db, educador_id)
    if not educador:
        raise HTTPException(status_code=404, detail="Educador não encontrado")
    return educador

@router.put("/{educador_id}", response_model=EducadorOut)
def atualizar_educador_route(
    educador_id: int,
    educador_update: EducadorUpdate,
    db: Session = Depends(get_db),
    _ = Depends(coordenador_required)
):
    educador = crud_educador.atualizar_educador(db, educador_id, educador_update)
    if not educador:
        raise HTTPException(status_code=404, detail="Educador não encontrado")
    return educador

@router.delete("/{educador_id}")
def deletar_educador(
    educador_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(coordenador_required)
):
    sucesso = crud_educador.deletar_educador(db, educador_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Educador não encontrado")
    return {"detail": "Educador excluído com sucesso"}
