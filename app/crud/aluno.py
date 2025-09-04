from sqlalchemy.orm import Session
from models.aluno import Aluno, Documento
from schemas.aluno import AlunoCreate, AlunoUpdate, DocumentoBase
from typing import List, Optional

def get_aluno(db: Session, aluno_id: int):
    """
    Busca um aluno pelo ID, incluindo seus documentos.
    """
    return db.query(Aluno).filter(Aluno.id == aluno_id).first()

def get_aluno_by_cpf(db: Session, aluno_cpf: str):
    """
    Busca um aluno pelo CPF, incluindo seus documentos.
    """
    return db.query(Aluno).filter(Aluno.cpf == aluno_cpf).first()

def get_alunos(db: Session, skip: int = 0, limit: int = 100) -> List[Aluno]:
    """
    Retorna uma lista de todos os alunos, com paginação.
    """
    return db.query(Aluno).offset(skip).limit(limit).all()

def criar_aluno(db: Session, aluno: AlunoCreate):
    """
    Cria um novo aluno no banco de dados.
    """
    # A lógica de documentos é removida daqui, pois será tratada em outra função
    db_aluno = Aluno(**aluno.model_dump())
    db.add(db_aluno)
    db.commit()
    db.refresh(db_aluno)
    return db_aluno

def criar_documento(db: Session, aluno_id: int, documento: DocumentoBase):
    """
    Associa um documento a um aluno existente no banco de dados.
    """
    db_documento = Documento(**documento.model_dump(), aluno_id=aluno_id)
    db.add(db_documento)
    db.commit()
    db.refresh(db_documento)
    return db_documento

def atualizar_aluno(db: Session, aluno_id: int, aluno_update: AlunoUpdate):
    """
    Atualiza as informações de um aluno existente.
    Este método lida apenas com os campos do Aluno e não com a lista de Documentos.
    """
    db_aluno = get_aluno(db, aluno_id)
    if db_aluno:
        # Apenas atualiza os campos que foram enviados
        for key, value in aluno_update.model_dump(exclude_unset=True).items():
            setattr(db_aluno, key, value)
            
        db.commit()
        db.refresh(db_aluno)
    return db_aluno

def deletar_aluno(db: Session, aluno_id: int):
    """
    Deleta um aluno do banco de dados pelo ID.
    O relacionamento configurado com `cascade="all, delete-orphan"`
    garante que os documentos relacionados também serão deletados.
    """
    db_aluno = get_aluno(db, aluno_id)
    if db_aluno:
        db.delete(db_aluno)
        db.commit()
        return True
    return False

def deletar_documento(db: Session, documento_id: int):
    """
    Deleta um documento do banco de dados pelo seu ID.
    """
    db_documento = db.query(Documento).filter(Documento.id == documento_id).first()
    if db_documento:
        db.delete(db_documento)
        db.commit()
        return True
    return False