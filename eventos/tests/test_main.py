"""
Testes para a aplicação principal do roleSP
"""

from fastapi.testclient import TestClient
from eventos.app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Testa o endpoint raiz"""
    response = client.get("/")
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "timestamp" in data
    assert data["version"] == "1.0.0"


def test_health_endpoint():
    """Testa o endpoint de health check"""
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert "status" in data
    assert "uptime" in data
    assert "timestamp" in data
    assert data["status"] == "OK"


def test_info_endpoint():
    """Testa o endpoint de informações"""
    response = client.get("/info")
    assert response.status_code == 200

    data = response.json()
    assert "name" in data
    assert "version" in data
    assert "environment" in data
    assert "timestamp" in data
    assert data["version"] == "1.0.0"


def test_docs_endpoint():
    """Testa se a documentação está disponível"""
    response = client.get("/docs")
    assert response.status_code == 200


def test_redoc_endpoint():
    """Testa se o ReDoc está disponível"""
    response = client.get("/redoc")
    assert response.status_code == 200


def test_openapi_endpoint():
    """Testa se o schema OpenAPI está disponível"""
    response = client.get("/openapi.json")
    assert response.status_code == 200

    data = response.json()
    assert "openapi" in data
    assert "info" in data
    assert data["info"]["title"] == "EventRadar"
    assert data["info"]["version"] == "1.0.0"
