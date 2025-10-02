"""
Testes do sistema de scraping
"""

import pytest
from fastapi.testclient import TestClient


def test_status_scraping(client: TestClient):
    """Testa status do scraping"""
    response = client.get("/scraping/status")
    assert response.status_code == 200
    data = response.json()
    assert "total_scrapers" in data
    assert "scrapers_executed" in data
    assert "total_events" in data


def test_executar_scraping(client: TestClient):
    """Testa execução do scraping"""
    response = client.post("/scraping/executar")
    assert response.status_code == 200
    data = response.json()
    assert "Scraping iniciado" in data["message"]
    assert "scrapers" in data


def test_listar_eventos_scraping(client: TestClient):
    """Testa listagem de eventos do scraping"""
    response = client.get("/scraping/eventos")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "eventos" in data


def test_listar_eventos_por_scraper(client: TestClient):
    """Testa listagem de eventos por scraper"""
    response = client.get("/scraping/eventos/exemplo")
    assert response.status_code == 200
    data = response.json()
    assert data["scraper"] == "exemplo"
    assert "total" in data
    assert "eventos" in data


def test_listar_eventos_scraper_inexistente(client: TestClient):
    """Testa listagem de eventos de scraper inexistente"""
    response = client.get("/scraping/eventos/scraper_inexistente")
    assert response.status_code == 200
    data = response.json()
    assert data["scraper"] == "scraper_inexistente"
    assert data["total"] == 0
    assert data["eventos"] == []
