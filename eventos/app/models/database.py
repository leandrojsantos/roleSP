"""
Configuração do banco de dados
"""

from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import StaticPool

from ..config import DATABASE_URL, ENVIRONMENT

# Engine do banco de dados
engine = create_engine(
    DATABASE_URL,
    echo=ENVIRONMENT == "development",  # Log SQL em desenvolvimento
    poolclass=StaticPool if "sqlite" in DATABASE_URL else None,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
)


def create_db_and_tables():
    """Cria as tabelas no banco de dados"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Dependency para obter sessão do banco de dados"""
    with Session(engine) as session:
        yield session
