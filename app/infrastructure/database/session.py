import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError, DBAPIError
from dotenv import load_dotenv

load_dotenv(verbose=True)

## Código para utilizar Supabase como banco de dados PostgreSQL
# Fetch variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

# Construct the SQLAlchemy connection string
DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

# Create the SQLAlchemy engine
ENGINE = create_engine(DATABASE_URL)

# Test the connection
try:
    with ENGINE.connect() as connection:
        print("PostgreSQL connection successful!")
except OperationalError as exception:
    print("Could not connect to the database. Check connection parameters.")
    # Log the specific error for debugging
    print(f"Error details: {exception}")
except DBAPIError as exception:
    # Catch other DBAPI-related errors
    print("A database error occurred.")
    print(f"Error details: {exception}")
except Exception as exception:
    # Fallback for truly unexpected errors
    print(f"An unexpected error occurred: {exception}")
    # Re-raise the exception after logging if appropriate
    raise

## Descomentar se não utilizar Supabase ##
## Este código utiliza DB PostgreSQL utilizando containers Docker
## Conexão local para debug (Container local)
#SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost:5432/mydatabase"
## Conexão para utilizar dentro do Docker Compose
#SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/mydatabase")
#SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

#engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)
Base = declarative_base()
