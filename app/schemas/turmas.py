from pydantic import BaseModel
from typing import Optional

class TurmaBase(BaseModel):
    nome: str
    educador_id: Optional[int] = None

class TurmaCreate(TurmaBase):
    pass

class TurmaOut(TurmaBase):
    id: int
    class Config:
        orm_mode = True 