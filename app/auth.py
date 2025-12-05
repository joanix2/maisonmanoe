"""
Utilitaires pour l'authentification JWT et le hashage des mots de passe
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from config import settings

# Configuration du hashage des mots de passe avec bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuration OAuth2 avec le schéma Bearer Token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Vérifie qu'un mot de passe en clair correspond au hash
    
    Args:
        plain_password: Mot de passe en clair
        hashed_password: Mot de passe hashé
        
    Returns:
        True si le mot de passe correspond, False sinon
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash un mot de passe avec bcrypt
    
    Args:
        password: Mot de passe en clair
        
    Returns:
        Mot de passe hashé
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crée un token JWT
    
    Args:
        data: Données à encoder dans le token (ex: {"sub": user_email})
        expires_delta: Durée de validité du token (par défaut: 30 minutes)
        
    Returns:
        Token JWT encodé
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.secret_key, 
        algorithm=settings.algorithm
    )
    
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    Décode un token JWT
    
    Args:
        token: Token JWT à décoder
        
    Returns:
        Données décodées du token ou None si invalide
    """
    try:
        payload = jwt.decode(
            token, 
            settings.secret_key, 
            algorithms=[settings.algorithm]
        )
        return payload
    except JWTError:
        return None


async def get_current_user_email(token: str = Depends(oauth2_scheme)) -> str:
    """
    Récupère l'email de l'utilisateur depuis le token JWT
    
    Args:
        token: Token JWT
        
    Returns:
        Email de l'utilisateur
        
    Raises:
        HTTPException: Si le token est invalide
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Impossible de valider les identifiants",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    
    return email


async def get_optional_current_user_email(token: Optional[str] = Depends(oauth2_scheme)) -> Optional[str]:
    """
    Récupère l'email de l'utilisateur depuis le token JWT (optionnel)
    Ne lève pas d'exception si le token est absent ou invalide
    
    Args:
        token: Token JWT (optionnel)
        
    Returns:
        Email de l'utilisateur ou None
    """
    if token is None:
        return None
    
    payload = decode_access_token(token)
    if payload is None:
        return None
    
    return payload.get("sub")
