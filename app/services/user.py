"""
Service de gestion des utilisateurs avec Neo4j
"""
from typing import Optional
from datetime import datetime
import uuid

from app.database import neo4j_db
from app.models.user import User, UserCreate, UserUpdate, UserInDB
from app.auth import get_password_hash, verify_password


class UserService:
    """Service pour gérer les utilisateurs dans Neo4j"""
    
    async def create_user(self, user_data: UserCreate) -> User:
        """
        Crée un nouveau utilisateur avec mot de passe hashé
        
        Args:
            user_data: Données de l'utilisateur
            
        Returns:
            Utilisateur créé
            
        Raises:
            ValueError: Si l'email existe déjà
        """
        # Vérifier si l'email existe déjà
        existing_user = await self.get_user_by_email(user_data.email)
        if existing_user:
            raise ValueError("Un utilisateur avec cet email existe déjà")
        
        user_id = str(uuid.uuid4())
        now = datetime.now()
        
        # Hash du mot de passe
        hashed_password = get_password_hash(user_data.password)
        
        # Préparer les données
        user_dict = user_data.model_dump(exclude={"password"})
        user_dict.update({
            "id": user_id,
            "hashed_password": hashed_password,
            "is_active": True,
            "is_admin": False,
            "created_at": now.isoformat(),
            "updated_at": now.isoformat()
        })
        
        # Créer le nœud User dans Neo4j
        query = """
        CREATE (u:User {
            id: $id,
            email: $email,
            first_name: $first_name,
            last_name: $last_name,
            phone: $phone,
            hashed_password: $hashed_password,
            is_active: $is_active,
            is_admin: $is_admin,
            created_at: $created_at,
            updated_at: $updated_at
        })
        RETURN u
        """
        
        result = neo4j_db.execute_query(query, user_dict)
        
        # Retourner l'utilisateur sans le mot de passe
        return User(**{k: v for k, v in user_dict.items() if k != "hashed_password"})
    
    async def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        """
        Récupère un utilisateur par son email
        
        Args:
            email: Email de l'utilisateur
            
        Returns:
            Utilisateur trouvé ou None
        """
        query = """
        MATCH (u:User {email: $email})
        RETURN u
        """
        
        result = neo4j_db.execute_query(query, {"email": email})
        
        if not result or len(result) == 0:
            return None
        
        # result est une liste de dicts: [{'u': {...}}]
        user_data = result[0].get('u')
        if not user_data:
            return None
        
        return UserInDB(**user_data)
    
    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """
        Récupère un utilisateur par son ID
        
        Args:
            user_id: ID de l'utilisateur
            
        Returns:
            Utilisateur trouvé ou None
        """
        query = """
        MATCH (u:User {id: $id})
        RETURN u
        """
        
        result = neo4j_db.execute_query(query, {"id": user_id})
        
        if not result or len(result) == 0:
            return None
        
        # result est une liste de dicts: [{'u': {...}}]
        user_node = result[0].get('u')
        if not user_node:
            return None
        
        user_data = {k: v for k, v in user_node.items() if k != "hashed_password"}
        
        return User(**user_data)
    
    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Authentifie un utilisateur
        
        Args:
            email: Email de l'utilisateur
            password: Mot de passe en clair
            
        Returns:
            Utilisateur si authentification réussie, None sinon
        """
        user_in_db = await self.get_user_by_email(email)
        
        if not user_in_db:
            return None
        
        if not verify_password(password, user_in_db.hashed_password):
            return None
        
        # Retourner l'utilisateur sans le mot de passe
        user_data = user_in_db.model_dump(exclude={"hashed_password"})
        return User(**user_data)
    
    async def update_user(self, user_id: str, user_data: UserUpdate) -> Optional[User]:
        """
        Met à jour un utilisateur
        
        Args:
            user_id: ID de l'utilisateur
            user_data: Données à mettre à jour
            
        Returns:
            Utilisateur mis à jour ou None si non trouvé
        """
        # Construire la requête de mise à jour dynamiquement
        update_dict = user_data.model_dump(exclude_unset=True)
        
        if not update_dict:
            return await self.get_user_by_id(user_id)
        
        # Hash du nouveau mot de passe si fourni
        if "password" in update_dict:
            update_dict["hashed_password"] = get_password_hash(update_dict.pop("password"))
        
        update_dict["updated_at"] = datetime.now().isoformat()
        
        # Construire les clauses SET
        set_clauses = [f"u.{key} = ${key}" for key in update_dict.keys()]
        set_clause = ", ".join(set_clauses)
        
        query = f"""
        MATCH (u:User {{id: $id}})
        SET {set_clause}
        RETURN u
        """
        
        params = {"id": user_id, **update_dict}
        result = neo4j_db.execute_query(query, params)
        
        if not result or len(result) == 0:
            return None
        
        user_node = result[0].get('u')
        if not user_node:
            return None
        
        user_data_dict = {k: v for k, v in user_node.items() if k != "hashed_password"}
        
        return User(**user_data_dict)
    
    async def delete_user(self, user_id: str) -> bool:
        """
        Supprime un utilisateur
        
        Args:
            user_id: ID de l'utilisateur
            
        Returns:
            True si supprimé, False sinon
        """
        query = """
        MATCH (u:User {id: $id})
        DELETE u
        RETURN COUNT(u) as deleted
        """
        
        result = neo4j_db.execute_query(query, {"id": user_id})
        return result and len(result) > 0 and result[0].get('deleted', 0) > 0


# Instance globale du service
user_service = UserService()
