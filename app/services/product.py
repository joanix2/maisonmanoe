"""
Service de gestion des produits avec Neo4j et embeddings
"""
from typing import List, Optional
from datetime import datetime
import uuid

from app.database import neo4j_db
from app.models import Product, ProductCreate, ProductUpdate, SearchQuery, SearchResult


class ProductService:
    """Service pour gérer les produits dans Neo4j"""
    
    def __init__(self):
        # Créer l'index vectoriel au démarrage
        neo4j_db.create_vector_index("Product", "embedding")
    
    def _generate_searchable_text(self, product_data: dict) -> str:
        """Génère un texte combiné pour l'embedding"""
        parts = [
            product_data.get("name", ""),
            product_data.get("description", ""),
            product_data.get("category", ""),
            product_data.get("short_description", "")
        ]
        return " ".join([p for p in parts if p])
    
    async def create_product(self, product_data: ProductCreate) -> Product:
        """
        Crée un nouveau produit avec embedding
        
        Args:
            product_data: Données du produit
            
        Returns:
            Produit créé avec son ID
        """
        product_id = str(uuid.uuid4())
        now = datetime.now()
        
        # Générer l'embedding
        searchable_text = self._generate_searchable_text(product_data.model_dump())
        embedding = neo4j_db.generate_embedding(searchable_text)
        
        # Préparer les données
        product_dict = product_data.model_dump()
        product_dict.update({
            "id": product_id,
            "created_at": now.isoformat(),
            "updated_at": now.isoformat(),
            "embedding": embedding
        })
        
        # Créer le nœud dans Neo4j
        query = """
        CREATE (p:Product $props)
        RETURN p
        """
        
        result = neo4j_db.execute_query(query, {"props": product_dict})
        
        if result:
            return Product(**result[0]["p"])
        
        raise Exception("Erreur lors de la création du produit")
    
    async def get_product(self, product_id: str) -> Optional[Product]:
        """Récupère un produit par son ID"""
        query = """
        MATCH (p:Product {id: $product_id})
        RETURN p
        """
        
        result = neo4j_db.execute_query(query, {"product_id": product_id})
        
        if result:
            return Product(**result[0]["p"])
        
        return None
    
    async def update_product(self, product_id: str, product_data: ProductUpdate) -> Optional[Product]:
        """
        Met à jour un produit et régénère son embedding si nécessaire
        
        Args:
            product_id: ID du produit
            product_data: Nouvelles données (uniquement les champs modifiés)
            
        Returns:
            Produit mis à jour ou None si non trouvé
        """
        # Récupérer le produit existant
        existing = await self.get_product(product_id)
        if not existing:
            return None
        
        # Préparer les données de mise à jour
        update_dict = product_data.model_dump(exclude_unset=True)
        
        # Si des champs affectant l'embedding sont modifiés, régénérer l'embedding
        embedding_fields = {"name", "description", "short_description", "category"}
        if any(field in update_dict for field in embedding_fields):
            # Fusionner avec les données existantes
            merged_data = existing.model_dump()
            merged_data.update(update_dict)
            
            searchable_text = self._generate_searchable_text(merged_data)
            update_dict["embedding"] = neo4j_db.generate_embedding(searchable_text)
        
        update_dict["updated_at"] = datetime.now().isoformat()
        
        # Construire la clause SET
        set_clauses = [f"p.{key} = ${key}" for key in update_dict.keys()]
        set_clause = ", ".join(set_clauses)
        
        query = f"""
        MATCH (p:Product {{id: $product_id}})
        SET {set_clause}
        RETURN p
        """
        
        params = {"product_id": product_id, **update_dict}
        result = neo4j_db.execute_query(query, params)
        
        if result:
            return Product(**result[0]["p"])
        
        return None
    
    async def delete_product(self, product_id: str) -> bool:
        """Supprime un produit"""
        query = """
        MATCH (p:Product {id: $product_id})
        DELETE p
        RETURN count(p) as deleted
        """
        
        result = neo4j_db.execute_query(query, {"product_id": product_id})
        return result[0]["deleted"] > 0 if result else False
    
    async def list_products(
        self,
        category: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 20,
        skip: int = 0
    ) -> List[Product]:
        """Liste les produits avec filtres optionnels"""
        where_clauses = []
        params = {"limit": limit, "skip": skip}
        
        if category:
            where_clauses.append("p.category = $category")
            params["category"] = category
        
        if status:
            where_clauses.append("p.status = $status")
            params["status"] = status
        
        where_clause = " AND ".join(where_clauses) if where_clauses else "1=1"
        
        query = f"""
        MATCH (p:Product)
        WHERE {where_clause}
        RETURN p
        ORDER BY p.created_at DESC
        SKIP $skip
        LIMIT $limit
        """
        
        result = neo4j_db.execute_query(query, params)
        return [Product(**r["p"]) for r in result]
    
    async def search_products(self, search_query: SearchQuery) -> List[SearchResult]:
        """
        Recherche de produits avec recherche vectorielle sémantique
        
        Args:
            search_query: Requête de recherche avec filtres
            
        Returns:
            Liste de résultats avec scores de pertinence
        """
        if search_query.use_semantic:
            # Recherche vectorielle
            results = neo4j_db.vector_search(
                query_text=search_query.query,
                label="Product",
                top_k=search_query.limit,
                min_score=0.3  # Score minimum de similarité
            )
            
            search_results = []
            for r in results:
                product = Product(**r["node"])
                
                # Appliquer les filtres supplémentaires
                if search_query.category and product.category != search_query.category:
                    continue
                if search_query.status and product.status != search_query.status:
                    continue
                if search_query.min_price and product.price < search_query.min_price:
                    continue
                if search_query.max_price and product.price > search_query.max_price:
                    continue
                
                search_results.append(
                    SearchResult(product=product, score=r["score"])
                )
            
            return search_results
        
        else:
            # Recherche textuelle classique
            where_clauses = ["toLower(p.name) CONTAINS toLower($query) OR toLower(p.description) CONTAINS toLower($query)"]
            params = {"query": search_query.query, "limit": search_query.limit}
            
            if search_query.category:
                where_clauses.append("p.category = $category")
                params["category"] = search_query.category
            
            if search_query.status:
                where_clauses.append("p.status = $status")
                params["status"] = search_query.status
            
            if search_query.min_price:
                where_clauses.append("p.price >= $min_price")
                params["min_price"] = search_query.min_price
            
            if search_query.max_price:
                where_clauses.append("p.price <= $max_price")
                params["max_price"] = search_query.max_price
            
            where_clause = " AND ".join(where_clauses)
            
            query = f"""
            MATCH (p:Product)
            WHERE {where_clause}
            RETURN p
            LIMIT $limit
            """
            
            result = neo4j_db.execute_query(query, params)
            return [SearchResult(product=Product(**r["p"]), score=1.0) for r in result]


# Instance globale
product_service = ProductService()
