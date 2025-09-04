from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.coordenador import CoordenadorCreate, CoordenadorOut
from crud import coordenador as crud_coordenador
from db.session import SessionLocal
from core.security import verify_password, create_access_token


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=CoordenadorOut)
def create_coordenador(coordenador: CoordenadorCreate, db: Session = Depends(get_db)):
    return crud_coordenador.create_coordenador(db, coordenador)

