from sqlalchemy.orm import Session
from models.aluno import Aluno
from schemas.aluno import AlunoCreate

def criar_aluno(db: Session, aluno: AlunoCreate):
    db_aluno = Aluno(**aluno.dict())
    db.add(db_aluno)
    db.commit()
    db.refresh(db_aluno)
    return db_aluno
