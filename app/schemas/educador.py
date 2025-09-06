from pydantic import BaseModel, EmailStr
from typing import List, Optional


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
    turmas: List[TurmaSimpleOut] = []

    class Config:
        orm_mode = True

class EducadorLogin(BaseModel):
    username: EmailStr
    password: str

class TokenEducador(BaseModel):
    access_token: str
    token_type: str = "bearer"
