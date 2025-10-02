"""
Testes da API
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime


def test_root_endpoint(client: TestClient):
    """Testa endpoint raiz"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Welcome to EventRadar!"
    assert data["version"] == "1.0.0"


def test_health_check(client: TestClient):
    """Testa endpoint de health check"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "OK"
    assert "uptime" in data
    assert "timestamp" in data


def test_info_endpoint(client: TestClient):
    """Testa endpoint de informações"""
    response = client.get("/info")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "EventRadar"
    assert data["version"] == "1.0.0"
    assert "environment" in data


def test_listar_eventos_vazio(client: TestClient):
    """Testa listagem de eventos quando não há eventos"""
    response = client.get("/eventos/")
    assert response.status_code == 200
    data = response.json()
    assert data == []


def test_criar_evento(client: TestClient, sample_evento_data):
    """Testa criação de evento"""
    response = client.post("/eventos/", json=sample_evento_data)
    assert response.status_code == 200
    data = response.json()
    assert data["titulo"] == sample_evento_data["titulo"]
    assert data["cidade"] == sample_evento_data["cidade"]
    assert data["id"] is not None


def test_criar_evento_duplicado(client: TestClient, sample_evento_data):
    """Testa criação de evento duplicado"""
    # Criar primeiro evento
    response1 = client.post("/eventos/", json=sample_evento_data)
    assert response1.status_code == 200

    # Tentar criar evento com mesma URL
    response2 = client.post("/eventos/", json=sample_evento_data)
    assert response2.status_code == 400
    assert "já existe" in response2.json()["detail"]["message"]


def test_obter_evento_por_id(client: TestClient, sample_evento_data):
    """Testa obtenção de evento por ID"""
    # Criar evento
    create_response = client.post("/eventos/", json=sample_evento_data)
    evento_id = create_response.json()["id"]

    # Obter evento
    response = client.get(f"/eventos/{evento_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == evento_id
    assert data["titulo"] == sample_evento_data["titulo"]


def test_obter_evento_inexistente(client: TestClient):
    """Testa obtenção de evento inexistente"""
    response = client.get("/eventos/999")
    assert response.status_code == 404
    assert "não encontrado" in response.json()["detail"]["message"]


def test_atualizar_evento(client: TestClient, sample_evento_data):
    """Testa atualização de evento"""
    # Criar evento
    create_response = client.post("/eventos/", json=sample_evento_data)
    evento_id = create_response.json()["id"]

    # Atualizar evento
    update_data = {"titulo": "Evento Atualizado"}
    response = client.put(f"/eventos/{evento_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["titulo"] == "Evento Atualizado"


def test_deletar_evento(client: TestClient, sample_evento_data):
    """Testa deleção de evento"""
    # Criar evento
    create_response = client.post("/eventos/", json=sample_evento_data)
    evento_id = create_response.json()["id"]

    # Deletar evento
    response = client.delete(f"/eventos/{evento_id}")
    assert response.status_code == 200
    assert "Deletado com sucesso" in response.json()["message"]

    # Verificar se foi deletado
    get_response = client.get(f"/eventos/{evento_id}")
    assert get_response.status_code == 404
    assert "não encontrado" in get_response.json()["detail"]["message"]


def test_filtrar_eventos_por_cidade(client: TestClient, sample_evento_data):
    """Testa filtro de eventos por cidade"""
    # Criar evento
    client.post("/eventos/", json=sample_evento_data)

    # Filtrar por cidade
    response = client.get("/eventos/?cidade=São Paulo")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["cidade"] == "São Paulo"


def test_filtrar_eventos_por_tipo(client: TestClient, sample_evento_data):
    """Testa filtro de eventos por tipo"""
    # Criar evento
    client.post("/eventos/", json=sample_evento_data)

    # Filtrar por tipo
    response = client.get("/eventos/?tipo=música")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["tipo"] == "música"


def test_filtrar_eventos_gratuitos(client: TestClient, sample_evento_data):
    """Testa filtro de eventos gratuitos"""
    # Criar evento pago
    client.post("/eventos/", json=sample_evento_data)

    # Criar evento gratuito
    evento_gratuito = sample_evento_data.copy()
    evento_gratuito["gratuito"] = True
    evento_gratuito["url_original"] = "https://teste.com/evento/2"
    client.post("/eventos/", json=evento_gratuito)

    # Filtrar por eventos gratuitos
    response = client.get("/eventos/?gratuito=true")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["gratuito"] is True


def test_paginacao_eventos(client: TestClient, sample_evento_data):
    """Testa paginação de eventos"""
    # Criar múltiplos eventos
    for i in range(5):
        evento = sample_evento_data.copy()
        evento["url_original"] = f"https://teste.com/evento/{i}"
        evento["titulo"] = f"Evento {i}"
        client.post("/eventos/", json=evento)

    # Testar paginação
    response = client.get("/eventos/?limit=2&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

    # Testar segunda página
    response = client.get("/eventos/?limit=2&offset=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_listar_cidades(client: TestClient, sample_evento_data):
    """Testa listagem de cidades"""
    # Criar evento
    client.post("/eventos/", json=sample_evento_data)

    # Listar cidades
    response = client.get("/eventos/cidades/")
    assert response.status_code == 200
    data = response.json()
    assert "São Paulo" in data


def test_listar_tipos(client: TestClient):
    """Testa listagem de tipos de eventos"""
    response = client.get("/eventos/tipos/")
    assert response.status_code == 200
    data = response.json()
    assert "música" in data
    assert "cultura" in data
    assert "tecnologia" in data
