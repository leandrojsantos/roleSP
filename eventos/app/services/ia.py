"""
Serviço de IA usando Ollama
"""

import os
import logging
from typing import Optional, Dict, Any
import httpx

from ..models import TipoEvento

logger = logging.getLogger(__name__)


class OllamaService:
    """Serviço para integração com Ollama"""

    def __init__(self):
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = os.getenv("OLLAMA_MODEL", "mistral")
        self.timeout = 30.0

    async def _make_request(self, prompt: str) -> Optional[str]:
        """Faz requisição para o Ollama"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={"model": self.model, "prompt": prompt, "stream": False},
                )

                if response.status_code == 200:
                    result = response.json()
                    return result.get("response", "").strip()
                else:
                    logger.error(f"Erro na requisição Ollama: {response.status_code}")
                    return None

        except httpx.TimeoutException:
            logger.error("Timeout na requisição para Ollama")
            return None
        except Exception as e:
            logger.error(f"Erro ao conectar com Ollama: {e}")
            return None

    async def is_available(self) -> bool:
        """Verifica se o Ollama está disponível"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
        except Exception:
            return False

    async def classify_event_type(
        self, title: str, description: str = ""
    ) -> TipoEvento:
        """
        Classifica o tipo de evento usando IA
        """
        if not await self.is_available():
            logger.warning("Ollama não disponível, usando classificação básica")
            return self._basic_classification(title, description)

        prompt = f"""
        Classifique o tipo de evento baseado no título e descrição abaixo.
        
        Título: {title}
        Descrição: {description}
        
        Escolha APENAS uma das opções:
        - música
        - cultura  
        - tecnologia
        - esporte
        - gastronomia
        - outros
        
        Responda apenas com a palavra da categoria escolhida:
        """

        response = await self._make_request(prompt)

        if response:
            # Mapear resposta para enum
            response_lower = response.lower().strip()
            type_mapping = {
                "música": TipoEvento.MUSICA,
                "musica": TipoEvento.MUSICA,
                "cultura": TipoEvento.CULTURA,
                "tecnologia": TipoEvento.TECNOLOGIA,
                "esporte": TipoEvento.ESPORTE,
                "gastronomia": TipoEvento.GASTRONOMIA,
                "outros": TipoEvento.OUTROS,
            }

            return type_mapping.get(response_lower, TipoEvento.OUTROS)

        return self._basic_classification(title, description)

    async def generate_summary(self, title: str, description: str) -> Optional[str]:
        """
        Gera resumo da descrição do evento
        """
        if not await self.is_available():
            logger.warning("Ollama não disponível, usando resumo básico")
            return self._basic_summary(description)

        prompt = f"""
        Crie um resumo conciso e atrativo para este evento:
        
        Título: {title}
        Descrição: {description}
        
        O resumo deve:
        - Ter no máximo 2 frases
        - Destacar os pontos principais
        - Ser atrativo para o público
        - Estar em português
        
        Resumo:
        """

        response = await self._make_request(prompt)
        return response if response else self._basic_summary(description)

    async def extract_keywords(self, title: str, description: str) -> str:
        """
        Extrai palavras-chave do evento
        """
        if not await self.is_available():
            return self._basic_keywords(title, description)

        prompt = f"""
        Extraia as principais palavras-chave deste evento:
        
        Título: {title}
        Descrição: {description}
        
        Retorne apenas as palavras-chave separadas por vírgula, sem espaços extras.
        Máximo 10 palavras-chave.
        
        Palavras-chave:
        """

        response = await self._make_request(prompt)
        return response if response else self._basic_keywords(title, description)

    async def analyze_event_sentiment(
        self, title: str, description: str
    ) -> Dict[str, Any]:
        """
        Analisa o sentimento e características do evento
        """
        if not await self.is_available():
            return {"sentiment": "neutral", "confidence": 0.5}

        prompt = f"""
        Analise este evento e responda em formato JSON:
        
        Título: {title}
        Descrição: {description}
        
        Responda com JSON contendo:
        - "sentiment": "positive", "neutral" ou "negative"
        - "confidence": número entre 0 e 1
        - "main_topics": array com 3 tópicos principais
        - "target_audience": descrição do público-alvo
        
        JSON:
        """

        response = await self._make_request(prompt)

        if response:
            try:
                import json

                return json.loads(response)
            except json.JSONDecodeError:
                logger.error("Erro ao fazer parse da resposta JSON do Ollama")

        return {"sentiment": "neutral", "confidence": 0.5}

    def _basic_classification(self, title: str, description: str) -> TipoEvento:
        """Classificação básica sem IA"""
        text = f"{title} {description}".lower()

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

    def _basic_summary(self, description: str) -> str:
        """Resumo básico sem IA"""
        if not description:
            return ""

        # Pegar as primeiras 2 frases
        sentences = description.split(".")
        if len(sentences) >= 2:
            return f"{sentences[0].strip()}. {sentences[1].strip()}."
        else:
            return description[:200] + "..." if len(description) > 200 else description

    def _basic_keywords(self, title: str, description: str) -> str:
        """Palavras-chave básicas sem IA"""
        text = f"{title} {description}".lower()

        # Palavras comuns para remover (lista simplificada)
        stop_words = {
            "o",
            "a",
            "os",
            "as",
            "um",
            "uma",
            "de",
            "da",
            "do",
            "das",
            "dos",
            "em",
            "na",
            "no",
            "nas",
            "nos",
            "para",
            "com",
            "por",
            "sobre",
            "que",
            "qual",
            "quando",
            "onde",
            "como",
            "se",
            "mas",
            "e",
            "ou",
            "ser",
            "estar",
            "ter",
            "fazer",
            "dizer",
            "ver",
            "saber",
            "poder",
        }

        # Extrair palavras significativas
        words = [word.strip('.,!?;:"()[]{}') for word in text.split()]
        keywords = [word for word in words if len(word) > 3 and word not in stop_words]

        return ", ".join(keywords[:10])


# Instância global do serviço de IA
ai_service = OllamaService()
