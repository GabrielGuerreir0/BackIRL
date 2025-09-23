from sqlalchemy import Column, Integer, String, DateTime
from db.base import Base

class Coordenador(Base):
    __tablename__ = "coordinators"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    codigo_recuperacao = Column(String)
    codigo_recuperacao_expiracao = Column(DateTime)
