"""
Module de connexion et gestion de Neo4j avec support des embeddings vectoriels
"""
from typing import List, Optional, Dict, Any
from neo4j import GraphDatabase, Driver
from sentence_transformers import SentenceTransformer
import numpy as np
from config import settings


class Neo4jConnection:
    """Gestionnaire de connexion Neo4j avec support des embeddings"""
    
    def __init__(self):
        self.driver: Optional[Driver] = None
        self.embedding_model: Optional[SentenceTransformer] = None
        self._initialize()
    
    def _initialize(self):
        """Initialise la connexion et le modèle d'embeddings"""
        # Connexion à Neo4j
        self.driver = GraphDatabase.driver(
            settings.neo4j_uri,
            auth=(settings.neo4j_user, settings.neo4j_password)
        )
        
        # Charger le modèle d'embeddings
        print(f"Chargement du modèle d'embeddings: {settings.embedding_model}")
        self.embedding_model = SentenceTransformer(settings.embedding_model)
        print(f"Modèle chargé. Dimension: {self.embedding_model.get_sentence_embedding_dimension()}")
        
        # Vérifier la connexion
        self.verify_connection()
    
    def verify_connection(self) -> bool:
        """Vérifie que la connexion à Neo4j fonctionne"""
        try:
            with self.driver.session() as session:
                result = session.run("RETURN 1 as test")
                record = result.single()
                if record and record["test"] == 1:
                    print("✓ Connexion à Neo4j établie")
                    return True
            return False
        except Exception as e:
            print(f"✗ Erreur de connexion à Neo4j: {e}")
            return False
    
    def close(self):
        """Ferme la connexion à Neo4j"""
        if self.driver:
            self.driver.close()
            print("Connexion à Neo4j fermée")
    
    def create_vector_index(self, label: str, property_name: str = "embedding"):
        """
        Crée un index vectoriel pour les recherches de similarité
        
        Args:
            label: Label du nœud (ex: "Product")
            property_name: Nom de la propriété contenant l'embedding
        """
        index_name = f"{label.lower()}_vector_index"
        
        with self.driver.session() as session:
            # Vérifier si l'index existe déjà
            check_query = """
            SHOW INDEXES
            YIELD name
            WHERE name = $index_name
            RETURN count(*) as count
            """
            result = session.run(check_query, index_name=index_name)
            exists = result.single()["count"] > 0
            
            if exists:
                print(f"Index vectoriel '{index_name}' existe déjà")
                return
            
            # Créer l'index vectoriel
            create_query = f"""
            CREATE VECTOR INDEX {index_name} IF NOT EXISTS
            FOR (n:{label})
            ON (n.{property_name})
            OPTIONS {{
                indexConfig: {{
                    `vector.dimensions`: {settings.embedding_dimension},
                    `vector.similarity_function`: 'cosine'
                }}
            }}
            """
            session.run(create_query)
            print(f"✓ Index vectoriel '{index_name}' créé pour {label}.{property_name}")
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Génère un embedding vectoriel pour un texte
        
        Args:
            text: Texte à transformer en embedding
            
        Returns:
            Liste de floats représentant l'embedding
        """
        if not self.embedding_model:
            raise RuntimeError("Modèle d'embeddings non chargé")
        
        embedding = self.embedding_model.encode(text, convert_to_numpy=True)
        return embedding.tolist()
    
    def execute_query(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Exécute une requête Cypher
        
        Args:
            query: Requête Cypher
            parameters: Paramètres de la requête
            
        Returns:
            Liste de dictionnaires avec les résultats
        """
        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            return [dict(record) for record in result]
    
    def vector_search(
        self,
        query_text: str,
        label: str,
        top_k: int = 10,
        min_score: float = 0.0
    ) -> List[Dict[str, Any]]:
        """
        Recherche vectorielle par similarité
        
        Args:
            query_text: Texte de recherche
            label: Label des nœuds à rechercher
            top_k: Nombre de résultats à retourner
            min_score: Score minimum de similarité (0-1)
            
        Returns:
            Liste de résultats avec score de similarité
        """
        # Générer l'embedding de la requête
        query_embedding = self.generate_embedding(query_text)
        
        # Recherche vectorielle
        cypher_query = f"""
        CALL db.index.vector.queryNodes(
            '{label.lower()}_vector_index',
            $top_k,
            $query_embedding
        )
        YIELD node, score
        WHERE score >= $min_score
        RETURN node, score
        ORDER BY score DESC
        """
        
        results = self.execute_query(
            cypher_query,
            {
                "query_embedding": query_embedding,
                "top_k": top_k,
                "min_score": min_score
            }
        )
        
        return results


# Instance globale
neo4j_db = Neo4jConnection()
