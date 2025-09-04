from sqlalchemy import Column, Integer, String, ForeignKey
from db.base import Base

class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    data_nascimento = Column(String, nullable=False)
    sexo = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    naturalidade = Column(String, nullable=False)
    cor_raca = Column(String, nullable=False)
    endereco = Column(String, nullable=False)
    turma_id = Column(Integer, ForeignKey('turmas.id'), nullable=False)
    # Responsável
    nome_responsavel = Column(String, nullable=True)
    parentesco_responsavel = Column(String, nullable=True)
    cpf_responsavel = Column(String, nullable=True)
    telefone_responsavel = Column(String, nullable=True)
    email_responsavel = Column(String, nullable=True)
    # Informações adicionais
    necessidades_especiais = Column(String, nullable=True)
    alergias = Column(String, nullable=True)
    tipo_sanguineo = Column(String, nullable=True)
    # Uploads
    documento_crianca = Column(String, nullable=True)
    documento_responsavel = Column(String, nullable=True)
