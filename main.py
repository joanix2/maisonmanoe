from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Maison Manoé", description="E-commerce pour décoration d'intérieur artisanale")

# Monter les fichiers statiques
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuration des templates
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Page d'accueil"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/recherche", response_class=HTMLResponse)
async def recherche(request: Request, q: str = ""):
    """Page de recherche de produits"""
    return templates.TemplateResponse("recherche.html", {"request": request, "query": q})


@app.get("/panier", response_class=HTMLResponse)
async def panier(request: Request):
    """Page du panier"""
    return templates.TemplateResponse("panier.html", {"request": request})


@app.get("/a-propos", response_class=HTMLResponse)
async def a_propos(request: Request):
    """Page à propos"""
    return templates.TemplateResponse("a-propos.html", {"request": request})


@app.get("/confidentialite", response_class=HTMLResponse)
async def confidentialite(request: Request):
    """Page de confidentialité"""
    return templates.TemplateResponse("confidentialite.html", {"request": request})


@app.get("/cgv", response_class=HTMLResponse)
async def cgv(request: Request):
    """Page des conditions générales de vente"""
    return templates.TemplateResponse("cgv.html", {"request": request})


@app.get("/profile", response_class=HTMLResponse)
async def profile(request: Request):
    """Page de profil utilisateur"""
    return templates.TemplateResponse("profile.html", {"request": request})


@app.get("/favoris", response_class=HTMLResponse)
async def favoris(request: Request):
    """Page des favoris"""
    return templates.TemplateResponse("favoris.html", {"request": request})


@app.get("/paiement", response_class=HTMLResponse)
async def paiement(request: Request):
    """Page de paiement"""
    return templates.TemplateResponse("paiement.html", {"request": request})


@app.get("/validation-paiement", response_class=HTMLResponse)
async def validation_paiement(request: Request):
    """Page de validation du paiement"""
    return templates.TemplateResponse("validation-paiement.html", {"request": request})


@app.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    """Page de contact"""
    return templates.TemplateResponse("contact.html", {"request": request})


@app.get("/retours", response_class=HTMLResponse)
async def retours(request: Request):
    """Page de retours et échanges"""
    return templates.TemplateResponse("retours.html", {"request": request})


@app.get("/livraison", response_class=HTMLResponse)
async def livraison(request: Request):
    """Page d'informations sur la livraison"""
    return templates.TemplateResponse("livraison.html", {"request": request})


@app.get("/faq", response_class=HTMLResponse)
async def faq(request: Request):
    """Page FAQ - Questions fréquentes"""
    return templates.TemplateResponse("faq.html", {"request": request})


@app.get("/inscription", response_class=HTMLResponse)
async def inscription(request: Request):
    """Page d'inscription"""
    return templates.TemplateResponse("inscription.html", {"request": request})


@app.get("/connexion", response_class=HTMLResponse)
async def connexion(request: Request):
    """Page de connexion"""
    return templates.TemplateResponse("connexion.html", {"request": request})


@app.get("/reset-password", response_class=HTMLResponse)
async def reset_password(request: Request):
    """Page de demande de réinitialisation du mot de passe"""
    return templates.TemplateResponse("reset-password.html", {"request": request})


@app.get("/new-password", response_class=HTMLResponse)
async def new_password(request: Request):
    """Page de création d'un nouveau mot de passe"""
    return templates.TemplateResponse("new-password.html", {"request": request})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
