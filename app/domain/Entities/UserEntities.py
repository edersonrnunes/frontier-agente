from dataclasses import dataclass
from datetime import datetime, date


@dataclass
class Usuario:
    id: int | None
    username: str
    email: str
    ultimologin: datetime | None = datetime.now()
    hashed_password: str | None = None
    disabled: bool | None = False
