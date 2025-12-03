from sqlalchemy.orm import Session

from app.domain.Entities import UserEntities as entities
from app.domain.Repositories.UserRepositories import UserRepository
from app.infrastructure.database.Models import UserModel as model

def _to_entity(db_usuario: model) -> entities.Usuario:
    """Mapeia o modelo SQLAlchemy para a entidade de domínio."""
    return entities.Usuario(
        id=db_usuario.id,
        username=db_usuario.username,
        email=db_usuario.email,
        ultimologin=db_usuario.ultimologin,
        hashed_password=db_usuario.hashed_password,
        disabled=db_usuario.disabled,
    )

class SQLAlchemyUserRepository(UserRepository):
    """Implementação do repositório de usuários usando SQLAlchemy."""   
    def __init__(self, db_session: Session):
        self._db = db_session

    def add(self, usuario: entities.Usuario) -> entities.Usuario:
        db_usuario = model.Usuario(**usuario.__dict__)
        self._db.add(db_usuario)
        self._db.commit()
        self._db.refresh(db_usuario)
        return _to_entity(db_usuario)


    def get_by_id(self, usuario_id: int) -> entities.Usuario | None:
        """Busca um usuário pelo ID no banco de dados."""
        db_usuario = self._db.query(model.Usuario).filter(model.Usuario.id == usuario_id).first()
        return _to_entity(db_usuario) if db_usuario else None


    def get_by_username(self, username: str) -> entities.Usuario | None:
        """Busca um usuário pelo nome de usuário no banco de dados."""
        user_model = self._db.query(model.Usuario).filter(model.Usuario.username == username).first()
        if user_model:
            return _to_entity(user_model)
        return None


    def get_by_email(self, email: str) -> entities.Usuario | None:
        """Busca um usuário pelo email no banco de dados."""
        user_model = self._db.query(model.Usuario).filter(model.Usuario.email == email).first()
        if user_model:
            return _to_entity(user_model)
        return None


    def update(self, usuario: entities.Usuario) -> entities.Usuario:
        """Atualiza um usuário existente no banco de dados."""
        db_usuario = self._db.query(model.Usuario).filter(model.Usuario.id == usuario.id).first()
        if not db_usuario:
            # Idealmente, o caso de uso já verificou a existência, mas é uma boa prática.
            raise ValueError(f"Usuário com id {usuario.id} não encontrado para atualização.")

        # Atualiza os campos a partir da entidade
        for key, value in usuario.__dict__.items():
            setattr(db_usuario, key, value)

        self._db.commit()
        return _to_entity(db_usuario)
