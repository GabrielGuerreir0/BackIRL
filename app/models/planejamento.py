# models/planejamento.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base

class Planejamento(Base):
    __tablename__ = "planejamentos"

    id = Column(Integer, primary_key=True, index=True)
    data_aula = Column(Date, nullable=False)
    tema = Column(String, nullable=False)
    disciplina = Column(String, nullable=False)

    educador_id = Column(Integer, ForeignKey("educadores.id"), nullable=False)

    educador = relationship("Educador", back_populates="planejamentos")
