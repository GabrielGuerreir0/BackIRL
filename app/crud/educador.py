from sqlalchemy.orm import Session, joinedload
from models.educador import Educador
from schemas.educador import EducadorCreate, EducadorOut
from core.security import hash_password, verify_password

def criar_educador(db: Session, educador: EducadorCreate):
    hashed_pw = hash_password(educador.password)
    db_educador = Educador(
        nome=educador.nome,
        email=educador.email,
        telefone=educador.telefone,
        data_nascimento=educador.data_nascimento,
        hashed_password=hashed_pw
    )
    db.add(db_educador)
    db.commit()
    db.refresh(db_educador)
    return db_educador

def listar_educadores(db: Session):
    return db.query(Educador).options(joinedload(Educador.turmas)).all()

def autenticar_educador(db: Session, email: str, password: str):
    educador = db.query(Educador).filter(Educador.email == email).first()
    if not educador:
        return None
    if not verify_password(password, educador.hashed_password):
        return None
    return educador

def atualizar_educador(db: Session, educador_id: int, dados: dict):
    educador = db.query(Educador).filter(Educador.id == educador_id).first()
    if not educador:
        return None
    for key, value in dados.items():
        if key == 'password':
            setattr(educador, 'hashed_password', hash_password(value))
        elif hasattr(educador, key):
            setattr(educador, key, value)
    db.commit()
    db.refresh(educador)
    return educador

def deletar_educador(db: Session, educador_id: int):
    educador = db.query(Educador).filter(Educador.id == educador_id).first()
    if not educador:
        return False
    db.delete(educador)
    db.commit()
    return True
def get_educador(db: Session, educador_id: int):
    return db.query(Educador).options(joinedload(Educador.turmas)).filter(Educador.id == educador_id).first()

def get_educador_by_email(db: Session, email: str):
    return db.query(Educador).options(joinedload(Educador.turmas)).filter(Educador.email == email).first()