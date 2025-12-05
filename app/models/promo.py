"""
Modèles Pydantic v2 pour les entités de l'application
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class PromoBase(BaseModel):
    """Modèle de base pour une promotion"""
    code: str = Field(..., min_length=3, max_length=20, pattern="^[A-Z0-9]+$")
    type: str = Field(..., pattern="^(percentage|fixed)$")
    value: float = Field(..., gt=0)
    max_uses: Optional[int] = Field(None, gt=0)
    end_date: Optional[datetime] = None
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "code": "NOEL2025",
                "type": "percentage",
                "value": 20.0,
                "max_uses": 100,
                "end_date": "2025-12-31T23:59:59"
            }
        }
    )


class Promo(PromoBase):
    """Modèle complet pour une promotion"""
    id: str
    uses: int = Field(default=0, ge=0)
    status: str = Field(default="active", pattern="^(active|scheduled|expired)$")
    created_at: datetime = Field(default_factory=datetime.now)
    
    model_config = ConfigDict(from_attributes=True)


class PromoCreate(PromoBase):
    """Modèle pour créer une promotion"""
    pass
