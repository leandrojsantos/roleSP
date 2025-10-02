"""
Classe base para scrapers
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
import asyncio
import logging
from playwright.async_api import async_playwright, Browser, Page
from selectolax.parser import HTMLParser

from ..models import EventoCreate, TipoEvento

logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """Classe base para todos os scrapers"""

    def __init__(self, name: str, base_url: str, delay: float = 1.0):
        self.name = name
        self.base_url = base_url
        self.delay = delay
        self.browser: Optional[Browser] = None

    async def __aenter__(self):
        """Context manager entry"""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(
            headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if self.browser:
            await self.browser.close()

    @abstractmethod
    async def scrape_events(self) -> List[EventoCreate]:
        """
        Método abstrato para extrair eventos
        Deve ser implementado por cada scraper específico
        """
        pass

    async def get_page(self, url: str) -> Page:
        """Cria uma nova página e navega para a URL"""
        if not self.browser:
            raise RuntimeError("Browser não inicializado")

        page = await self.browser.new_page()

        # Configurar user agent para evitar bloqueios
        await page.set_extra_http_headers(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
        )

        try:
            await page.goto(url, wait_until="networkidle", timeout=30000)
            await asyncio.sleep(self.delay)  # Delay entre requisições
            return page
        except Exception as e:
            await page.close()
            raise e

    def parse_html(self, html: str) -> HTMLParser:
        """Parse HTML usando Selectolax"""
        return HTMLParser(html)

    def extract_text(self, element, selector: str = None) -> Optional[str]:
        """Extrai texto de um elemento HTML"""
        if element is None:
            return None

        if selector:
            element = element.css_first(selector)
            if not element:
                return None

        return element.text(strip=True) if element else None

    def extract_attr(self, element, attr: str, selector: str = None) -> Optional[str]:
        """Extrai atributo de um elemento HTML"""
        if element is None:
            return None

        if selector:
            element = element.css_first(selector)
            if not element:
                return None

        return element.attributes.get(attr) if element else None

    def normalize_text(self, text: str) -> str:
        """Normaliza texto removendo espaços extras e quebras de linha"""
        if not text:
            return ""
        return " ".join(text.split())

    def parse_date(self, date_str: str) -> Optional[datetime]:
        """
        Parse de data genérico
        Pode ser sobrescrito por scrapers específicos
        """
        if not date_str:
            return None

        # Implementação básica - pode ser melhorada
        try:
            # Tentar formatos comuns
            formats = [
                "%d/%m/%Y %H:%M",
                "%d/%m/%Y",
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d",
                "%d-%m-%Y %H:%M",
                "%d-%m-%Y",
            ]

            for fmt in formats:
                try:
                    return datetime.strptime(date_str.strip(), fmt)
                except ValueError:
                    continue

            logger.warning(f"Formato de data não reconhecido: {date_str}")
            return None

        except Exception as e:
            logger.error(f"Erro ao fazer parse da data {date_str}: {e}")
            return None

    def classify_event_type(self, title: str, description: str = "") -> TipoEvento:
        """
        Classificação básica de tipo de evento baseada em palavras-chave
        Pode ser melhorada com IA
        """
        text = f"{title} {description}".lower()

        # Palavras-chave para cada tipo
        keywords = {
            TipoEvento.MUSICA: [
                "música",
                "show",
                "concerto",
                "festival",
                "banda",
                "cantor",
                "dj",
            ],
            TipoEvento.CULTURA: [
                "teatro",
                "exposição",
                "museu",
                "arte",
                "cultura",
                "dança",
                "balé",
            ],
            TipoEvento.TECNOLOGIA: [
                "tech",
                "tecnologia",
                "programação",
                "desenvolvimento",
                "startup",
                "hackathon",
            ],
            TipoEvento.ESPORTE: [
                "futebol",
                "basquete",
                "corrida",
                "maratona",
                "esporte",
                "atletismo",
            ],
            TipoEvento.GASTRONOMIA: [
                "gastronomia",
                "culinária",
                "chef",
                "restaurante",
                "comida",
                "degustação",
            ],
        }

        for tipo, words in keywords.items():
            if any(word in text for word in words):
                return tipo

        return TipoEvento.OUTROS

    def extract_price(self, price_text: str) -> Optional[float]:
        """Extrai preço de texto"""
        if not price_text:
            return None

        # Remove caracteres não numéricos exceto vírgula e ponto
        import re

        price_clean = re.sub(r"[^\d,.]", "", price_text)

        if not price_clean:
            return None

        try:
            # Substitui vírgula por ponto para float
            price_clean = price_clean.replace(",", ".")
            return float(price_clean)
        except ValueError:
            return None
