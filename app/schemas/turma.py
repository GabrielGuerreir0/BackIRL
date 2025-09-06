from pydantic import BaseModel, EmailStr
from typing import Optional, List

from .aluno import AlunoOut 

class EducadorSimpleOut(BaseModel):
    id: int
    nome: str
    email: EmailStr

    class Config:
        from_attributes = True

class TurmaBase(BaseModel):
    nome: str
    educador_id: int 

class TurmaCreate(TurmaBase):
    pass

class TurmaUpdate(BaseModel):
    nome: Optional[str] = None
    educador_id: Optional[int] = None

class TurmaOut(BaseModel):
    id: int
    nome: str
    educador: EducadorSimpleOut
    alunos: List[AlunoOut] = []
    class Config:
        from_attributes = True