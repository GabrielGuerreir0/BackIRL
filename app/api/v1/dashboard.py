from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import SessionLocal
from models.aluno import Aluno
from models.educador import Educador

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/resumo")
def get_dashboard_data(db: Session = Depends(get_db)):
    total_alunos = db.query(Aluno).count()
    total_educadores = db.query(Educador).count()
    periodo_letivo = 2025

    return {
        "total_alunos": total_alunos,
        "total_educadores": total_educadores,
        "periodo_letivo": periodo_letivo
    }
