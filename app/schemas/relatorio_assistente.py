from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional

class AlunoSimpleOut(BaseModel):
    id: int
    nome: str

    model_config = ConfigDict(from_attributes=True)


class AssistenteSimpleOut(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class RelatorioBase(BaseModel):
    report: str
    aluno_id: int


class RelatorioCreate(RelatorioBase):
    pass


class RelatorioUpdate(BaseModel):
    report: Optional[str] = None


class RelatorioOut(RelatorioBase):
    id: int
    data_relatorio: date
    aluno: AlunoSimpleOut
    assistente: AssistenteSimpleOut
    
    model_config = ConfigDict(from_attributes=True)