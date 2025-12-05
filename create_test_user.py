"""
Script pour créer un utilisateur de test
"""
import asyncio
from app.services.user import user_service
from app.models.user import UserCreate


async def main():
    print("\n=== Création d'un utilisateur de test ===\n")
    
    # Données de test
    test_user = UserCreate(
        email="test@maisonmanoe.fr",
        password="Test123456!",
        first_name="Jean",
        last_name="Dupont",
        phone="+33 6 12 34 56 78"
    )
    
    try:
        # Créer l'utilisateur
        user = await user_service.create_user(test_user)
        
        print("✅ Utilisateur de test créé avec succès !")
        print(f"   Email: {user.email}")
        print(f"   Nom: {user.first_name} {user.last_name}")
        print(f"   Téléphone: {user.phone}")
        print(f"   ID: {user.id}")
        print(f"\n🔑 Mot de passe: Test123456!")
        print(f"\n💡 Vous pouvez maintenant vous connecter sur http://localhost:8000/connexion")
        
    except ValueError as e:
        print(f"⚠️  Erreur: {e}")
        print("   L'utilisateur existe peut-être déjà.")
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")


if __name__ == "__main__":
    asyncio.run(main())
