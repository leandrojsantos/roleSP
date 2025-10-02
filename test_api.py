"""
Testes MINIMAL para kd-Role
"""

import pytest
from fastapi.testclient import TestClient
from eventos import app

client = TestClient(app)


class TestMinimalAPI:
    """Testes básicos da API minimal"""

    def test_root_endpoint(self):
        """Testa endpoint raiz"""
        response = client.get("/")
        assert response.status_code == 200
        assert "kd-Role" in response.json()["message"]

    def test_list_eventos(self):
        """Testa listagem de eventos"""
        response = client.get("/eventos")
        assert response.status_code == 200
        eventos = response.json()
        assert isinstance(eventos, list)

        # Deve ter os eventos de exemplo
        if eventos:
            assert all("nome" in evento for evento in eventos)
            assert all("cidade" in evento for evento in eventos)
            assert all("data" in evento for evento in eventos)

    def test_create_evento(self):
        """Testa criação de evento"""
        novo_evento = {
            "nome": "Teste Evento",
            "cidade": "Test City",
            "data": "2025-12-31",
            "url": "https://test.com",
        }

        response = client.post("/eventos", json=novo_evento)
        assert response.status_code == 200
        assert "sucesso" in response.json()["mensagem"]

    def test_list_cidades(self):
        """Testa listagem de cidades"""
        response = client.get("/cidades")
        assert response.status_code == 200
        cidades = response.json()
        assert isinstance(cidades, list)

        # Cidades devem ser strings únicas
        if cidades:
            assert all(isinstance(cidade, str) for cidade in cidades)

    def test_filter_by_cidade(self):
        """Testa filtro por cidade"""
        response = client.get("/eventos?cidade=São%20Paulo")
        assert response.status_code == 200
        eventos = response.json()

        # Todos os eventos devem ser de São Paulo (se houver)
        if eventos:
            assert all("São Paulo" in evento["cidade"] for evento in eventos)

    def test_limit_parameter(self):
        """Testa parâmetro limite"""
        response = client.get("/eventos?limite=2")
        assert response.status_code == 200
        eventos = response.json()

        assert len(eventos) <= 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
