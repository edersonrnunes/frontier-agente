import os
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone


import app.infrastructure.security.token as token_service
import app.infrastructure.security.hashing as hashing

from app.application.Dto import UserDtos
from app.domain.Entities import UserEntities
from app.domain.Repositories import UserRepositories


ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


class AutenticateUser:
    def __init__(self, user_repo: UserRepositories.UserRepository):
        self._user_repo = user_repo
    
    def execute(self, username: str, password: str) -> Optional[UserEntities.Usuario]:
        """Executa a lógica de autenticação e atualiza o hash se necessário."""
        user = self._user_repo.get_by_username(username)
        if not user:
            return None

        verified, new_hash = self.verify_and_update_password(
            password, user.hashed_password
        )

        if not verified:
            return None

        if new_hash:
            # O hash foi atualizado, precisamos salvar o novo hash no banco.
            user.hashed_password = new_hash
            self._user_repo.update(user)

        return user
    
    @staticmethod
    def verify_and_update_password(plain_password: str, hashed_password: str) -> tuple[bool, str | None]:
        return hashing.Hash.verify_and_update(hashed_password, plain_password)


class GetCurrentUser:
    def __init__(self, user_repo: UserRepositories.UserRepository):
        self._user_repo = user_repo

    def execute(self, token: str) -> UserEntities.Usuario:
        """Decodifica o token e retorna o usuário."""
        try:
            payload = token_service.decode_access_token(token)
            username: str = payload.get("sub")
            if username is None:
                raise token_service.credentials_exception()
        except InvalidTokenError:
            raise token_service.credentials_exception()

        user = self._user_repo.get_by_username(username=username)
        if user is None:
            raise token_service.credentials_exception()
        return user


class CriaTokenAcesso:
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = token_service.create_access_token(to_encode)
        return encoded_jwt

    @staticmethod
    def get_password_hash(password: str) -> str:
        return hashing.Hash.bcrypt(password)


class CreateUser:
    """Caso de uso para criar um novo usuário."""

    def __init__(self, user_repo: UserRepositories.UserRepository):
        self._user_repo = user_repo

    def execute(self, user_create: UserDtos.UsuarioCreate) -> UserEntities.Usuario:
        """Cria um novo usuário com senha hasheada."""
        if self._user_repo.get_by_username(user_create.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuário já foi registrado",
            )
        
        if self._user_repo.get_by_email(user_create.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já foi registrado",
            )

        hashed_password = CriaTokenAcesso.get_password_hash(user_create.password)
        user_entity = UserEntities.Usuario(
            id=None,  # O ID será gerado pelo banco de dados
            hashed_password=hashed_password,
            disabled=False,  # Por padrão, o usuário é criado ativo
            **user_create.model_dump(exclude={"password", "disabled"}),
        )
        return self._user_repo.add(user_entity)
