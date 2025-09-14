from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import date, datetime # ADICIONADO: Import para os tipos de data

# --- Schemas Base ---
# Schema para representar um educador de forma simples em outros DTOs.
class EducadorNameOut(BaseModel):
    id: int
    nome: str

# Schema para representar uma turma de forma simples em outros DTOs.
class TurmaNameOut(BaseModel):
    id: int
    nome: str


# --- Schemas de Relatório ---

class RelatorioBase(BaseModel):
    report: str
    data_relatorio: date # ADICIONADO: Data a qual o relatório se refere.
    educador_id: int
    turma_id: int

class RelatorioCreate(RelatorioBase):
    pass

class RelatorioUpdate(BaseModel):
    report: Optional[str] = None
    data_relatorio: Optional[date] = None # ADICIONADO: Permite corrigir a data.

# Schema de saída para um relatório completo
class RelatorioOut(RelatorioBase):
    id: int
    data_relatorio: date # ADICIONADO: Data de criação automática.
    educador: EducadorNameOut
    turma: TurmaNameOut

    model_config = ConfigDict(from_attributes=True)

# Schema para um relatório dentro da lista de um Educador
class RelatorioForEducadorOut(BaseModel):
    id: int
    report: str
    data_relatorio: date # ADICIONADO
    turma: TurmaNameOut

    model_config = ConfigDict(from_attributes=True)

# Schema para um relatório dentro da lista de uma Turma
class RelatorioForTurmaOut(BaseModel):
    id: int
    report: str
    data_relatorio: date # ADICIONADO
    educador: EducadorNameOut

    model_config = ConfigDict(from_attributes=True)

class RelatorioForDateOut(BaseModel):
    id: int
    report: str
    turma: TurmaNameOut
    educador: EducadorNameOut

    model_config = ConfigDict(from_attributes=True)


# --- Schemas de Resposta Aninhados ---

# Schema para a resposta completa de uma Turma com seus relatórios
class TurmaWithRelatoriosOut(TurmaNameOut):
    relatorios: List[RelatorioForTurmaOut] = []

    model_config = ConfigDict(from_attributes=True)

# Schema para a resposta completa de um Educador com seus relatórios
class EducadorWithRelatoriosOut(EducadorNameOut):
    relatorios: List[RelatorioForEducadorOut] = []

    model_config = ConfigDict(from_attributes=True)