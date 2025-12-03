from fastapi import FastAPI

#from app.infrastructure.database.Models import UserModel
from app.infrastructure.database.session import Base, ENGINE

# Import all models to ensure they are registered with the Base metadata
from app.web.endpoints.cadastro_endpoints import router as api_router
from app.web.endpoints.auth import router as auth_router

# Cria as tabelas no banco de dados (se não existirem)
# Em um ambiente de produção, você provavelmente usaria Alembic para gerenciar migrações.
Base.metadata.create_all(bind=ENGINE)

app = FastAPI(
    title="API com DDD e Autenticação",
    description="Uma API de exemplo com FastAPI, PostgreSQL, DDD e OAuth2.",
    version="1.0.0",
)

app.include_router(api_router)
app.include_router(auth_router)
