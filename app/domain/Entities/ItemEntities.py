from dataclasses import dataclass


@dataclass
class Item:
    id: int | None
    name: str
    description: str | None = None
    color: str | None = None