from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from db.base import Base
from datetime import date

class RelatorioAssistente(Base):
    __tablename__ = "relatorios_assistentes"

    id = Column(Integer, primary_key=True, index=True)
    report = Column(Text, nullable=False)
    data_relatorio = Column(Date, nullable=False, default=date.today)
    
    assistente_id = Column(Integer, ForeignKey('assistentes.id'), nullable=False)
    aluno_id = Column(Integer, ForeignKey('alunos.id'), nullable=False)

    assistente = relationship("AssistenteSocial", back_populates="relatorios")

    aluno = relationship("Aluno", back_populates="relatorios_assistente")