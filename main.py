from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

# Import des routes
from app.routes import api_router, pages_router
from app.database import neo4j_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestion du cycle de vie de l'application"""
    # Startup
    print("🚀 Démarrage de l'application...")
    print("✓ Connexion à Neo4j établie")
    yield
    # Shutdown
    print("🛑 Arrêt de l'application...")
    neo4j_db.close()


app = FastAPI(
    title="Maison Manoé",
    description="E-commerce pour décoration d'intérieur artisanale avec recherche sémantique",
    version="1.0.0",
    lifespan=lifespan
)

# Monter les fichiers statiques
app.mount("/static", StaticFiles(directory="static"), name="static")

# Inclure les routes
app.include_router(api_router)    # API REST (/api/products)
app.include_router(pages_router)  # Toutes les pages HTML (client + auth + admin)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
