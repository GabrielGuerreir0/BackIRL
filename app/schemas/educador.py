from pydantic import BaseModel, EmailStr

class EducadorBase(BaseModel):
    nome: str
    email: EmailStr
    telefone: str
    turma_responsavel: str
    cpf: str
    data_nascimento: str

class EducadorCreate(EducadorBase):
    password: str

class EducadorOut(EducadorBase):
    id: int

    class Config:
        orm_mode = True

class EducadorLogin(BaseModel):
    username: EmailStr
    password: str

class TokenEducador(BaseModel):
    access_token: str
    token_type: str = "bearer"
