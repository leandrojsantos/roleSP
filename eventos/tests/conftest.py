"""
Configuração de testes
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlalchemy.pool import StaticPool

from eventos.app.main import app
from eventos.app.models import get_session


# Engine de teste (SQLite em memória)
test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


@pytest.fixture(scope="session")
def event_loop():
    """Cria event loop para testes assíncronos"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def session():
    """Cria sessão de banco de dados para testes"""
    SQLModel.metadata.create_all(test_engine)

    with Session(test_engine) as session:
        yield session

    SQLModel.metadata.drop_all(test_engine)


@pytest.fixture(scope="function")
def client(session):
    """Cria cliente de teste FastAPI"""

    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def sample_evento_data():
    """Dados de exemplo para eventos"""
    return {
        "titulo": "Teste Evento",
        "descricao": "Descrição do evento de teste",
        "data_inicio": "2024-12-31T20:00:00",
        "data_fim": "2024-12-31T23:00:00",
        "local": "Local de Teste",
        "cidade": "São Paulo",
        "estado": "SP",
        "endereco": "Rua Teste, 123",
        "preco": 50.0,
        "gratuito": False,
        "tipo": "música",
        "status": "ativo",
        "url_original": "https://teste.com/evento/1",
        "fonte": "teste.com",
        "tags": "teste, música, evento",
    }
