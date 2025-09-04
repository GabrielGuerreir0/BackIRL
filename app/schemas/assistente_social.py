from pydantic import BaseModel, EmailStr

class AssistenteBase(BaseModel):
    name: str
    email: EmailStr

class AssistenteCreate(AssistenteBase):
    password: str

class AssistenteOut(AssistenteBase):
    id: int

    class Config:
        orm_mode = True
