"""
Package Pages routes
Regroupe toutes les routes HTML pour les pages
"""
from app.routes.pages.client import router as client_router
from app.routes.pages.auth import router as auth_router
from app.routes.pages.admin import router as admin_router

__all__ = [
    "client_router",
    "auth_router",
    "admin_router"
]
