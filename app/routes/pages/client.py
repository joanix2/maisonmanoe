"""
Routes pour les pages client (public)
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["client"])
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Page d'accueil"""
    return templates.TemplateResponse("client/index.html", {"request": request})


@router.get("/recherche", response_class=HTMLResponse)
async def recherche(request: Request, q: str = ""):
    """Page de recherche de produits"""
    return templates.TemplateResponse("client/recherche.html", {"request": request, "query": q})


@router.get("/produit/{product_id}", response_class=HTMLResponse)
async def product_detail(request: Request, product_id: str):
    """Page de détail d'un produit"""
    return templates.TemplateResponse("client/produit.html", {
        "request": request,
        "product_id": product_id
    })


@router.get("/panier", response_class=HTMLResponse)
async def panier(request: Request):
    """Page du panier"""
    return templates.TemplateResponse("client/panier.html", {"request": request})


@router.get("/favoris", response_class=HTMLResponse)
async def favoris(request: Request):
    """Page des favoris"""
    return templates.TemplateResponse("client/favoris.html", {"request": request})


@router.get("/profile", response_class=HTMLResponse)
async def profile(request: Request):
    """Page de profil utilisateur"""
    # Détecte si on vient de l'admin (via referer ou query param)
    referer = request.headers.get("referer", "")
    from_admin = "/admin" in referer or request.query_params.get("from") == "admin"
    
    return templates.TemplateResponse("client/profile.html", {
        "request": request,
        "from_admin": from_admin
    })


@router.get("/paiement", response_class=HTMLResponse)
async def paiement(request: Request):
    """Page de paiement"""
    return templates.TemplateResponse("client/paiement.html", {"request": request})


@router.get("/validation-paiement", response_class=HTMLResponse)
async def validation_paiement(request: Request):
    """Page de validation du paiement"""
    return templates.TemplateResponse("client/validation-paiement.html", {"request": request})


@router.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    """Page de contact"""
    return templates.TemplateResponse("client/contact.html", {"request": request})


@router.get("/a-propos", response_class=HTMLResponse)
async def a_propos(request: Request):
    """Page à propos"""
    return templates.TemplateResponse("client/a-propos.html", {"request": request})


@router.get("/cgv", response_class=HTMLResponse)
async def cgv(request: Request):
    """Page des conditions générales de vente"""
    return templates.TemplateResponse("client/cgv.html", {"request": request})


@router.get("/confidentialite", response_class=HTMLResponse)
async def confidentialite(request: Request):
    """Page de confidentialité"""
    return templates.TemplateResponse("client/confidentialite.html", {"request": request})


@router.get("/retours", response_class=HTMLResponse)
async def retours(request: Request):
    """Page de retours et échanges"""
    return templates.TemplateResponse("client/retours.html", {"request": request})


@router.get("/livraison", response_class=HTMLResponse)
async def livraison(request: Request):
    """Page d'informations sur la livraison"""
    return templates.TemplateResponse("client/livraison.html", {"request": request})


@router.get("/faq", response_class=HTMLResponse)
async def faq(request: Request):
    """Page FAQ - Questions fréquentes"""
    return templates.TemplateResponse("client/faq.html", {"request": request})
