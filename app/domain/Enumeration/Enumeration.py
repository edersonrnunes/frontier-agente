from enum import Enum


class TipoLinha(Enum):
    CELULAR = 1
    FIXO = 2
    WHATSAPP = 3 
    
class TipoUso(Enum):
    PESSOAL = 1
    COMERCIAL = 2

class TipoEmpresa(Enum):
    PARTICULAR = 1
    COMERCIAL = 2