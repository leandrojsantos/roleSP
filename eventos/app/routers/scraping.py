"""
Router para endpoints de scraping
"""

from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlmodel import Session, select

from ..models import get_session, Evento
from ..scraping import ScrapingManager, ExemploScraper

router = APIRouter(prefix="/scraping", tags=["scraping"])

# Instância global do gerenciador de scraping
scraping_manager = ScrapingManager()

# Adicionar scraper de exemplo
scraping_manager.add_scraper(ExemploScraper())


@router.post("/executar")
async def executar_scraping(
    background_tasks: BackgroundTasks, session: Session = Depends(get_session)
):
    """
    Executa o scraping de todos os scrapers configurados
    """
    try:
        # Executar scraping em background
        background_tasks.add_task(run_scraping_task, session)

        return {
            "message": "Scraping iniciado em background",
            "scrapers": [scraper.name for scraper in scraping_manager.scrapers],
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao iniciar scraping: {str(e)}"
        )


async def run_scraping_task(session: Session):
    """Tarefa de background para executar o scraping"""
    try:
        # Executar todos os scrapers
        results = await scraping_manager.run_all_scrapers()

        # Salvar eventos no banco de dados
        for scraper_name, eventos in results.items():
            for evento_data in eventos:
                # Verificar se evento já existe
                existing = session.exec(
                    select(Evento).where(
                        Evento.url_original == evento_data.url_original
                    )
                ).first()

                if not existing:
                    evento = Evento.model_validate(evento_data)
                    session.add(evento)

        session.commit()

    except Exception as e:
        print(f"Erro no scraping em background: {e}")


@router.get("/status")
async def status_scraping():
    """
    Retorna o status atual do scraping
    """
    stats = scraping_manager.get_statistics()
    return stats


@router.get("/eventos")
async def listar_eventos_scraping():
    """
    Lista eventos encontrados pelo scraping (sem salvar no banco)
    """
    all_events = scraping_manager.get_all_events()
    return {"total": len(all_events), "eventos": all_events}


@router.get("/eventos/{scraper_name}")
async def listar_eventos_por_scraper(scraper_name: str):
    """
    Lista eventos de um scraper específico
    """
    events = scraping_manager.get_events_by_scraper(scraper_name)
    return {"scraper": scraper_name, "total": len(events), "eventos": events}
