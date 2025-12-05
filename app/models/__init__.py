"""
Package models pour l'application Maison Manoé
Regroupe tous les modèles Pydantic
"""
from app.models.product import (
    ProductBase,
    Product,
    ProductCreate,
    ProductUpdate,
    SearchQuery,
    SearchResult
)
from app.models.promo import (
    PromoBase,
    Promo,
    PromoCreate
)
from app.models.user import (
    UserBase,
    User,
    UserCreate,
    UserUpdate,
    UserInDB,
    Token,
    TokenData,
    LoginRequest
)

__all__ = [
    # Product models
    "ProductBase",
    "Product",
    "ProductCreate",
    "ProductUpdate",
    "SearchQuery",
    "SearchResult",
    # Promo models
    "PromoBase",
    "Promo",
    "PromoCreate",
    # User models
    "UserBase",
    "User",
    "UserCreate",
    "UserUpdate",
    "UserInDB",
    "Token",
    "TokenData",
    "LoginRequest"
]
