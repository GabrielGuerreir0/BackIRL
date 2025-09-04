from sqlalchemy.orm import Session, joinedload
from models.turma import Turma
from models.aluno import Aluno
from schemas.turma import TurmaCreate, TurmaUpdate
from typing import List, Optional

def criar_turma(db: Session, turma: TurmaCreate):
    """
    Cria uma nova turma no banco de dados.
    """
    db_turma = Turma(**turma.model_dump())
    db.add(db_turma)
    db.commit()
    db.refresh(db_turma)
    return db_turma

def get_turma(db: Session, turma_id: int):
    """
    Busca uma turma pelo ID, incluindo a lista de alunos associados.
    """
    # Usando joinedload para carregar os alunos em uma única consulta
    return db.query(Turma).options(joinedload(Turma.alunos)).filter(Turma.id == turma_id).first()

def listar_turmas(db: Session, skip: int = 0, limit: int = 100) -> List[Turma]:
    """
    Retorna uma lista de todas as turmas com paginação.
    """
    # Usando joinedload para carregar os alunos em uma única consulta por otimização
    return db.query(Turma).options(joinedload(Turma.alunos)).offset(skip).limit(limit).all()

def atualizar_turma(db: Session, turma_id: int, turma_update: TurmaUpdate):
    """
    Atualiza as informações de uma turma existente.
    """
    db_turma = get_turma(db, turma_id)
    if not db_turma:
        return None
    
    update_data = turma_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_turma, key, value)
    
    db.commit()
    db.refresh(db_turma)
    return db_turma

def excluir_turma(db: Session, turma_id: int):
    """
    Exclui uma turma do banco de dados.
    A exclusão de alunos associados deve ser tratada separadamente,
    a menos que a relação seja configurada para CASCADE.
    """
    db_turma = get_turma(db, turma_id)
    if not db_turma:
        return None
    
    db.delete(db_turma)
    db.commit()
    return {"message": "Turma excluída com sucesso"}



def adicionar_aluno_a_turma(db: Session, turma_id: int, aluno_id: int):
    """
    Adiciona um aluno a uma turma, atualizando a chave estrangeira do aluno.
    """
    db_turma = get_turma(db, turma_id)
    db_aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()

    if not db_turma:
        return {"error": "Turma não encontrada"}, 404
    if not db_aluno:
        return {"error": "Aluno não encontrado"}, 404

    db_aluno.turma_id = turma_id
    db.commit()
    db.refresh(db_aluno)
    return db_aluno

def remover_aluno_da_turma(db: Session, aluno_id: int):
    """
    Remove um aluno de uma turma, definindo o turma_id como nulo.
    """
    db_aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    
    if not db_aluno:
        return {"error": "Aluno não encontrado"}, 404

    db_aluno.turma_id = None
    db.commit()
    db.refresh(db_aluno)
    return db_aluno