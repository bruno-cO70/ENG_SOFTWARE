from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from urllib.parse import quote_plus
import os


load_dotenv()

DB_PASSWORD = quote_plus(os.getenv('DB_PASSWORD')) #Função para converter caracteres em um formato seguro, Adicionado por conta de não conseguir ler o @ da senha

DATABASE_URL = (
    f"postgresql://{os.getenv('DB_USER')}:"  #Busca user .env 
    f"{DB_PASSWORD}@" 
    f"{os.getenv('DB_HOST')}:" #Busca endereço .env
    f"{os.getenv('DB_PORT')}/" #Busca porta conexão .env
    f"{os.getenv('DB_NAME')}" #Busca nome no .env
    )

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()