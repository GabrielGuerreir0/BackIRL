# Em schemas/assistente_social.py

from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class AssistenteBase(BaseModel):
    name: str
    email: EmailStr

class AssistenteCreate(AssistenteBase):
    password: str

# ADICIONADO: Schema para atualização, com todos os campos opcionais.
class AssistenteUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class AssistenteOut(AssistenteBase):
    id: int

    # AJUSTADO: Usando a sintaxe moderna do Pydantic V2.
    model_config = ConfigDict(from_attributes=True)