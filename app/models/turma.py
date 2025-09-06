from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base

class Turma(Base):
    __tablename__ = "turmas"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, unique=True)
    educador_id = Column(Integer, ForeignKey('educadores.id'), nullable=False)

    educador = relationship("Educador", back_populates="turmas")
    
    alunos = relationship("Aluno", back_populates="turma")