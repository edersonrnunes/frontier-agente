"""Módulo de injeção de dependências para a aplicação web."""

from typing import Annotated, Generator

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.infrastructure.database import session
from app.application.UseCase import AutenticacaoUseCases
from app.domain.Entities import UserEntities

from app.domain.Repositories import (
    ItemRepositories,
    UserRepositories,
)
from app.infrastructure.database.Repositories import (
    ItemRepositories,
    UserRepositories
)

### Dependências para repositórios e casos de uso
def get_db() -> Generator[Session, None, None]:
    """Obtém uma sessão do banco de dados."""
    db = session.SessionLocal()
    try:
        yield db
    finally:
        db.close()


### Dependências para Itens
def get_item_repository(
    db: Annotated[Session, Depends(get_db)]
) -> ItemRepositories.ItemRepositories:
    """Obtém o repositório de itens."""
    return ItemRepositories.SQLAlchemyItemRepository(db_session=db)


### Dependências para Autenticação
def get_autenticacao_repository(
    db: Annotated[Session, Depends(get_db)]
) -> UserRepositories.UserRepository:
    """Obtém o repositório de autenticação."""
    return UserRepositories.SQLAlchemyUserRepository(db_session=db)


def get_autenticate_user_use_case(
    repo: Annotated[UserRepositories.UserRepository, Depends(get_autenticacao_repository)]
) -> AutenticacaoUseCases.AutenticateUser:
    """Obtém o caso de uso para autenticar um usuário."""
    return AutenticacaoUseCases.AutenticateUser(user_repo=repo)


def get_current_user_use_case(
    repo: Annotated[UserRepositories.UserRepository, Depends(get_autenticacao_repository)]
) -> AutenticacaoUseCases.GetCurrentUser:
    """Obtém o caso de uso para buscar o usuário atual pelo token."""
    return AutenticacaoUseCases.GetCurrentUser(user_repo=repo)


def get_current_user(
    token: Annotated[str, Depends(AutenticacaoUseCases.oauth2_scheme)],
    use_case: Annotated[AutenticacaoUseCases.GetCurrentUser, Depends(get_current_user_use_case)]
) -> UserEntities.Usuario:
    """Dependência para obter o usuário atual a partir do token."""
    return use_case.execute(token=token)


def get_current_active_user(
    current_user: Annotated[UserEntities.Usuario, Depends(get_current_user)]
) -> UserEntities.Usuario:
    """Dependência para obter o usuário ativo atual."""
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_create_user_use_case(
    repo: Annotated[UserRepositories.UserRepository, Depends(get_autenticacao_repository)],
) -> AutenticacaoUseCases.CreateUser:
    """Obtém o caso de uso para criar um usuário."""
    return AutenticacaoUseCases.CreateUser(user_repo=repo)
