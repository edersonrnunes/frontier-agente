"""Endpoints para autenticação."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.application.Dto import TokenDtos, UserDtos
from app.domain.Entities import UserEntities
from app.application.UseCase import AutenticacaoUseCases as auth_use_cases
from app.web.dependencies import (
    get_autenticate_user_use_case,
    get_current_active_user,
    get_create_user_use_case,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post("/token", response_model=TokenDtos.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_use_case: Annotated[
        auth_use_cases.AutenticateUser, Depends(get_autenticate_user_use_case)
    ],
):
    """
    Endpoint para login e obtenção de token JWT.

    Forneça `username` e `password` para receber um `access_token`.
    """
    user = auth_use_case.execute(
        username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth_use_cases.CriaTokenAcesso.create_access_token(
        data={"sub": user.username}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=UserDtos.Usuario)
async def read_users_me(
    current_user: Annotated[UserEntities.Usuario, Depends(get_current_active_user)],
):
    """
    Endpoint protegido para obter informações do usuário logado.
    Requer um token JWT válido no header `Authorization: Bearer <token>`.
    """
    return current_user


@router.post("/register", response_model=UserDtos.Usuario, status_code=status.HTTP_201_CREATED, summary="Registrar um novo usuário")
async def register_user(
    user_in: UserDtos.UsuarioCreate,
    create_user_use_case: Annotated[auth_use_cases.CreateUser, Depends(get_create_user_use_case)],
):
    """
    Cria um novo usuário no sistema. A senha será armazenada de forma segura.
    """
    return create_user_use_case.execute(user_in)