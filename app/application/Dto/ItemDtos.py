from pydantic import BaseModel, ConfigDict


# Schema base para o Item, com os campos comuns.
class ItemBase(BaseModel):
    name: str
    description: str | None = None
    color: str | None = None


# Schema usado para criar um Item (não precisa de ID, pois é gerado pelo DB).
class ItemCreate(ItemBase):
    pass


# Schema usado para ler um Item do DB (inclui o ID).
class Item(ItemBase):
    id: int

    model_config = ConfigDict(from_attributes=True)  # Permite que o Pydantic leia dados de modelos ORM e dataclasses.
