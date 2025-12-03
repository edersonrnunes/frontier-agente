from dataclasses import dataclass
from datetime import date


@dataclass
class Pessoa:
    id: int | None
    nome_completo: str
    cpf: str
    data_nascimento: date | None = None
    usuario_id: int