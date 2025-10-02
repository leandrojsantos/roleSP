"""
Router para endpoints de eventos
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from datetime import datetime, timezone

from ..models import (
    Evento,
    EventoCreate,
    EventoRead,
    EventoUpdate,
    get_session,
    TipoEvento,
)
from ..config import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE, SUCCESS_MESSAGES
from ..utils import validate_pagination_params, create_error_response

router = APIRouter(prefix="/eventos", tags=["eventos"])


@router.get("/", response_model=List[EventoRead])
async def listar_eventos(
    cidade: Optional[str] = Query(None, description="Filtrar por cidade"),
    tipo: Optional[str] = Query(None, description="Filtrar por tipo de evento"),
    gratuito: Optional[bool] = Query(None, description="Filtrar por eventos gratuitos"),
    data_inicio: Optional[datetime] = Query(None, description="Data de início mínima"),
    data_fim: Optional[datetime] = Query(None, description="Data de fim máxima"),
    limit: int = Query(
        DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE, description="Limite de resultados"
    ),
    offset: int = Query(0, ge=0, description="Offset para paginação"),
    session: Session = Depends(get_session),
):
    """
    Lista eventos com filtros opcionais

    - **cidade**: Filtrar por cidade (ex: "São Paulo", "Mauá")
    - **tipo**: Filtrar por tipo (música, cultura, tecnologia, etc.)
    - **gratuito**: Filtrar por eventos gratuitos
    - **data_inicio**: Data de início mínima
    - **data_fim**: Data de fim máxima
    - **limit**: Número máximo de resultados (1-100)
    - **offset**: Número de resultados para pular
    """
    # Validar parâmetros de paginação
    limit, offset = validate_pagination_params(limit, offset)

    query = select(Evento)

    # Aplicar filtros
    if cidade:
        query = query.where(Evento.cidade.ilike(f"%{cidade}%"))

    if tipo:
        query = query.where(Evento.tipo == tipo)

    if gratuito is not None:
        query = query.where(Evento.gratuito == gratuito)

    if data_inicio:
        query = query.where(Evento.data_inicio >= data_inicio)

    if data_fim:
        query = query.where(Evento.data_fim <= data_fim)

    # Aplicar paginação
    query = query.offset(offset).limit(limit)

    # Ordenar por data de início
    query = query.order_by(Evento.data_inicio)

    eventos = session.exec(query).all()
    return eventos


@router.get("/{evento_id}", response_model=EventoRead)
async def obter_evento(evento_id: int, session: Session = Depends(get_session)):
    """
    Obtém um evento específico por ID
    """
    evento = session.get(Evento, evento_id)
    if not evento:
        raise create_error_response("Evento não encontrado", 404)
    return evento


@router.post("/", response_model=EventoRead)
async def criar_evento(evento: EventoCreate, session: Session = Depends(get_session)):
    """
    Cria um novo evento (endpoint interno para o scraper)
    """
    # Verificar se já existe um evento com a mesma URL
    existing_evento = session.exec(
        select(Evento).where(Evento.url_original == evento.url_original)
    ).first()

    if existing_evento:
        raise create_error_response("Evento com esta URL já existe", 400)

    db_evento = Evento.model_validate(evento)
    session.add(db_evento)
    session.commit()
    session.refresh(db_evento)

    return db_evento


@router.put("/{evento_id}", response_model=EventoRead)
async def atualizar_evento(
    evento_id: int, evento_update: EventoUpdate, session: Session = Depends(get_session)
):
    """
    Atualiza um evento existente
    """
    evento = session.get(Evento, evento_id)
    if not evento:
        raise create_error_response("Evento não encontrado", 404)

    # Atualizar apenas os campos fornecidos
    evento_data = evento_update.model_dump(exclude_unset=True)
    for field, value in evento_data.items():
        setattr(evento, field, value)

    evento.atualizado_em = datetime.now(timezone.utc)

    session.add(evento)
    session.commit()
    session.refresh(evento)

    return evento


@router.delete("/{evento_id}")
async def deletar_evento(evento_id: int, session: Session = Depends(get_session)):
    """
    Deleta um evento
    """
    evento = session.get(Evento, evento_id)
    if not evento:
        raise create_error_response("Evento não encontrado", 404)

    session.delete(evento)
    session.commit()

    return {"message": SUCCESS_MESSAGES["DELETED"]}


@router.get("/cidades/", response_model=List[str])
async def listar_cidades(session: Session = Depends(get_session)):
    """
    Lista todas as cidades disponíveis
    """
    query = select(Evento.cidade).distinct().order_by(Evento.cidade)
    cidades = session.exec(query).all()
    return cidades


@router.get("/tipos/", response_model=List[str])
async def listar_tipos():
    """
    Lista todos os tipos de eventos disponíveis
    """
    return [tipo.value for tipo in TipoEvento]
