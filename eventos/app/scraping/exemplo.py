"""
Exemplo de scraper para demonstração
"""

from typing import List
from datetime import datetime, timedelta
import random

from .base import BaseScraper
from ..models import EventoCreate, TipoEvento


class ExemploScraper(BaseScraper):
    """Scraper de exemplo que gera eventos fictícios"""

    def __init__(self):
        super().__init__(name="exemplo", base_url="https://exemplo.com", delay=0.5)

    async def scrape_events(self) -> List[EventoCreate]:
        """Gera eventos de exemplo para demonstração"""

        # Lista de eventos de exemplo
        eventos_exemplo = [
            {
                "titulo": "Festival de Música Eletrônica",
                "descricao": "O maior festival de música eletrônica da região com os melhores DJs nacionais e internacionais.",
                "local": "Parque Ibirapuera",
                "cidade": "São Paulo",
                "estado": "SP",
                "endereco": "Av. Pedro Álvares Cabral, s/n - Vila Mariana",
                "preco": 150.0,
                "gratuito": False,
                "tipo": TipoEvento.MUSICA,
                "fonte": "exemplo.com",
            },
            {
                "titulo": "Workshop de Python para Iniciantes",
                "descricao": "Aprenda Python do zero com projetos práticos e mentoria especializada.",
                "local": "Centro de Convenções",
                "cidade": "Mauá",
                "estado": "SP",
                "endereco": "Rua da Tecnologia, 123 - Centro",
                "preco": 0.0,
                "gratuito": True,
                "tipo": TipoEvento.TECNOLOGIA,
                "fonte": "exemplo.com",
            },
            {
                "titulo": "Exposição de Arte Contemporânea",
                "descricao": "Mostra com obras de artistas brasileiros contemporâneos.",
                "local": "Museu de Arte Moderna",
                "cidade": "São Paulo",
                "estado": "SP",
                "endereco": "Av. Paulista, 1578 - Bela Vista",
                "preco": 25.0,
                "gratuito": False,
                "tipo": TipoEvento.CULTURA,
                "fonte": "exemplo.com",
            },
            {
                "titulo": "Corrida de Rua 5K",
                "descricao": "Corrida beneficente com percurso de 5km pela cidade.",
                "local": "Parque da Cidade",
                "cidade": "Mauá",
                "estado": "SP",
                "endereco": "Av. dos Esportes, 456 - Jardim Mauá",
                "preco": 30.0,
                "gratuito": False,
                "tipo": TipoEvento.ESPORTE,
                "fonte": "exemplo.com",
            },
            {
                "titulo": "Degustação de Vinhos",
                "descricao": "Degustação de vinhos nacionais com sommelier especializado.",
                "local": "Restaurante Gourmet",
                "cidade": "São Paulo",
                "estado": "SP",
                "endereco": "Rua Augusta, 789 - Consolação",
                "preco": 80.0,
                "gratuito": False,
                "tipo": TipoEvento.GASTRONOMIA,
                "fonte": "exemplo.com",
            },
        ]

        eventos = []
        base_date = datetime.now() + timedelta(days=7)  # Eventos para próxima semana

        for i, evento_data in enumerate(eventos_exemplo):
            # Gerar datas aleatórias
            days_offset = random.randint(0, 30)
            hours_offset = random.randint(9, 21)
            minutes_offset = random.choice([0, 30])

            data_inicio = base_date + timedelta(
                days=days_offset, hours=hours_offset, minutes=minutes_offset
            )
            data_fim = data_inicio + timedelta(hours=random.randint(2, 6))

            evento = EventoCreate(
                titulo=evento_data["titulo"],
                descricao=evento_data["descricao"],
                data_inicio=data_inicio,
                data_fim=data_fim,
                local=evento_data["local"],
                cidade=evento_data["cidade"],
                estado=evento_data["estado"],
                endereco=evento_data["endereco"],
                preco=evento_data["preco"],
                gratuito=evento_data["gratuito"],
                tipo=evento_data["tipo"],
                url_original=f"https://exemplo.com/evento/{i+1}",
                fonte=evento_data["fonte"],
                tags="exemplo, demonstração, teste",
            )

            eventos.append(evento)

        return eventos
