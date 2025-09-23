from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from db.base import Base

class Assistente(Base):
    __tablename__ = "assistentes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    codigo_recuperacao = Column(String, nullable=True)
    codigo_recuperacao_expiracao = Column(DateTime, nullable=True)

    relatorios = relationship("RelatorioAssistente", back_populates="assistente", cascade="all, delete-orphan")