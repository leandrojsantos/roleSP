"""
Router para endpoints de IA
"""

from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlmodel import Session, select

from ..models import get_session, Evento, TipoEvento
from ..services import ai_service

router = APIRouter(prefix="/ia", tags=["ia"])


class ClassifyRequest(BaseModel):
    title: str
    description: Optional[str] = ""


class SummaryRequest(BaseModel):
    title: str
    description: str


class KeywordsRequest(BaseModel):
    title: str
    description: str


class AnalyzeRequest(BaseModel):
    title: str
    description: str


@router.get("/status")
async def ia_status():
    """
    Verifica se o serviço de IA está disponível
    """
    is_available = await ai_service.is_available()
    return {
        "available": is_available,
        "model": ai_service.model,
        "base_url": ai_service.base_url,
    }


@router.post("/classify")
async def classify_event_type(request: ClassifyRequest):
    """
    Classifica o tipo de evento usando IA
    """
    try:
        tipo = await ai_service.classify_event_type(
            request.title, request.description or ""
        )
        return {
            "tipo": tipo.value,
            "title": request.title,
            "description": request.description,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na classificação: {str(e)}")


@router.post("/summary")
async def generate_summary(request: SummaryRequest):
    """
    Gera resumo da descrição do evento
    """
    try:
        summary = await ai_service.generate_summary(request.title, request.description)
        return {"summary": summary, "original": request.description}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar resumo: {str(e)}")


@router.post("/keywords")
async def extract_keywords(request: KeywordsRequest):
    """
    Extrai palavras-chave do evento
    """
    try:
        keywords = await ai_service.extract_keywords(request.title, request.description)
        return {
            "keywords": keywords,
            "title": request.title,
            "description": request.description,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao extrair palavras-chave: {str(e)}"
        )


@router.post("/analyze")
async def analyze_event(request: AnalyzeRequest):
    """
    Analisa o evento (sentimento, tópicos, público-alvo)
    """
    try:
        analysis = await ai_service.analyze_event_sentiment(
            request.title, request.description
        )
        return {
            "analysis": analysis,
            "title": request.title,
            "description": request.description,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na análise: {str(e)}")


@router.post("/process-event/{evento_id}")
async def process_event_with_ai(
    evento_id: int, session: Session = Depends(get_session)
):
    """
    Processa um evento existente com IA (classificação, resumo, etc.)
    """
    evento = session.get(Evento, evento_id)
    if not evento:
        raise HTTPException(status_code=404, detail="Evento não encontrado")

    try:
        # Classificar tipo
        tipo = await ai_service.classify_event_type(
            evento.titulo, evento.descricao or ""
        )

        # Gerar resumo
        summary = await ai_service.generate_summary(
            evento.titulo, evento.descricao or ""
        )

        # Extrair palavras-chave
        keywords = await ai_service.extract_keywords(
            evento.titulo, evento.descricao or ""
        )

        # Atualizar evento
        evento.tipo = tipo
        evento.resumo = summary
        evento.tags = keywords

        session.add(evento)
        session.commit()
        session.refresh(evento)

        return {"message": "Evento processado com IA", "evento": evento}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao processar evento: {str(e)}"
        )


@router.post("/batch-process")
async def batch_process_events(
    limit: int = 10, session: Session = Depends(get_session)
):
    """
    Processa múltiplos eventos com IA
    """
    # Buscar eventos sem resumo ou classificação
    query = (
        select(Evento)
        .where((Evento.resumo.is_(None)) | (Evento.tipo == TipoEvento.OUTROS))
        .limit(limit)
    )

    eventos = session.exec(query).all()

    if not eventos:
        return {"message": "Nenhum evento para processar"}

    processed = 0
    errors = 0

    for evento in eventos:
        try:
            # Classificar tipo
            tipo = await ai_service.classify_event_type(
                evento.titulo, evento.descricao or ""
            )

            # Gerar resumo
            summary = await ai_service.generate_summary(
                evento.titulo, evento.descricao or ""
            )

            # Extrair palavras-chave
            keywords = await ai_service.extract_keywords(
                evento.titulo, evento.descricao or ""
            )

            # Atualizar evento
            evento.tipo = tipo
            evento.resumo = summary
            evento.tags = keywords

            session.add(evento)
            processed += 1

        except Exception as e:
            print(f"Erro ao processar evento {evento.id}: {e}")
            errors += 1

    session.commit()

    return {
        "message": "Processamento em lote concluído",
        "processed": processed,
        "errors": errors,
        "total": len(eventos),
    }
