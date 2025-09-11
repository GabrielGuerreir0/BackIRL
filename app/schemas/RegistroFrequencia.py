# /schemas/registro_frequencia.py

from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import List
from models.RegistroFrequencia import StatusFrequencia 

# --- Schemas para CRIAÇÃO ---
class FrequenciaCreate(BaseModel):
    aluno_id: int
    status: StatusFrequencia

class FrequenciaCreateList(BaseModel):
    frequencias: List[FrequenciaCreate]

# --- Schemas para LEITURA (Respostas da API) ---
class FrequenciaAlunoResponse(BaseModel):
    aluno_id: int
    nome_completo: str
    status: StatusFrequencia

class FrequenciaHistoricoAluno(BaseModel):
    data: date
    status: StatusFrequencia
    turma_nome: str

# --- Schemas para o Histórico Completo da Turma ---
class FrequenciaDetalheAluno(BaseModel):
    aluno_id: int
    nome_completo: str
    status: StatusFrequencia

class RegistroDiario(BaseModel):
    data: date
    frequencias: List[FrequenciaDetalheAluno]

class HistoricoTurmaResponse(BaseModel):
    turma_nome: str
    registros: List[RegistroDiario]

class FrequenciaAlunoResponse(BaseModel):
    
    aluno_id: int
    nome_completo: str
    data: date
    status: StatusFrequencia
    
# --- Schema Completo do Modelo ---
class Frequencia(BaseModel):
    id: int
    aluno_id: int
    turma_id: int
    data: date
    status: StatusFrequencia

    model_config = ConfigDict(from_attributes=True)