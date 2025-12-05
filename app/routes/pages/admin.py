"""
Routes pour l'administration (dashboard, promos, produits, texte)
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/admin", tags=["admin"])
templates = Jinja2Templates(directory="templates")


@router.get("", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    """Dashboard administrateur"""
    return templates.TemplateResponse("admin/dashboard.html", {"request": request})


@router.get("/promos", response_class=HTMLResponse)
async def admin_promos(request: Request):
    """Gestion des promotions"""
    return templates.TemplateResponse("admin/promos.html", {"request": request})


@router.get("/produits", response_class=HTMLResponse)
async def admin_produits(request: Request):
    """Gestion des produits"""
    return templates.TemplateResponse("admin/produits.html", {"request": request})


@router.get("/texte", response_class=HTMLResponse)
async def admin_texte(request: Request):
    """Gestion des contenus texte"""
    return templates.TemplateResponse("admin/texte.html", {"request": request})
