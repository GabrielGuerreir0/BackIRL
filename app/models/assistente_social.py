from sqlalchemy import Column, Integer, String
from db.base import Base

class Assistente(Base):
    __tablename__ = "assistentes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)