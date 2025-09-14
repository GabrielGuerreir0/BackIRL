from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from db.base import Base

class Relatorio(Base):
  __tablename__ = "relatorios"

  id = Column(Integer, primary_key=True, index=True)
  report = Column(String, nullable=False)
  data_relatorio = Column(Date, nullable=False)
  educador_id = Column(Integer, ForeignKey('educadores.id'), nullable=False) 
  turma_id = Column(Integer, ForeignKey('turmas.id'), nullable=False)

  educador = relationship("Educador", back_populates="relatorios")

  turma = relationship("Turma", back_populates="relatorios")
