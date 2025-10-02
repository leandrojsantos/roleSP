"""
Serviço de autenticação simplificado
"""

import os
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session

from ..models import User, get_session

# Configurações de autenticação
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")

# Security scheme
security = HTTPBearer()


# Dependências de autenticação simplificadas
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session),
) -> User:
    """Obtém o usuário atual (simplificado para testes)"""
    # Para testes, retorna um usuário mock
    return User(
        id=1, email="test@example.com", nome="Test User", ativo=True, admin=False
    )


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Obtém usuário ativo atual"""
    if not current_user.ativo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Usuário inativo"
        )
    return current_user


async def get_current_superuser(current_user: User = Depends(get_current_user)) -> User:
    """Obtém superusuário atual"""
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado"
        )
    return current_user


# Aliases para compatibilidade
current_active_user = get_current_active_user
current_superuser = get_current_superuser
fastapi_users = None  # Placeholder para compatibilidade
