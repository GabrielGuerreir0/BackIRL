from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base

class Aluno(Base):
    """
    Entidade Aluno consolidada, incluindo informações pessoais, de responsável,
    escolares, de saúde e de documentação.
    """
    __tablename__ = "alunos"

    # --- Informações Pessoais ---
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    data_nascimento = Column(Date, nullable=False)
    rg = Column(String, nullable=True)
    cpf = Column(String, unique=True, nullable=False)
    certidao_nascimento = Column(String, nullable=True)
    
    # --- Informações do Responsável ---
    nome_responsavel = Column(String, nullable=True)
    parentesco_responsavel = Column(String, nullable=True)
    rg_responsavel = Column(String, nullable=True)
    cpf_responsavel = Column(String, nullable=True)
    
    # --- Informações Escolares ---
    escola = Column(String, nullable=False)
    serie = Column(String, nullable=False)
    turno = Column(String, nullable=False)

    # --- Informações de Saúde e Aprendizagem ---
    nivel_leitura_escrita = Column(String, nullable=True)
    quadro_cronico_saude = Column(Boolean, default=False)
    quadro_cronico = Column(String, nullable=True)
    
    apresenta_transtorno_psicologico = Column(Boolean, default=False)
    transtorno_psicologico = Column(String, nullable=True)

    possui_deficiencia_transtorno_aprendizagem = Column(Boolean, default=False)
    deficiencia_transtorno_aprendizagem = Column(String, nullable=True)

    possui_acompanhamento_especializado = Column(Boolean, default=False)
    acompanhamento_especializado = Column(String, nullable=True)

    # --- Informações de Medicação ---
    pode_tomar_medicacao = Column(Boolean, default=False)
    descricao_medicacao = Column(String, nullable=True)
    dosagem_medicacao = Column(String, nullable=True)

     # Adicionando a chave estrangeira para a Turma
    turma_id = Column(Integer, ForeignKey("turmas.id"), nullable=True)

    # Relação de volta para a turma
    turma = relationship("Turma", back_populates="alunos")
    
    # --- Upload de Documentos ---
    documentos = relationship("Documento", back_populates="aluno", cascade="all, delete-orphan")

    turma = relationship("Turma", back_populates="alunos")

class Documento(Base):
    """
    Entidade para armazenar informações sobre documentos PDF associados a um aluno.
    """
    __tablename__ = "documentos"

    id = Column(Integer, primary_key=True, index=True)
    nome_arquivo = Column(String, nullable=False)
    caminho_arquivo = Column(String, nullable=False)

    # Chave estrangeira que conecta o documento a um aluno.
    aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=False)
    aluno = relationship("Aluno", back_populates="documentos")
