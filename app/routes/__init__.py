"""
Package de routes pour l'application Maison Manoé
"""
from fastapi import APIRouter

# Import des routes API
from app.routes.api.products import router as products_api_router
from app.routes.api.auth import router as auth_api_router

# Import des routes pages
from app.routes.pages.client import router as client_router
from app.routes.pages.auth import router as auth_router
from app.routes.pages.admin import router as admin_router

# Router principal pour les API
api_router = APIRouter()
api_router.include_router(products_api_router)
api_router.include_router(auth_api_router)

# Router principal pour les pages HTML
pages_router = APIRouter()
pages_router.include_router(client_router)
pages_router.include_router(auth_router)
pages_router.include_router(admin_router)

__all__ = ["api_router", "pages_router"]
