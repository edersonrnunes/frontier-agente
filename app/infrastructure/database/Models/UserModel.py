from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.orm import relationship
from .PessoaModel import Pessoa

from app.infrastructure.database.session import Base


class Usuario(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True)
    ultimologin = Column(Date)
    hashed_password = Column(String, nullable=False)
    disabled = Column(Boolean, default=False)

    # Relacionamentos com outros modelos
    pessoas = relationship(Pessoa, back_populates="owner", cascade="all, delete-orphan")