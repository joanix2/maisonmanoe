"""
Script d'initialisation de la base de données Neo4j
"""
from app.database import neo4j_db
from app.models import ProductCreate
from app.services.product import product_service
import asyncio


async def create_sample_products():
    """Crée des produits d'exemple"""
    
    sample_products = [
        ProductCreate(
            name="Vase céramique artisanal",
            description="Vase en céramique fait main par un artisan provençal. Chaque pièce est unique avec des variations naturelles de couleur et de texture. Parfait pour des bouquets de fleurs fraîches ou séchées.",
            short_description="Vase en céramique artisanale provençale",
            price=45.00,
            category="Décoration",
            stock=12,
            status="online",
            width=15.0,
            height=25.0,
            depth=15.0,
            main_image="/images/vase-ceramique.jpg"
        ),
        ProductCreate(
            name="Bougie parfumée artisanale",
            description="Bougie naturelle en cire de soja avec mèches en coton. Parfum délicat de lavande et bergamote. Durée de combustion : 40 heures. Fabriquée en France dans le respect de l'environnement.",
            short_description="Bougie naturelle parfum lavande",
            price=28.00,
            category="Décoration",
            stock=24,
            status="online",
            width=8.0,
            height=10.0,
            depth=8.0,
            main_image="/images/bougie.jpg"
        ),
        ProductCreate(
            name="Coussin en lin naturel",
            description="Coussin en lin lavé 100% naturel. Douceur et élégance pour votre canapé ou votre lit. Le lin est une matière noble, respirante et durable. Housse amovible avec fermeture éclair invisible.",
            short_description="Coussin lin naturel 45x45cm",
            price=35.00,
            category="Textile",
            stock=8,
            status="online",
            width=45.0,
            height=45.0,
            depth=12.0,
            main_image="/images/coussin-lin.jpg"
        ),
        ProductCreate(
            name="Lampe de table en bois",
            description="Lampe de chevet en bois massif tourné à la main. Pied en chêne français avec finition naturelle. Abat-jour en lin écru. Design intemporel qui s'adapte à tous les intérieurs.",
            short_description="Lampe chevet bois massif",
            price=89.00,
            category="Luminaires",
            stock=6,
            status="online",
            width=30.0,
            height=45.0,
            depth=30.0,
            main_image="/images/lampe-bois.jpg"
        ),
        ProductCreate(
            name="Plaid en laine mérinos",
            description="Plaid doux et chaud en pure laine mérinos. Tissé en France selon des méthodes traditionnelles. Parfait pour les soirées d'hiver. Entretien facile, lavable en machine à 30°C.",
            short_description="Plaid laine mérinos 130x180cm",
            price=125.00,
            category="Textile",
            stock=15,
            status="online",
            width=130.0,
            height=180.0,
            depth=5.0,
            main_image="/images/plaid-laine.jpg"
        ),
        ProductCreate(
            name="Miroir rond en rotin",
            description="Miroir mural avec cadre en rotin naturel tressé à la main. Style bohème chic qui apporte chaleur et lumière à votre intérieur. Fixations murales incluses.",
            short_description="Miroir rotin tressé Ø60cm",
            price=68.00,
            category="Décoration",
            stock=10,
            status="online",
            width=60.0,
            height=60.0,
            depth=5.0,
            main_image="/images/miroir-rotin.jpg"
        )
    ]
    
    print("\n🌱 Création des produits d'exemple...\n")
    
    for product_data in sample_products:
        try:
            product = await product_service.create_product(product_data)
            print(f"✓ Produit créé: {product.name} (ID: {product.id})")
        except Exception as e:
            print(f"✗ Erreur lors de la création de {product_data.name}: {e}")
    
    print("\n✅ Produits d'exemple créés avec succès!\n")


async def init_database():
    """Initialise la base de données"""
    print("🚀 Initialisation de la base de données Neo4j\n")
    
    # Vérifier la connexion
    if not neo4j_db.verify_connection():
        print("❌ Impossible de se connecter à Neo4j")
        return
    
    # Créer les contraintes
    print("📋 Création des contraintes...")
    constraints = [
        "CREATE CONSTRAINT product_id_unique IF NOT EXISTS FOR (p:Product) REQUIRE p.id IS UNIQUE",
        "CREATE CONSTRAINT promo_code_unique IF NOT EXISTS FOR (pr:Promo) REQUIRE pr.code IS UNIQUE"
    ]
    
    for constraint in constraints:
        try:
            neo4j_db.execute_query(constraint)
            print(f"✓ Contrainte créée")
        except Exception as e:
            print(f"⚠ {e}")
    
    # Créer les index vectoriels
    print("\n🔍 Création des index vectoriels...")
    neo4j_db.create_vector_index("Product", "embedding")
    
    # Créer des produits d'exemple
    await create_sample_products()
    
    print("✅ Base de données initialisée!\n")


if __name__ == "__main__":
    asyncio.run(init_database())
