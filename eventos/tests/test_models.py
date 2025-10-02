"""
Testes dos modelos de dados
"""

import pytest
from datetime import datetime
from sqlmodel import Session

from eventos.app.models import (
    Evento,
    EventoCreate,
    EventoUpdate,
    TipoEvento,
    StatusEvento,
)


def test_evento_create_model():
    """Testa criação de modelo EventoCreate"""
    evento_data = {
        "titulo": "Teste Evento",
        "descricao": "Descrição do evento",
        "data_inicio": datetime.now(),
        "local": "Local Teste",
        "cidade": "São Paulo",
        "estado": "SP",
        "url_original": "https://teste.com",
        "fonte": "teste.com",
    }

    evento = EventoCreate(**evento_data)
    assert evento.titulo == "Teste Evento"
    assert evento.cidade == "São Paulo"
    assert evento.gratuito is True  # Valor padrão


def test_evento_model_defaults():
    """Testa valores padrão do modelo Evento"""
    evento_data = {
        "titulo": "Teste Evento",
        "data_inicio": datetime.now(),
        "local": "Local Teste",
        "cidade": "São Paulo",
        "estado": "SP",
        "url_original": "https://teste.com",
        "fonte": "teste.com",
    }

    evento = EventoCreate(**evento_data)
    assert evento.gratuito is True
    assert evento.tipo == TipoEvento.OUTROS
    assert evento.status == StatusEvento.ATIVO


def test_evento_update_model():
    """Testa modelo de atualização"""
    update_data = {"titulo": "Novo Título", "preco": 100.0}

    evento_update = EventoUpdate(**update_data)
    assert evento_update.titulo == "Novo Título"
    assert evento_update.preco == 100.0
    assert evento_update.descricao is None  # Campo não fornecido


def test_tipo_evento_enum():
    """Testa enum TipoEvento"""
    assert TipoEvento.MUSICA.value == "música"
    assert TipoEvento.CULTURA.value == "cultura"
    assert TipoEvento.TECNOLOGIA.value == "tecnologia"
    assert TipoEvento.ESPORTE.value == "esporte"
    assert TipoEvento.GASTRONOMIA.value == "gastronomia"
    assert TipoEvento.OUTROS.value == "outros"


def test_status_evento_enum():
    """Testa enum StatusEvento"""
    assert StatusEvento.ATIVO.value == "ativo"
    assert StatusEvento.CANCELADO.value == "cancelado"
    assert StatusEvento.FINALIZADO.value == "finalizado"


def test_evento_database_model(session: Session):
    """Testa modelo Evento no banco de dados"""
    evento_data = {
        "titulo": "Teste Evento",
        "descricao": "Descrição do evento",
        "data_inicio": datetime.now(),
        "local": "Local Teste",
        "cidade": "São Paulo",
        "estado": "SP",
        "url_original": "https://teste.com",
        "fonte": "teste.com",
    }

    evento = Evento(**evento_data)
    session.add(evento)
    session.commit()
    session.refresh(evento)

    assert evento.id is not None
    assert evento.criado_em is not None
    assert evento.atualizado_em is not None
    assert evento.titulo == "Teste Evento"
