"""
Modelos de dados para eventos usando SQLModel
"""

from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field
from enum import Enum


class TipoEvento(str, Enum):
    """Tipos de eventos suportados"""

    MUSICA = "música"
    CULTURA = "cultura"
    TECNOLOGIA = "tecnologia"
    ESPORTE = "esporte"
    GASTRONOMIA = "gastronomia"
    OUTROS = "outros"


class StatusEvento(str, Enum):
    """Status do evento"""

    ATIVO = "ativo"
    CANCELADO = "cancelado"
    FINALIZADO = "finalizado"


class EventoBase(SQLModel):
    """Modelo base para eventos"""

    titulo: str = Field(max_length=200, description="Título do evento")
    descricao: Optional[str] = Field(default=None, description="Descrição do evento")
    resumo: Optional[str] = Field(default=None, description="Resumo gerado por IA")
    data_inicio: datetime = Field(description="Data e hora de início")
    data_fim: Optional[datetime] = Field(default=None, description="Data e hora de fim")
    local: str = Field(max_length=200, description="Local do evento")
    cidade: str = Field(max_length=100, description="Cidade do evento")
    estado: str = Field(max_length=2, description="Estado (UF)")
    endereco: Optional[str] = Field(default=None, description="Endereço completo")
    preco: Optional[float] = Field(default=None, description="Preço do evento")
    gratuito: bool = Field(default=True, description="Se o evento é gratuito")
    tipo: TipoEvento = Field(default=TipoEvento.OUTROS, description="Tipo do evento")
    status: StatusEvento = Field(
        default=StatusEvento.ATIVO, description="Status do evento"
    )
    url_original: str = Field(description="URL de origem do evento")
    fonte: str = Field(max_length=100, description="Fonte do evento (site/plataforma)")
    tags: Optional[str] = Field(default=None, description="Tags separadas por vírgula")
    imagem_url: Optional[str] = Field(
        default=None, description="URL da imagem do evento"
    )


class Evento(EventoBase, table=True):
    """Modelo de evento para o banco de dados"""

    __tablename__ = "eventos"

    id: Optional[int] = Field(default=None, primary_key=True)
    criado_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    atualizado_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relacionamentos futuros podem ser adicionados aqui


class EventoCreate(EventoBase):
    """Modelo para criação de eventos"""

    pass


class EventoRead(EventoBase):
    """Modelo para leitura de eventos"""

    id: int
    criado_em: datetime
    atualizado_em: datetime


class EventoUpdate(SQLModel):
    """Modelo para atualização de eventos"""

    titulo: Optional[str] = None
    descricao: Optional[str] = None
    resumo: Optional[str] = None
    data_inicio: Optional[datetime] = None
    data_fim: Optional[datetime] = None
    local: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    endereco: Optional[str] = None
    preco: Optional[float] = None
    gratuito: Optional[bool] = None
    tipo: Optional[TipoEvento] = None
    status: Optional[StatusEvento] = None
    tags: Optional[str] = None
    imagem_url: Optional[str] = None
