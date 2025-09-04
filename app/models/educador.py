from sqlalchemy import Column, Integer, String
from db.base import Base
from sqlalchemy.orm import relationship

class Educador(Base):
    __tablename__ = "educadores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    telefone = Column(String, nullable=False)
    turma_responsavel = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    data_nascimento = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    planejamentos = relationship("Planejamento", back_populates="educador", cascade="all, delete-orphan")
