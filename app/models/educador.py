from sqlalchemy import Column, Integer, String, Date, DateTime
from db.base import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class Educador(Base):
    __tablename__ = "educadores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    telefone = Column(String, nullable=False)
    data_nascimento = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    codigo_recuperacao = Column(String)
    codigo_recuperacao_expiracao = Column(DateTime)
    
    turma = relationship(
        "Turma",
        back_populates="educador",
        uselist=False
    )


    planejamentos = relationship("Planejamento", back_populates="educador", cascade="all, delete-orphan")

    relatorios = relationship("Relatorio", back_populates="educador", cascade="all, delete-orphan")