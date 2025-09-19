from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base

class Turma(Base):
    __tablename__ = "turmas"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, unique=True)
    educador_id = Column(Integer, ForeignKey('educadores.id'), nullable=False, unique=True)

    educador = relationship(
        "Educador",
        back_populates="turma",
        uselist=False
    )
    
    alunos = relationship("Aluno", back_populates="turma")

    relatorios = relationship("Relatorio", back_populates="turma", cascade="all, delete-orphan")

    frequencias = relationship("RegistroFrequencia", back_populates="turma")