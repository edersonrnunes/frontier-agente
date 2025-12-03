from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime

class UsuarioBase(BaseModel):
    username: str
    email: EmailStr
    ultimologin: datetime | None
    disabled: bool | None = False

# Schema usado para criar um usuário, recebendo a senha em texto plano.
class UsuarioCreate(UsuarioBase):
    password: str

# Schema usado para ler um usuário do DB (não expõe a senha).
class Usuario(UsuarioBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class UserInDB(UsuarioBase):
    """Modelo de entidade de usuário como armazenado no banco de dados."""
    hashed_password: str
