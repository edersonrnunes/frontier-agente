from abc import ABC, abstractmethod
from typing import List

from app.domain.Entities import ItemEntities as entities


class ItemRepository(ABC):
    @abstractmethod
    def add(self, item: entities.Item) -> entities.Item:
        raise NotImplementedError

    @abstractmethod
    def listItens(self, skip: int = 0, limit: int = 100) -> List[entities.Item]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, item_id: int) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def update(self, item: entities.Item) -> entities.Item:
        raise NotImplementedError

    @abstractmethod
    def get_items_by_color(self, color: str) -> List[entities.Item]: 
        raise NotImplementedError