"""
Utilitários comuns da aplicação
"""

from typing import Any, Dict, Optional
from fastapi import HTTPException, status
from datetime import datetime, timezone

from .config import ERROR_MESSAGES


def create_error_response(
    message: str,
    status_code: int = status.HTTP_400_BAD_REQUEST,
    details: Optional[Dict[str, Any]] = None,
) -> HTTPException:
    """Cria uma resposta de erro padronizada"""
    return HTTPException(
        status_code=status_code, detail={"message": message, "details": details or {}}
    )


def get_current_timestamp() -> datetime:
    """Retorna timestamp atual em UTC"""
    return datetime.now(timezone.utc)


def validate_pagination_params(limit: int, offset: int) -> tuple[int, int]:
    """Valida e normaliza parâmetros de paginação"""
    from .config import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

    if limit < 1:
        limit = DEFAULT_PAGE_SIZE
    elif limit > MAX_PAGE_SIZE:
        limit = MAX_PAGE_SIZE

    if offset < 0:
        offset = 0

    return limit, offset


def normalize_text(text: str) -> str:
    """Normaliza texto removendo espaços extras e quebras de linha"""
    if not text:
        return ""
    return " ".join(text.split())


def extract_price_from_text(price_text: str) -> Optional[float]:
    """Extrai preço de texto"""
    if not price_text:
        return None

    import re

    # Remove caracteres não numéricos exceto vírgula e ponto
    price_clean = re.sub(r"[^\d,.]", "", price_text)

    if not price_clean:
        return None

    try:
        # Substitui vírgula por ponto para float
        price_clean = price_clean.replace(",", ".")
        return float(price_clean)
    except ValueError:
        return None


def format_currency(value: float) -> str:
    """Formata valor como moeda brasileira"""
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def truncate_text(text: str, max_length: int = 200) -> str:
    """Trunca texto para um tamanho máximo"""
    if not text or len(text) <= max_length:
        return text
    return text[:max_length].rstrip() + "..."
