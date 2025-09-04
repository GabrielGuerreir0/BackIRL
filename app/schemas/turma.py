from pydantic import BaseModel, ConfigDict
from typing import Optional, List

# Não importa AlunoOut aqui, use uma referência de string
# from .aluno import AlunoOut 

class TurmaBase(BaseModel):
    nome: str
    educador_id: Optional[int] = None

class TurmaCreate(TurmaBase):
    pass

class TurmaUpdate(TurmaBase):
    pass

class TurmaOut(TurmaBase):
    id: int
    # Use 'AlunoOut' como uma string para referenciar a classe
    alunos: List['AlunoOut'] = []
    
    class Config:
        from_attributes = True

# Importe AlunoOut após a definição de TurmaOut para que model_rebuild possa encontrá-la
from .aluno import AlunoOut 

# Chame model_rebuild para resolver a referência circular
TurmaOut.model_rebuild()