from sqlalchemy import Column, Integer, String
from db.base import Base
from sqlalchemy.orm import relationship

class Educador(Base):
    __tablename__ = "educadores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    telefone = Column(String, nullable=False)
    data_nascimento = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    turmas = relationship("Turma", back_populates="educador")

    # A relação com planejamentos permanece a mesma
    planejamentos = relationship("Planejamento", back_populates="educador", cascade="all, delete-orphan")