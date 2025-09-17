from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from models.relatorio_assistente import RelatorioAssistente
from schemas.relatorio_assistente import RelatorioCreate, RelatorioUpdate


def criar_relatorio(db: Session, relatorio: RelatorioCreate, assistente_id: int) -> RelatorioAssistente:
    """Cria um novo relatório no banco de dados."""
    db_relatorio = RelatorioAssistente(
        **relatorio.model_dump(),
        assistente_id=assistente_id
    )
    db.add(db_relatorio)
    db.commit()
    db.refresh(db_relatorio)
    return db_relatorio

# --- READ ---

def get_relatorio(db: Session, relatorio_id: int) -> Optional[RelatorioAssistente]:
    """Busca um único relatório pelo seu ID."""
    return db.query(RelatorioAssistente)\
             .options(joinedload(RelatorioAssistente.assistente), joinedload(RelatorioAssistente.aluno))\
             .filter(RelatorioAssistente.id == relatorio_id).first()

# --- NOVA FUNÇÃO ADICIONADA ---
def get_relatorios(db: Session, skip: int = 0, limit: int = 100) -> List[RelatorioAssistente]:
    """
    Busca todos os relatórios do sistema, com paginação.
    Útil para uma visão geral de administrador.
    """
    return db.query(RelatorioAssistente)\
             .options(joinedload(RelatorioAssistente.assistente), joinedload(RelatorioAssistente.aluno))\
             .order_by(RelatorioAssistente.data_relatorio.desc())\
             .offset(skip)\
             .limit(limit)\
             .all()

def get_relatorios_por_aluno(db: Session, aluno_id: int, skip: int = 0, limit: int = 100) -> List[RelatorioAssistente]:
    """Busca todos os relatórios associados a um aluno específico, com paginação."""
    return db.query(RelatorioAssistente)\
             .filter(RelatorioAssistente.aluno_id == aluno_id)\
             .options(joinedload(RelatorioAssistente.assistente), joinedload(RelatorioAssistente.aluno))\
             .order_by(RelatorioAssistente.data_relatorio.desc())\
             .offset(skip)\
             .limit(limit)\
             .all()

# --- UPDATE ---

def atualizar_relatorio(db: Session, relatorio_id: int, relatorio_update: RelatorioUpdate) -> Optional[RelatorioAssistente]:
    """Atualiza um relatório existente no banco de dados."""
    db_relatorio = get_relatorio(db, relatorio_id)
    if not db_relatorio:
        return None

    update_data = relatorio_update.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_relatorio, key, value)
    
    db.add(db_relatorio)
    db.commit()
    db.refresh(db_relatorio)
    return db_relatorio

# --- DELETE ---

def deletar_relatorio(db: Session, relatorio_id: int) -> bool:
    """
    Deleta um relatório do banco de dados.
    ✅ AJUSTE: Reutiliza a função get_relatorio para consistência.
    """
    db_relatorio = get_relatorio(db, relatorio_id=relatorio_id)
    if db_relatorio:
        db.delete(db_relatorio)
        db.commit()
        return True
    return False