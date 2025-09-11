# /crud/auth.py

from sqlalchemy.orm import Session
from typing import Tuple, Optional, Union
from models.educador import Educador
from models.coordenador import Coordenador
from models.assistente_social import Assistente
from core.security import verify_password

UserModel = Union[Educador, Coordenador, Assistente]

def authenticate_user(db: Session, email: str, password: str) -> Tuple[Optional[UserModel], Optional[str]]:
    # Tenta como Educador
    educador = db.query(Educador).filter(Educador.email == email).first()
    if educador and verify_password(password, educador.hashed_password):
        return educador, "educador"

    # Tenta como Coordenador
    coordenador = db.query(Coordenador).filter(Coordenador.email == email).first()
    if coordenador and verify_password(password, coordenador.hashed_password):
        return coordenador, "coordenador"
        
    # Tenta como Assistente
    assistente = db.query(Assistente).filter(Assistente.email == email).first()
    if assistente and verify_password(password, assistente.hashed_password):
        return assistente, "assistente_social"

    return None, None