# Em crud/assistente_social.py

from sqlalchemy.orm import Session
from typing import List

# Importando o modelo e os schemas
from models.assistente_social import Assistente
from schemas.assistente_social import AssistenteCreate, AssistenteUpdate
from core.security import hash_password

# --- Funções de Leitura (Read) ---
# Adicione esta função ao seu CRUD de assistente

def get_assistente(db: Session, assistente_id: int) -> Assistente | None:
    """Busca um único assistente social pelo seu ID."""
    return db.query(Assistente).filter(Assistente.id == assistente_id).first()

def get_assistente_by_email(db: Session, email: str) -> Assistente | None:
    return db.query(Assistente).filter(Assistente.email == email).first()

def get_assistentes(db: Session, skip: int = 0, limit: int = 100) -> List[Assistente]:
    """Busca uma lista de assistentes sociais com paginação."""
    return db.query(Assistente).offset(skip).limit(limit).all()


# --- Função de Criação (Create) ---

def create_assistente(db: Session, assistente: AssistenteCreate) -> Assistente:
    """Cria um novo assistente social no banco de dados."""
    hashed_pw = hash_password(assistente.password)
    db_assistente = Assistente(
        name=assistente.name,
        email=assistente.email,
        hashed_password=hashed_pw
    )
    db.add(db_assistente)
    db.commit()
    db.refresh(db_assistente)
    return db_assistente


# --- Função de Atualização (Update) ---

def update_assistente(
    db: Session,
    db_assistente: Assistente,
    assistente_in: AssistenteUpdate
) -> Assistente:
    """Atualiza os dados de um assistente social."""
    update_data = assistente_in.model_dump(exclude_unset=True)

    # Se a senha for enviada, faz o hash antes de salvar
    if "password" in update_data:
        hashed_pw = hash_password(update_data["password"])
        update_data["hashed_password"] = hashed_pw
        del update_data["password"] # Remove a senha em texto plano

    for field, value in update_data.items():
        setattr(db_assistente, field, value)

    db.commit()
    db.refresh(db_assistente)
    return db_assistente


# --- Função de Deleção (Delete) ---

def delete_assistente(db: Session, assistente_id: int) -> Assistente | None:
    """Deleta um assistente social do banco de dados."""
    db_assistente = get_assistente(db, assistente_id)
    if db_assistente:
        db.delete(db_assistente)
        db.commit()
    return db_assistente