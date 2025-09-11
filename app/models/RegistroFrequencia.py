# /models/registro_frequencia.py

from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base
import enum

class StatusFrequencia(str, enum.Enum):
    presente = "presente"
    ausente = "ausente"
    justificado = "justificado"

class RegistroFrequencia(Base):
    __tablename__ = "registros_frequencia"

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=False)
    turma_id = Column(Integer, ForeignKey("turmas.id"), nullable=False)
    data = Column(Date, nullable=False)
    status = Column(Enum(StatusFrequencia), nullable=False)

    aluno = relationship("Aluno", back_populates="frequencias")
    turma = relationship("Turma", back_populates="frequencias")