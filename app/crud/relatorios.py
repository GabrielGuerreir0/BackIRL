from sqlalchemy.orm import Session
from datetime import date
from typing import List

# Importando os modelos
from models.relatorio import Relatorio
from models.educador import Educador
from models.turma import Turma

# Importando os schemas
from schemas.relatorio import RelatorioCreate, RelatorioUpdate


# --- Funções de CRUD Básicas ---

def get_relatorio(db: Session, relatorio_id: int) -> Relatorio | None:
    """Busca um único relatório pelo seu ID."""
    return db.query(Relatorio).filter(Relatorio.id == relatorio_id).first()

def get_relatorios(db: Session, skip: int = 0, limit: int = 100) -> List[Relatorio]:
    """Busca uma lista de relatórios com paginação."""
    return db.query(Relatorio).order_by(Relatorio.created_at.desc()).offset(skip).limit(limit).all()

def create_relatorio(db: Session, relatorio: RelatorioCreate) -> Relatorio:
    db_relatorio = Relatorio(**relatorio.model_dump())
    db.add(db_relatorio)
    db.commit()
    db.refresh(db_relatorio)
    return db_relatorio

def update_relatorio(
    db: Session,
    db_relatorio: Relatorio,
    relatorio_update: RelatorioUpdate
) -> Relatorio:
    """Atualiza os campos de um relatório existente."""
    update_data = relatorio_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_relatorio, key, value)
    db.commit()
    db.refresh(db_relatorio)
    return db_relatorio

def delete_relatorio(db: Session, relatorio_id: int) -> Relatorio | None:
    """Deleta um relatório do banco de dados pelo seu ID."""
    db_relatorio = get_relatorio(db, relatorio_id)
    if db_relatorio:
        db.delete(db_relatorio)
        db.commit()
    return db_relatorio


# --- Funções para Respostas Aninhadas ---

def get_educador_with_relatorios(db: Session, educador_id: int) -> Educador | None:
    """Busca um educador e seus relatórios associados."""
    return db.query(Educador).filter(Educador.id == educador_id).first()

def get_turma_with_relatorios(db: Session, turma_id: int) -> Turma | None:
    """Busca uma turma e seus relatórios associados."""
    return db.query(Turma).filter(Turma.id == turma_id).first()


# --- Funções de Busca por Data (Adicionadas) ---

def get_relatorios_by_date(db: Session, data: date) -> List[Relatorio]:
    """Retorna todos os relatórios de uma data específica."""
    return db.query(Relatorio).filter(Relatorio.data_relatorio == data).order_by(Relatorio.data_relatorio.desc()).all()

def get_relatorios_by_turma_and_date(db: Session, turma_id: int, data: date) -> List[Relatorio]:
    """Retorna todos os relatórios de uma turma em uma data específica."""
    return db.query(Relatorio).filter(
        Relatorio.turma_id == turma_id,
        Relatorio.data_relatorio == data
    ).order_by(Relatorio.data_relatorio.desc()).all()

def get_relatorios_by_educador_and_date(db: Session, educador_id: int, data: date) -> List[Relatorio]:
    """Retorna todos os relatórios de um educador em uma data específica."""
    return db.query(Relatorio).filter(
        Relatorio.educador_id == educador_id,
        Relatorio.data_relatorio == data
    ).order_by(Relatorio.data_relatorio.desc()).all()