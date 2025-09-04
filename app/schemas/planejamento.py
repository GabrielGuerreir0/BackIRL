# schemas/planejamento.py
from pydantic import BaseModel
from datetime import date

class PlanejamentoBase(BaseModel):
    data_aula: date
    tema: str
    disciplina: str

class PlanejamentoCreate(PlanejamentoBase):
    educador_id: int

class PlanejamentoUpdate(PlanejamentoBase):
    pass

class PlanejamentoOut(PlanejamentoBase):
    id: int
    class Config:
        orm_mode = True
