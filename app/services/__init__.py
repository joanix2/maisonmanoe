"""
Package services pour l'application Maison Manoé
Regroupe toute la logique métier
"""
from app.services.product import product_service
from app.services.user import user_service

__all__ = [
    "product_service",
    "user_service"
]
