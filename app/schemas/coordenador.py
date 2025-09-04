from pydantic import BaseModel, EmailStr

class CoordenadorBase(BaseModel):
    name: str
    email: EmailStr

class CoordenadorCreate(CoordenadorBase):
    password: str

class CoordenadorOut(CoordenadorBase):
    id: int

    class Config:
        orm_mode = True
