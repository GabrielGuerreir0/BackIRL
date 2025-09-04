from models.assistente_social import Assistente
from schemas.assistente_social import AssistenteCreate
from core.security import hash_password
from sqlalchemy.orm import Session

def create_assistente(db: Session, assistente: AssistenteCreate):
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