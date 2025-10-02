"""
Testes do serviço de IA
"""

import pytest
from fastapi.testclient import TestClient


def test_ia_status(client: TestClient):
    """Testa status do serviço de IA"""
    response = client.get("/ia/status")
    assert response.status_code == 200
    data = response.json()
    assert "available" in data
    assert "model" in data
    assert "base_url" in data


def test_classify_event_type(client: TestClient):
    """Testa classificação de tipo de evento"""
    request_data = {
        "title": "Festival de Música Eletrônica",
        "description": "O maior festival de música eletrônica da região",
    }

    response = client.post("/ia/classify", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert "tipo" in data
    assert "title" in data
    assert "description" in data


def test_generate_summary(client: TestClient):
    """Testa geração de resumo"""
    request_data = {
        "title": "Workshop de Python",
        "description": "Aprenda Python do zero com projetos práticos e mentoria especializada. O workshop inclui exercícios hands-on, projetos reais e certificado de conclusão.",
    }

    response = client.post("/ia/summary", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert "original" in data


def test_extract_keywords(client: TestClient):
    """Testa extração de palavras-chave"""
    request_data = {
        "title": "Exposição de Arte Contemporânea",
        "description": "Mostra com obras de artistas brasileiros contemporâneos. Inclui pinturas, esculturas e instalações interativas.",
    }

    response = client.post("/ia/keywords", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert "keywords" in data
    assert "title" in data
    assert "description" in data


def test_analyze_event(client: TestClient):
    """Testa análise de evento"""
    request_data = {
        "title": "Corrida de Rua 5K",
        "description": "Corrida beneficente com percurso de 5km pela cidade. Inscrições abertas para todas as idades.",
    }

    response = client.post("/ia/analyze", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert "analysis" in data
    assert "title" in data
    assert "description" in data


def test_process_event_with_ia(client: TestClient, sample_evento_data):
    """Testa processamento de evento com IA"""
    # Criar evento
    create_response = client.post("/eventos/", json=sample_evento_data)
    evento_id = create_response.json()["id"]

    # Processar com IA
    response = client.post(f"/ia/process-event/{evento_id}")
    assert response.status_code == 200
    data = response.json()
    assert "Evento processado" in data["message"]
    assert "evento" in data


def test_process_event_inexistente(client: TestClient):
    """Testa processamento de evento inexistente"""
    response = client.post("/ia/process-event/999")
    assert response.status_code == 404
    assert "não encontrado" in response.json()["detail"]


def test_batch_process_events(client: TestClient, sample_evento_data):
    """Testa processamento em lote"""
    # Criar alguns eventos
    for i in range(3):
        evento = sample_evento_data.copy()
        evento["url_original"] = f"https://teste.com/evento/{i}"
        evento["titulo"] = f"Evento {i}"
        client.post("/eventos/", json=evento)

    # Processar em lote
    response = client.post("/ia/batch-process?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert "Processamento em lote concluído" in data["message"]
    assert "processed" in data
    assert "errors" in data
    assert "total" in data
