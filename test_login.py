"""
Script pour tester la connexion et vérifier les utilisateurs dans Neo4j
"""
import asyncio
from app.database import neo4j_db
from app.services.user import user_service


async def main():
    print("\n=== Test de connexion et vérification des utilisateurs ===\n")
    
    # Lister tous les utilisateurs
    query = """
    MATCH (u:User)
    RETURN u.email as email, u.first_name as first_name, u.last_name as last_name, u.is_admin as is_admin
    """
    
    users = neo4j_db.execute_query(query)
    
    if not users:
        print("❌ Aucun utilisateur trouvé dans la base de données")
        print("\nVeuillez d'abord créer un utilisateur :")
        print("  - Via l'interface web : http://localhost:8000/inscription")
        print("  - Via le script : python create_admin.py")
        return
    
    print(f"✅ {len(users)} utilisateur(s) trouvé(s) :\n")
    for i, user in enumerate(users, 1):
        admin_badge = " 👑 ADMIN" if user.get('is_admin') else ""
        print(f"  {i}. {user.get('email')} - {user.get('first_name')} {user.get('last_name')}{admin_badge}")
    
    print("\n" + "="*50)
    
    # Test de récupération d'un utilisateur
    if users:
        test_email = users[0].get('email')
        print(f"\n🔍 Test de récupération de l'utilisateur : {test_email}")
        
        user = await user_service.get_user_by_email(test_email)
        
        if user:
            print(f"✅ Utilisateur trouvé !")
            print(f"   - ID: {user.id}")
            print(f"   - Email: {user.email}")
            print(f"   - Nom: {user.first_name} {user.last_name}")
            print(f"   - Actif: {user.is_active}")
            print(f"   - Admin: {user.is_admin}")
            print(f"   - Mot de passe hashé: {user.hashed_password[:20]}...")
        else:
            print(f"❌ Impossible de récupérer l'utilisateur")
    
    print("\n" + "="*50 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
