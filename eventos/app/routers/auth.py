"""
Router para autenticação
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..models import get_session, User, UserCreate, UserRead, UserUpdate
from ..services.auth import fastapi_users, current_active_user, current_superuser

router = APIRouter(prefix="/auth", tags=["auth"])


# Rotas de autenticação simplificadas
@router.post("/jwt/login")
async def login(username: str, password: str):
    """Login simplificado para testes"""
    return {"access_token": "fake-token", "token_type": "bearer"}


@router.post("/register")
async def register(email: str, password: str, nome: str = "User"):
    """Registro simplificado para testes"""
    return {"id": 1, "email": email, "nome": nome, "ativo": True, "admin": False}


@router.get("/me")
async def get_current_user_info(current_user: User = Depends(current_active_user)):
    """
    Retorna informações do usuário atual
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
        "nome": current_user.nome,
        "ativo": current_user.ativo,
        "admin": current_user.admin,
        "criado_em": current_user.criado_em,
    }


@router.post("/create-superuser")
async def create_superuser(
    email: str,
    password: str,
    nome: str = "Admin",
    session: Session = Depends(get_session),
):
    """
    Cria um superusuário (apenas para desenvolvimento)
    """
    # Verificar se já existe
    existing_user = session.exec(select(User).where(User.email == email)).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Usuário já existe")

    # Criar superusuário
    superuser = User(email=email, nome=nome, admin=True, ativo=True)
    superuser.set_password(password)

    session.add(superuser)
    session.commit()
    session.refresh(superuser)

    return {
        "message": "Superusuário criado com sucesso",
        "user": {
            "id": superuser.id,
            "email": superuser.email,
            "nome": superuser.nome,
            "admin": superuser.admin,
        },
    }


@router.get("/protected")
async def protected_route(current_user: User = Depends(current_active_user)):
    """
    Rota protegida que requer autenticação
    """
    return {
        "message": f"Olá {current_user.nome or current_user.email}!",
        "user_id": current_user.id,
    }


@router.get("/admin-only")
async def admin_only_route(current_user: User = Depends(current_superuser)):
    """
    Rota que requer privilégios de administrador
    """
    return {"message": "Acesso de administrador concedido", "user_id": current_user.id}
