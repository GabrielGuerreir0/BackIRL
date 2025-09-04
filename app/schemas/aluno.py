from pydantic import BaseModel
from typing import Optional

class AlunoBase(BaseModel):
    nome: str
    data_nascimento: str
    sexo: str
    cpf: str
    naturalidade: str
    cor_raca: str
    endereco: str
    turma_id: int
    # Responsável
    nome_responsavel: Optional[str] = None
    parentesco_responsavel: Optional[str] = None
    cpf_responsavel: Optional[str] = None
    telefone_responsavel: Optional[str] = None
    email_responsavel: Optional[str] = None
    # Informações adicionais
    necessidades_especiais: Optional[str] = None
    alergias: Optional[str] = None
    tipo_sanguineo: Optional[str] = None
    # Uploads (armazenar caminho do arquivo)
    documento_crianca: Optional[str] = None
    documento_responsavel: Optional[str] = None

class AlunoCreate(AlunoBase):
    pass

class AlunoOut(AlunoBase):
    id: int
    class Config:
        orm_mode = True
