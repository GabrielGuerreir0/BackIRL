from sqlalchemy.orm import Session
from datetime import date
from typing import List, Optional
from collections import defaultdict
from models.RegistroFrequencia import RegistroFrequencia 
from models.aluno import Aluno
from models.turma import Turma
import schemas.RegistroFrequencia as schemas

def upsert_frequencia_batch(db: Session, turma_id: int, data: date, frequencias: List[schemas.FrequenciaCreate]):
    aluno_ids = [f.aluno_id for f in frequencias]
    registros_existentes_map = {reg.aluno_id: reg for reg in db.query(RegistroFrequencia).filter(RegistroFrequencia.aluno_id.in_(aluno_ids), RegistroFrequencia.data == data)}
    novos_registros = []
    for frequencia_in in frequencias:
        if registro_existente := registros_existentes_map.get(frequencia_in.aluno_id):
            registro_existente.status = frequencia_in.status
        else:
            novos_registros.append(RegistroFrequencia(aluno_id=frequencia_in.aluno_id, turma_id=turma_id, data=data, status=frequencia_in.status))
    if novos_registros:
        db.add_all(novos_registros)
    db.commit()
    return len(frequencias)

def get_frequencia_by_turma_and_dia(db: Session, turma_id: int, data: date) -> List[RegistroFrequencia]:
    return db.query(RegistroFrequencia).join(Aluno).filter(RegistroFrequencia.turma_id == turma_id, RegistroFrequencia.data == data).all()

def get_historico_frequencia_by_aluno(db: Session, aluno_id: int) -> List[RegistroFrequencia]:
    return db.query(RegistroFrequencia).join(Turma).filter(RegistroFrequencia.aluno_id == aluno_id).order_by(RegistroFrequencia.data.desc()).all()

def get_frequencia_by_aluno_and_dia(db: Session, aluno_id: int, data: date) -> Optional[RegistroFrequencia]:
    return db.query(RegistroFrequencia).filter(RegistroFrequencia.aluno_id == aluno_id, RegistroFrequencia.data == data).first()

""" def get_historico_completo_da_turma(db: Session, turma_id: int):
    turma = db.query(Turma).filter(Turma.id == turma_id).first()
    if not turma: return None
    registros = db.query(RegistroFrequencia).join(Aluno).filter(RegistroFrequencia.turma_id == turma_id).order_by(RegistroFrequencia.data.desc()).all()
    registros_por_data = defaultdict(list)
    for reg in registros:
        registros_por_data[reg.data].append({"aluno_id": reg.aluno.id, "nome_completo": reg.aluno.nome, "status": reg.status.value})
    return {"turma_nome": turma.nome, "registros": [{"data": data, "frequencias": freqs} for data, freqs in registros_por_data.items()]}
 """
def get_historico_completo_por_turma(db: Session, turma_id: int) -> List[RegistroFrequencia]:
    return db.query(RegistroFrequencia)\
        .join(Aluno)\
        .filter(RegistroFrequencia.turma_id == turma_id)\
        .order_by(RegistroFrequencia.data.desc(), Aluno.nome.asc())\
        .all()

def get_frequencia_por_turma_e_intervalo_de_datas(
    db: Session, 
    turma_id: int, 
    data_inicio: date, 
    data_fim: date
) -> List[RegistroFrequencia]:
    return db.query(RegistroFrequencia)\
        .join(Aluno)\
        .filter(
            RegistroFrequencia.turma_id == turma_id,
            RegistroFrequencia.data >= data_inicio,
            RegistroFrequencia.data <= data_fim
        )\
        .order_by(RegistroFrequencia.data.desc(), Aluno.nome.asc())\
        .all()