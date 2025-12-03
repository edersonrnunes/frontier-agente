"""Módulo para hashing e verificação de senhas."""

from passlib.context import CryptContext

# Adicionamos "plaintext" como um esquema válido, mas o marcamos como obsoleto.
# Isso permite que o passlib verifique senhas em texto plano, mas as identifique
# como necessitando de atualização para bcrypt.
pwd_context = CryptContext(schemes=["bcrypt", "plaintext"], deprecated="plaintext")


class Hash:
    """Classe para manipulação de hashes de senha."""

    @staticmethod
    def bcrypt(password: str) -> str:
        """Gera o hash de uma senha."""
        return pwd_context.hash(password)

    @staticmethod
    def verify(hashed_password: str, plain_password: str) -> bool:
        """Verifica se a senha corresponde ao hash."""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def verify_and_update(hashed_password: str, plain_password: str) -> tuple[bool, str | None]:
        """Verifica a senha e, se necessário, retorna um novo hash atualizado."""
        return pwd_context.verify_and_update(plain_password, hashed_password)