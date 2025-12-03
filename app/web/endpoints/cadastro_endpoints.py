import logging
logger = logging.getLogger(__name__)

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated

from app.application.UseCase import (
    ItemUseCases
)

from app.application.Dto import (
    ItemDtos
)

from app.domain.Entities import (
    UserEntities
)

from app.domain.Repositories import (
    ItemRepositories
)

from app.web.dependencies import (
    get_item_repository,
    get_current_active_user
)

router = APIRouter()

@router.get("/")
def read_root():
    """
    Este endpoint retorna uma mensagem de boas-vindas.
    """
    return {"message": "Bem-vindo à Frontier AI!"}

@router.get("/health", tags=["Health"])
def health_check(
    repo: ItemRepositories.ItemRepository = Depends(get_item_repository)
):
    item_use_cases = ItemUseCases.ListItemsUseCase(repo)
    items = item_use_cases.execute(skip=0, limit=10)
    if not items:
        return {"status": "Database connection failed"}, status.HTTP_500_INTERNAL_SERVER_ERROR
    return {"status": "ok"}

## Item
@router.post("/items/", response_model=ItemDtos.Item, status_code=status.HTTP_201_CREATED, tags=["Items"])
def create_item(
    current_user: Annotated[UserEntities.Usuario, Depends(get_current_active_user)],
    item_dto: ItemDtos.ItemCreate,
    repo: ItemRepositories.ItemRepository = Depends(get_item_repository),
):
    print(f"User '{current_user.username}' creating item with data: {item_dto}")
    item_use_cases = ItemUseCases.CreateItemUseCase(repo)
    result = item_use_cases.execute(item_dto)
    return result

@router.get("/items/", response_model=list[ItemDtos.Item], tags=["Items"])
def read_items(
    current_user: Annotated[UserEntities.Usuario, Depends(get_current_active_user)],
    skip: int = 0, limit: int = 100,
    repo: ItemRepositories = Depends(get_item_repository)
):
    print(f"User '{current_user.username}' reading items with skip={skip} and limit={limit}")
    item_use_cases = ItemUseCases.ListItemsUseCase(repo)
    items = item_use_cases.execute(skip=skip, limit=limit)
    return items

@router.get("/items/color/{color}", response_model=list[ItemDtos.Item], tags=["Items"])
def read_items_by_color(
    current_user: Annotated[UserEntities.Usuario, Depends(get_current_active_user)],
    color: str,
    repo: ItemRepositories.ItemRepository = Depends(get_item_repository)
):
    print(f"User '{current_user.username}' reading items with color={color}")
    item_use_cases = ItemUseCases.GetItemsByColorUseCase(repo)
    items = item_use_cases.execute(color=color)
    return items
