from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Obtenha o caminho absoluto do diretório atual do script
current_directory = Path(__file__).resolve().parent

# Concatene o caminho do banco de dados ao diretório atual
database_path = current_directory / "pair_mms.db"

# Crie a URL do banco de dados usando o caminho absoluto
SQLALCHEMY_DATABASE_URL = f"sqlite:///{database_path}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Certifique-se de criar todas as tabelas do banco de dados
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
