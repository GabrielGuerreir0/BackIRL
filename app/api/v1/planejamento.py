# api/v1/planejamento.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import SessionLocal
from schemas.planejamento import *
from crud import planejamento as crud_planejamento


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/educador/{educador_id}", response_model=list[PlanejamentoOut])
def listar_planejamentos(educador_id: int, db: Session = Depends(get_db)):
    return crud_planejamento.get_planejamentos_by_educador(db, educador_id)

@router.post("/", response_model=PlanejamentoOut)
def criar_planejamento(planejamento: PlanejamentoCreate, db: Session = Depends(get_db)):
    return crud_planejamento.create_planejamento(db, planejamento)

@router.put("/{planejamento_id}", response_model=PlanejamentoOut)
def atualizar_planejamento(planejamento_id: int, dados: PlanejamentoUpdate, db: Session = Depends(get_db)):
    return crud_planejamento.update_planejamento(db, planejamento_id, dados)

@router.delete("/{planejamento_id}")
def deletar_planejamento(planejamento_id: int, db: Session = Depends(get_db)):
    crud_planejamento.delete_planejamento(db, planejamento_id)
    return {"msg": "Planejamento deletado com sucesso"}
