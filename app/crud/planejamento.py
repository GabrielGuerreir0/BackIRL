# crud/crud_planejamento.py
from sqlalchemy.orm import Session
from models.planejamento import Planejamento
from schemas.planejamento import PlanejamentoCreate, PlanejamentoUpdate

def get_planejamentos_by_educador(db: Session, educador_id: int):
    return db.query(Planejamento).filter(Planejamento.educador_id == educador_id).all()

def create_planejamento(db: Session, planejamento: PlanejamentoCreate):
    db_obj = Planejamento(**planejamento.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_planejamento(db: Session, planejamento_id: int, planejamento_data: PlanejamentoUpdate):
    db_obj = db.query(Planejamento).get(planejamento_id)
    for key, value in planejamento_data.dict().items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_planejamento(db: Session, planejamento_id: int):
    db_obj = db.query(Planejamento).get(planejamento_id)
    db.delete(db_obj)
    db.commit()
