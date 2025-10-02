"""
Modelos de usuário para autenticação
"""

from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field
from fastapi_users_db_sqlmodel import SQLModelBaseUserDB


class UserBase(SQLModel):
    """Modelo base para usuários"""

    email: str = Field(unique=True, index=True, max_length=255)
    nome: Optional[str] = Field(default=None, max_length=100)
    ativo: bool = Field(default=True)
    admin: bool = Field(default=False)


class User(UserBase, SQLModelBaseUserDB, table=True):
    """Modelo de usuário para o banco de dados"""

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    criado_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    atualizado_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relacionamentos futuros podem ser adicionados aqui


class UserCreate(UserBase):
    """Modelo para criação de usuários"""

    password: str = Field(min_length=8, max_length=100)


class UserRead(UserBase):
    """Modelo para leitura de usuários"""

    id: int
    criado_em: datetime
    atualizado_em: datetime


class UserUpdate(SQLModel):
    """Modelo para atualização de usuários"""

    email: Optional[str] = None
    nome: Optional[str] = None
    ativo: Optional[bool] = None
    admin: Optional[bool] = None
    password: Optional[str] = None
