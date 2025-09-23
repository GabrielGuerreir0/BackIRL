# Em crud/assistente_social.py

from sqlalchemy.orm import Session
from typing import List

# Importando o modelo e os schemas
from models.assistente_social import AssistenteSocial
from schemas.assistente_social import AssistenteCreate, AssistenteUpdate
from core.security import hash_password


def get_assistente(db: Session, assistente_id: int) -> AssistenteSocial | None:
    """Busca um assistente social pelo ID."""
    return db.query(AssistenteSocial).filter(AssistenteSocial.id == assistente_id).first()


def get_assistente_by_email(db: Session, email: str) -> AssistenteSocial | None:
    """Busca um assistente social pelo email."""
    return db.query(AssistenteSocial).filter(AssistenteSocial.email == email).first()


def get_assistentes(db: Session, skip: int = 0, limit: int = 100) -> List[AssistenteSocial]:
    """Busca uma lista de assistentes sociais com paginação."""
    return db.query(AssistenteSocial).offset(skip).limit(limit).all()


def create_assistente(db: Session, assistente: AssistenteCreate) -> AssistenteSocial:
    """Cria um novo assistente social no banco de dados."""
    hashed_password = hash_password(assistente.password)
    
    db_assistente = AssistenteSocial(
        name=assistente.name,
        email=assistente.email,
        hashed_password=hashed_password
    )
    
    db.add(db_assistente)
    db.commit()
    db.refresh(db_assistente)
    
    return db_assistente


def update_assistente(
    db: Session,
    db_assistente: AssistenteSocial,
    assistente_in: AssistenteUpdate
) -> AssistenteSocial:
    """Atualiza os dados de um assistente social."""
    update_data = assistente_in.model_dump(exclude_unset=True)
    
    # Se a senha for enviada, faz o hash antes de salvar
    if "password" in update_data:
        hashed_pw = hash_password(update_data["password"])
        update_data["hashed_password"] = hashed_pw
        del update_data["password"]  # Remove a senha em texto plano
        
    for field, value in update_data.items():
        setattr(db_assistente, field, value)
        
    db.commit()
    db.refresh(db_assistente)
    return db_assistente


def delete_assistente(db: Session, assistente_id: int) -> AssistenteSocial | None:
    """Deleta um assistente social do banco de dados."""
    db_assistente = get_assistente(db, assistente_id)
    if db_assistente:
        db.delete(db_assistente)
        db.commit()
    return db_assistente