"""
Modèles Pydantic v2 pour les utilisateurs et l'authentification
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, ConfigDict


class UserBase(BaseModel):
    """Modèle de base pour un utilisateur"""
    email: EmailStr = Field(..., description="Email de l'utilisateur")
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "jean.dupont@example.com",
                "first_name": "Jean",
                "last_name": "Dupont",
                "phone": "+33612345678"
            }
        }
    )


class UserCreate(UserBase):
    """Modèle pour créer un utilisateur"""
    password: str = Field(..., min_length=8, max_length=100, description="Mot de passe (min 8 caractères)")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "jean.dupont@example.com",
                "first_name": "Jean",
                "last_name": "Dupont",
                "phone": "+33612345678",
                "password": "MotDePasse123!"
            }
        }
    )


class User(UserBase):
    """Modèle complet pour un utilisateur"""
    id: str
    is_active: bool = Field(default=True)
    is_admin: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    model_config = ConfigDict(from_attributes=True)


class UserInDB(User):
    """Modèle utilisateur avec mot de passe hashé (pour la DB)"""
    hashed_password: str


class UserUpdate(BaseModel):
    """Modèle pour mettre à jour un utilisateur"""
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    password: Optional[str] = Field(None, min_length=8, max_length=100)
    
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """Modèle pour le token JWT"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Données contenues dans le token JWT"""
    email: Optional[str] = None
    user_id: Optional[str] = None


class LoginRequest(BaseModel):
    """Modèle pour la requête de connexion"""
    email: EmailStr
    password: str
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "jean.dupont@example.com",
                "password": "MotDePasse123!"
            }
        }
    )
