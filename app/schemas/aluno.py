from pydantic import BaseModel, ConfigDict, computed_field, Field
from typing import Optional, List
from datetime import date
from schemas.RegistroFrequencia import Frequencia
from models.RegistroFrequencia import StatusFrequencia# Corrigido o import para o nome do arquivo

# --- Schemas que não mudam ---

# Schema simples para turma (sem referência circular)
class TurmaSimpleOut(BaseModel):
    id: int
    nome: str
    
    class Config:
        from_attributes = True

# Schemas para a entidade Documento
class DocumentoBase(BaseModel):
    nome_arquivo: str
    caminho_arquivo: str

class DocumentoOut(DocumentoBase):
    id: int
    class Config:
        from_attributes = True

# Schema Base com todos os campos do banco
class AlunoBase(BaseModel):
    # --- Informações Pessoais ---
    nome: str
    data_nascimento: date
    rg: Optional[str] = None
    cpf: str
    certidao_nascimento: Optional[str] = None
    
    # --- Informações do Responsável ---
    nome_responsavel: Optional[str] = None
    parentesco_responsavel: Optional[str] = None
    rg_responsavel: Optional[str] = None
    cpf_responsavel: Optional[str] = None
    
    # --- Informações Escolares ---
    escola: Optional[str] = None
    serie: Optional[str] = None
    turno: Optional[str] = None
    turma_id: Optional[int] = None

    # --- Informações de Saúde e Aprendizagem ---
    nivel_leitura_escrita: Optional[str] = None
    quadro_cronico_saude: Optional[bool] = False
    quadro_cronico: Optional[str] = None
    apresenta_transtorno_psicologico: Optional[bool] = False
    transtorno_psicologico: Optional[str] = None
    possui_deficiencia_transtorno_aprendizagem: Optional[bool] = False
    deficiencia_transtorno_aprendizagem: Optional[str] = None
    possui_acompanhamento_especializado: Optional[bool] = False
    acompanhamento_especializado: Optional[str] = None

    # --- Informações de Medicação ---
    pode_tomar_medicacao: Optional[bool] = False
    descricao_medicacao: Optional[str] = None
    dosagem_medicacao: Optional[str] = None

class AlunoCreate(AlunoBase):
    pass

class AlunoUpdate(AlunoBase):
    pass

class AlunoOut(AlunoBase):
    id: int
    turma: Optional[TurmaSimpleOut] = None 
    documentos: List[DocumentoOut] = []
    
    class Config:
        from_attributes = True

class AlunoComSituacaoOut(AlunoOut):
    # O campo 'frequencias' agora é definido aqui, onde ele é realmente usado.
    # exclude=True ainda é importante para não incluí-lo no JSON final.
    frequencias: List[Frequencia] = Field(default=[], exclude=True)

    @computed_field
    @property
    def percentual_ausencia(self) -> float:
        # A lógica aqui continua a mesma e vai funcionar perfeitamente.
        if not self.frequencias:
            return 0.0
        
        total_aulas = len(self.frequencias)
        total_ausencias = sum(1 for f in self.frequencias if f.status == StatusFrequencia.ausente)
        
        if total_aulas == 0:
            return 0.0
            
        percentual = (total_ausencias / total_aulas) * 100
        return round(percentual, 2)

    @computed_field
    @property
    def situacao(self) -> str:
        percentual = self.percentual_ausencia

        if percentual <= 25:
            return "Satisfatório"
        elif 25 < percentual < 50:
            return "Atenção"
        else: # percentual >= 50
            return "Insatisfatório"
