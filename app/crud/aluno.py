from sqlalchemy import func, case, cast, Float, select
from sqlalchemy.orm import Session, joinedload
from models.aluno import Aluno, Documento
from schemas.aluno import AlunoCreate, AlunoUpdate, DocumentoBase
from typing import List, Optional
from core.enums import EnumSituacao, StatusFrequencia
from models.RegistroFrequencia import RegistroFrequencia

def get_aluno(db: Session, aluno_id: int):
    return db.query(Aluno)\
           .options(
               joinedload(Aluno.turma), 
               joinedload(Aluno.documentos),
               joinedload(Aluno.frequencias)  # <<< ALTERADO AQUI
           )\
           .filter(Aluno.id == aluno_id).first()

def get_aluno_by_cpf(db: Session, aluno_cpf: str):
    return db.query(Aluno)\
           .options(
               joinedload(Aluno.turma), 
               joinedload(Aluno.documentos),
               joinedload(Aluno.frequencias)  # <<< ALTERADO AQUI
           )\
           .filter(Aluno.cpf == aluno_cpf).first()

def get_alunos(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    search: Optional[str] = None,
    turma_id: Optional[int] = None,
    situacao: Optional[EnumSituacao] = None
) -> List[Aluno]:
    
    query = db.query(Aluno)

    # Filtro 1: Busca por nome (search)
    if search:
        query = query.filter(Aluno.nome.ilike(f"%{search}%"))

    # Filtro 2: ID da Turma
    if turma_id:
        query = query.filter(Aluno.turma_id == turma_id)

    # Filtro 3: Situação (lógica complexa)
    if situacao:
        # Subconsulta para calcular o percentual de ausência de cada aluno
        subquery = (
            select(
                RegistroFrequencia.aluno_id,
                (
                    cast(func.count(case((RegistroFrequencia.status == StatusFrequencia.ausente, 1),)), Float)
                    / cast(func.count(RegistroFrequencia.id), Float)
                    * 100.0
                ).label("percentual_ausencia"),
            )
            .group_by(RegistroFrequencia.aluno_id)
            .subquery()
        )
        
        # Junta a query principal com a subconsulta
        query = query.outerjoin(subquery, Aluno.id == subquery.c.aluno_id)

        # Pega o percentual, tratando alunos sem frequência como 0% de ausência
        percentual = func.coalesce(subquery.c.percentual_ausencia, 0)

        # Cria a mesma lógica da "situação" do schema, mas em SQL
        situacao_sql = case(
            (percentual <= 25, EnumSituacao.satisfatorio),
            (percentual < 50, EnumSituacao.atencao),
            else_=EnumSituacao.insatisfatorio
        )
        
        # Aplica o filtro da situação
        query = query.filter(situacao_sql == situacao)

    # Carrega os relacionamentos e aplica paginação
    return query.options(
        joinedload(Aluno.turma), 
        joinedload(Aluno.documentos),
        joinedload(Aluno.frequencias)
    ).offset(skip).limit(limit).all()

def criar_aluno(db: Session, aluno: AlunoCreate):
    """
    Cria um novo aluno no banco de dados, incluindo a associação com a turma.
    """
    aluno_data = aluno.model_dump(exclude_unset=True)
    db_aluno = Aluno(**aluno_data)

    db.add(db_aluno)
    db.commit()
    db.refresh(db_aluno)

    db_aluno.frequencias = []
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
    Atualiza as informações de um aluno existente, incluindo a associação com a turma.
    """
    db_aluno = get_aluno(db, aluno_id)
    if db_aluno:
        # Apenas atualiza os campos que foram enviados no objeto AlunoUpdate
        update_data = aluno_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
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

def get_documento(db: Session, documento_id: int):
    
    return db.query(Documento).filter(Documento.id == documento_id).first()