"""
Modèles Pydantic v2 pour les entités de l'application
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class ProductBase(BaseModel):
    """Modèle de base pour un produit"""
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    short_description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0)
    category: str = Field(..., min_length=1)
    stock: int = Field(..., ge=0)
    status: str = Field(default="draft", pattern="^(draft|online|out-of-stock)$")
    
    # Dimensions
    width: Optional[float] = Field(None, gt=0)
    height: Optional[float] = Field(None, gt=0)
    depth: Optional[float] = Field(None, gt=0)
    
    # Images
    main_image: Optional[str] = None
    additional_images: List[str] = Field(default_factory=list)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Vase céramique artisanal",
                "description": "Vase en céramique fait main par un artisan provençal",
                "short_description": "Vase en céramique artisanale",
                "price": 45.00,
                "category": "Décoration",
                "stock": 12,
                "status": "online",
                "width": 15.0,
                "height": 25.0,
                "depth": 15.0
            }
        }
    )


class Product(ProductBase):
    """Modèle complet pour un produit avec ID et métadonnées"""
    id: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    embedding: Optional[List[float]] = None  # Vecteur d'embedding pour recherche sémantique
    
    model_config = ConfigDict(from_attributes=True)


class ProductCreate(ProductBase):
    """Modèle pour créer un produit"""
    pass


class ProductUpdate(BaseModel):
    """Modèle pour mettre à jour un produit (tous les champs optionnels)"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    short_description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    category: Optional[str] = None
    stock: Optional[int] = Field(None, ge=0)
    status: Optional[str] = Field(None, pattern="^(draft|online|out-of-stock)$")
    width: Optional[float] = None
    height: Optional[float] = None
    depth: Optional[float] = None
    main_image: Optional[str] = None
    additional_images: Optional[List[str]] = None
    
    model_config = ConfigDict(from_attributes=True)


class SearchQuery(BaseModel):
    """Modèle pour une requête de recherche"""
    query: str = Field(..., min_length=1)
    category: Optional[str] = None
    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, ge=0)
    status: Optional[str] = Field(None, pattern="^(draft|online|out-of-stock)$")
    use_semantic: bool = Field(default=True, description="Utiliser la recherche sémantique avec embeddings")
    top_k: int = Field(default=10, ge=1, le=100, description="Nombre maximum de résultats")
    min_score: float = Field(default=0.5, ge=0, le=1, description="Score minimum de similarité")


class SearchResult(BaseModel):
    """Modèle pour un résultat de recherche avec score"""
    product: Product
    score: float = Field(..., ge=0, le=1, description="Score de similarité (0-1)")
    
    model_config = ConfigDict(from_attributes=True)