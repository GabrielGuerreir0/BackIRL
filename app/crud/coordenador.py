from models.coordenador import Coordenador
from schemas.coordenador import CoordenadorCreate
from core.security import hash_password
from sqlalchemy.orm import Session

def create_coordenador(db: Session, coordenador: CoordenadorCreate):
    hashed_pw = hash_password(coordenador.password)
    db_coordenador = Coordenador(
        name=coordenador.name,
        email=coordenador.email,
        hashed_password=hashed_pw
    )
    db.add(db_coordenador)
    db.commit()
    db.refresh(db_coordenador)
    return db_coordenador
