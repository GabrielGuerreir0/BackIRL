from pydantic import BaseModel, EmailStr
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class TurmaSimpleOut(BaseModel):
    id: int
    nome: str

    class Config:
        from_attributes = True

class EducadorBase(BaseModel):
    nome: str
    email: EmailStr
    telefone: str
    data_nascimento: str

class EducadorCreate(EducadorBase):
    password: str

class EducadorUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None
    data_nascimento: Optional[str] = None
    password: Optional[str] = None



class EducadorOut(EducadorBase):
    id: int
    turma: Optional[TurmaSimpleOut] = None

    model_config = ConfigDict(from_attributes=True)

class EducadorNameOut(EducadorBase):
    id: int
    nome: str

class EducadorLogin(BaseModel):
    username: EmailStr
    password: str

class TokenEducador(BaseModel):
    access_token: str
    token_type: str = "bearer"

class SolicitarRecuperacaoSenha(BaseModel):
    email: EmailStr

class ValidarCodigoRecuperacao(BaseModel):
    email: EmailStr
    codigo: str

class RedefinirSenha(BaseModel):
    email: EmailStr
    codigo: str
    nova_senha: str
