# frontierai Template

Esse é o template para estruturar sua API REST utilizando os princípios do Domain-Driven Design (DDD). Isso tornará sua aplicação mais robusta, escalável e alinhada com as regras de negócio.

Vou refatorar o projeto fornecido para seguir uma arquitetura em camadas, um padrão comum em DDD, separando as responsabilidades em:

## Como executar o projeto

# Execute no terminal:

Navegue para dentro do diretório do projeto

```bash
python -m venv .venv
source .venv/Scripts/activate  # No Windows: .venv\Scripts\activate
source .venv/bin/deactivate # Para desativar o ambiente virtual
```

# Instal dependencias

pip install -r requirements.txt

# Rodar o projeto:

docker run --name some-postgres -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=mydatabase -p 5432:5432 -d postgres

# Executar local para desenvolvimento e debug
uvicorn main:app --reload


# docker build local
docker build -it frontierai-backend .
# Rodar o projeto local:
docker run -it -p 8000:8000 frontierai-backend:latest /bin/bash

# Executar o container do último commit
# Pull última versão
docker pull edersonnunes/frontierai-backend:latest
# Executar container local
docker run -it -p 8000:8000 edersonnunes/frontierai-backend:latest /bin/bash

export user=postgres.hcywzsyhaykbgppvnykt 
export password=6O1izkH9ENXi5azG 
export host=aws-1-us-east-2.pooler.supabase.com 
export port=5432 
export dbname=postgres
export SECRET_KEY="36d60414ee9a499ced4b489761646081a7a50faeaa904a1f11d9adfe9027fccf"
export ALGORITHM="HS256"
export ACCESS_TOKEN_EXPIRE_MINUTES=30

## Como executar os testes

# Execute no terminal a partir do diretório raiz:

```bash
pytest
```

# Para iniciar o projeto é necessário ter instalado na máquina

1. python3
2. pip
3. Docker CE

# extensions VSCode

1. Container Tools
2. Docker
3. Pylance
4. Python
5. Python Debugger
6. Python Extension Pack
7. Python Ident

# Domain (Domínio):

O coração da aplicação. Contém as entidades, objetos de valor e a lógica de negócio principal, sem depender de detalhes de infraestrutura (como banco de dados ou frameworks web).
# Application (Aplicação):

Orquestra as tarefas e casos de uso. Utiliza o domínio para executar as ações solicitadas pelas camadas externas (como a API).
# Infrastructure (Infraestrutura):

Contém os detalhes técnicos, como o framework web (FastAPI), implementações de repositórios (SQLAlchemy), configuração de banco de dados, etc.
A nova estrutura de arquivos ficará assim:
.
├── app/
│   ├── __init__.py
│   ├── application/
│   │   ├── __init__.py
│   │   ├── dtos.py
│   │   └── use_cases.py
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── entities.py
│   │   └── repositories.py
│   └── infrastructure/
│       ├── __init__.py
│       ├── database/
│       │   ├── __init__.py
│       │   ├── models.py
│       │   ├── repositories.py
│       │   └── session.py
│       └── web/
│           ├── __init__.py
│           ├── dependencies.py
│           └── endpoints.py
├── .env
├── docker-compose.yml
├── Dockerfile
├── main.py
└── requirements.txt

## Documen

https://fastapi.tiangolo.com/tutorial/response-model/

# docker compose

docker-compose up --build
docker-compose down

# criando container PostgreSQL para debug local

POSTGRES_USER=user
POSTGRES_PASSWORD=password

docker run --name some-postgres -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=mydatabase -p 5432:5432 -d postgres

Como Executar
Salve os arquivos acima na estrutura de pastas correta.
Instale o uvicorn, que é um servidor ASGI para rodar sua aplicação:
bash
pip install "uvicorn[standard]"
A partir do diretório raiz do seu projeto (frontierai), execute o servidor:
bash
uvicorn main:app --reload
Agora, a mágica acontece! Você pode acessar a documentação interativa do Swagger UI no seu navegador em:

http://127.0.0.1:8000/docs
E a documentação alternativa do ReDoc em:

http://127.0.0.1:8000/redoc
Lá você poderá ver e interagir com seus endpoints POST /items/ e GET /items/, com schemas, exemplos e a capacidade de testá-los diretamente pelo navegador.

# Para gerar uma chave secreta aleatória segura, use o comando:

openssl rand -hex 32

