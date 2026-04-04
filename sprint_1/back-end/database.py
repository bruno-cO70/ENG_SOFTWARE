from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = (

    f"postgresql://{os.getenv('DB_user')}:"  #Busca user .env 
    f"{os.getenv('DB_password')}@" #Busca senha .env
    f"{os.getenv('DB_host')}:" #Busca endereço .env
    f"{os.getenv('DB_port')}/" #Busca porta conexão .env
    f"{os.getenv('DB_name')}" #Busca nome no .env
    )

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()