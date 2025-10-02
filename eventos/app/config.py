"""
Configurações centralizadas da aplicação
"""

import os
from typing import List

# Configurações da aplicação
APP_NAME = "EventRadar"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Plataforma que busca, filtra, resume e exibe eventos de diversas fontes online com IA"

# Configurações de ambiente
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
PORT = int(os.getenv("PORT", 8000))

# Configurações de banco de dados
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://eventradar:eventradar123@localhost:5432/eventradar"
)

# Para desenvolvimento local e testes (SQLite)
if ENVIRONMENT in ["development", "test"]:
    DATABASE_URL = "sqlite:///./eventos.db"

# Configurações de IA
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")

# Configurações de segurança
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")

# Configurações CORS
CORS_ORIGINS: List[str] = ["*"]
CORS_CREDENTIALS = True
CORS_METHODS = ["*"]
CORS_HEADERS = ["*"]

# Configurações de paginação
DEFAULT_PAGE_SIZE = 50
MAX_PAGE_SIZE = 100

# Configurações de scraping
DEFAULT_SCRAPING_DELAY = 1.0

# Mensagens de erro padronizadas
ERROR_MESSAGES = {
    "NOT_FOUND": "Recurso não encontrado",
    "ALREADY_EXISTS": "Recurso já existe",
    "INVALID_DATA": "Dados inválidos",
    "UNAUTHORIZED": "Não autorizado",
    "FORBIDDEN": "Acesso negado",
    "INTERNAL_ERROR": "Erro interno do servidor",
}

# Mensagens de sucesso padronizadas
SUCCESS_MESSAGES = {
    "CREATED": "Criado com sucesso",
    "UPDATED": "Atualizado com sucesso",
    "DELETED": "Deletado com sucesso",
    "PROCESSED": "Processado com sucesso",
}
