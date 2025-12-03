from abc import ABC, abstractmethod
from typing import List

from app.domain.Entities import PessoaEntities as entities


class PessoaRepository(ABC):
    @abstractmethod
    def add(self, pessoa: entities.Pessoa) -> entities.Pessoa:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, pessoa_id: int) -> entities.Pessoa | None:
        raise NotImplementedError

    @abstractmethod
    def list(self, skip: int = 0, limit: int = 100) -> List[entities.Pessoa]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, pessoa_id: int) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def update(self, pessoa: entities.Pessoa) -> entities.Pessoa:
        raise NotImplementedError
