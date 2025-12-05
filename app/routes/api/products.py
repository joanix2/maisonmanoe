"""
API Routes pour les produits
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from app.models import Product, ProductCreate, ProductUpdate, SearchQuery, SearchResult
from app.services.product import product_service

router = APIRouter(prefix="/api/products", tags=["products"])


@router.post("", response_model=Product, status_code=201)
async def create_product(product: ProductCreate):
    """Créer un nouveau produit"""
    try:
        return await product_service.create_product(product)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: str):
    """Récupérer un produit par son ID"""
    product = await product_service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return product


@router.put("/{product_id}", response_model=Product)
async def update_product(product_id: str, product: ProductUpdate):
    """Mettre à jour un produit"""
    updated = await product_service.update_product(product_id, product)
    if not updated:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return updated


@router.delete("/{product_id}", status_code=204)
async def delete_product(product_id: str):
    """Supprimer un produit"""
    deleted = await product_service.delete_product(product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Produit non trouvé")


@router.get("", response_model=List[Product])
async def list_products(
    category: Optional[str] = Query(None, description="Filtrer par catégorie"),
    status: Optional[str] = Query(None, description="Filtrer par statut"),
    limit: int = Query(20, ge=1, le=100, description="Nombre de résultats"),
    skip: int = Query(0, ge=0, description="Nombre de résultats à sauter")
):
    """Lister les produits avec filtres optionnels"""
    return await product_service.list_products(
        category=category,
        status=status,
        limit=limit,
        skip=skip
    )


@router.post("/search", response_model=List[SearchResult])
async def search_products(search: SearchQuery):
    """
    Rechercher des produits avec recherche sémantique
    
    La recherche sémantique utilise des embeddings pour trouver des produits
    similaires même si les mots exacts ne correspondent pas.
    """
    return await product_service.search_products(search)
