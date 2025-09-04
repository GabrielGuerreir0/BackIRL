from sqlalchemy.orm import Session
from models.turma import Turma
from schemas.turma import TurmaCreate

def criar_turma(db: Session, turma: TurmaCreate):
    db_turma = Turma(**turma.dict())
    db.add(db_turma)
    db.commit()
    db.refresh(db_turma)
    return db_turma

def listar_turmas(db: Session):
    return db.query(Turma).all()

def atualizar_turma(db: Session, turma_id: int, turma_update: dict):
    db_turma = db.query(Turma).filter(Turma.id == turma_id).first()
    if not db_turma:
        return None
    
    for key, value in turma_update.items():
        if hasattr(db_turma, key):
            setattr(db_turma, key, value)
    
    db.commit()
    db.refresh(db_turma)
    return db_turma

def excluir_turma(db: Session, turma_id: int):
    db_turma = db.query(Turma).filter(Turma.id == turma_id).first()
    if not db_turma:
        return None
    
    db.delete(db_turma)
    db.commit()
    return {"message": "Turma excluída com sucesso"} 