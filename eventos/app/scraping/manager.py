"""
Gerenciador de scrapers
"""

import asyncio
import logging
from typing import List, Dict, Any
from datetime import datetime, timezone

from .base import BaseScraper
from ..models import EventoCreate

logger = logging.getLogger(__name__)


class ScrapingManager:
    """Gerencia múltiplos scrapers"""

    def __init__(self):
        self.scrapers: List[BaseScraper] = []
        self.results: Dict[str, List[EventoCreate]] = {}

    def add_scraper(self, scraper: BaseScraper):
        """Adiciona um scraper ao gerenciador"""
        self.scrapers.append(scraper)
        logger.info(f"Scraper {scraper.name} adicionado")

    async def run_all_scrapers(self) -> Dict[str, List[EventoCreate]]:
        """
        Executa todos os scrapers em paralelo
        """
        if not self.scrapers:
            logger.warning("Nenhum scraper configurado")
            return {}

        logger.info(f"Iniciando scraping com {len(self.scrapers)} scrapers")

        # Executar todos os scrapers em paralelo
        tasks = []
        for scraper in self.scrapers:
            task = asyncio.create_task(self._run_single_scraper(scraper))
            tasks.append(task)

        # Aguardar todos os scrapers terminarem
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Processar resultados
        for i, result in enumerate(results):
            scraper_name = self.scrapers[i].name

            if isinstance(result, Exception):
                logger.error(f"Erro no scraper {scraper_name}: {result}")
                self.results[scraper_name] = []
            else:
                self.results[scraper_name] = result
                logger.info(f"Scraper {scraper_name} encontrou {len(result)} eventos")

        total_events = sum(len(events) for events in self.results.values())
        logger.info(f"Scraping concluído. Total de eventos encontrados: {total_events}")

        return self.results

    async def _run_single_scraper(self, scraper: BaseScraper) -> List[EventoCreate]:
        """Executa um único scraper"""
        try:
            async with scraper:
                events = await scraper.scrape_events()
                return events
        except Exception as e:
            logger.error(f"Erro ao executar scraper {scraper.name}: {e}")
            raise e

    def get_all_events(self) -> List[EventoCreate]:
        """Retorna todos os eventos de todos os scrapers"""
        all_events = []
        for events in self.results.values():
            all_events.extend(events)
        return all_events

    def get_events_by_scraper(self, scraper_name: str) -> List[EventoCreate]:
        """Retorna eventos de um scraper específico"""
        return self.results.get(scraper_name, [])

    def get_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas do scraping"""
        stats = {
            "total_scrapers": len(self.scrapers),
            "scrapers_executed": len(self.results),
            "total_events": sum(len(events) for events in self.results.values()),
            "events_by_scraper": {
                name: len(events) for name, events in self.results.items()
            },
            "last_run": datetime.now(timezone.utc).isoformat(),
        }
        return stats
