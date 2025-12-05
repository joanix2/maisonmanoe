"""
Routes API pour l'authentification
"""
from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.models.user import User, UserCreate, Token, LoginRequest
from app.services.user import user_service
from app.auth import create_access_token, get_current_user_email
from app.config import settings

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """
    Inscription d'un nouvel utilisateur
    
    - **email**: Email unique de l'utilisateur
    - **password**: Mot de passe (min 8 caractères)
    - **first_name**: Prénom
    - **last_name**: Nom
    - **phone**: Téléphone (optionnel)
    """
    try:
        user = await user_service.create_user(user_data)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest):
    """
    Connexion d'un utilisateur avec email et mot de passe
    
    - **email**: Email de l'utilisateur
    - **password**: Mot de passe
    
    Retourne un token JWT pour authentifier les requêtes suivantes
    """
    user = await user_service.authenticate_user(login_data.email, login_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Compte utilisateur désactivé"
        )
    
    # Créer le token JWT
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id},
        expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")


@router.post("/token", response_model=Token)
async def login_oauth2(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Connexion OAuth2 (compatible avec le schéma OAuth2PasswordBearer)
    
    Endpoint utilisé automatiquement par FastAPI pour l'authentification via formulaire
    """
    user = await user_service.authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Compte utilisateur désactivé"
        )
    
    # Créer le token JWT
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id},
        expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=User)
async def get_current_user(current_user_email: str = Depends(get_current_user_email)):
    """
    Récupère les informations de l'utilisateur connecté
    
    Nécessite un token JWT valide dans le header Authorization: Bearer <token>
    """
    user = await user_service.get_user_by_email(current_user_email)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )
    
    return user
