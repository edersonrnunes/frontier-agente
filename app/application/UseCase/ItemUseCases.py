from app.domain.Repositories import ItemRepositories
from app.application.Dto import ItemDtos
from app.domain.Entities import ItemEntities

class CreateItemUseCase:
    def __init__(self, item_repo: ItemRepositories.ItemRepository):
        self._repo = item_repo

    def execute(self, item_create: ItemDtos.ItemCreate) -> ItemEntities.Item:
        item_entity = ItemEntities.Item(
            id=None,
            name=item_create.name,
            description=item_create.description
        )
        return self._repo.add(item_entity)

class ListItemsUseCase:
    def __init__(self, item_repo: ItemRepositories.ItemRepository):
        self._repo = item_repo

    def execute(self, skip: int = 0, limit: int = 100) -> list[ItemEntities.Item]:
        return self._repo.listItens(skip=skip, limit=limit)
    
class GetItemsByColorUseCase:
    def __init__(self, item_repo: ItemRepositories.ItemRepository):
        self._repo = item_repo

    def execute(self, color: str) -> list[ItemEntities.Item]:
        return self._repo.get_items_by_color(color)
