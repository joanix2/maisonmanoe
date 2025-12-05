"""
Package API routes
Regroupe toutes les routes API REST
"""
from app.routes.api.products import router as products_router
from app.routes.api.auth import router as auth_router

__all__ = [
    "products_router",
    "auth_router"
]
