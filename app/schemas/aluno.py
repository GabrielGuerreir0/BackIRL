from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import date

# Schema simples para turma (sem referência circular)
class TurmaSimple(BaseModel):
    id: int
    nome: str
    
    class Config:
        from_attributes = True

# Schemas para a entidade Documento
class DocumentoBase(BaseModel):
    nome_arquivo: str
    caminho_arquivo: str

class DocumentoOut(DocumentoBase):
    id: int
    class Config:
        from_attributes = True

# Schemas para a entidade Aluno
class AlunoBase(BaseModel):
    # --- Informações Pessoais ---
    nome: str
    data_nascimento: date
    rg: Optional[str] = None
    cpf: str
    certidao_nascimento: Optional[str] = None
    
    # --- Informações do Responsável ---
    nome_responsavel: Optional[str] = None
    parentesco_responsavel: Optional[str] = None
    rg_responsavel: Optional[str] = None
    cpf_responsavel: Optional[str] = None
    
    # --- Informações Escolares ---
    escola: Optional[str] = None
    serie: Optional[str] = None
    turno: Optional[str] = None

    # Adicionando a chave estrangeira para a turma
    turma_id: Optional[int] = None

    # --- Informações de Saúde e Aprendizagem ---
    nivel_leitura_escrita: Optional[str] = None
    quadro_cronico_saude: Optional[bool] = False
    quadro_cronico: Optional[str] = None
    
    apresenta_transtorno_psicologico: Optional[bool] = False
    transtorno_psicologico: Optional[str] = None

    possui_deficiencia_transtorno_aprendizagem: Optional[bool] = False
    deficiencia_transtorno_aprendizagem: Optional[str] = None

    possui_acompanhamento_especializado: Optional[bool] = False
    acompanhamento_especializado: Optional[str] = None

    # --- Informações de Medicação ---
    pode_tomar_medicacao: Optional[bool] = False
    descricao_medicacao: Optional[str] = None
    dosagem_medicacao: Optional[str] = None

class AlunoCreate(AlunoBase):
    pass

class AlunoUpdate(AlunoBase):
    pass

class AlunoOut(AlunoBase):
    id: int
    # Use TurmaSimple em vez de TurmaOut para evitar referência circular
    turma: Optional[TurmaSimple] = None 
    documentos: List[DocumentoOut] = []
    
    class Config:
        from_attributes = True