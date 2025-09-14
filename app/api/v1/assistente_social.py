# Em routers/assistente_social.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Importando schemas e o módulo CRUD
from schemas.assistente_social import AssistenteCreate, AssistenteOut, AssistenteUpdate
from crud import assistente_social as crud_assistente
from db.session import get_db # Assumindo que seu get_db está aqui

router = APIRouter()

@router.post("/", response_model=AssistenteOut, status_code=status.HTTP_201_CREATED)
def create_assistente(assistente: AssistenteCreate, db: Session = Depends(get_db)):
    db_assistente = crud_assistente.get_assistente_by_email(db, email=assistente.email)
    if db_assistente:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    return crud_assistente.create_assistente(db=db, assistente=assistente)

@router.get("/", response_model=List[AssistenteOut])
def read_assistentes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    assistentes = crud_assistente.get_assistentes(db, skip=skip, limit=limit)
    return assistentes

@router.get("/{assistente_id}", response_model=AssistenteOut)
def read_assistente(assistente_id: int, db: Session = Depends(get_db)):
    db_assistente = crud_assistente.get_assistente(db, assistente_id=assistente_id)
    if db_assistente is None:
        raise HTTPException(status_code=404, detail="Assistente social não encontrado")
    return db_assistente

@router.put("/{assistente_id}", response_model=AssistenteOut)
def update_assistente(
    assistente_id: int,
    assistente_in: AssistenteUpdate,
    db: Session = Depends(get_db)
):
    db_assistente = crud_assistente.get_assistente(db, assistente_id=assistente_id)
    if db_assistente is None:
        raise HTTPException(status_code=404, detail="Assistente social não encontrado")
    
    updated_assistente = crud_assistente.update_assistente(
        db=db, db_assistente=db_assistente, assistente_in=assistente_in
    )
    return updated_assistente

@router.delete("/{assistente_id}", response_model=AssistenteOut)
def delete_assistente(assistente_id: int, db: Session = Depends(get_db)):
    db_assistente = crud_assistente.delete_assistente(db, assistente_id=assistente_id)
    if db_assistente is None:
        raise HTTPException(status_code=404, detail="Assistente social não encontrado")
    return db_assistente