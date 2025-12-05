#!/usr/bin/env python3
"""
Script pour créer des produits de démonstration
"""
import asyncio
import sys
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent))

from app.models.product import ProductCreate
from app.services.product import product_service


async def create_demo_products():
    """Créer des produits de démonstration"""
    
    products = [
        {
            "name": "Vase céramique artisanal",
            "description": "Magnifique vase en céramique fait main par un artisan provençal. Chaque pièce est unique avec ses propres nuances de couleur. Parfait pour mettre en valeur vos plus belles fleurs ou comme pièce décorative à part entière.",
            "short_description": "Vase en céramique fait main, pièce unique",
            "price": 45.00,
            "category": "Décoration",
            "stock": 12,
            "status": "online",
            "width": 15.0,
            "height": 25.0,
            "depth": 15.0,
            "main_image": "https://images.unsplash.com/photo-1578500494198-246f612d3b3d?w=800",
        },
        {
            "name": "Bougie parfumée artisanale",
            "description": "Bougie parfumée coulée à la main avec de la cire de soja naturelle. Parfum délicat et notes boisées pour une ambiance chaleureuse. Durée de combustion de 40 heures. Sans paraffine ni additifs chimiques.",
            "short_description": "Bougie naturelle en cire de soja, 40h de combustion",
            "price": 28.00,
            "category": "Décoration",
            "stock": 24,
            "status": "online",
            "width": 8.0,
            "height": 10.0,
            "depth": 8.0,
            "main_image": "https://images.unsplash.com/photo-1602874801006-c8f8f5f0e42f?w=800",
        },
        {
            "name": "Coussin en lin naturel",
            "description": "Coussin confectionné dans un lin européen de haute qualité. Tissu respirant et hypoallergénique. Le lin apporte une touche d'élégance naturelle à votre intérieur. Housse amovible lavable en machine.",
            "short_description": "Coussin 100% lin européen, housse amovible",
            "price": 35.00,
            "category": "Textile",
            "stock": 8,
            "status": "online",
            "width": 45.0,
            "height": 5.0,
            "depth": 45.0,
            "main_image": "https://images.unsplash.com/photo-1566301363515-d0e24e8a5ef7?w=800",
        },
        {
            "name": "Diffuseur d'intérieur 100ml",
            "description": "Diffuseur de parfum pour la maison avec bâtonnets en rotin. Notes fraîches et florales pour parfumer délicatement votre intérieur. Durée de diffusion de 2 à 3 mois. Flacon en verre recyclé.",
            "short_description": "Diffuseur parfumé avec bâtonnets, 100ml",
            "price": 32.00,
            "category": "Décoration",
            "stock": 15,
            "status": "online",
            "width": 6.0,
            "height": 12.0,
            "depth": 6.0,
            "main_image": "https://images.unsplash.com/photo-1602874801027-b8d1f0d13f97?w=800",
        },
        {
            "name": "Plaid en laine mérinos",
            "description": "Plaid luxueux en pure laine mérinos. Doux, chaud et élégant, il apportera une touche cosy à votre canapé ou votre lit. Tissage traditionnel et finitions soignées. Dimensions généreuses 130x180cm.",
            "short_description": "Plaid 100% laine mérinos, 130x180cm",
            "price": 89.00,
            "category": "Textile",
            "stock": 6,
            "status": "online",
            "width": 130.0,
            "height": 2.0,
            "depth": 180.0,
            "main_image": "https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=800",
        },
        {
            "name": "Corbeille en jonc de mer",
            "description": "Panier de rangement tressé à la main en jonc de mer naturel. Parfait pour ranger vos plaids, coussins ou jouets. Matériau écologique et durable. Style bohème et naturel.",
            "short_description": "Panier tressé en jonc de mer naturel",
            "price": 42.00,
            "category": "Décoration",
            "stock": 10,
            "status": "online",
            "width": 40.0,
            "height": 35.0,
            "depth": 40.0,
            "main_image": "https://images.unsplash.com/photo-1595428774223-ef52624120d2?w=800",
        },
        {
            "name": "Tasse en grès artisanale",
            "description": "Ensemble de 4 tasses en grès émaillé. Chaque tasse est unique avec ses variations de couleur naturelles. Parfaites pour le thé ou le café. Fabriquées par des artisans céramistes français.",
            "short_description": "Set de 4 tasses en grès émaillé",
            "price": 52.00,
            "category": "Vaisselle",
            "stock": 8,
            "status": "online",
            "width": 10.0,
            "height": 8.0,
            "depth": 10.0,
            "main_image": "https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?w=800",
        },
        {
            "name": "Miroir en rotin naturel",
            "description": "Miroir mural avec encadrement en rotin tressé. Design bohème et chaleureux qui s'intègre parfaitement dans tous les intérieurs. Diamètre 50cm. Accroche murale fournie.",
            "short_description": "Miroir rond en rotin tressé, Ø50cm",
            "price": 68.00,
            "category": "Décoration",
            "stock": 5,
            "status": "online",
            "width": 50.0,
            "height": 3.0,
            "depth": 50.0,
            "main_image": "https://images.unsplash.com/photo-1618220179428-22790b461013?w=800",
        },
    ]
    
    print("🌟 Création des produits de démonstration...\n")
    
    for i, product_data in enumerate(products, 1):
        try:
            product = ProductCreate(**product_data)
            created = await product_service.create_product(product)
            print(f"✅ {i}. {created.name} - {created.price}€ (ID: {created.id})")
        except Exception as e:
            print(f"❌ Erreur lors de la création de '{product_data['name']}': {e}")
    
    print(f"\n🎉 {len(products)} produits ont été créés avec succès!")
    print("\n📍 Vous pouvez maintenant:")
    print("   - Voir les produits sur http://localhost:8000/admin/produits")
    print("   - Voir la page d'accueil sur http://localhost:8000/")
    print("   - Voir la page de recherche sur http://localhost:8000/recherche")


if __name__ == "__main__":
    asyncio.run(create_demo_products())
