from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.assistente_social import AssistenteCreate, AssistenteOut
from crud import assistente_social as crud_assistente
from db.session import SessionLocal
from core.security import verify_password, create_access_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=AssistenteOut)
def create_assistente(assistente: AssistenteCreate, db: Session = Depends(get_db)):
    return crud_assistente.create_assistente(db, assistente)
